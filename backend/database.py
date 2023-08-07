import pandas as pd

food_schema = ["id", "food", "price", "store", "date"]
tag_schema = ["id", "tag"]

food_db_file = "data/food_table.csv"
food_table = pd.read_csv(food_db_file)

tag_db_file = "data/tag_table.csv"
tag_table = pd.read_csv(tag_db_file)

def insert(table, row):
    if table == "food":
        validate_row(food_schema,row)
        food_table.loc[len(food_table)] = [row[col] for col in food_schema]
        food_table.to_csv(food_db_file, index=False)
    elif table == "tag":
        validate_row(tag_schema,row)
        tag_table.loc[len(tag_table)] = [row[col] for col in tag_schema]
        tag_table.to_csv(tag_db_file, index=False)
    else:
        raise Exception("Table does not exist: " + table)

def insert_df(table, df):
    global food_table
    global tag_table
    if table == "food":
        validate_row(food_schema, df.columns)
        # Remove unwanted columns
        for col in df.columns:
            if col not in food_schema:
                df = df.drop(col, axis=1)
        food_table = pd.concat([food_table, df])
        food_table.to_csv(food_db_file, index=False)
    elif table == "tag":
        validate_row(tag_schema, df.columns)
        # Remove unwanted columns
        for col in df.columns:
            if col not in tag_schema:
                df = df.drop(col, axis=1)
        tag_table = pd.concat([tag_table, df])
        tag_table.to_csv(tag_db_file, index=False)
    else:
        raise Exception("Table does not exist: " + table)
        


def update(table, id, row):
    if table == "food":
        validate_row(food_schema, row)
        food_table.loc[food_table["id"] == id] = [row[col] for col in food_schema]
        food_table.to_csv(food_db_file, index=False)
    elif table == "tag":
        validate_row(tag_schema, row)
        tag_table.loc[tag_table["id"] == id] = [row[col] for col in tag_schema]
        tag_table.to_csv(tag_db_file, index=False)
    else:
        raise Exception("Table does not exist: " + table)



def delete_food(id):
    global food_table
    food_table = food_table.drop(food_table[food_table["id"] == id].index)
    food_table.to_csv(food_db_file, index=False)

def delete_tag(id, tag):
    global tag_table
    tag_table = tag_table.drop(tag_table[(tag_table["id"] == id) & (tag_table["tag"] == tag)].index)
    tag_table.to_csv(tag_db_file, index=False)

def get_table(table):
    if table == "food":
        return food_table.copy()
    elif table == "tag":
        return tag_table.copy()
    else:
        raise Exception("Table does not exist: " + table)

def get_food(id):
    return food_table.loc[food_table["id"] == id]

def get_tags(id):
    return tag_table.loc[tag_table["id"] == id]

def clear_table(table):
    global food_table
    global tag_table
    if table == "food":
        food_table = pd.DataFrame(columns=food_schema)
        food_table.to_csv(food_db_file, index=False)
    elif table == "tag":
        tag_table = pd.DataFrame(columns=tag_schema)
        tag_table.to_csv(tag_db_file, index=False)
    else:
        raise Exception("Table does not exist: " + table)


def validate_row(schema, row):
    for col in schema:
        if col not in row:
            raise Exception("Missing column " + str(col))
        

def main():
    pass



if __name__ == "__main__":
    main()