import csv
import pyodbc
 
def populate_table(cursor, table_name, data, columns):
    placeholders = ', '.join(['?'] * len(columns))  # Change to '?' for pyodbc
    columns = ', '.join(columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.executemany(sql, data)
 
def populate_database(csv_file, server, user, password, database):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
 
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            person_data = []
            preference_data = []
            language_data = []
            interest_data = []
            hobby_data = []
            enjoys_data = []
            interested_in_data = []
            speaks_data = []
            prefers_data = []
 
            for row in reader:
                # Collect data for each table
                person_data.append([row['UserID'], row['Fname'], row['Lname'], row['DOB'], row['Photo'], row['Gender'], row['Password'], row['Email'], row['PhoneNumber'], row['Address']])
                preference_data.append([row['PreferenceID'], row['GenderPreference'], row['AgeRange'], row['DistanceRange'], row['RelationshipType']])
                language_data.append([row['Language']])
                interest_data.append([row['InterestID'], row['InterestName'], row['InterestDescription']])
                hobby_data.append([row['HobbyID'], row['HobbyName'], row['HobbyDescription']])
                enjoys_data.append([row['HobbyID'], row['PreferenceID']])
                interested_in_data.append([row['InterestID'], row['PreferenceID']])
                speaks_data.append([row['PreferenceID'], row['Language']])
                prefers_data.append([row['UserID'], row['PreferenceID']])
 
            # Populate tables
            populate_table(cursor, 'Person', person_data, ['UserID', 'Fname', 'Lname', 'DOB', 'Photolink', 'Gender', 'Password', 'Email', 'PhoneNumber', 'Address'])
            # populate_table(cursor, 'Preference', preference_data, ['PreferenceID', 'GenderPreference', 'MinAge', 'MaxAge', 'MinDistance', 'MaxDistance', 'RelationshipType'])
            populate_table(cursor, 'Language', language_data, ['Name'])
            populate_table(cursor, 'Interest', interest_data, ['InterestID', 'Name', 'Description'])
            populate_table(cursor, 'Hobby', hobby_data, ['HobbyID', 'Name', 'Description'])
            populate_table(cursor, 'Enjoys', enjoys_data, ['HobbyID', 'PreferenceID'])
            populate_table(cursor, 'Interested In', interested_in_data, ['InterestID', 'PreferenceID'])
            populate_table(cursor, 'Speaks', speaks_data, ['PreferenceID', 'Name'])
            populate_table(cursor, 'Prefers', prefers_data, ['UserID', 'PreferenceID'])
 
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()
 
def main():
    csv_file = "data.csv"
    server = 'golem.csse.rose-hulman.edu'  # Update with your MSSQL server
    user = 'bestmatch_esm'
    password = 'Findyourbestmatch123'
    database = 'BestMatchDatabase'
    populate_database(csv_file, server, user, password, database)
 
if __name__ == '__main__':
    main()
 