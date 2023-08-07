from flask import Flask, request
from werkzeug.utils  import secure_filename
from flask_cors import CORS
import os
import json
import pandas as pd
import datetime
import traceback

import database
from receipt_OCR import receipt_OCR

app = Flask(__name__)

mapping_file = open('./data/mappings.json', 'r')
mappings = json.loads(mapping_file.read())
mapping_file.close()


# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload():
    store = request.args.get('store')
    print(store)
    filename = ""
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        filename = './uploads/%s' % secure_filename(fname)
        f.save(filename)

    try:
        result = receipt_OCR(filename, store)
    except Exception as e:
        print(traceback.print_exc())
        return {
            "msg": "Error extracting text from image. Try adjusting the crop or orientation of the picture.",
            "error": str(e)
        }, 500
    return result.reset_index().to_json(orient='records')


@app.route('/storelist', methods=['POST'])
def store_list():
    try:
        date = request.args.get('date')
        data = request.get_json(force=True)
        old = data["old"]
        new = data["new"]
    except Exception as e:
        return {
            "msg": "Error parsing input",
            "error": e
        }, 500

    try:
        changed = False
        for row in new:
            if row["food"] != old[row["index"]]["food"]:
                mappings[old[row["index"]]["food"]] = row["food"]
                changed = True

        if changed:
            mapping_file = open('./data/mappings.json', 'w')
            mapping_file.write(json.dumps(mappings))
            mapping_file.close()

    except Exception as e:
        return {
            "msg": "Error finding changed foods",
            "error": e
        }, 500

    try:
        df = pd.DataFrame.from_records(new)
        df["date"] = [date for _ in df["food"]]

        df = df.drop('index', axis=1)
        print(df)

        database.insert_df("food", df)
        with open('./data/tags.json', "r+") as f:
            data = json.loads(f.read())
            for i in range(len(df)):
                row = df.iloc[i]
                if row["food"] in data:
                    for tag in data[row["food"]]:
                        database.insert("tag", {"id": row["id"], "tag": tag})


    except Exception as e:
        return {
            "msg": "Error persisting data",
            "error": e
        }, 500
    


    return "Okay!"

@app.route('/data', methods=['GET'])
def get_data():
    food_table = database.get_table("food")
    tag_table = database.get_table("tag")

    tags_grouped = tag_table.groupby("id", group_keys=True)["tag"].apply(list).to_dict()
    print(tags_grouped)
    json_data = json.loads(food_table.reset_index().to_json(orient='records'))
    for elem in json_data:
        if elem["id"] in tags_grouped:
            elem["tags"] = tags_grouped[elem["id"]]
        else:
            elem["tags"] = []
    return json_data


@app.route('/', methods=['GET'])
def home():
    return "Hello world!"


@app.route('/emptydb', methods=['GET'])
def empty_database():
    database.clear_table("food")
    database.clear_table("tag")
    return "Done"

@app.route('/addtag', methods=['POST'])
def add_tag():
    body = request.get_json(force=True)
    tag = body["tag"]
    id = body["id"]
    database.insert("tag", {
        "id": id,
        "tag": tag
    })
    food_item = database.get_food(id)
    if len(food_item) == 0:
        return "Done"
    else:
        food_item = food_item.iloc[0]

    with open('./data/tags.json', "r+") as f:
        data = json.loads(f.read())
        f.seek(0)
        if food_item["food"] not in data:
            data[food_item["food"]] = [] 
        data[food_item["food"]].append(tag)
        data[food_item["food"]] = list(set(data[food_item["food"]]))
        f.write(json.dumps(data,indent=4, separators=(',', ': ')))
        f.truncate()
    return "Done"

@app.route('/removetag', methods=['POST'])
def remove_tag():
    body = request.get_json(force=True)
    tag = body["tag"]
    id = body["id"]
    database.delete_tag(id, tag)
    
    food_item = database.get_food(id)
    if len(food_item) == 0:
        return "Done"
    else:
        food_item = food_item.iloc[0]

    with open('./data/tags.json', "r+") as f:
        data = json.loads(f.read())
        f.seek(0)
        if food_item["food"] not in data:
            return "Done"
        if tag not in data[food_item["food"]]:
            return "Done"
        data[food_item["food"]].remove(tag)
        f.write(json.dumps(data,indent=4, separators=(',', ': ')))
        f.truncate()
    return "Done"

@app.route('/analysis/bytag', methods=["GET"])
def get_expenses_by_tag():
    data = pd.merge(database.get_table("food"), database.get_table("tag"), on="id")
    summed = data.groupby("tag")["price"].sum()
    return summed.to_dict()


@app.route('/analysis/byweek', methods=["GET"])
def get_expenses_by_week():
    data = database.get_table("food")
    data["week"] = data["date"].apply(lambda date: datetime.datetime.strptime(date, '%Y/%m/%d').timetuple().tm_yday // 7)
    data["label"] = data["week"].apply(lambda week: (datetime.datetime(2023, 1, 1) + datetime.timedelta(days=week * 7)).strftime('%b %d'))
    result = {}
    for index, row in data.iterrows():
        if row["label"] not in result:
            result[row["label"]] = 0
        result[row["label"]] += row["price"]

    return result

if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(host='0.0.0.0', port=3000, debug=True)