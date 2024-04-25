import tkinter as tk
from tkinter import messagebox
import pyodbc

def show_login():
    welcome_frame.pack_forget()
    login_frame.pack()

def show_create_account():
    welcome_frame.pack_forget()
    # This is where you would call another function to display the registration form
    messagebox.showinfo("Create Account", "Here you could implement registration functionality.")

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
app.geometry('500x250')
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

app.mainloop()
