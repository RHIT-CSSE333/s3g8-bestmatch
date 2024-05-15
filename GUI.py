import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from tkcalendar import DateEntry
import matchingalgo

import passlib.hash
import cloudinary
import cloudinary.uploader
import cloudinary.api

from tkinter import filedialog

from PIL import Image, ImageTk
import requests
from io import BytesIO

current_user_id = None
current_preference_id = None
photo_label = None
 
cloudinary.config( 
  cloud_name = "dish9tzjr", 
  api_key = "922323626444279", 
  api_secret = "5_ePcnUjoH66Txx5GlfBc5DIOOo",
  secure=True
)

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            photo_url = upload_image_to_cloudinary(file_path)
            return photo_url
        except Exception as e:
            messagebox.showerror("Upload Error", "Failed to upload image: " + str(e))
    return ""
 
def upload_image_to_cloudinary(file_path):
    response = cloudinary.uploader.upload(file_path)
    return response['url']

def connect_db():
    """Establish a connection to the database."""
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=golem.csse.rose-hulman.edu;'
        'DATABASE=BestMatchDatabase;'
        'UID=bestmatch_esm;'
        'PWD=Findyourbestmatch123'
    )
 
def show_login():
    welcome_frame.pack_forget()
    login_frame.pack()
 
def show_create_account():
    welcome_frame.pack_forget()
    register_frame.pack()
 
def upload_and_update_photo():
    photo_url = select_image()
    if photo_url:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE Person SET Photolink = ? WHERE UserID = ?", (photo_url, current_user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Update Successful", "Your profile picture has been updated.")
            load_user_photo(photo_url) 
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    else:
        messagebox.showerror("Upload Failed", "No image was selected or upload failed.")

def show_preferences():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT GenderPreference, MinAge, MaxAge, MaxDistance, RelationshipType FROM Preference WHERE PreferenceID = ?", (current_preference_id,))  # Make sure to maintain current_user_id somewhere
        preference = cursor.fetchone()

        cursor.execute("SELECT Photolink FROM Person WHERE UserID = ?", (current_user_id,))
        photo_link = cursor.fetchone()

        conn.close()
 
        if preference:
            gender_pref_entry.set(preference.GenderPreference)
            min_age_slider.set(preference.MinAge)  
            max_age_slider.set(preference.MaxAge) 
            max_distance_entry.delete(0, tk.END)
            max_distance_entry.insert(0, preference.MaxDistance)
            relationship_type_entry.set(preference.RelationshipType)
        
        if photo_link and photo_link[0]:
            load_user_photo(photo_link[0])
       
        profile_frame.pack_forget()
        preferences_frame.pack()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

 
