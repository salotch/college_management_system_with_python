import sqlite3
import datetime

db = sqlite3.connect("data_base.db")
cursor = db.cursor()
# cursor.execute("DROP TABLE reg2")
# cursor.execute("DROP TABLE reg1")#to delete table if we need to
# cursor.execute("DROP TABLE students") #to delete table if we need to
cursor.execute("""CREATE TABLE IF NOT EXISTS students
(name TEXT, id INTEGER, level INTEGER, password TEXT, GPA REAL, group_ TEXT)""")
# cursor.execute("DROP TABLE courses") #to delete table if we need to
cursor.execute("""CREATE TABLE IF NOT EXISTS courses
(code TEXT NOT NULL, name TEXT NOT NULL, hours INTEGER NOT NULL)""")
# creating a table with news like the beginning of the second term or the begging of midterm exams
cursor.execute("CREATE TABLE IF NOT EXISTS news(content TEXT,date TEXT)")
# cursor.execute("DROP TABLE registered_courses") #to delete table if we need to

# cursor.execute("CREATE TABLE IF NOT EXISTS registered_courses (id INTEGER, course_code TEXT)")
print("""
*** WELCOME tO COLLAGE MANAGEMENT SYSTEM *** """)


# control can
def control_list():
    print("""
What do want to do?
1 _ Add student.
2 _ Remove student.
3 _ Edit student information.
4 _ Add courses. 
5 _ Remove courses.
6 _ See all information of a student.
7 _ Post News.
8 _ Log Out.
""")

# student can
def student_list():
    print("""What do want to do?
1 _ Register courses.
2 _ Edit courses.
3 _ Choose my group.
4 _ See News.
5 _ Log Out.
""")


# functions of control
def ADD_STUDENT():
    # name
    n = input("Enter the student's full_name: ").capitalize()
    # id
    id = input("Enter the student's ID: ")
    # check from different id
    cursor.execute(f"SELECT id FROM students WHERE id ='{id}'")
    if cursor.fetchone() != None:
        id = input(f"This id '{id}' already in database, enter a different id:  ")
    # level
    l = input("Enter the student's level (1/2/3/4/5/6/7), if more write else: ").lower()
    if l == "else":
        l = input("Enter the student's level: ")
    # password
    password = input("Enter the student's password: ")
    # check from different password
    cursor.execute(f"SELECT password FROM students WHERE password ='{password}'")
    if cursor.fetchone() != None:
        password = input("Error: This password is already exists, Enter a different password: ")

    # GPA of student
    GPA = float(input("Enter the student's GPA: "))
    # check GPA from 0 to 4 only
    while True:
        if not (0 <= GPA <= 4):
            GPA = float(input("Please enter GPA from 0 to 4 only: "))
        else:
            break
    # group
    g = ' '
    stu = (n, id, l, password, GPA, g)
    cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)", stu)
    print("Student information \"added\" successfully")
    print()
    cursor.execute(f"SELECT * FROM students WHERE id = '{id}'")
    data = cursor.fetchall()
    for row in data:
        print(f"""Added information of student:
    (full name => {row[0]}, stu_id => {row[1]}, level=> {row[2]}, password=> {row[3]}, GPA=> {row[4]}, group=>{row[5]})""")
    db.commit()
    cursor.execute("select rowid from students where id=?", (id,))
    row = cursor.fetchone()
    command = " CREATE TABLE IF NOT EXISTS reg" + str(row[0]) + "(code TEXT, name TEXT, hours INTEGER, grade TEXT)"
    cursor.execute(command)  # for every student there is a table called reg and his rowid for his registered_courses
    db.commit()


