import csv
import pyodbc
from passlib.hash import bcrypt

def populate_table(cursor, table_name, data, columns, return_ids=False):
    placeholders = ', '.join(['?'] * len(columns))
    columns = ', '.join(columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.executemany(sql, data)
    if return_ids:
        return cursor.execute("SELECT @@IDENTITY").fetchone()[0]  # Fetch last inserted ID

def fetch_user_ids(cursor, emails):
    placeholders = ', '.join('?' for _ in emails)
    query = "SELECT UserID, Email FROM Person WHERE Email IN ({})".format(placeholders)
    cursor.execute(query, emails)
    return cursor.fetchall()

def hash_passwords(person_data):
    """ Hash passwords using bcrypt """
    for person in person_data:
        password_index = 5  
        person[password_index] = bcrypt.hash(person[password_index])

def populate_database(csv_file, server, user, password, database):
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        person_data = []
        preference_data = []
        emails = []
        language_data = []
        hobby_data = []

        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                person_data.append([row['Fname'], row['Lname'], row['DOB'], row['Photolink'], row['Gender'], row['Password'], row['Email'], row['PhoneNumber'], row['Address'], row['PartnerValues']])
                emails.append(row['Email'])  # Collect emails to fetch UserIDs later
        hash_passwords(person_data)
        populate_table(cursor, 'Person', person_data, ['Fname', 'LName', 'DOB', 'Photolink', 'Gender', 'Password', 'Email', 'PhoneNumber', 'Address', 'PartnerValues'])
        connection.commit()

        # Fetch UserIDs
        user_ids = fetch_user_ids(cursor, emails)
        email_to_userid = {email: user_id for user_id, email in user_ids}

        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Email'] in email_to_userid:
                    user_id = email_to_userid[row['Email']]
                    preference_id = populate_table(cursor, 'Preference', [[user_id, row['GenderPreference'], row['MaxDistance'], row['MinAge'], row['MaxAge'], row['RelationshipType']]], ['UserID', 'GenderPreference', 'MaxDistance', 'MinAge', 'MaxAge', 'RelationshipType'], return_ids=True)
                    # Collect language and hobby data
                    languages = [row.get(f'LanguageName{i}') for i in range(1, 4) if row.get(f'LanguageName{i}')]
                    for lang in languages:
                        language_data.append([lang, user_id, preference_id])
                    hobbies = [(row.get(f'HobbyName{i}'), row.get(f'HobbyDescription{i}')) for i in range(1, 4) if row.get(f'HobbyName{i}') and row.get(f'HobbyDescription{i}')]
                    for hobby_name, hobby_desc in hobbies:
                        hobby_data.append([hobby_name, hobby_desc, user_id, preference_id])

        if language_data:
            populate_table(cursor, 'Language', language_data, ['Name', 'UserID', 'PreferenceID'])
        if hobby_data:
            populate_table(cursor, 'Hobby', hobby_data, ['Name', 'Description', 'UserID', 'PreferenceID'])

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
