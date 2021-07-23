import sqlite3
import sys, traceback
import re

#Change connect(thisthing) to exercise.db when testing is complete
# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('workout_tracker.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

try:
    c.execute('''CREATE TABLE IF NOT EXISTS  benefit(
                benefit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                benefit_name varchar(45) NOT NULL UNIQUE
                )''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (1, "arms")''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (2, "legs")''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (3, "chest")''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (4, "shoulders")''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (5, "back")''')
    # c.execute('''INSERT INTO benefit (benefit_id, benefit_name) VALUES (6, "core")''')
except:
    traceback.print_exc(file=sys.stdout)
    # print("There was an error creating the 'benefit' table")

try:
    c.execute('''CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(40),
            password VARCHAR(255),
            email VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255)
            )''')

except:
    print("There was an error creating the 'user' table.")

try:
    c.execute('''CREATE TABLE IF NOT EXISTS exercise(
            exercise_id INTEGER PRIMARY KEY,
            exercise_name VARCHAR(40) NOT NULL UNIQUE
            )''')

except:
    print("There was an error creating the 'exercise' table.")

try:
    c.execute('''CREATE TABLE IF NOT EXISTS workout(
            workout_id INTEGER PRIMARY KEY,
            start datetime,
            end datetime
            )''')

except:
    print("There was an error creating the 'workout' table")


try:
    c.execute('''CREATE TABLE IF NOT EXISTS workout_exercise(
            workout_id INTEGER,
            exercise_id INTEGER,
            UNIQUE (workout_id, exercise_id),
            FOREIGN KEY(workout_id) REFERENCES workout(workout_id),
            FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id)
            )''')

except:
    # traceback.print_exc(file=sys.stdout)
    print("There was an error creating the 'workout_exercise' table")

try:
    c.execute('''CREATE TABLE IF NOT EXISTS user_workout(
            uw_id INTEGER PRIMARY KEY AUTOINCREMENT,
            workex_id INTEGER,
            exercise_id INTEGER,
            weight INTEGER,
            reps INTEGER,
            FOREIGN KEY(workex_id) REFERENCES workout_exercise(we_id),
            FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id)
            )''')

except:
    print("There was an error creating the 'user_workout' table")

try:
    c.execute('''CREATE TABLE IF NOT EXISTS exercise_benefit(
            exercise_id INTEGER,
            benefit_id INTEGER,
            UNIQUE (exercise_id, benefit_id) ON CONFLICT REPLACE,
            FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id),
            FOREIGN KEY(benefit_id) REFERENCES benefit(benefit_id)
            );''')
except:
    print("There was an error creating the 'exerciseBenefit' table")

try:
    c.execute('''
              CREATE VIEW IF NOT EXISTS ex_ben_view
              AS
              SELECT * FROM (exercise ex 
              JOIN exercise_benefit exben
              ON ex.exercise_id == exben.exercise_id
              JOIN benefit ben
              ON exben.benefit_id == ben.benefit_id)
              JOIN exercise ex2
              ON ex.exercise_name == ex2.exercise_name
              ''')
except:
      print("Error creating view.")

try: 
    conn.commit()
except:
    print("Error committing executions.")

try:
    conn.close()
except:
    print("Error closing the database.")
    
def createEx(name):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    try:
        c.execute('INSERT INTO exercise VALUES(null,?)',(name,))
        conn.commit()
        conn.close()
    except:
        conn.commit()
        conn.close()
        return(1)

def viewEx():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM exercise;')
    for exer in c:
        print(str(exer[0])+":\t"+exer[1])
    conn.commit()
    conn.close()

def createBen(name):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('INSERT INTO benefit VALUES(null,?)',(name,))
    conn.commit()
    conn.close()

def viewBen():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM benefit;')
    for ben in c:
        print(str(ben[0])+":\t"+ben[1])
    conn.commit()
    conn.close()

def createExBen(ename,bname):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM exercise WHERE exercise_name ="'+ename+'"')
    exer_id = c.fetchone()[0]
    
    c.execute('SELECT * FROM benefit WHERE benefit_name ="'+bname+'"')
    ben_id = c.fetchone()[0]
    
    c.execute('INSERT INTO exercise_benefit VALUES(?,?)',(exer_id,ben_id))
    conn.commit()
    conn.close()
    
def createUser(username,password,email,first_name,last_name):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('INSERT INTO user VALUES(null,?,?,?,?,?)',(username,password,email,first_name,last_name))
    conn.commit()
    conn.close()
    
def viewUsers():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM user')
    users = c.fetchall()
    if len(users) == 0:
        print("\nNo users present in the database. Add a user to start tracking.")
    for user in users:
        print(user)
    conn.commit()
    conn.close()
    
