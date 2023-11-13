try:
    import mysql.connector
    import random
    import time
    import os
    import sys
    from pprint import pprint
    
    print("INSTALLATION INSTRUCTIONS.")
    print("!!change mysql config in line 16 and 23")
    print("!!make sure that the file 'words.txt' is in the same directory as the python file")
    print("!!you can change database name in line 14")
    x = input("If everything is okay then input anything to continue. \n")
    
    dbname = 'gamedatabase'
    # Database config for auto set up ref line 35 to 134
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "asdf",
        "auth_plugin": "mysql_native_password"
    }
    # Main connection to database 
    dbnamed_config = {
        "host": "localhost",
        "user": "root",
        "password": "asdf",
        "database":f'{dbname}',
        "auth_plugin": "mysql_native_password"
    }
    
    def clear_screen():
        os.system("cls")
    
    def typing(message):
        print("")
        #print(message) # Eliminate this after testing...
        for word in message:
            time.sleep(random.choice([0.3, 0.11, 0.08, 0.07,0.07, 0.07, 0.06, 0.06, 0.05, 0.01]))
            sys.stdout.write(word)
            sys.stdout.flush()
        time.sleep(.1)
        return ""

    clear_screen()

    
    # Database setup
    print("Logging Into MYSQL...")
    time.sleep(1)

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    print("Checking if DataBases Exists or not...")
    time.sleep(1)

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
    except Exception as e:
        print("Error Creating Database")
        print(e)
    try:
        cursor.execute(f"USE {dbname}")
    except Exception as e:
        print("Error Selecting Databse")
        print(e)

    print("Checking if table users is set up or not...")
    time.sleep(1)

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
        user_id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        account_creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
        );
        """)
    except Exception as e:
        print("Error Creating Table Users")
        print(e)

    print("Checking if table records is set up or not...")
    time.sleep(1)

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alluserplays (
        time DECIMAL(10,2) NOT NULL,
        time_submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(255) NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );
        """)
    except Exception as e:
        print("Error Creating Table alluserplays")
        print(e)

    print("Checking if table leaderboard is set up or not...")
    time.sleep(1)

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
        user_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        best_time DECIMAL(10,2) NULL,
        PRIMARY KEY (user_id)
        );
        """)
    except Exception as e:
        print("Error Creating Table Leaderboard")
        print(e)
    print("Creating Triggers...")
    time.sleep(1)

    # Trigger

    try:
        create_trigger_sql = """
            CREATE TRIGGER update_trigger
            AFTER INSERT ON alluserplays
            FOR EACH ROW
            BEGIN
                INSERT INTO leaderboard (user_id, name, best_time)
                VALUES (NEW.user_id, NEW.name, NEW.time)
                ON DUPLICATE KEY UPDATE
                name = NEW.name,
                best_time = LEAST(NEW.time, IFNULL(leaderboard.best_time, NEW.time));
            END
            """
        cursor.execute(create_trigger_sql)
        time.sleep(1)
    except Exception as e:
        print("Error Creating Trigger.")
        print("Trigger Might Already exist")
        print(f"ERROR: {e}")
        time.sleep(1.5)


    connection.commit()
    cursor.close()
    connection.close()
    # Database Connection
    database = mysql.connector.connect(**dbnamed_config)
    print(r'''
 _____                             _   _               _____    _        _     _ _     _              _ _ 
/  __ \                           | | (_)             |  ___|  | |      | |   | (_)   | |            | | |
| /  \/ ___  _ __  _ __   ___  ___| |_ _  ___  _ __   | |__ ___| |_ __ _| |__ | |_ ___| |__   ___  __| | |
| |    / _ \| '_ \| '_ \ / _ \/ __| __| |/ _ \| '_ \  |  __/ __| __/ _` | '_ \| | / __| '_ \ / _ \/ _` | |
| \__/\ (_) | | | | | | |  __/ (__| |_| | (_) | | | | | |__\__ \ || (_| | |_) | | \__ \ | | |  __/ (_| |_|
 \____/\___/|_| |_|_| |_|\___|\___|\__|_|\___/|_| |_| \____/___/\__\__,_|_.__/|_|_|___/_| |_|\___|\__,_(_)
                                                                                                          
                                                                                                          
''')
    time.sleep(2)
    cursor = database.cursor()
    x = input('Input Anything to Continue.\n')
    clear_screen()

    def signup():
        clear_screen()
        print()
        print(r'''
 _____ _                         
/  ___(_)                        
\ `--. _  __ _ _ __  _   _ _ __  
 `--. \ |/ _` | '_ \| | | | '_ \ 
/\__/ / | (_| | | | | |_| | |_) |
\____/|_|\__, |_| |_|\__,_| .__/ 
          __/ |           | |    
         |___/            |_|    
''')
        username = input("Enter Your UserName: ")
        password = input("Enter Your Password: ")
        cpass = input("Confirm Your Password: ")
        if password == cpass: 
            sql_command = '''INSERT INTO users(name,password) values(%s,%s)'''
            values = (username,password)
            try:
                cursor.execute(sql_command,values)
                database.commit()
                print(f"User account {username} successfully created.")
                x = input("Input Anything to Continue. \n")
                clear_screen()
            except Exception as e:
                print("Something went wrong while creating the account.")
                print("User might already exsist.")
                print(F"ERROR: {e}")
                x = input("Input Anything to Continue. \n")
        else:
            print("Password Didn't match")
            x = input("Input Anything to Continue.\n")
            clear_screen()

    def login():
        clear_screen()
        print()
        print(r'''
 _                 _       
| |               (_)      
| |     ___   __ _ _ _ __  
| |    / _ \ / _` | | '_ \ 
| |___| (_) | (_| | | | | |
\_____/\___/ \__, |_|_| |_|
              __/ |        
             |___/         
''')
        print()
        user = input("Enter Your UserName: ")
        password = input("Enter Your Password: ")
        try:
            sql_command ='''SELECT * FROM users WHERE name=%s and password=%s'''
            values = (user,password)
            cursor.execute(sql_command,values)
            temp = cursor.fetchall()
            data = temp
            if len(data) > 1:
                print("Multiple account. ERROR!")
                x = input("Input Anything to Continue. \n")
            elif len(data) == 0:
                print("Either Password or Username is wrong.")
                print("Or the account doesn't exist")
                x = input("Input Anything to Continue. \n")
            elif len(data) == 1:
                print("Login Successfull.")
                x = input("Input Anything to Continue to Game Menu.\n")
                user_id = data[0][0]
                gamemenu(user_id,user)
            else:
                print("Something went wrong. #login_conditions")
                x = input("Input Anything to Continue. \n")

        except Exception as e:
            print("Something went wrong while fetching your account.")
            print(f"ERROR: {e}")
            x = input("Input Anything to Continue. \n")

    def submitgamescore(user,id,time):
        sqlcommand = '''INSERT INTO alluserplays (user_id,name,time) values(%s,%s,%s)'''
        values = (id,user,time)
        try:
            cursor.execute(sqlcommand,values)
            database.commit()
            return 'Score Submitted'
        except Exception as e:
            return f"Error, Couldn't Sumbit score. ERROR: {e}"

    def playerrecords(id,user):
        clear_screen()
        print(r'''
__   __                ______                       _     
\ \ / /                | ___ \                     | |    
 \ V /___  _   _ _ __  | |_/ /___  ___ ___  _ __ __| |___ 
  \ // _ \| | | | '__| |    // _ \/ __/ _ \| '__/ _` / __|
  | | (_) | |_| | |    | |\ \  __/ (_| (_) | | | (_| \__ \
  \_/\___/ \__,_|_|    \_| \_\___|\___\___/|_|  \__,_|___/
                                                          
                                                          
''')
        sqlcommand = '''SELECT * FROM alluserplays WHERE name=%s and user_id=%s'''
        values = (user,id)
        try:
            cursor.execute(sqlcommand,values)
            fetch = cursor.fetchall()
            data = fetch
            if len(data) != 0:
                for i in data:
                    playertime = i[0]
                    date_submitted = i[1]
                    name = i[2]
                    userid = i[3]
                    formatted_data =f"UserID:{userid}, Player:{name}, Time:{playertime}, Submission Date:{date_submitted}"
                    print(formatted_data)
                    print("~-~-~-~-~")
                x = input("Input Anything to Continue. \n")
                clear_screen()
            else:
                print("No Records found.")
                x = input("Input Anything to Continue.\n")
                clear_screen()
                
        except Exception as e:
            print("Something went wrong.")
            print(f"ERROR: {e}")    

    def leaderboard():
        clear_screen()
        print(r'''
 _                    _           _                         _ 
| |                  | |         | |                       | |
| |     ___  __ _  __| | ___ _ __| |__   ___   __ _ _ __ __| |
| |    / _ \/ _` |/ _` |/ _ \ '__| '_ \ / _ \ / _` | '__/ _` |
| |___|  __/ (_| | (_| |  __/ |  | |_) | (_) | (_| | | | (_| |
\_____/\___|\__,_|\__,_|\___|_|  |_.__/ \___/ \__,_|_|  \__,_|
                                                              
                                                              
''')
        print()
        sqlcommand = '''SELECT user_id, name, best_time FROM leaderboard ORDER BY best_time ASC'''
        cursor.execute(sqlcommand)
        rows = cursor.fetchall()
        for row in rows:
            user_id, name, best_time = row
            formatted_info = f'Time: {best_time}, Name: {name}, userID: {user_id}'
            print(formatted_info)
        x = input("Input Anything to Continue. \n")

    def how_to_play():
        clear_screen()
        print()
        print(r'''
 _    _               _______          _     
| |  | |             | | ___ \        | |    
| |  | | ___  _ __ __| | |_/ /   _ ___| |__  
| |/\| |/ _ \| '__/ _` |    / | | / __| '_ \ 
\  /\  / (_) | | | (_| | |\ \ |_| \__ \ | | |
 \/  \/ \___/|_|  \__,_\_| \_\__,_|___/_| |_|
                                                                                         
''')
        print()
        print("The aim to get the fastest time for 15 random words.")
        print("For each correct word, your final time will be reduced by 1 second.")
        print("For each wrong word, your final time will be increased by 1 second.")
        print("~Format~")
        print('''
    +2.58 word time.                              <---- Time you took to clear each word
    Correct! -1 seconds.                          <---- Word Status
    Type the following word: umbrella             <---- Word To Type
    ''')
        x = input("Input Anything to Start the Game. \n")

    def timer():
        # Timer
        clear_screen()
        print(r'''
 ____   
|___ \  
  __) | 
 |__ <  
 ___) | 
|____/  
        
''')
        time.sleep(1)
        clear_screen()
        print(r'''
 ___   
|__ \  
   ) | 
  / /  
 / /_  
|____| 
       
''')
        time.sleep(1)
        clear_screen()
        print(r'''
 __  
/_ | 
 | | 
 | | 
 | | 
 |_| 
     
''')
        time.sleep(1)
        clear_screen()
        print(r'''
  _______   ______    __       _______   ______    __       _______   ______    __  
 /  _____| /  __  \  |  |     /  _____| /  __  \  |  |     /  _____| /  __  \  |  | 
|  |  __  |  |  |  | |  |    |  |  __  |  |  |  | |  |    |  |  __  |  |  |  | |  | 
|  | |_ | |  |  |  | |  |    |  | |_ | |  |  |  | |  |    |  | |_ | |  |  |  | |  | 
|  |__| | |  `--'  | |__|    |  |__| | |  `--'  | |__|    |  |__| | |  `--'  | |__| 
 \______|  \______/  (__)     \______|  \______/  (__)     \______|  \______/  (__) 
                                                                                    
''')
        time.sleep(1)
        clear_screen()

    def game(id,user):
        
        clear_screen()
        final_time = 0
        words_right = 0
        words_wrong = 0
        wordcounter = 0
        used_words = []
        try:
            with open('words.txt') as file:
                words = [line.strip() for line in file]
        except Exception as e:
            print(f"ERROR: {e}")
            x = input("Input Anything to Start the Game. \n")
            gamemenu(id,user)



        def get_random_word():
            if len(used_words) == len(words):
                return "No more words available."
            while True:
                index = random.randint(0, len(words) - 1)
                if index not in used_words:
                    used_words.append(index)
                    return words[index]
            
            
        print()
        print(r'''
 _    _               _______          _     
| |  | |             | | ___ \        | |    
| |  | | ___  _ __ __| | |_/ /   _ ___| |__  
| |/\| |/ _ \| '__/ _` |    / | | / __| '_ \ 
\  /\  / (_) | | | (_| | |\ \ |_| \__ \ | | |
 \/  \/ \___/|_|  \__,_\_| \_\__,_|___/_| |_|
                                                                                         
''')
        print()
        print("Input Anything Character to Play.")
        print("Input '1' for 'How to Play.'")
        print("Input '2' to go back.")
        try:
            ch = input()
            if ch == '1':
                how_to_play()
            elif ch == '2':
                gamemenu(id,user)
            else:
                pass
        except:
            print("Something went Wrong.")
            print(f"ERROR: {e}")
            x = input("Input Anything to Continue. \n")
            gamemenu(id,user)
        # ini timer
        timer()
        starttime = time.time()
        while wordcounter < 15:
            playword = get_random_word()
            print(f"Type the following word: {playword}")
            word_starttime = time.time()
            playerinput = input()
            print()
            word_endtime = time.time()
            if playerinput == playword:
                print(f"+{round(word_endtime-word_starttime,2)} word time.")
                print("Correct! -1 seconds.")
                words_right += 1
            else:
                print(f"+{round(word_endtime-word_starttime,2)} word time.")
                print("Wrong! +1 seconds.")
                words_wrong += 1
            wordcounter += 1
        endtime = time.time()
        print('=======================================')
        typing(r""""
 _____                        _____                _ 
