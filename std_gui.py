
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from openpyxl import Workbook
from tkinter import simpledialog
from datetime import datetime
import time
from tkinter import filedialog
from PIL import Image, ImageTk
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="student_management"
    )
def login():
    username = username_entry.get()
    password = password_entry.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        messagebox.showinfo("Welcome", f"Welcome, {username}!")
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        username_entry.focus()
def change_password():
    username = username_entry.get()
    old_password = password_entry.get()
    if username == "" or old_password == "":
        messagebox.showerror(
            "Error",
            "Enter Username and Current Password"
        )
        return
    new_password = tk.simpledialog.askstring(
        "Change Password",
        "Enter New Password:",
        show="*"
    )
    if new_password is None or new_password == "":
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login WHERE username=%s AND password=%s",
        (username, old_password)
    )
    if cursor.fetchone():
        cursor.execute(
            "UPDATE login SET password=%s WHERE username=%s",
            (new_password, username)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Password Changed Successfully!"
        )
    else:
        messagebox.showerror(
            "Error",
            "Invalid Username or Current Password"
        )
    cursor.close()
    conn.close()
def add_student():
    roll_no = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if roll_no == "" or name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number!")
        return
    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Error", "Name must contain only letters!")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE roll_no=%s",
            (roll_no,)
        )
        if cursor.fetchone():
            messagebox.showerror("Error", "Roll Number Already Exists!")
            cursor.close()
            conn.close()
            return
        cursor.execute(
            "INSERT INTO students (roll_no, name, age, course, photo_path) VALUES (%s,%s,%s,%s,%s)",
            (roll_no, name, age, course, photo_path)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Student Added Successfully!")
        update_student_count()
        clear_fields()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
def view_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name, age, course FROM students")
    rows = cursor.fetchall()
    view_window = tk.Toplevel(root)
    view_window.title("Student List")
    view_window.geometry("700x400")
    view_window.configure(bg="#EAF4FC")
    scrollbar = tk.Scrollbar(view_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree = ttk.Treeview(
        view_window,
        columns=("Roll", "Name", "Age", "Course"),
        show="headings",
        yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=tree.yview)
    tree.heading("Roll", text="Roll Number")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Course", text="Course")
    tree.column("Roll", width=100, anchor="center")
    tree.column("Name", width=200, anchor="center")
    tree.column("Age", width=80, anchor="center")
    tree.column("Course", width=180, anchor="center")
    tree.pack(fill="both", expand=True)
    for row in rows:
        tree.insert("", tk.END, values=row)
    cursor.close()
    conn.close()
def search_student():
    roll_no = roll_entry.get()
    if roll_no == "":
        messagebox.showerror("Error", "Enter Roll Number")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, age, course, photo_path FROM students WHERE roll_no=%s",
        (roll_no,)
    )
    row = cursor.fetchone()
    if row:
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        name_entry.insert(0, row[0])
        age_entry.insert(0, row[1])
        course_entry.insert(0, row[2])
        photo_path = row[3]
        if photo_path:
            image = Image.open(photo_path)
            image = image.resize((120, 120))
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
    else:
        messagebox.showerror("Error", "Student Not Found")
    cursor.close()
    conn.close()
def update_student():
    roll_no = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if roll_no == "":
        messagebox.showerror("Error", "Enter Roll Number")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name=%s, age=%s, course=%s WHERE roll_no=%s",
        (name, age, course, roll_no)
    )
    conn.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student Updated Successfully!")
    else:
        messagebox.showerror("Error", "Student Not Found!")
    cursor.close()
    conn.close()
def delete_student():
    roll_no = roll_entry.get()
    if roll_no == "":
        messagebox.showerror("Error", "Enter Roll Number")
        return
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )
    if not confirm:
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE roll_no=%s",
        (roll_no,)
    )
    conn.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student Deleted Successfully!")
        update_student_count()
        clear_fields()
    else:
        messagebox.showerror("Error", "Student Not Found!")
    cursor.close()
    conn.close()
def update_clock():
    current_time = time.strftime("%I:%M:%S %p")
    clock_label.config(text=f"🕒 Time : {current_time}")
    root.after(1000, update_clock)
def export_to_excel():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name, age, course FROM students")
    rows = cursor.fetchall()
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Students"
    sheet.append(["Roll Number", "Name", "Age", "Course"])
    for row in rows:
        sheet.append(row)
    workbook.save("students.xlsx")
    cursor.close()
    conn.close()
    messagebox.showinfo(
        "Success",
        "Student data exported to students.xlsx successfully!"
    )
def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    photo_label.config(
        text="❌ No Photo Selected",
        image=""
    )
    photo_label.image = None
    image_label.config(image="")
    image_label.image = None
    roll_entry.focus()
def choose_photo():
    global photo_path
    filename = filedialog.askopenfilename(
        title="Select Student Photo",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )
    if filename:
        photo_path = filename
        photo_label.config(text="✅ Photo Selected")
