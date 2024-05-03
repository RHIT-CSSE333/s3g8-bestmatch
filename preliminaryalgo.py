import pyodbc
import spacy

nlp = spacy.load('en_core_web_md')

def connect_db():
    """Establish a connection to the database."""
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=golem.csse.rose-hulman.edu;'
        'DATABASE=BestMatchDatabase;'
        'UID=bestmatch_esm;'
        'PWD=Findyourbestmatch123'
    )

def fetch_user_preferences(user_id):
    """Fetch user gender, age, and preference data from the database."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.Gender, p.Age, pr.GenderPreference, pr.MinAge, pr.MaxAge, pr.MaxDistance
            FROM Person p
            JOIN Preference pr ON p.UserID = pr.UserID
            WHERE p.UserID = ?
            """, user_id)
        return cursor.fetchone()

def fetch_user_details(user_id):
    """Fetch hobbies, languages, partner values, and relationship type for a user."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT TOP 3 Description FROM Hobby WHERE UserID = ?", user_id)
        hobbies = [hobby[0] for hobby in cursor.fetchall()]

        cursor.execute("SELECT TOP 3 Name FROM Language WHERE UserID = ?", user_id)
        languages = [language[0] for language in cursor.fetchall()]

        cursor.execute("""
            SELECT p.PartnerValues, pr.RelationshipType
            FROM Person p
            JOIN Preference pr ON p.UserID = pr.UserID
            WHERE p.UserID = ?
        """, user_id)
        partner_values, relationship_type = cursor.fetchone()

        return hobbies, ' '.join(languages), partner_values, relationship_type

def calculate_distance(user1_address, user2_address):
    """Mock function to calculate geographical distance between two users."""
    return 10  

def calculate_similarity(text1, text2):
    """Calculate textual similarity using NLP."""
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)

def preliminary_algo(user1_id, user2_id):
    """Check basic compatibility based on gender preference, age range, and distance."""
    user1_data = fetch_user_preferences(user1_id)
    user2_data = fetch_user_preferences(user2_id)
    if user1_data and user2_data:
        user1_gender, user1_age, user1_gender_pref, user1_min_age, user1_max_age, user1_max_dist = user1_data
        user2_gender, user2_age, user2_gender_pref, user2_min_age, user2_max_age, user2_max_dist = user2_data
        if user1_gender in user2_gender_pref and user2_gender in user1_gender_pref and \
           user1_min_age <= user2_age <= user1_max_age and user2_min_age <= user1_age <= user2_max_age and \
           calculate_distance(user1_data, user2_data) <= min(user1_max_dist, user2_max_dist):
            return True
    return False

def matching_algo(user1_id, user2_id):
    """Calculate detailed compatibility if preliminary checks pass."""
    if preliminary_algo(user1_id, user2_id):
        user1_hobbies, user1_languages, user1_partner_values, user1_relationship_type = fetch_user_details(user1_id)
        user2_hobbies, user2_languages, user2_partner_values, user2_relationship_type = fetch_user_details(user2_id)
        hobby_similarity = sum(calculate_similarity(hobby1, hobby2) for hobby1 in user1_hobbies for hobby2 in user2_hobbies) / (len(user1_hobbies) * len(user2_hobbies))
        language_similarity = calculate_similarity(user1_languages, user2_languages)
        partner_values_similarity = calculate_similarity(user1_partner_values, user2_partner_values)
        relationship_type_match = 1 if user1_relationship_type == user2_relationship_type else 0
        compatibility_score = (hobby_similarity + language_similarity + partner_values_similarity + relationship_type_match) / 4 * 100
       # with connect_db() as conn:
          #  cursor = conn.cursor()
          #  cursor.execute("INSERT INTO Match (UserID1, UserID2, Percentage) VALUES (?, ?, ?)", user1_id, user2_id, compatibility_score)
          #  conn.commit()
        return compatibility_score
    else:
        return 0

# Example usage
user1_id = 460
user2_id = 465
compatibility_score = matching_algo(user1_id, user2_id)
print(f"Compatibility score for users {user1_id} and {user2_id}: {compatibility_score:.2f}%.")