|  __ \                      |  _  |              | |
| |  \/ __ _ _ __ ___   ___  | | | |_   _____ _ __| |
| | __ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__| |
| |_\ \ (_| | | | | | |  __/ \ \_/ /\ V /  __/ |  |_|
 \____/\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|  (_)
                                                     
                                                                                              
          """)
        print('=======================================')
        print(f"You took {round(endtime-starttime,2)} to finish.")
        print(f"With {words_right} right word(s) and {words_wrong} wrong word(s)")
        final_time = round(endtime-starttime,2) - words_right
        final_time = final_time + words_wrong
        print(f"Your Final time is {round(final_time,2)}")
        sumbit = submitgamescore(user,id,round(final_time,2))
        print(sumbit)
        x = input("Input Anything To Continue. \n")

    def gamemenu(id,user):
        while True:
            clear_screen()
            print()
            print(r'''
 _    _               _______          _     
| |  | |             | | ___ \        | |    
| |  | | ___  _ __ __| | |_/ /   _ ___| |__  
| |/\| |/ _ \| '__/ _` |    / | | / __| '_ \ 
\  /\  / (_) | | | (_| | |\ \ |_| \__ \ | | |
 \/  \/ \___/|_|  \__,_\_| \_\__,_|___/_| |_|
                                                                                         
''')
            print()
            print(f"===Welcome {user}===")
            print("~Game Menu~")
            print("1. Play.")
            print("2. Show All Your Records.")
            print("3. Go Back to Main Menu. (Log out)")
            try:
                ch = int(input("Enter Your Choice: "))
                if ch == 1:
                    game(id,user)
                elif ch == 2:
                    playerrecords(id,user)
                elif ch == 3:
                    menu()
                else:
                    print("Wrong Choice Try Again.")
                    x = input("Input Anything to Continue. \n")
            except Exception as e:
                print("Error! Try Again.")
                print(f"ERROR: {e}")
                print("")
                x = input("Input Anything to Continue. \n")

    def menu():
        while True:
            clear_screen()
            print()
            print(r'''
___  ___                 
|  \/  |                 
| .  . | ___ _ __  _   _ 
| |\/| |/ _ \ '_ \| | | |
| |  | |  __/ | | | |_| |
\_|  |_/\___|_| |_|\__,_|
                         
                         
''')
            print("1. Login")
            print("2. Create an Account")
            print("3. Show Global Leaderboard")
            print("4. Exit Program")
            try:
                ch = int(input("Enter Your Choice: "))
                if ch == 1:
                    login()
                elif ch == 2:
                    signup()
                elif ch == 3:
                    leaderboard()
                elif ch == 4:
                    sys.exit()
                else:
                    print("Wrong Choice. Try again!")
            except Exception as e:
                print("Error! Wrong Input")
                print(f"ERROR: {e}")
                x = input("Input anything to continue.\n")
    menu()
except Exception as e:
    print(f"Game Crashed")
    print("Restart Again")
    print(f"ERROR: {e}")
    x = input('Input Anything to Continue.\n')


# 
'''
WordList - https://github.com/dolph/dictionary/blob/master/popular.txt
AsciiArt - http://www.patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

'''

# BackSQL Commands
# DATETIME to TIMESTAMP on MYSQL 5.5
'''

CREATE TABLE Users (
  user_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  account_creation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id)
);

All player records table (used for searching)

CREATE TABLE alluserplays(
 time DECIMAL(10,2) NOT NULL,
 time_submitted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 name VARCHAR(255) NOT NULL,
 user_id INT NOT NULL,
 FOREIGN KEY (user_id) REFERENCES users(user_id)
);

leaderboard table (best times of each player)

CREATE TABLE leaderboard (
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    best_time DECIMAL(10,2) NULL,
    PRIMARY KEY (user_id)
);

Trigger for leaderboard to auto update! IMPORTANT

DELIMITER $$

CREATE TRIGGER update_trigger
AFTER INSERT ON alluserplays
FOR EACH ROW
BEGIN
    INSERT INTO leaderboard (user_id, name, best_time)
    VALUES (NEW.user_id, NEW.name, NEW.time)
    ON DUPLICATE KEY UPDATE
    name = NEW.name,
    best_time = LEAST(NEW.time, IFNULL(leaderboard.best_time, NEW.time));
END$$

DELIMITER ;

'''