def update_user_preferences():
    gender_pref = gender_pref_entry.get()
    min_age = min_age_slider.get()    
    max_age = max_age_slider.get()
    max_distance = int(max_distance_entry.get())
    relationship_type = relationship_type_entry.get()
   
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        cursor.execute("EXEC Update_User_Preferences @PreferenceID = ?, @GenderPreference = ?, @MinAge = ?, @MaxAge = ?, @MaxDistance = ?, @RelationshipType = ?",
                       (current_preference_id, gender_pref, min_age, max_age, max_distance, relationship_type))
        conn.commit()
        messagebox.showinfo("Success", "Preferences updated successfully.")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def load_user_photo(url):
    global photo_label
    try:
        response = requests.get(url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((100, 150), Image.LANCZOS) 
        img_tk = ImageTk.PhotoImage(img)

        if photo_label is None: 
            photo_label = tk.Label(profile_frame, image=img_tk)
            photo_label.image = img_tk  
            photo_label.pack(before=user_fullname_label) 
        else:
            photo_label.config(image=img_tk)  
            photo_label.image = img_tk  

    except Exception as e:
        messagebox.showerror("Image Load Error", "Failed to load image: " + str(e))

def create_account():
    email = entry_email_register.get()
    password = entry_password_register.get()
    first_name = entry_fname.get()
    last_name = entry_lname.get()
    dob = cal.get_date().strftime('%Y-%m-%d')  
    gender = gender_combobox.get()
    address = entry_address.get()
    phone_number = entry_phone.get()  
    partner_value = entry_partner_values.get()
    
    photo_link = select_image() 
 
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        hasher = passlib.hash.bcrypt.using(rounds=12)
        hashed_password = hasher.hash(password)
 
        print("Uploading photo URL to database:", photo_link) 
        cursor.execute("EXEC Insert_User @Fname = ?, @LName = ?, @DOB = ?, @Photo = ?, @Gender = ?, @Password = ?, @Email = ?, @PhoneNumber = ?, @Address = ?, @PartnerValues = ?",
                       (first_name, last_name, dob, photo_link, gender, hashed_password, email, phone_number, address, partner_value))
        conn.commit()
        messagebox.showinfo("Account Created", "Your account has been created successfully.")
        conn.close()
    except pyodbc.DatabaseError as e:
        error_message = str(e)
        if "Missing required fields" in error_message:
            messagebox.showerror("Missing Fields", "Please fill in all required fields.")
        elif "User must be at least 18 years old" in error_message:
            messagebox.showerror("Age Requirement", "User must be at least 18 years old.")
        elif "Invalid email format" in error_message:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        elif "Failed to insert new user" in error_message:
            messagebox.showerror("Database Error", "Failed to create account. Please try again later.")
        else:
            messagebox.showerror("Database Error", error_message)
    except Exception as e:
        messagebox.showerror("Error", str(e))
 
def login():
    global current_user_id, current_preference_id
    email = entry_email.get()
    password = entry_password.get()
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
 
        cursor.execute("""
            SELECT UserID, FName, LName, Password, Photolink
            FROM Person
            WHERE Email = ?
        """, (email,))
 
 
        user = cursor.fetchone()
        if user:
            stored_password = user[3]
            if passlib.hash.bcrypt.verify(password, stored_password):
                messagebox.showinfo("Login Success", "You have successfully logged in.")
                current_user_id = user[0]
                user_fullname_label.config(text=f"{user[1]} {user[2]}")
                if user[4]:  # user[4] is the Photolink
                    load_user_photo(user[4])
                login_frame.pack_forget()
                profile_frame.pack()
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password")
        else:
            messagebox.showerror("Login Failed", "User not found")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
 
def update_match_status(match_id, status, match_frame):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("""
                    UPDATE Has
                    SET Accepted = 1
                    WHERE MatchID = ? AND UserID1 = ?
                """, (match_id, current_user_id))
                conn.commit()
               
                cursor.execute("""
                    SELECT COUNT(*) FROM Has
                    WHERE MatchID = ? AND Accepted = 1
                """, (match_id,))
                count = cursor.fetchone()[0]
               
                if count == 2:  
                    messagebox.showinfo("Success", "Congrats, you have found your match!")
                    match_frame.destroy()
 
            else:
                cursor.execute("""
                    DELETE FROM Has
                    WHERE MatchID = ?
                """, (match_id,))
                cursor.execute("""
                    DELETE FROM Match
                    WHERE MatchID = ?
                """, (match_id,))
                conn.commit()
 
            messagebox.showinfo("Success", "Match updated successfully.")
            match_frame.destroy()
 
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to update match status: {e}")
 
 
 
def show_matches():
    potential_user_ids = fetch_all_users_ids()  
    for user_id in potential_user_ids:
        if user_id != current_user_id:
            print(user_id)  
            matchingalgo.matching_algo(current_user_id, user_id)
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.MatchID, m.Percentage, p.UserID, p.FName, p.LName
            FROM Has h
            JOIN Match m ON h.MatchID = m.MatchID
            JOIN Person p ON h.UserID2 = p.UserID
            WHERE h.UserID1 = ? AND h.Accepted = 0
        """, (current_user_id,))
        matches = cursor.fetchall()
        conn.close()

        for widget in matches_frame.winfo_children():
            widget.destroy()
 
        if not matches:
            no_match_label = tk.Label(matches_frame, text="No match found.")
            no_match_label.pack()
        else:
            for match in matches:
                match_frame = tk.Frame(matches_frame)
                match_frame.pack(pady=5, fill=tk.X)
 
                tk.Label(match_frame, text=f"Match with {match[3]} {match[4]}: {match[1]:.2f}%").pack(side=tk.LEFT)
                view_profile_button = tk.Button(match_frame, text="View Profile", command=lambda uid=match[2]: view_user_profile(uid))
                view_profile_button.pack(side=tk.RIGHT, padx=10)

                accept_button = tk.Button(match_frame, text="Accept", command=lambda m=match, mf=match_frame: update_match_status(m[0], True, mf))
                accept_button.pack(side=tk.RIGHT, padx=10)
 
                decline_button = tk.Button(match_frame, text="Decline", command=lambda m=match, mf=match_frame: update_match_status(m[0], False, mf))
                decline_button.pack(side=tk.RIGHT)
 
        show_matches_page()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
 
def fetch_all_users_ids():
    """ Fetch all user IDs from the database. """
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT UserID FROM Person")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch user IDs: {e}")
        return []
 
def delete_account():
    global current_user_id, current_preference_id
    response = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
    if response:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("EXEC DeleteUser @UserID = ?", (current_user_id,))
            conn.commit()
 
            messagebox.showinfo("Account Deleted", "Your account has been successfully deleted.")
 
            current_user_id = None
            current_preference_id = None
 
            preferences_frame.pack_forget()
            welcome_frame.pack()
 
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

def view_user_profile(user_id):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        cursor.execute("EXEC GetUserProfile @UserID = ?", (user_id,))
        user_info = cursor.fetchone()
        conn.close()
        if user_info:
            user_details = f"Name: {user_info[0]} {user_info[1]}\nDOB: {user_info[2]}\nEmail: {user_info[3]}\nPhone: {user_info[4]}"
            messagebox.showinfo("User Profile", user_details)
        else:
            messagebox.showerror("Profile Error", "User profile not found.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

 
def show_matches_page():
    profile_frame.pack_forget()
   
    matches_frame.pack()
 
app = tk.Tk()
app.geometry('500x500')
app.title("Best Match Dating System")
 
# Welcome Frame
welcome_frame = tk.Frame(app)
welcome_frame.pack(fill='both', expand=True)
welcome_label = tk.Label(welcome_frame, text="Welcome to Best Match Dating System!", font=("Helvetica", 16))
welcome_label.pack(pady=20)
 
new_user_label = tk.Label(welcome_frame, text="New User?")
new_user_label.pack()
create_account_btn = tk.Button(welcome_frame, text="Create Account", command=show_create_account)
create_account_btn.pack(pady=5)
 
existing_user_label = tk.Label(welcome_frame, text="Existing User?")
existing_user_label.pack()
login_btn = tk.Button(welcome_frame, text="Login", command=show_login)
login_btn.pack(pady=5)
 
# Login Frame
login_frame = tk.Frame(app)
 
tk.Label(login_frame, text="Email:").pack()
entry_email = tk.Entry(login_frame, width=25)
entry_email.pack()
 
tk.Label(login_frame, text="Password:").pack()
entry_password = tk.Entry(login_frame, show="*", width=25)
entry_password.pack()
 
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
 
# Register Frame
register_frame = tk.Frame(app)
 
tk.Label(register_frame, text="Email:").pack()
entry_email_register = tk.Entry(register_frame, width=25)
entry_email_register.pack()
 
tk.Label(register_frame, text="Password:").pack()
entry_password_register = tk.Entry(register_frame, show="*", width=25)
entry_password_register.pack()
 
tk.Label(register_frame, text="First Name:").pack()
entry_fname = tk.Entry(register_frame, width=25)
entry_fname.pack()
 
tk.Label(register_frame, text="Last Name:").pack()
entry_lname = tk.Entry(register_frame, width=25)
entry_lname.pack()
 
tk.Label(register_frame, text="Date of Birth:").pack()
cal = DateEntry(register_frame, width=25, year=2000, month=1, day=1, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
cal.pack()
 
tk.Label(register_frame, text="Gender:").pack()
gender_combobox = ttk.Combobox(register_frame, values=["Male", "Female", "All"])
gender_combobox.pack()
 
tk.Label(register_frame, text="Address:").pack()
entry_address = tk.Entry(register_frame, width=25)
entry_address.pack()
 
tk.Label(register_frame, text="Phone Number:").pack()
entry_phone = tk.Entry(register_frame, width=25)
entry_phone.pack()
 
tk.Label(register_frame, text="Partner Values:").pack()
entry_partner_values = tk.Entry(register_frame, width=25)
entry_partner_values.pack()

upload_image_btn = tk.Button(register_frame, text="Upload Image", command=lambda: entry_photo_link.insert(0, select_image()))
upload_image_btn.pack()
entry_photo_link = tk.Entry(register_frame, width=25)
entry_photo_link.pack()

tk.Button(register_frame, text="Create My Account", command=create_account).pack(pady=10)
 
# Profile Frame
profile_frame = tk.Frame(app)

user_fullname_label = tk.Label(profile_frame, text="", font=("Helvetica", 16))  
user_fullname_label.pack(pady=20)
 
update_profile_btn = tk.Button(profile_frame, text="Update My Profile", command=show_preferences)
update_profile_btn.pack(pady=10)
 
matches_frame = tk.Frame(app)
show_matches_btn = tk.Button(profile_frame, text="Show My Matches", command=show_matches)
show_matches_btn.pack(pady=10)
 
# Preferences Frame
preferences_frame = tk.Frame(app)
 
# Input fields for preferences
tk.Label(preferences_frame, text="Gender Preference:").pack()
gender_pref_entry = ttk.Combobox(preferences_frame, values=["Male", "Female", "All"])
gender_pref_entry.pack()
 
tk.Label(preferences_frame, text="Minimum Age:").pack()
min_age_slider = tk.Scale(preferences_frame, from_=18, to=100, orient='horizontal', length=200)
min_age_slider.set(18)  # Default value
min_age_slider.pack()
 
tk.Label(preferences_frame, text="Maximum Age:").pack()
max_age_slider = tk.Scale(preferences_frame, from_=18, to=100, orient='horizontal', length=200)
max_age_slider.set(55)  # Default value
max_age_slider.pack()
 
tk.Label(preferences_frame, text="Maximum Distance (km):").pack()
max_distance_entry = tk.Entry(preferences_frame)
max_distance_entry.pack()
 
tk.Label(preferences_frame, text="Relationship Type:").pack()
relationship_type_entry = ttk.Combobox(preferences_frame, values=["Short-Term", "Long-Term", "Marriage", "Friendship"])
relationship_type_entry.pack()

photo_upload_btn = tk.Button(preferences_frame, text="Upload New Profile Picture", command=upload_and_update_photo)
photo_upload_btn.pack(pady=10)
 
update_preferences_btn = tk.Button(preferences_frame, text="Update Preferences", command=update_user_preferences)
update_preferences_btn.pack(pady=10)
 
update_profile_btn.config(command=show_preferences)
 
delete_account_btn = tk.Button(preferences_frame, text="Delete My Account", command=delete_account, bg='red', fg='white')
delete_account_btn.pack(pady=10)
 
app.mainloop()