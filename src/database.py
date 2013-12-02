import sqlite3
import os
import locations
import time
from logger import log
from logger import get_time

db_path = os.path.join(locations.current_folder(), '.database.db')

def verify_database_existence():
	#Check to see if DB exists
	if (os.path.isfile(db_path) ):
		try:
			db_connection = sqlite3.connect(db_path)
			db_connection.close()
			return(True)
		except Exception, err:			
			for error in err:
				logger.log("DataBase: Unable to verify existence" + error)
	else:
		return(False)
	
def create_fresh_tables():
	#If DB doesn't exist create its tables and keys
	db_connection = sqlite3.connect(db_path)
	db = db_connection.cursor()
		
	db.execute('''CREATE TABLE images 
			(id INTEGER PRIMARY KEY, name TEXT, location TEXT, date_added INTEGER,
				date_taken INTEGER, caption TEXT)''')
	db.execute('''CREATE TABLE tags (id INTEGER PRIMARY KEY, image_id integer, tag TEXT)''')
	db.execute('''CREATE TABLE alerts (id INTEGER PRIMARY KEY, alert TEXT, status TEXT, date_added INTEGER, inactive_date INTEGER)''')

	#Create index on tags
	db.execute(''' CREATE INDEX tagIndex ON tags(tag ASC) ''')	


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
			logger.log("DataBase: Unable to connect" + error)
			return (False)


def create_test_data():
	
	db_connection = connect_to_database()
	db = db_connection.cursor()

	#Buid data string to insert
	imageData = [
		(None, 'Callie Hanging out', os.path.join(locations.image_save_location(), '1.jpg'), get_time(), get_time(), "Callie hanging out"),
		(None, 'Callie Christmas', os.path.join(locations.image_save_location(), '2.jpg'), get_time(), get_time(), ""),
		(None, 'Boop', os.path.join(locations.image_save_location(), '3.jpg'), get_time(), get_time(), ""),
		(None, 'Squeak', os.path.join(locations.image_save_location(), '4.jpg'), get_time(), get_time(), ""),		
	]		

	tagData = [
		(None, 1, "Callie"),
		(None, 1, "Josh"),
		(None, 1, "Linz"),
		(None, 2, "Callie"),
		(None, 3, "Callie"),
		(None, 3, "Josh"),
		(None, 4, "Callie"),		
	]

	alertData = [
		(None, "Outage Coming up on the 4th", "active", time.time(), time.time() + 2),
		(None, "Callies Birthday Coming up!!", "active", time.time(), time.time() + 0.5),

	]

	db.executemany('INSERT INTO images VALUES (?,?,?,?,?,?)', imageData)
	db.executemany('INSERT INTO tags VALUES (?,?,?)', tagData)
	db.executemany('INSERT INTO alerts VALUES (?,?,?,?,?)', alertData)

	try:
		db_connection.commit()
		db_connection.close()
		log("DataBase: Inserted test data into db")
	except Exception, err:
		for error in err:
			log("DataBase: Unable to insert test data - " + error)
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
	try:
		db.execute('''SELECT Count(*) from images''')
		the_count = db.fetchone()
		db_connection.close()

		return (the_count[0] + 1)
	except Exception, err:
		db_connection.close()
		
		for error in err:
			log("DataBase: Unable to get images table count " + str(error) )
			return (False)
