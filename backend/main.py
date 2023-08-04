from flask import Flask, request
from werkzeug.utils  import secure_filename
from flask_cors import CORS
import os
import json
import pandas as pd
import datetime

from receipt_OCR import receipt_OCR

app = Flask(__name__)

mapping_file = open('./mappings.json', 'r')
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

    result = receipt_OCR(filename, store)
    return result.reset_index().to_json(orient='records')
    # return [{"index":0,"food":"Sparkling Apple Cider","price":5.79,"store":"Key Food"},{"index":1,"food":"RICE SELECT SUSHI","price":9.79,"store":"Key Food"},{"index":2,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"},{"index":3,"food":"Shredded Mozerella Cheese","price":4.99,"store":"Key Food"}]


@app.route('/storelist', methods=['POST'])
def store_list():
    database = pd.read_csv('./db.csv')

    date = request.args.get('date')
    data = request.get_json(force=True)
    old = data["old"]
    new = data["new"]

    changed = False
    for row in new:
        if row["food"] != old[row["index"]]["food"]:
            mappings[old[row["index"]]["food"]] = row["food"]
            changed = True

    if changed:
        mapping_file = open('./mappings.json', 'w')
        mapping_file.write(json.dumps(mappings))
        mapping_file.close()

    df = pd.DataFrame.from_records(new)
    df["date"] = [date for _ in df["food"]]

    df = df.drop('index', axis=1)
    print(df)

    database = pd.concat([database, df])
    database.to_csv("./db.csv", index=False)

    return "Okay!"

@app.route('/data', methods=['GET'])
def get_data():
    database = pd.read_csv('./db.csv')
    return database.reset_index().to_json(orient='records')


@app.route('/', methods=['GET'])
def home():
    return "Hello world!"


@app.route('/emptydb', methods=['GET'])
def empty_database():
    database = pd.DataFrame(columns=['food', 'price', 'store', 'date'])
    database.to_csv('db.csv', index=False)
    return "Done!"



if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./uploads')
    app.run(host='0.0.0.0', port=3000, debug=True)