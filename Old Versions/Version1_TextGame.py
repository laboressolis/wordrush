import mysql.connector
import random
import time
import os

database = mysql.connector.connect(host='localhost',user='root',passwd='asdf',database='db1',auth_plugin='mysql_native_password')
cursor = database.cursor()

word_list = ["apple", "banana", "cat", "dog", "elephant", "fish", "giraffe", "horse",
 "ice cream", "juice", "kangaroo", "lion", "monkey", "nest", "octopus", "panda", "queen", "rainbow", "sun",
 "train", "umbrella", "violin", "watermelon", "x-ray", "yacht", "zebra"]

def clear_screen():
  """Clears the screen."""
  os.system('cls')

def get_random_word():
	random_index = random.randint(0,len(word_list)-1)
	random_word = word_list[random_index]
	return random_word

def submitgamescore(user,id,time):
	sqlcommand = '''INSERT INTO alluserplays (user_id,name,time) values(%s,%s,%s)'''
	values = (id,user,time)
	try:
		cursor.execute(sqlcommand,values)
		database.commit()
	except Exception as e:
		print("Something went wrong!")
		print(f"ERROR:{e} ")
	return 'Score Submitted'

def playerrecords(user,id):
	clear_screen()
	sqlcommand = '''SELECT * FROM alluserplays WHERE name=%s and user_id=%s'''
	values = (user,id)
	try:	
		cursor.execute(sqlcommand,values)
		getdata = cursor.fetchall()
	except Exception as e:
		print("Something went wrong!")
		print(f"ERROR:{e} ")
	data = getdata
	if len(data) != 0:
		for i in data:
			playertime = i[0]
			date_submitted = i[1]
			name = i[2]
			id = i[3]
			data1 = [f'UserID:{id}',f'Player:{name}',f'Time:{playertime}',f'Submission date:{date_submitted}',]
			print(data1)
			time.sleep(0.5)
		x = input("Press anything to continue! \n")
		clear_screen()
	else:
		print("No Records found!")
		x = input("Press anything to continue! \n")
		clear_screen()

def leaderboard():
	clear_screen()
	sqlcommand = '''SELECT * FROM leaderboard'''
	try:	
		cursor.execute(sqlcommand)
		getdata = cursor.fetchall()
	except Exception as e:
		print("Something went wrong!")
		print(f"ERROR:{e} ")
	data = getdata
	if len(data) != 0:
		alldata = []
		for i in data:
			playertime = i[2]
			temptime = playertime
			name = i[1]
			id = i[0]
			data1 = [f'{temptime}',f'Player:{name}',f'UserID:{id}']
			alldata.append(data1)
			time.sleep(0.5)
		# Sorting Function
		def custom_sort(item):
			return float(item[0])
		sorted_data = sorted(data1, key=custom_sort)
		for k in sorted_data:
			print(k)

		x = input("Press anything to continue! \n")
		clear_screen()
	else:
		print("No Records found!")
		x = input("Press anything to continue! \n")
		clear_screen()

def game(user,id):
	clear_screen()
	gamecounter = 0
	score = 0
	counter = 0
	print("Best in cmd!")
	print('=======================================')
	print("Press any character to play!")
	print("Press 1 for 'How to play'.")
	print("Press 2 to quit the game now.\n")
	temp_ch = input()
	if temp_ch == '1':
		print("HOW TO PLAY!")
		print('===========================')
		print("This game is all about time.")
		print("You will be given 20 random words to type.")
		time.sleep(.5)
		print("You have to type them as fast as you can.")
		time.sleep(5)
		print("For each correct word, your final time will be reduced by 1 sec.")
		time.sleep(.2)
		print("The game will now start!")
		time.sleep(1)
		temp = input("Press any key to continue")
		clear_screen()
	elif temp_ch == '2':
		gamemenu(user,id)
	else:
		pass
	for i in range(3,1,-1):
		print(i)
		time.sleep(1)
	print("START!")
	clear_screen()
	start_time = time.time()
	while gamecounter < 5:
		playword = get_random_word()
		word_start_time = time.time()
		print(f"Type the following word: '{playword}' \n")
		playerinput = input()
		print()
		word_end_time = time.time()
		word_time = word_end_time - word_start_time
		if playerinput == playword:
			print('Correct! +1 pts')
			print(f'+{round(word_time,2)} seconds \n')
			counter += 1
		else:
			print('Wrong! -1 pts')
			print(f'+{round(word_time,2)} seconds \n')
			counter -= 1
		gamecounter += 1
	end_time = time.time()
	game_time = end_time - start_time
	print(f"You took {round(game_time,2)} seconds to complete!")
	print(f"With {counter} correct words!")
	score = round(game_time - counter,2)
	score2 = score
	print(f"Your final score is {score}")
	submitc = submitgamescore(user,id,score2)
	print(submitc)
	time.sleep(5)
	clear_screen()

def signup():
	clear_screen()
	name = input("Enter your Name: ")
	password = input("Enter your Password: ")
	cpassword = input("Confirm your Password: ")
	if password == cpassword:
		sqlcommand = 'INSERT INTO users(name,password) values(%s,%s)'
		values = (name,password)
		try:
			cursor.execute(sqlcommand,values)
			database.commit()
		except Exception as e:
			print("Something went wrong!")
			print(f"ERROR:{e} ")
		print("USER ACCOUNT CREATED")
		print(f"Welcome! {name}!")
		time.sleep(3)
		clear_screen()
	else:
		print("Password didn't match")
		time.sleep(3)
		clear_screen()

def login():
	clear_screen()
	name = input("Enter Your Username: ")
	password = input("Enter Your Password: ")
	sqlcommand = 'SELECT * FROM users where name=%s and password=%s'
	values = (name,password)
	try:
		cursor.execute(sqlcommand,values)
		data = cursor.fetchone()
		temp = data
		if temp == None:
			print("No users found!")
		elif name == temp[1] and password == temp[2]:
			print("Login Successfull")
			user_id = temp[0]
			gamemenu(name,user_id)
		else:
			print("Either username or password is wrong!")
	except Exception as e:
		print("Something went wrong!")
		print(f"ERROR:{e} ")

	time.sleep(7)
	clear_screen()

def gamemenu(user,id):
	clear_screen()
	while True:
		print(f"Welcome {user}!")
		print('GAME MENU')
		print('1.Play Game')
		print('2.Show all your records!')
		print('3.Exit')
		ch = int(input("Enter Your choice: "))
		if ch == 1:
			game(user,id)
		elif ch == 2:
			playerrecords(user,id)
		elif ch == 3:
			break
		else:
			print("Wrong Choice Try Again!")
			clear_screen()
	
def menu():
	clear_screen()
	while True:
		print('1.Login')
		print('2.Create an Account')
		print('3.Leaderboard')
		print('4.Exit')
		ch = int(input("Enter Your Choice: "))
		if ch == 1:
			login()
		elif ch == 2:
			signup()
		elif ch == 3:
			leaderboard()
		elif ch == 4:
			break
		else:
			print("Wrong Choice Try again!")
			time.sleep(3)
			clear_screen()
menu()


'''
ALL PRE STUFF FOR SQL

Main user info table 

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