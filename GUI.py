import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
from tkcalendar import Calendar, DateEntry

def show_login():
    welcome_frame.pack_forget()
    login_frame.pack()

def show_create_account():
    welcome_frame.pack_forget()
    register_frame.pack()

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
    # Placeholder for the Photo link, as your UI doesn't include it yet.
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
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def login():
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
        cursor.execute("SELECT * FROM Person WHERE Email = ? AND Password = ?", (email, password))
        if cursor.fetchone():
            messagebox.showinfo("Login Success", "You have successfully logged in.")
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

app.mainloop()