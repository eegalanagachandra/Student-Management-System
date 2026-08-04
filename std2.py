import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naga@0992",
        database="student_management"
    )
def add_student():
    while True:
        roll_no = input("Enter Roll Number: ").strip()
        if roll_no == "":
            print("Roll Number cannot be empty!")
        else:
            break
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE roll_no=%s",
        (roll_no,)
    )
    if cursor.fetchone():
        print("Roll Number Already Exists!")
        cursor.close()
        conn.close()
        return
    cursor.close()
    conn.close()
    while True:
        name = input("Enter Name: ").strip()
        if name == "":
            print("Name cannot be empty!")
        else:
            break
    while True:
        age = input("Enter Age: ").strip()
        if age.isdigit():
            break
        else:
            print("Age must be a number!")
    while True:
        course = input("Enter Course: ").strip()
        if course == "":
            print("Course cannot be empty!")
        else:
            break
    student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course
    }
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO students (roll_no, name, age, course) VALUES (%s, %s, %s, %s)",
    (roll_no, name, age, course)
    )
    conn.commit()
    conn.close()
    print("Student Added Successfully!")
def view_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name, age, course FROM students")
    students = cursor.fetchall()
    if len(students) == 0:
        print("No Student Records Found!")
    else:
        print("\n===== STUDENT LIST =====")
        for student in students:
            print(f"Roll No : {student[0]}")
            print(f"Name    : {student[1]}")
            print(f"Age     : {student[2]}")
            print(f"Course  : {student[3]}")
            print("----------------------------")
    cursor.close()
    conn.close()
def search_student():
    search_roll = input("Enter Roll Number to Search: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT roll_no, name, age, course FROM students WHERE roll_no=%s",
        (search_roll,)
    )
    student = cursor.fetchone()
    if student:
        print("\n===== STUDENT FOUND =====")
        print(f"Roll No : {student[0]}")
        print(f"Name    : {student[1]}")
        print(f"Age     : {student[2]}")
        print(f"Course  : {student[3]}")
    else:
        print("Student Not Found!")
    cursor.close()
    conn.close()
def update_student():
    update_roll = input("Enter Roll Number to Update: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE roll_no=%s",
        (update_roll,)
    )
    student = cursor.fetchone()
    if student:
        print("Student Found!")
        new_name = input("Enter New Name: ")
        new_age = input("Enter New Age: ")
        new_course = input("Enter New Course: ")
        cursor.execute(
            "UPDATE students SET name=%s, age=%s, course=%s WHERE roll_no=%s",
            (new_name, new_age, new_course, update_roll)
        )
        conn.commit()
        print("Student Updated Successfully!")
    else:
        print("Student Not Found!")
    cursor.close()
    conn.close()
def delete_student():
    delete_roll = input("Enter Roll Number to Delete: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE roll_no=%s",
        (delete_roll,)
    )
    student = cursor.fetchone()
    if student:
        cursor.execute(
            "DELETE FROM students WHERE roll_no=%s",
            (delete_roll,)
        )
        conn.commit()
        print("Student Deleted Successfully!")
    else:
        print("Student Not Found!")
    cursor.close()
    conn.close()
while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. update student")
    print("5. Delete Student")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Thank You! Exiting Student Management System...")
        break
    else:
        print("Invalid Choice! Please Try Again.")