
#create a database in sql
#now creatw a tables as per ypur subject
#and connect with python and run this code in your pc


import mysql.connector
from datetime import date
import speech_recognition as sr
import pandas as pd

# Get the current date
current_date = date.today()
j = current_date.strftime('%d%m%y')
# Print the current date in the default format (YYYY-MM-DD)

print("\n______________________________________________________")
print("|\tToday is :",j,"\t                     |")
print("|____________________________________________________|")
sub=input("enter the subject name :")
print("\n______________________________________________________")
subjects=["ds","toc","se","bc","hci"]#insert ypur subject here

    
listener = sr.Recognizer()
# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chetan",#your sql password
    database="attendance",#your database name
    auth_plugin="mysql_native_password"

)
cur=mydb.cursor()
count=0
presnt_count=0
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=10)  # Increased timeout to 10 seconds
            command = listener.recognize_google(voice)
            command = command.lower()
           
    except sr.WaitTimeoutError:
        pass
        # print("Listening timed out. Please try again.")
    except sr.UnknownValueError:
        pass
        # print("Could not understand the audio.")
    return command
def show():
    get=input("enter the date in this format yyyymmdd:")
    l=f"select NAME,status{get} from '{sub}'"
    l=cur.execute(l)
    re=cur.fetchall()
    max_item_length = max(len(item[0]) for item in re)
    max_description_length = max(len(item[1]) for item in re)

    horizontal_line = "+" + "-" * (max_item_length + 2) + "+" + "-" * (max_description_length + 2) + "+"

    print(horizontal_line)
    for item, description in re:
      print(f"| {item:{max_item_length}} | {description:{max_description_length}} |")
    print(horizontal_line)
j = current_date.strftime('%d%m%y')
if sub.lower() in subjects:
    sub=sub

    print("|                                                    |\n|                                                    |\n|                                                    |\n|                                                    |")
    print("| \twhat do tou want to do choose \t             |\n|\t1) for attendance  \t                     |\n|\t2) show attendance     \t                     |\n|\t3) calcuate average  \t                     |\n|\t4) studnet how many day he/she prsent        |\n|\t4) cerate the exel file                      |\n|            \t               \t                     |\n|            \t               \t                     |\n|            \t               \t                     |\n|____________________________________________________|")
    while True:
        what=input("\n\npress 1 or 2 or 3 or 4 or 5  or 6 for exit:")
        l=f"select * from '{sub}'"
        l=cur.execute(l)
        re=cur.fetchall() 
        if what=="2":
            show()
        elif what=="1":
        
            k=f"alter table '{sub}' add status{j} varchar(100);"
            
            cur.execute(k)
            mydb.commit()
            for i in range(len(re)):
                print(re[i][0], re[i][1])
                while True:
                    command = take_command()
                    command=command.lower()
                    print(command)
                    if command == "prsent" or command == "present":
                            ma = f"UPDATE '{sub}' SET status{j}='present' WHERE roll='{re[i][0]}';"
                            cur.execute(ma)
                            mydb.commit()
                            break
                    elif command=="absent":
                            ma = f"UPDATE '{sub}' SET status{j}='absent' WHERE roll='{re[i][0]}';"
                            cur.execute(ma)
                            mydb.commit()
                            break
                    else:
                            print("Listening timed out. Please try again.")
                cur.execute(ma)

        elif what == "3":
            print("_____________________________________________________")
            print("|                                                    |\n|                                                    |")
            print("|     Calculate Average Attendance                   |")
            print("|                                                    |")
            roll = input("|     Enter the roll of student:        ")
            l = f"select * from '{sub}' where roll='{roll}'"
            l = cur.execute(l)
            re = cur.fetchall()
            
            for i in re:
                for j in i:
                    if j == "prsent" or j == "absent" or j == "present":
                        count += 1
                    if j == "prsent" or j == "present":
                        presnt_count += 1
            print("|                                                    |")
            print(f"| Average Attendance: {(presnt_count / count) * 100}%                          |")
            print("|                                                    |")
            print("|____________________________________________________|")
        elif what == "4":
            print("_____________________________________________________")
            print("|                                                    |\n|                                                    |")
            print("|            Calculate present days                  |")
            print("|                                                    |")
            roll = input("|           Enter the roll of student: ")
            l = f"select * from '{sub}' where roll='{roll}'"
            l = cur.execute(l)
            re = cur.fetchall()
            presnt_count = 0
            for i in re:
             for j in i:
                if j == "prsent" or j == "present":
                    presnt_count += 1
            print("|                                                    |")
            print(f"|           Student's present days: {presnt_count}                |")
            print("|                                                    |")
            print("|                                                    |")
            print("|____________________________________________________|")
        elif (what == "5"):
            try:
        # Query to retrieve data
                sql_query = f"SELECT * FROM '{sub}'"

        # Create a pandas DataFrame from the SQL query result
                df = pd.read_sql_query(sql_query, mydb)

        # Save the DataFrame to an Excel file
                excel_file_name = f"'{sub}'_data.xlsx"
                df.to_excel(excel_file_name, index=False)

                print(f'Data from the "student" table has been exported to "{excel_file_name}".')

            except Exception as e:
                pass
        
        elif what == "6":
            break
        else:
            print("Invalid choice. Please choose a valid option.")    
    what=input("do tou want to show attendance y/n:")
    if what=="Y" or what == "y":
        show()
    else:
        pass 
    print("all done")
else:
    print("you enterd a wrong subject")