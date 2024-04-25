import csv
import pyodbc
import spacy

def populate_table(cursor, table_name, data, columns):
    placeholders = ", ".join(["?"] * len(columns))
    columns = ", ".join(columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.executemany(sql, data)


def populate_database(csv_file, server, user, password, database):
    connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}"
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        person_data = []
        preference_data = []
        language_set = set()
        hobby_data = []
        match_data = []
        prefers_data = []
        speaks_data = []
        preferspeaks_data = []
        enjoys_data = [] 
        preferenjoys_data = []
        has_data=[]


        with open(csv_file, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                person_data.append(
                    [
                        row["Fname"],
                        row["Lname"],
                        row["DOB"],
                        row["Photolink"],
                        row["Gender"],
                        row["Password"],
                        row["Email"],
                        row["PhoneNumber"],
                        row["Address"],
                        row["PartnerValues"],
                    ]
                )
                preference_data.append(
                    [
                        row["GenderPreference"],
                        row["MinDistance"],
                        row["MaxDistance"],
                        row["MinAge"],
                        row["MaxAge"],
                        row["RelationshipType"],
                    ]
                )
                language_set.update(
                    [row["LanguageName1"], row["LanguageName2"], row["LanguageName3"]]
                )
                hobby_data.append((row["HobbyName1"], row["HobbyDescription1"]))
                match_data.append([
                    row["MatchID"],
                    row["Percentage"],
                    row["UserID1"],
                    row["UserID2"]
                ])
                prefers_data.append([
                    row["UserID"],
                    row["PreferenceID"]
                ])
                speaks_data.append([
                    row["UserID"],
                    row["LanguageName"]
                ])
                preferspeaks_data.append([
                    row["PreferenceID"], 
                    row["LanguageName"]
                ])
                enjoys_data.append([
                    row["UserID"],
                    row["HobbyID"]
                ])
                preferenjoys_data.append([
                    row["HobbyID"],
                    row["PreferenceID"]
                ])
                has_data.append([
                    row["UserID"],
                    row["MatchID"]
                ])


        # Populate entity tables
        populate_table(
            cursor,
            "Person",
            person_data,
            [
                "Fname",
                "LName",
                "DOB",
                "Photolink",
                "Gender",
                "Password",
                "Email",
                "PhoneNumber",
                "Address",
                "PartnerValues",
            ],
        )
        populate_table(
            cursor,
            "Preference",
            preference_data,
            [
                "GenderPreference",
                "MinDistance",
                "MaxDistance",
                "MinAge",
                "MaxAge",
                "RelationshipType",
            ],
        )
        populate_table(
            cursor, "Language", [(lang,) for lang in language_set if lang], ["Name"]
        )
        populate_table(cursor, "Hobby", hobby_data, ["Name", "Description"])
        populate_table(
            cursor,
            "Match",
            match_data,
            [
                "MatchID",
                "Percentage",
                "UserID1",
                "UserID2"
            ],
        )
        populate_table(
            cursor,
            "Prefers",
            prefers_data,
            [
                "UserID",
                "PreferenceID"
            ],
        )
        populate_table(
            cursor,
            "Speaks",
            speaks_data,
            [
                "UserID",
                "LanguageName"
            ],
        )
        populate_table(
            cursor,
            "PreferSpeaks",
            preferspeaks_data,
            [
                "PreferenceID",
                "LanguageName"
            ],
        )
        populate_table(
            cursor,
            "Enjoys",
            enjoys_data,
            [
                "UserID",
                "HobbyID"
            ],
        )
        populate_table(
            cursor,
            "PreferEnjoys",
            preferenjoys_data,
            [
                "HobbyID",
                "PreferenceID"
            ],
        )
        populate_table(
            cursor,
            "Has",
            has_data,
            [
                "UserID",
                "MatchID"
            ],
        )


        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()


def textCompare(String1, String2):
    nlp = spacy.load("en_core_web_lg")
    doc1 = nlp(String1)
    doc2 = nlp(String2)
    return doc1.similarity(doc2)

def main():
    csv_file = "DatingAppData_Direct.csv"
    server = "golem.csse.rose-hulman.edu"
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, server, user, password, database)



if __name__ == "__main__":
    main()