def REMOVE_STUDENT():
    print("All information in students table:")
    cursor.execute(f"SELECT * FROM students")
    data = cursor.fetchall()
    for row in data:
        print(
            f"""(full name => {row[0]}, stu_id => {row[1]}, level=> {row[2]}, password=> {row[3]}, GPA=> {row[4]}, group=>{row[5]})""")
    while True:
        id = input("Enter the student's ID: ")
        cursor.execute(f"SELECT id FROM students WHERE id = '{id}'")
        if cursor.fetchone() is None:
            id = input("Sorry this id does not exist in database, enter an available ID :")
        else:
            break
    cursor.execute("select rowid from students where id=?", (id,))
    row = cursor.fetchone()
    command = "DROP TABLE reg" + str(row[0])
    cursor.execute(command)
    cursor.execute(f"DELETE FROM students WHERE id = '{id}'")
    print("ALL information of student \"removed\" successfully")
    print()
    print("All information in students table after removing:")
    cursor.execute(f"SELECT * FROM students")
    data = cursor.fetchall()
    for row in data:
        print(
            f"""(full name => {row[0]}, stu_id => {row[1]}, level=> {row[2]}, password=> {row[3]}, GPA=> {row[4]}, group=>{row[5]})""")
    db.commit()


def EDIT_STUDENT_INFORMATION():
    print("All information in students table:")
    cursor.execute(f"SELECT * FROM students")
    data = cursor.fetchall()
    for row in data:
        print(
            f"""(full name => {row[0]}, stu_id => {row[1]}, level=> {row[2]}, password=> {row[3]}, GPA=> {row[4]}, group=>{row[5]})""")

    id = input("Enter the student's ID: ")
    while True:
        cursor.execute(f"SELECT rowid,* FROM students WHERE id = '{id}'")
        row = cursor.fetchone()
        if row is None:
            id = input("Sorry this ID does not exist in database, enter an available ID :")
        else:
            break
    row_id = row[0]
    print(
        f"""(full name => {row[1]}, stu_id => {row[2]}, level=> {row[3]}, password=> {row[4]}, GPA=> {row[5]}, group=>{row[6]})""")
    command1 = "SELECT * from reg" + str(row_id)
    cursor.execute(command1)
    print("Student's Registered courses")
    for rows in cursor.fetchall():
        print(f"""(Code => {rows[0]}, Name=> {rows[1]}, Hours=> {rows[2]}, Grade=> {rows[3]})""")
    print("\n")
    end = True
    # default values
    n = row[1]
    id = row[2]
    l = row[3]
    p = row[4]
    GPA = row[5]
    g = row[6]
    while end:
        choice = input("""Which Information Do you Want to Edit?
1)Student's Full Name
2)Student's ID
3)Student's Level
4)Student's Password
5)Student's GPA
6)Student's Group
7)Student's Registered courses
8)Log Out
            """)
        flag_e = False

        if choice == '1':
            n = input("Enter the student's full_name: ").capitalize()
            flag_e = True
        elif choice == '2':
            id = input("Enter the student's ID: ")
            while True:
                cursor.execute(f"SELECT id FROM students WHERE id = '{id}'")
                i = cursor.fetchone()
                if i is None:
                    break
                else:
                    id = input("Sorry this id already exists in database, enter a valid ID: ")
            flag_e = True
        elif choice == '3':
            # level
            l = input("Enter the new level of the student (1/2/3/4/5/6/7), if more write else: ").lower()
            if l == "else":
                l = input("Enter the student's level: ")
            flag_e = True
        elif choice == '4':
            # password
            p = input("Enter the new password of the student: ")
            flag_e = True
        elif choice == '5':
            # GPA of student
            GPA = float(input("Enter the new GPA of the student: "))
            # check GPA from 0 to 4 only
            while not (0 <= GPA <= 4):
                GPA = float(input("Please enter GPA from 0 to 4 only: "))
            flag_e = True
        elif choice == '6':
            # group
            g = input("Enter the student's group, if there is no group press enter: ").capitalize()
            if g is None:
                g = ' '
            flag_e = True
        elif choice == '7':
            code = input("Enter The Code of The Course You Want to Edit its Grade: ")
            command1 = "SELECT * from reg" + str(row_id) + " WHERE code =?"
            while True:
                cursor.execute(command1, (code,))
                j = cursor.fetchone()
                if j is None:
                    code = input("Enter The Right Code of The Course You Want to Edit its Grade: ")
                else:
                    grade = input("Enter its Grade(A+,A,B+,B,C+,C,D+,D): ")
                    command1 = f"UPDATE reg" + str(row_id) + " SET grade = ? WHERE code=?"
                    cursor.execute(command1, (grade, code))
                    break
            flag_e = True
        if flag_e:
            stu = (n, id, l, p, GPA, g)
            cursor.execute(
                f"UPDATE students SET name = ?, id = ?, level = ?, password = ?, GPA = ?, group_ = ? where rowid = {row_id}",
                stu)
            print("Student information \"edited\" successfully")
            print()
            cursor.execute(f"SELECT * FROM students WHERE rowid = '{row_id}'")
            data = cursor.fetchall()
            for k in data:
                print(f"""edited information of the student:
                        (full name => {k[0]}, stu_id => {k[1]}, level=> {k[2]}, password=> {k[3]}, GPA=> {k[4]}, group=>{k[5]})""")
            command1 = "SELECT * from reg" + str(row_id)
            cursor.execute(command1)
            for rr in cursor.fetchall():
                print(f"""(Code => {rr[0]}, Name=> {rr[1]}, Hours=> {rr[2]}, Grade=> {rr[3]})""")
        if choice == '8':
            end = False
    db.commit()


