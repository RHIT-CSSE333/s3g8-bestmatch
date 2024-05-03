import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from tkcalendar import Calendar, DateEntry


current_user_id = None
current_preference_id = None

def show_login():
    welcome_frame.pack_forget()
    login_frame.pack()

def show_create_account():
    welcome_frame.pack_forget()
    register_frame.pack()

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
        cursor.execute("SELECT GenderPreference, MinAge, MaxAge, MinDistance, MaxDistance, RelationshipType FROM Preference WHERE PreferenceID = ?", (current_preference_id,))  # Make sure to maintain current_user_id somewhere
        preference = cursor.fetchone()
        conn.close()

        # Populate fields if preferences exist
        if preference:
            gender_pref_entry.set(preference.GenderPreference)
            min_age_entry.delete(0, tk.END)
            min_age_entry.insert(0, preference.MinAge)
            max_age_entry.delete(0, tk.END)
            max_age_entry.insert(0, preference.MaxAge)
            min_distance_entry.delete(0, tk.END)
            min_distance_entry.insert(0, preference.MinDistance)
            max_distance_entry.delete(0, tk.END)
            max_distance_entry.insert(0, preference.MaxDistance)
            relationship_type_entry.set(preference.RelationshipType)
        
        profile_frame.pack_forget()
        preferences_frame.pack()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def update_user_preferences():
    gender_pref = gender_pref_entry.get()
    min_age = int(min_age_entry.get())
    max_age = int(max_age_entry.get())
    min_distance = int(min_distance_entry.get())
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
        cursor.execute("EXEC Update_User_Preferences @PreferenceID = ?, @GenderPreference = ?, @MinAge = ?, @MaxAge = ?, @MinDistance = ?, @MaxDistance = ?, @RelationshipType = ?",
                       (current_preference_id, gender_pref, min_age, max_age, min_distance, max_distance, relationship_type))
        conn.commit()
        messagebox.showinfo("Success", "Preferences updated successfully.")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def create_account():
    email = entry_email_register.get()
    password = entry_password_register.get()
    first_name = entry_fname.get()
    last_name = entry_lname.get()
    dob = cal.get_date().strftime('%Y-%m-%d')  # Format date as yyyy-mm-dd
    gender = gender_combobox.get()
    address = entry_address.get()
    phone_number = entry_phone.get()  # Retrieve phone number from input
    partner_value = entry_partner_values.get()
    photo_link = ""

    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=golem.csse.rose-hulman.edu;'
            'DATABASE=BestMatchDatabase;'
            'UID=bestmatch_esm;'
            'PWD=Findyourbestmatch123'
        )
        cursor = conn.cursor()
        cursor.execute("EXEC Insert_User @Fname = ?, @LName = ?, @DOB = ?, @Photo = ?, @Gender = ?, @Password = ?, @Email = ?, @PhoneNumber = ?, @Address = ?, @PartnerValues = ?",
                       (first_name, last_name, dob, photo_link, gender, password, email, phone_number, address, partner_value))
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
            SELECT p.UserID, p.FName, p.LName, p.PreferenceID
            FROM Person p
            WHERE p.Email = ? AND p.Password = ?
        """, (email, password))

        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Login Success", "You have successfully logged in.")
            current_user_id = user.UserID
            current_preference_id = user.PreferenceID  
            user_fullname_label.config(text=f"{user.FName} {user.LName}")  
            login_frame.pack_forget()
            profile_frame.pack()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


app = tk.Tk()
app.geometry('500x400')
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
gender_combobox = ttk.Combobox(register_frame, values=["Male", "Female", "Non-Binary"])
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

tk.Button(register_frame, text="Create My Account", command=create_account).pack(pady=10)

# Profile Frame
profile_frame = tk.Frame(app)

user_fullname_label = tk.Label(profile_frame, text="", font=("Helvetica", 16))  
user_fullname_label.pack(pady=20)

update_profile_btn = tk.Button(profile_frame, text="Update My Profile", command=show_preferences)
update_profile_btn.pack(pady=10)

# Preferences Frame
preferences_frame = tk.Frame(app)

# Input fields for preferences
tk.Label(preferences_frame, text="Gender Preference:").pack()
gender_pref_entry = ttk.Combobox(preferences_frame, values=["Male", "Female", "Non-Binary", "No Preference"])
gender_pref_entry.pack()

tk.Label(preferences_frame, text="Minimum Age:").pack()
min_age_entry = tk.Entry(preferences_frame)
min_age_entry.pack()

tk.Label(preferences_frame, text="Maximum Age:").pack()
max_age_entry = tk.Entry(preferences_frame)
max_age_entry.pack()

tk.Label(preferences_frame, text="Minimum Distance (km):").pack()
min_distance_entry = tk.Entry(preferences_frame)
min_distance_entry.pack()

tk.Label(preferences_frame, text="Maximum Distance (km):").pack()
max_distance_entry = tk.Entry(preferences_frame)
max_distance_entry.pack()

tk.Label(preferences_frame, text="Relationship Type:").pack()
relationship_type_entry = ttk.Combobox(preferences_frame, values=["Short-Term", "Long-Term", "Marriage", "Friendship"])
relationship_type_entry.pack()

update_preferences_btn = tk.Button(preferences_frame, text="Update Preferences", command=update_user_preferences)
update_preferences_btn.pack(pady=10)

update_profile_btn.config(command=show_preferences)



app.mainloop()