def viewExByBen():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    benefit = input("\nWhat is the benefit you want to filter by?\t")
    c.execute('SELECT * FROM ex_ben_view WHERE benefit_name = "'+benefit+'"')
    result = c.fetchall()
    if len(result)==0:
        print("\nThere were no exercises found with that benefit.")
    else:
        for ex in result:
            print(str(ex[0])+":\n\t "+ex[1]+"\nBenefits:\n"+ex[5])
            print("---------------------------------------")
        conn.commit()
        conn.close()

def getBenNameById(id):
    conn=sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM benefit WHERE benefit_id = "'+str(id)+'"')
    ben_name = c.fetchone()[1]
    conn.commit()
    conn.close()
    return (ben_name)

def getExNameById(id):
    conn=sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM exercise WHERE exercise_id = "'+str(id)+'"')
    exer_name = c.fetchone()[1]
    conn.commit()
    conn.close()
    return (exer_name)

def getBenNameListByExId(id):
    ben_name_list = []
    conn=sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM exercise_benefit WHERE exercise_id = "'+str(id)+'"')
    # object with all rows of queried exercise_id
    for ex_ben in c:
        ben_name_list.append(getBenNameById(ex_ben[2]))
    conn.commit()
    conn.close()
    return (ben_name_list)

def viewExBen():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('''SELECT * FROM ex_ben_view;''')
    ex_dict = {"1":{"ex_name":"","bens":[]}}
    # For each row in ex_ben_view (exercise paired with single benefit)
    for exben in c:
        # save tuple parts to variables
        ex_id = exben[0]
        ex_name = exben[1]
        ben_name = exben[5]

        if str(ex_id) in ex_dict.keys():
            ex_dict[str(ex_id)].update({"ex_name":ex_name})
            ex_dict[str(ex_id)]["bens"].append(ben_name)
        else:
            ex_dict[str(ex_id)]={"ex_name":ex_name,"bens":[ben_name]}
        
    for ex_id in ex_dict:
        if ex_id[0] == "":
            print("\nNo exercises found. Add an exercise to start tracking.")
            break
        else:
            print("Name: "+"\n\t"+ex_dict[str(ex_id)]["ex_name"])
            print("Benefits: ")
            for ben in ex_dict[str(ex_id)]["bens"]:
                print("\t"+ben)
            print("--------------------------")
    conn.commit()
    conn.close()

def createWorkout(start, end):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('INSERT INTO workout VALUES(null,?,?)',(start,end))
    conn.commit()
    conn.close()
    
def viewWorkouts():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM workout')
    for workout in c:
        print(workout)
    conn.commit()
    conn.close()

def createUserWorkout(work_exer_id,exer_id,weight,reps):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('INSERT INTO user_workout VALUES(null,?,?,?,?)',(work_exer_id,exer_id,weight,reps))
    conn.commit()
    conn.close()

def viewUserWorkout():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM user_workout')
    for workout in c:
        print(workout)
    conn.commit()
    conn.close()

def createWorkoutExercise(workout_id, exercise_id):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('INSERT INTO workout_exercise VALUES(null,?,?)',(workout_id,exercise_id))
    conn.commit()
    conn.close()
    
def viewWorkoutExercise():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM workout_exercise')
    for workout in c:
        print(workout)
    conn.commit()
    conn.close()

def exerciseExists(ex_name):
    return(createEx(ex_name))

def benIdByName(ben_name):
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM benefit WHERE benefit_name ="'+ben_name+'"')
    ben_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return(ben_id)

def addExercise():
    ex_name = input("What is the name of the exercise?")
    benefits = []
    if(not exerciseExists(ex_name)):
        createEx(ex_name)
        benefits = addBensToList(ex_name)
        print("'"+ex_name+"' and benefits have been added to the database.")
        for ben_name in benefits:
            createExBen(ex_name, ben_name)
        print(benefits)
    else:
        print("\nThat exercise is already in the database.")

def addBensToList(ex_name):
    ids = []
    ben_names = []
    more = "y"
    while more == "y":
        viewBen()
        choice = input("Which of these are benefits of "+ex_name+"?\nPlease choose the corresponding number.\t")
        while not re.match("^[1-"+str(countBenefits())+"]{1}$",choice):
            viewBen()
            choice = input("I don't understand, try again.\nPlease choose the corresponding number.\t")
        ids.append(int(choice))
        more = input("\nIs there another benefit of this exercise? ('y'or 'n')\n")
        while not re.match("(y|n)$",more):
            more = input("\nI don't understand. Is there another benefit of this exercise? ('y'or 'n')\t") 
    for num in ids:
        ben_names.append(getBenNameById(num))
    return(ben_names)