def ADD_COURSES():
    while True:
        c = input("Enter the code of the course you want to add: ").lower()
        cursor.execute("SELECT code from courses WHERE code = ?", (c,))
        if cursor.fetchone() is not None:
            print(f"Sorry this code '{c}' already exist in your courses")
        else:
            break

    n = input("Enter the name of the course: ")
    n = n.lower()
    h = input("Enter the hours of the course: ")

    courses = [(c, n, h)]
    # courses.append(course) i will do something like that with sql
    cursor.executemany("INSERT INTO courses VALUES (?,?,?)", courses)
    print("courses \"added\" successfully")
    print("")
    print("Added courses: ")
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    for row in data:
        print(row)
    db.commit()


def REMOVE_COURSES():
    # display available courses
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    print("Available Courses:")
    for course in courses:
        print(f"(The course code=> '{course[0]}', course name=> '{course[1]}', course hours=> {course[2]} hours)")
    print("\n")
    while True:
        course_code = input("Enter the code of the course you want to remove: ").lower()
        cursor.execute("SELECT * from courses WHERE code = ?", (course_code,))
        if cursor.fetchone() is None:
            print(f"Sorry this course '{course_code}' not exist in your courses")
        else:
            break
    cursor.execute("DELETE FROM courses WHERE code =?", (course_code,))
    print("course information \"removed\" successfully")
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    print("\nThe left Courses are:")
    for course in data:
        print(f"(The course code=> '{course[0]}', course name=> '{course[1]}', course hours=> {course[2]} hours)")
    db.commit()


def SEE_ALL_INFORMATION_OF_A_STUDENT():
    while True:
        id = input("Enter the student's ID: ")
        cursor.execute(f"SELECT id FROM students WHERE id = '{id}'")
        if cursor.fetchone() is None:
            print("Sorry this ID does not exist in database")
        else:
            break
    cursor.execute(f"SELECT * FROM students WHERE id = '{id}'")
    print("")
    data = cursor.fetchall()
    for row in data:
        print(f"""All information of the student:
(full name => {row[0]}, stu_id => {row[1]}, level=> {row[2]}, password=> {row[3]}, GPA=> {row[4]}, group=>{row[5]})""")

    cursor.execute("select rowid from students where id=?", (id,))
    row = cursor.fetchone()
    command = "SELECT * from reg" + str(row[0])
    cursor.execute(command)
    data = cursor.fetchall()
    print("Registered courses: ")
    for row in data:
        print(f"""(Code => {row[0]}, Name=> {row[1]}, Hours=> {row[2]}, Grade=> {row[3]})""")
    db.commit()


