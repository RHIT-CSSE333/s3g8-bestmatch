import csv
import random
import traceback
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
                # language_set.update(
                #     [row["LanguageName1"], row["LanguageName2"], row["LanguageName3"]]
                # )

                # hobby_data.append((row["HobbyName1"], row["HobbyDescription1"]))
                
                # Collect regular and preferred hobbies from all available columns
                for i in range(1, 4):  # Assuming up to three regular hobbies
                    hobby_key = f"HobbyName{i}"
                    desc_key = f"HobbyDescription{i}"
                    if row.get(hobby_key) and row.get(desc_key):
                        hobby_data.append((row[hobby_key], row[desc_key]))

                for i in range(1, 4):  # Assuming up to three preferred hobbies
                    pref_hobby_key = f"PreferredHobbyName{i}"
                    pref_desc_key = f"PreferredHobbyDescription{i}"
                    if row.get(pref_hobby_key) and row.get(pref_desc_key):
                        hobby_data.append((row[pref_hobby_key], row[pref_desc_key]))

                languages = [
                    "Amharic",
                    "Arabic Algerian Spoken",
                    "Arabic Egyptian Spoken",
                    "Arabic Mesopotamian Spoken",
                    "Arabic Moroccan Spoken",
                    "Arabic Najdi Spoken",
                    "Arabic North Levantine Spoken",
                    "Arabic Saidi Spoken",
                    "Arabic Sanaani Spoken",
                    "Arabic Sudanese Spoken",
                    "Arabic Tunisian Spoken",
                    "Assamese",
                    "Azerbaijani North",
                    "Azerbaijani South",
                    "Belarusan",
                    "Bengali",
                    "Bhopuri",
                    "Bulgarian",
                    "Burmese",
                    "Cebuano",
                    "Chhattisgarhi",
                    "Chinese Gan",
                    "Chinese Hakka",
                    "Chinese Jinyu",
                    "Chinese Mandarin",
                    "Chinese Min Bei",
                    "Chinese Min Nan",
                    "Chinese Wu",
                    "Chinese Xiang",
                    "Chinese Yue",
                    "Chittagonian",
                    "Czech",
                    "Dutch",
                    "English",
                    "Farsi Western",
                    "French",
                    "Fulfulde Nigerian",
                    "German Standard",
                    "Greek",
                    "Gujarati",
                    "Hausa",
                    "Haitian Creole French",
                    "Haryanvi",
                    "Hindi",
                    "Hungarian",
                    "Igbo",
                    "Ilocano",
                    "Indonesian",
                    "Italian",
                    "Japanese",
                    "Javanese",
                    "Kannada",
                    "Kazakh",
                    "Korean",
                    "Lombard",
                    "Madura",
                    "Magahi",
                    "Malagasy",
                    "Malay",
                    "Malayalam",
                    "Marathi",
                    "Marwari",
                    "Nepali",
                    "Oriya",
                    "Oromo West-Central",
                    "Panjabi Eastern",
                    "Panjabi Western",
                    "Pashto Northern",
                    "Pashto Southern",
                    "Polish",
                    "Portuguese",
                    "Romanian",
                    "Russian",
                    "Rwanda",
                    "Saraiki",
                    "Sindhi",
                    "Sinhala",
                    "Somali",
                    "Spanish",
                    "Sunda",
                    "Swedish",
                    "Tagalog",
                    "Tamil",
                    "Tatar",
                    "Telugu",
                    "Thai",
                    "Thai Northeastern",
                    "Turkish",
                    "Ukrainian",
                    "Urdu",
                    "Uyghur",
                    "Uzbek Northern",
                    "Vietnamese",
                    "Yoruba",
                    "Zhuang Northern",
                    "Zulu"
                ]
                
                languages = [(lang,) for lang in languages]
                
                # # Inserting languages into the table
                # for language in languages:
                #     cursor.execute("INSERT INTO Languages (Language) VALUES (?)", language)


                # match_data.append([
                #     row["MatchID"],
                #     row["Percentage"],
                #     row["UserID1"],
                #     row["UserID2"]
                # ])

                # prefers_data.append([
                #     row["UserID"],
                #     row["PreferenceID"]
                # ])
                # speaks_data.append([
                #     row["UserID"],
                #     row["LanguageName"]
                # ])
                # preferspeaks_data.append([
                #     row["PreferenceID"],
                #     row["LanguageName"]
                # ])
                # enjoys_data.append([
                #     row["UserID"],
                #     row["HobbyID"]
                # ])
                # preferenjoys_data.append([
                #     row["HobbyID"],
                #     row["PreferenceID"]
                # ])
                # has_data.append([
                #     row["UserID"],
                #     row["MatchID"]
                # ])
                
                # num_records = 8
                    
                # prefers_data.append((random.randint(1, 8), random.randint(1, 8)))     
                # speaks_data.append((random.randint(1, 8), random.choice(languages)))     
                # preferspeaks_data.append((random.randint(1, 8), random.choice(languages)))     
                # enjoys_data.append((random.randint(1, 8), random.randint(1, 24)))     
                # preferenjoys_data.append((random.randint(1, 8), random.randint(1, 24)))     
                # has_data.append((random.randint(1, 8), random.randint(1, 56))) 
                    
                    
                # num_records = 8
                
                # userid1 = random.randint(1, 8)
                # userid2 = random.randint(1, 8)
                # while userid1 == userid2:
                #     userid1 = random.randint(1, 8)
                   
                # match_data.append([                          
                #                        random.random(),      
                #                        userid1,
                #                        userid2         
                #                        ])
                    
                    
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
            cursor, "Language", languages, ["Name"]
        )
        populate_table(
            cursor, "Hobby", hobby_data, ["Name", "Description"]
        )
        
        # populate_table(
        #     cursor,
        #     "Match",
        #     match_data,
        #     ["Percentage", "UserID1", "UserID2"],
        # )
        # populate_table(
        #     cursor,
        #     "Prefers",
        #     prefers_data,
        #     ["UserID", "PreferenceID"],
        # )
        # populate_table(
        #     cursor,
        #     "Speaks",
        #     speaks_data,
        #     ["UserID", "LanguageName"],
        # )
        # populate_table(
        #     cursor,
        #     "PreferSpeaks",
        #     preferspeaks_data,
        #     ["PreferenceID", "LanguageName"],
        # )
        # populate_table(
        #     cursor,
        #     "Enjoys",
        #     enjoys_data,
        #     ["UserID", "HobbyID"],
        # )
        # populate_table(
        #     cursor,
        #     "PreferEnjoys",
        #     preferenjoys_data,
        #     ["HobbyID", "PreferenceID"],
        # )
        # populate_table(
        #     cursor,
        #     "Has",
        #     has_data,
        #     ["UserID", "MatchID"],
        # )

        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        connection.rollback()
    finally:
        connection.close()


def textCompare(String1, String2):
    nlp = spacy.load("en_core_web_lg")
    doc1 = nlp(String1)
    doc2 = nlp(String2)
    return doc1.similarity(doc2)


def main():
    csv_file = "data.csv"
    server = "golem.csse.rose-hulman.edu"
    user = "bestmatch_esm"
    password = "Findyourbestmatch123"
    database = "BestMatchDatabase"
    populate_database(csv_file, server, user, password, database)


if __name__ == "__main__":
    main()