def update_student_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    count_label.config(text=f"📊 Total Students : {total}")
    cursor.close()
    conn.close()
photo_path = ""
root = tk.Tk()
root.title("Student Management System")
root.geometry("650x760")
root.withdraw()
root.configure(bg="#EAF4FC")
title_label = tk.Label(
    root,
    text="🎓 Student Management System",
    font=("Arial", 20, "bold"),
    bg="#EAF4FC",
    fg="darkblue"
)
title_label.pack(pady=20)
count_label = tk.Label(
    root,
    text="📊 Total Students : 0",
    font=("Arial", 12, "bold"),
    bg="#EAF4FC",
    fg="darkgreen"
)
count_label.pack(pady=5)
status_label = tk.Label(
    root,
    text="🟢 Database Status : Connected",
    font=("Arial", 12, "bold"),
    bg="#EAF4FC",
    fg="green"
)
status_label.pack(pady=3)
today = datetime.now().strftime("%d-%m-%Y")
date_label = tk.Label(
    root,
    text=f"📅 Date : {today}",
    font=("Arial", 12, "bold"),
    bg="#EAF4FC",
    fg="darkblue"
)
date_label.pack(pady=3)
clock_label = tk.Label(
    root,
    text="🕒 Time :",
    font=("Arial", 12, "bold"),
    bg="#EAF4FC",
    fg="purple"
)
clock_label.pack(pady=3)
form_frame = tk.Frame(root, bg="#EAF4FC")
form_frame.pack(pady=10)
login_window = tk.Toplevel()
login_window.title("Login")
login_window.geometry("300x200")
tk.Label(login_window, text="Username").pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack()
tk.Label(login_window, text="Password").pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()
login_button = tk.Button(
    login_window,
    text="Login",
    command=login
)
login_button.pack(pady=15)
login_window.bind("<Return>", lambda event: login())
change_password_button = tk.Button(
    login_window,
    text="Change Password",
    command=change_password
)
change_password_button.pack()
tk.Label(
    form_frame,
    text="Roll Number",
    bg="#EAF4FC",
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=10, pady=10, sticky="e")
roll_entry = tk.Entry(form_frame, width=35)
roll_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Label(
    form_frame,
    text="Name",
    bg="#EAF4FC",
    font=("Arial", 10, "bold")
).grid(row=1, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(form_frame, width=35)
name_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Label(
    form_frame,
    text="Age",
    bg="#EAF4FC",
    font=("Arial", 10, "bold")
).grid(row=2, column=0, padx=10, pady=10, sticky="e")
age_entry = tk.Entry(form_frame, width=35)
age_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Label(
    form_frame,
    text="Course",
    bg="#EAF4FC",
    font=("Arial", 10, "bold")
).grid(row=3, column=0, padx=10, pady=10, sticky="e")
course_entry = tk.Entry(form_frame, width=35)
course_entry.grid(row=3, column=1, padx=10, pady=10)
photo_label = tk.Label(
    form_frame,
    text="❌ No Photo Selected",
    bg="#EAF4FC",
    fg="red",
    font=("Arial", 10, "bold")
)
photo_label.grid(row=4, column=0, columnspan=2, pady=10)
photo_button = tk.Button(
    form_frame,
    text="Choose Photo",
    command=choose_photo,
    bg="navy",
    fg="white",
    font=("Arial", 10, "bold"), 
    width=20
)
photo_button.grid(row=5, column=0, columnspan=2, pady=10)
image_label = tk.Label(
    form_frame,
    bg="#EAF4FC"
)
image_label.grid(row=6, column=0, columnspan=2, pady=10)
button_frame = tk.Frame(root, bg="#EAF4FC")
button_frame.pack(pady=20)
add_button = tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    bg="green",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
add_button.grid(row=0, column=0, padx=10, pady=10)
view_button = tk.Button(
    button_frame,
    text="View Students",
    command=view_students,
    bg="blue",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
view_button.grid(row=0, column=1, padx=10, pady=10)
search_button = tk.Button(
    button_frame,
    text="Search Student",
    command=search_student,
    bg="gold",
    fg="black",
    font=("Arial", 10, "bold"),
    width=20
)
search_button.grid(row=1, column=0, padx=10, pady=10)
update_button = tk.Button(
    button_frame,
    text="Update Student",
    command=update_student,
    bg="orange",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
update_button.grid(row=1, column=1, padx=10, pady=10)
delete_button = tk.Button(
    button_frame,
    text="Delete Student",
    command=delete_student,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
delete_button.grid(row=2, column=0, padx=10, pady=10)
clear_button = tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    bg="gray",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
clear_button.grid(row=2, column=1, padx=10, pady=10)
export_button = tk.Button(
    button_frame,
    text="Export to Excel",
    command=export_to_excel,
    bg="purple",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
export_button.grid(row=3, column=0, padx=10, pady=10)
exit_button = tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy,
    bg="darkred",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)
exit_button.grid(row=3, column=1, padx=10, pady=10)
update_student_count()
update_clock()
root.mainloop()