def POST_NEWS():
    new = input("Type The News You Want To Post: ")
    date = "Wrote in " + str(datetime.datetime.now())
    cursor.execute("INSERT INTO news VALUES(?,?)", (new, date))
    db.commit()


# functions of student
def LOGIN():
    print("")
    print("Student login")
    print("")
    while True:
        id = input("Enter your ID: ")
        password = input("Enter your password: ")
        cursor.execute("SELECT id FROM students WHERE id=? AND password=?", (id, password))
        result = cursor.fetchone()
        if result:
            cursor.execute("SELECT name FROM students WHERE id=?", (id,))
            name = cursor.fetchone()
            print("""\nLogin successful ! 
            welcome""", name[0])
            return id
            break
        else:
            print("Login failed. Invalid credentials.")
    db.commit()


def REGISTER_COURSES(id):
    # display the courses that the student already registered to
    print("The Courses That You Have Registered to")
    cursor.execute("select rowid from students where id=?", (id,))
    r = cursor.fetchone()
    row_id = r[0]
    command = "SELECT * from reg" + str(row_id)
    cursor.execute(command)
    data = cursor.fetchall()
    for rr in data:
        print(f"""(code => {rr[0]}, Name=> {rr[1]}, Hours=> {rr[2]}, Grade=> {rr[3]})""")
    print("\n")
    # display available courses
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    print("Available Courses:")
    for course in courses:
        print(f"(the course code=> '{course[0]}', course name=> '{course[1]}', course hours=> {course[2]} hours)")
    print("\n")
    while True:
        code = input("Enter the code of the course you want to register: ")
        cursor.execute("SELECT * FROM courses WHERE code = ?", (code,))
        c = cursor.fetchone()
        if c:
            command = "SELECT * from reg" + str(row_id) + " WHERE code=?"
            cursor.execute(command, (code,))
            r = cursor.fetchone()
            if r:
                print("\n")
                print("You Have Registered to This Course Before")
            else:
                code = c[0]
                name = c[1]
                hours = c[2]
                break
        else:
            print("\n")
            print(f"Error: Course with ID '{code}' does not exist.")
    # to check if there is enough hours to register this course
    command = "SELECT * from reg" + str(row_id) + " WHERE grade=' '"
    cursor.execute(command)
    used_hours = 0
    data = cursor.fetchall()
    for r in data:
        used_hours += r[2]
    if used_hours == 18 and used_hours + hours != 18:
        print("\n")
        print("You don't have enough hours in this term to register new course")
        return
    elif used_hours + hours > 18:
        print("\n")
        print("You Only Have " + str(18 - used_hours) + " Hours Left You Cannot Register This Course")
        print("\n")
        return
    else:
        command = "INSERT INTO reg" + str(row_id) + " VALUES(?,?,?,?)"
        cursor.execute(command, (code, name, hours, ' '))
        command1 = "SELECT * from reg" + str(row_id)
        cursor.execute(command1)
        for row in cursor.fetchall():
            print(f"""(Code => {row[0]}, Name=> {row[1]}, Hours=> {row[2]}, Grade=> {row[3]})""")
        print("\n")
        print("Course registered successfully!")
        print("\n")
        db.commit()


def CHOOSE_GROUP(id):
    #   check if the student already have chose groups or not
    cursor.execute(f"SELECT * FROM students WHERE id={id}")
    d = cursor.fetchone()
    if d[5] != ' ':
        print("You Have Choose your Group Before")
        return
    while True:
        g = input("Which group Do You Want? (A/B): ")
        if g == "A" or g == "B" or g == "a" or g == "b":
            g = g.upper()
            cursor.execute(f"UPDATE students SET group_ =(?) WHERE id={id}", (g,))
            print("group added successfully!")
            break
        else:
            print("Invalid Group!")

    db.commit()


