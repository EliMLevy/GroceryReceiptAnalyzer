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

        database.insert_df(df)
    except Exception as e:
        return {
            "msg": "Error persisting data",
            "error": e
        }, 500

    return "Okay!"

@app.route('/data', methods=['GET'])
def get_data():
    table = database.get_table()
    return table.reset_index().to_json(orient='records')


@app.route('/', methods=['GET'])
def home():
    return "Hello world!"


@app.route('/emptydb', methods=['GET'])
def empty_database():
    database.clear_table()
    return "Done!"



if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(host='0.0.0.0', port=3000, debug=True)