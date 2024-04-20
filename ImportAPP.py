import csv
import mysql.connector


def populate_database(csv_file, host, user, password, database, port):
    connection = mysql.connector.connect(
        host=host, user=user, port=port, password=password, database=database
    )
    cursor = connection.cursor()
    print("Connected to the database.")

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

        

def main():
    print("Populating the database...")
    csv_file = "data.csv"
    host = "golem.csse.rose-hulman.edu"
    port = 3306
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, host, user, password, database, port)


if __name__ == "__main__":
    main()


def populate_table1(cursor, data):
    print("Populating table1...")
    pass

def populate_table2(cursor, data):
    print("Populating table2...")
    pass