def SEE_NEWS():
    cursor.execute("SELECT * FROM news order by date DESC")
    data = cursor.fetchall()
    for row in data:
        print(row[0], "\n", row[1], "\n__________________________________________________________")
    db.commit()


def auth_control():
    print("")
    print("Control login")
    print("")
    flag = True
    while flag:
        username = input(str("Enter the user name: ")).lower()
        password = input(str("Enter the password: "))
        if username == "control":
            if password == '1234567':
                flag = False
                print("""Login successful ! 
            Welcome to Control's Page !""")
            else:
                print("Incorrect password!")
        else:
            print("Login details not recognized")
    db.commit()


def EDIT_COURSES(id):
    # Print the currently registered courses to the student
    cursor.execute(f"SELECT rowid FROM students WHERE id={id}")
    data = cursor.fetchone()
    row_id = data[0]
    command1 = "SELECT * from reg" + str(row_id)
    cursor.execute(command1)
    courses = cursor.fetchall()
    if courses:
        action = input("Do you want to add or remove a course? (Type 'add' or 'remove'): ").lower()
        if action == 'add':
            REGISTER_COURSES(id)
        elif action == 'remove':
            print("The Courses You Can Remove: ")
            # print the registered courses
            command1 = "SELECT * from reg" + str(row_id) + " WHERE grade =' '"
            cursor.execute(command1)
            for row in cursor.fetchall():
                print(f"""(Code => {row[0]}, Name=> {row[1]}, Hours=> {row[2]}, Grade=> {row[3]})""")
            while True:
                course_code_to_remove = input("Enter the course code you want to remove: ")
                # check if the student is registered to the course
                command1 = "SELECT * from reg" + str(row_id) + " WHERE code = ? and grade = ' '"
                cursor.execute(command1, (course_code_to_remove,))
                course_info = cursor.fetchone()
                if course_info:
                    command1 = "DELETE FROM reg" + str(row_id) + " WHERE code = ? "
                    cursor.execute(command1, (course_code_to_remove,))
                    print("Course removed successfully.")
                    break
                else:
                    print("You are not registered for this course")
    else:
        print("You are not registered for any courses.")
    db.commit()



while True:
    user_choice = input("""
        STUDENT
        CONTROL
        EXIT

Enter your choice: """).lower()

    if user_choice == "control":
        auth_control()
        while True:
            control_list()
            control_choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")
            while control_choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                print(f"This value \"{control_choice}\" does not exist, enter a valid value ")
                control_choice = input("Enter your choice (1/2/3/4/5/6/7/8) : ").strip()
            if control_choice == "1":
                ADD_STUDENT()
            elif control_choice == "2":
                REMOVE_STUDENT()
            elif control_choice == "3":
                EDIT_STUDENT_INFORMATION()
            elif control_choice == "4":
                ADD_COURSES()
            elif control_choice == "5":
                REMOVE_COURSES()
            elif control_choice == "6":
                SEE_ALL_INFORMATION_OF_A_STUDENT()
            elif control_choice == "7":
                POST_NEWS()
            elif control_choice == "8":
                break

    elif user_choice == "student":
        id = LOGIN()
        while True:
            print("")
            student_list()
            student_choice = input("Enter your choice (1/2/3/4/5): ")
            while student_choice not in ["1", "2", "3", "4", "5"]:
                print(f"This value \"{student_choice}\" does not exist, enter a valid value: ")
                student_choice = input("Enter your choice (1/2/3/4/5): ").strip()
            if student_choice == "1":
                REGISTER_COURSES(id)
            elif student_choice == "2":
                EDIT_COURSES(id)
            elif student_choice == "3":
                CHOOSE_GROUP(id)
            elif student_choice == "4":
                SEE_NEWS()
            elif student_choice == "5":
                break
    elif user_choice == "exit":
        db.close()
        exit()
    else:
        print("Error: This value does not exist")

