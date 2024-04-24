import csv
import pyodbc


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

        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()


def main():
    csv_file = "DatingAppData_Direct.csv"
    server = "golem.csse.rose-hulman.edu"
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, server, user, password, database)


if __name__ == "__main__":
    main()
