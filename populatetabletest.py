import csv
import pyodbc

def populate_table(cursor, table_name, data, columns, return_ids=False):
    placeholders = ', '.join(['?'] * len(columns))
    columns = ', '.join(columns)
    result_ids = []

    # Form the basic INSERT statement
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    for row_data in data:
        # If return_ids is True, fetch the identity of the last inserted row
        if return_ids:
            # Execute INSERT and immediately fetch the identity
            cursor.execute(f"{sql}; SELECT SCOPE_IDENTITY();", row_data)
            result_id = cursor.fetchone()  # Fetch the result of SELECT SCOPE_IDENTITY()
            if result_id and result_id[0] is not None:
                result_ids.append(result_id[0])
        else:
            cursor.execute(sql, row_data)
    
    return result_ids  # Return list of fetched identity values if any


def populate_database(csv_file, server, user, password, database):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Insert person and get UserID
                person_id = populate_table(cursor, 'Person', [[row['Fname'], row['Lname'], row['DOB'], row['Photolink'], row['Gender'], row['Password'], row['Email'], row['PhoneNumber'], row['Address'], row['PartnerValues']]], ['Fname', 'LName', 'DOB', 'Photolink', 'Gender', 'Password', 'Email', 'PhoneNumber', 'Address', 'PartnerValues'], return_ids=True)

                # Prepare and insert preference with UserID
                preference_id = populate_table(cursor, 'Preference', [[person_id, row['GenderPreference'], row['MaxDistance'], row['MinAge'], row['MaxAge'], row['RelationshipType']]], ['UserID', 'GenderPreference', 'MaxDistance', 'MinAge', 'MaxAge', 'RelationshipType'], return_ids=True)

                # Insert languages and hobbies for each user and preference
                languages = [row.get(f'LanguageName{i}') for i in range(1, 4) if row.get(f'LanguageName{i}')]
                for lang in languages:
                    populate_table(cursor, 'Language', [[lang, person_id, preference_id]], ['Name', 'UserID', 'PreferenceID'])

                # Collect and insert hobbies
                hobbies = [(row.get(f'HobbyName{i}'), row.get(f'HobbyDescription{i}')) for i in range(1, 4) if row.get(f'HobbyName{i}') and row.get(f'HobbyDescription{i}')]
                for hobby_name, hobby_desc in hobbies:
                    populate_table(cursor, 'Hobby', [[hobby_name, hobby_desc, person_id, preference_id]], ['Name', 'Description', 'UserID', 'PreferenceID'])

        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

def main():
    csv_file = "data.csv"
    server = 'golem.csse.rose-hulman.edu'
    user = 'bestmatch_esm'
    password = 'Findyourbestmatch123'
    database = 'BestMatchDatabase'
    populate_database(csv_file, server, user, password, database)

if __name__ == '__main__':
    main()
