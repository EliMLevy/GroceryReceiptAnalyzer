import pandas as pd

schema = ["id", "food", "price", "date", "tags"]

db_file = "data/db.csv"
database = pd.read_csv(db_file)

def insert(row):
    global database
    validate_row(row)

    database.loc[len(database)] = [row[col] for col in schema]
    database.to_csv(db_file, index=False)


def insert_df(df):
    global database
    validate_row(df.columns)

    database = pd.concat([database, df])
    database.to_csv(db_file, index=False)

def update(id, row):
    validate_row(row)

    database.loc[database["id"] == id] = row
    database.to_csv(db_file, index=False)

def delete(id):
    database = database.drop(database[database["id"] == id].index)
    database.to_csv(db_file, index=False)

def get_table():
    return database.copy()

def get(id):
    return database.loc[database["id"] == id]

def clear_table():
    database = pd.DataFrame(columns=schema)
    database.to_csv(db_file, index=False)


def validate_row(row):
    for col in schema:
        if col not in row:
            raise Exception("Missing column " + str(col))
        

def main():
    insert({
        "id": "45223",
        "food": "sethseq",
        "price": "1.24",
        "store": "Trader Joes",
        "date": "2023/08/05",
        "tags": ["1", "2", "3"]
    })
    print(database)

    df = pd.DataFrame({"id": ["321", "432"], 
                       "food":["aefw", "faew"], 
                       "price":["121", "3123"], 
                       "store": ["asefa", "faew"], 
                       "date":["awefa", "afwefa"], 
                       "tags":[["a", "b", "c"], ["d", "e", "f"]]})

    insert_df(df)
    print(database)

    insert({
        "id": "45223",
        "food": "sethseq",
        "store": "Trader Joes",
        "date": "2023/08/05",
        "tags": ["1", "2", "3"]
    })



if __name__ == "__main__":
    main()