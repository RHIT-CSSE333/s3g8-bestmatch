import csv
import mysql.connector


def populate_database(csv_file, host, user, password, database):
    # Connect to the database
    connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = connection.cursor()

    try:
        # Read the CSV file and separate data for each table
        table1_data = []
        table2_data = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if exists
            for row in reader:
                # Separate data for each table
                # For example, if first column determines which table the data belongs to
                if row[0] == 'table1':
                    table1_data.append(row[1:])  # Exclude the table indicator
                elif row[0] == 'table2':
                    table2_data.append(row[1:])

        # Populate table1
        populate_table1(cursor, table1_data)

        # Populate table2
        populate_table2(cursor, table2_data)

        # Commit changes
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        # Rollback changes if there's an error
        connection.rollback()
    finally:
        # Close connection
        connection.close()


    # Populate table1
        def populate_table1(cursor, data):
            # Implementation of populate_table1 function
            pass
        
        
    # Populate table2
        def populate_table2(cursor, data):
            # Implementation of populate_table2 function
            pass



def main():
    csv_file = "data.csv"
    host = "golem"  # or your MySQL host
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, host, user, password, database)

