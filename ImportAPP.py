import csv
import mysql.connector


def populate_database(csv_file, host, user, password, database):
    # Connect to BestMatch database
    connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = connection.cursor()

    # Read CSV file and insert data into the database
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if exists
        for row in reader:
            # Insert data into your tables using SQL INSERT statements
            cursor.execute(
                "INSERT INTO your_table_name (column1, column2, ...) VALUES (%s, %s, ...), INSERT INTO your_table_name (column1, column2, ...) VALUES (%s, %s, ...)",
                row,
            )

    # Commit changes and close the connection
    connection.commit()
    connection.close()


def main():
    csv_file = "data.csv"
    host = "golem"  # or your MySQL host
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, host, user, password, database)

