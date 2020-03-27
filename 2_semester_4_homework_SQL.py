import sqlite3
import pandas as pd

dictionary = {"float64": "REAL",
              "int64": "INTEGER",
              "object": "TEXT"}

def make_db(data_file):
    print("reading data")
    df = pd.read_csv(data_file)
    print("finishing reading")
    with sqlite3.connect("Boring_name.db") as connection:
        print("Starting")
        inside_table = ""
        for i in range(1, len(df.dtypes)):
            inside_table += f'{df.columns[i].replace(" ", "_").replace("-", "")} {dictionary[str(df.dtypes[i])]},\n'
        inside_table = inside_table.strip()[:-1]
        command = f'CREATE TABLE IF NOT EXISTS main_boring_table({inside_table})'
        connection.execute(command)
        column_names_to_insert = ", ".join([col.replace(" ", "_").replace("-", "") for col in df.columns[1:]])
        for i in range(df.shape[0]):
            if not i % 50000:
                print(i)
                connection.commit()
            items_to_insert = ", ".join([f"'{str(item)}'" for item in df.loc[i, :][1:]])
            command = f'INSERT INTO main_boring_table({column_names_to_insert}) VALUES ({items_to_insert})'
            connection.execute(command)
        connection.commit()

        # This part wasn't actually tested and I am not sure it works fine. But I suddenly started to get
        # Process finished with exit code 137 (interrupted by signal 9: SIGKILL)
        # thing and they say it indicates memory issues (which is reasonable since your df has millions of lines)
        # I only wonder, why previously it worked...
        # Anyway, I think I'll be ok with not getting these 3 balls for CASCADE
        column_names_of_new_table = [col.replace(" ", "_").replace("-", "") for col in df.columns[:3]]
        coltypes = [dictionary[str(tp)] for tp in df.dtypes[:3]]
        command = f'CREATE TABLE IF NOT EXISTS may_this_name_be_more_boring_question_mark(' \
                  f'{column_names_of_new_table[0]} {coltypes[0]},' \
                  f'{column_names_of_new_table[1]} {coltypes[1]} PRIMARY KEY,' \
                  f'{column_names_of_new_table[2]} {coltypes[2]},' \
                  f'FOREIGN KEY ({column_names_of_new_table[0]}) REFERENCES main_boring_table ({column_names_of_new_table[0]}) ON UPDATE CASCADE)'
        connection.execute(command)
        connection.commit()

# Here create a database and fill it with given data

# make_db("genstudio.csv")

# And then I just show you how I use these new functions you advised to look up.

with sqlite3.connect("Boring_name.db") as connection:
    command = "UPDATE main_boring_table SET SNP_Name = 'some_boring_name' WHERE SNP_Index = 2"
    connection.execute(command)
    command = "DELETE FROM main_boring_table WHERE SNP_Index = 3"
    connection.execute(command)
    connection.commit()