def countBenefits():
    conn = sqlite3.connect('workout_tracker.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    c.execute('SELECT * FROM benefit')
    benefits = c.fetchall()
    conn.commit()
    conn.close()
    return(len(benefits))


####################
##  MAIN FUNCTION ##
####################

def tracker():
    print("\nWELCOME TO WORKOUT TRACKER")
    menu_choice = mainMenu()
    while not re.match("^[1-5]{1}$",menu_choice):
        print("Not a valid choice, select another option.")
        menu_choice = mainMenu()
    if menu_choice == "1":
        userMenu()
    elif menu_choice == "2":
        exerciseMenu()
    elif menu_choice == "3":
        workoutsMenu()
    elif menu_choice == "4":
        benefitMenu()
    elif menu_choice == "5":
        print("\nNow closing...")
        print("Thank you for using Workout Tracker")
        print("==========================\n")
        sys.exit(1)

###########
## MENUS ##
###########

def benefitMenu():
    print("\nBENEFITS MENU")
    print("==========================")
    print("\t 1. View Benefits")
    print("\t 2. Create Benefits")
    print("\t 3. Return to Main Menu")
    ben_choice = input("\nWhat would you like to do?\t")
    while not re.match("^[1-3]{1}$", ben_choice):
        ben_choice = input("\nNot a valid choice, select another option.\t")
    if ben_choice == "1":
        viewBen()
        benefitMenu()
    elif ben_choice == "2":
        new_ben = input("\nWhat is the new benefit you would like to add?\t")
        accurate = validate(new_ben)
        if (accurate):
            createBen(new_ben)
        benefitMenu()
    elif ben_choice == "3":
        tracker()

def exerciseMenu():
    print("\nEXERCISES MENU")
    print("==========================")
    print("\t 1. View Exercises")
    print("\t 2. Create New Exercise")
    print("\t 3. Find Exercise by Benefits")
    print("\t 4. Return to Main Menu")
    ex_choice = input("\nWhat would you like to do? (pick a number)\t")
    while not re.match("^[1-4]{1}$",ex_choice):
        ex_choice = print("\nNot a valid choice, select another option.\t")
    if ex_choice == "1":
        viewExBen()
        exerciseMenu()
    elif ex_choice == "2":
        addExercise()
        exerciseMenu()
    elif ex_choice == "3":
        viewExByBen()
        exerciseMenu()
    elif ex_choice == "4":
        tracker()  

def userMenu():
    print("\nUSERS MENU")
    print("==========================")
    print("\t 1. View Users")
    print("\t 2. Create New User")
    print("\t 3. Return to Main Menu")
    user_choice = input("\nWhat would you like to do? (pick a number)\t")
    while not re.match("^[1-3]{1}$",user_choice):
        print("\nNot a valid choice, select another option.")
        user_choice = userMenu()
    if user_choice == "1":
        viewUsers()
        userMenu()
    elif user_choice == "2":
        username = input("Please enter the username: ")
        email = input("Please enter the email: ")
        password = input("Please enter the password: ")
        first_name = input("Please enter the first name: ")
        last_name = input("Please enter the last name: ")
        createUser(username,password,email,first_name,last_name)
        userMenu()
    elif user_choice == "3":
        tracker()

def workoutsMenu():
    print("\nWORKOUTS MENU")
    print("==========================")
    print("\t 1. View Workouts")
    print("\t 2. Create Workout")
    print("\t 3. Filter Workouts by Benefit")
    print("\t 4. Return to Main Menu")
    wo_choice = input("What would you like to do?\t")
    while not re.match("^[1-4]{1}$",wo_choice):
        wo_choice = print("\nNot a valid choice, select another option.\t")
    if wo_choice == "1":
        viewWorkouts()
        workoutsMenu()
    elif wo_choice == "2":
        addWorkout()
        workoutsMenu()
    elif wo_choice == "3":
        viewWorkoutByBen()
        workoutsMenu()
    elif wo_choice == "4":
        tracker()  

def mainMenu():
    print("\nMAIN MENU")
    print("==========================")
    print("\t 1. Users")
    print("\t 2. Exercises")
    print("\t 3. Workouts")
    print("\t 4. Benefits")
    print("\t 5. Close Workout Tracker")
    menu_choice = input("\nWhat would you like to do? (pick a number)\t")
    return(menu_choice)

def validate(string):
    ok = input("You entered '"+string+"'. Is this what you meant to type? ")
    while not re.match("",ok):
        ok = input("Please indicate 'y'(yes) or 'n'(no) to confirm. \nDid you mean to type '"+string+"'?")
    if ok == "y":
        return True
    else:
        return False

tracker()