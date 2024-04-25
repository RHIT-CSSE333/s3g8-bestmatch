import csv
import pyodbc


def populate_database(csv_file, server, database, username, password):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    print("Connected to the database.")
    cursor = connection.cursor()

    try:
        table1_data = []
        table2_data = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == "table1":
                    table1_data.append(row[1:])
                elif row[0] == "table2":
                    table2_data.append(row[1:])

        populate_table1(cursor, table1_data)

        populate_table2(cursor, table2_data)

        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()
        


def populate_table1(cursor, data):
    print("Populating table1...")
    


def populate_table2(cursor, data):
    print("Populating table2...")
    



def main():
    print("Populating the database...")
    csv_file = "data.csv"
    server = "golem.csse.rose-hulman.edu"
    database = "BestMatchDatabase"
    username = "bestmatch_esm"
    password = "Findyourbestmatch123"
    populate_database(csv_file, server, database, username, password)


if __name__ == "__main__":
    main()
