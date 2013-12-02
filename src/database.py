import sqlite3
import os
import locations
from logger import log

db_path = os.path.join(locations.current_folder(), '.database.db')

def verify_database_existence():
	#Check to see if DB exists
	if (os.path.isfile(db_path) ):
		try:
			db_connection = sqlite3.connect(db_path)
			db_connection.close()
			return(True)
		except Exception, err:			
			for i in err:
				logger.log("Unable to verify DB Existence - " + i)
	else:
		return(False)
	
def create_fresh_tables():
	#If DB doesn't exist create its tables and keys
	db_connection = sqlite3.connect(db_path)
	db = db_connection.cursor()
		
	db.execute('''CREATE TABLE images 
			(id INTEGER PRIMARY KEY, name TEXT, location TEXT, date_added INTEGER,
				date_taken INTEGER, caption TEXT)''')
	db.execute('''CREATE TABLE tags (id, tag TEXT)''')
	#db.execute(''' CREATE INDEX sourceIndex ON jobs(source ASC) ''')
	#db.execute(''' CREATE INDEX statusIndex ON jobs(status ASC) ''')

	db_connection.commit()
	db_connection.close()

def connect_to_database():
	try:
		#If DB doesn't exist create its tables and keys
		db_connection = sqlite3.connect(db_path)
		db = db_connection.cursor()				
		return (db_connection)
	except Exception, err:
		for error in err:
			logger.log("Unable to connect to DB - " + error)
			return (False)


def create_test_data():
	
	db_connection = connect_to_database()
	db = db_connection.cursor()

	#Buid data string to insert
	jobsData = [
		(None, 'http://i.imgur.com/NRfBaS6.jpg', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20Setup.exe', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters11.avi', "Queued", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters21.avi', "Failed", 0, logger.getTime(), "email"),
		(None, 'http://xxx.com/buttblasters1.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters2.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://thisismeaddingaURL.com', "Downloading", 0, logger.getTime(), "email"),
		(None, 'http://i.imgur.com/lOOw9rq.gif', "Downloading", 0, logger.getTime(), "web"),
		(None, 'http://google.com/cockmunchers3.avi', "Queued", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters16.avi', "Succesful", 0, logger.getTime(), "web"),
		(None, 'http://xxx.com/buttblasters16.avi', "Failed", 0, logger.getTime(), "email"),			
	]		

	configData = [
		(None,'E-Mail', 'email_username', 'pydownloadserver', 'text', 'GMail Username:'),
		(None,'E-Mail', 'email_password', 'Kaiser123', 'password', 'Gmail Password:'),
		(None,'General', 'download_path', current_folder, 'text', "Download Location:"),
		(None,'Server', 'server_host', '0.0.0.0', 'text', "Host:"),
		(None,'Server', 'server_port', '12334', 'text', "Port")
		
	]

	db.executemany('INSERT INTO jobs VALUES (?,?,?,?,?,?)', jobsData)
	db.executemany('INSERT INTO config VALUES (?,?,?,?,?,?)', configData)

	try:
		db_connection.commit()
		db_connection.close()
		logger.log(logger.getTime() + " Inserted test data into db")
	except Exception, err:
		for error in err:
			logger.log("Unable to insert test data" + error)
			db_connection.close()			

def verify_folder_existence():

	if not os.path.isdir(locations.image_save_location()):
		try:
			os.mkdir( locations.image_save_location() )
		except OSError, err:
			for error in err:
				log(error)



	if not os.path.isdir(locations.thumbnail_save_location()):		
		try:
			os.mkdir( locations.thumbnail_save_location() )
		except OSError, err:
			for error in err:
				log(error)



def get_latest_image_id():
	db_connection = connect_to_database()
	db = db_connection.cursor()

	the_count = db.execute('''COUNT tables''')
	db_connect.close()
	return (the_count)
