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
			(id INTEGER PRIMARY KEY, name TEXT, image_location TEXT, thumb_location TEXT, date_added INTEGER,
				date_taken INTEGER, caption TEXT)''')

	#Create 3 Tag tables - primary / sub / and event
	db.execute('''CREATE TABLE tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, tag TEXT NOT NULL)''')	
	db.execute('''CREATE TABLE sub_tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, parent_tag TEXT NOT NULL, sub_tag TEXT NOT NULL)''')
	db.execute('''CREATE TABLE event_tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, parent_tag TEXT NOT NULL, parent_sub_tag NOT NULL, event_tag NOT NULL)''')

	db.execute('''CREATE TABLE alerts (id INTEGER PRIMARY KEY, alert TEXT, status TEXT, date_added INTEGER, inactive_date INTEGER)''')

	#Create index on tags
	db.execute(''' CREATE INDEX tagIndex ON tags(tag ASC) ''')
	db.execute(''' CREATE INDEX subtagIndex ON sub_tags(sub_tag ASC) ''')
	db.execute(''' CREATE INDEX eventtagIndex ON event_tags(event_tag ASC) ''')


	db_connection.commit()
	log("Database: Created DB Schema")
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

	isave = locations.image_save_location()
	tsave = locations.thumbnail_save_location()

	#Buid data string to insert
	imageData = [
		(None, 'Callie Hanging out', os.path.join(isave, '1.jpg'), os.path.join(tsave, '1.jpg'),get_time(), get_time(), "Callie hanging out"),
		(None, 'Callie Christmas', os.path.join(isave, '2.jpg'), os.path.join(tsave, '2.jpg'),get_time(), get_time(), ""),
		(None, 'Boop', os.path.join(isave, '3.jpg'), os.path.join(tsave, '3.jpg'),get_time(), get_time(), ""),
		(None, 'Squeak', os.path.join(isave, '4.jpg'), os.path.join(tsave, '4.jpg'),get_time(), get_time(), ""),		
	]		

	tagData = [
		(None, 0, "Kids"),
		(None, 0, "Josh"),
		(None, 0, "Linz"),		
		(None, 0, "Dogs"),
		(None, 0, "Family"),
		(None, 0, "Vacation"),
	]

	subTagData = [
		(None, 0, "Kids", "Callie"),
		(None, 0, "Josh", "Portrait"),
		(None, 0, "Josh", "With Callie"),
		(None, 0, "Josh", "Photography"),
		(None, 0, "Linz", "Portrait"),
		(None, 0, "Linz", "With Callie"),
		(None, 0, "Linz", "Photography"),
		(None, 0, "Family", "Johnsons"),
		(None, 0, "Family", "Zamudios"),
	]

	eventTagData = [
		(None, 0, "Kids", "Callie", "Callies 1st Birthday"),
		(None, 0, "Josh", "With Callie", "Callies 1st Birthday"),
		(None, 0, "Linz", "With Callie", "Callies 1st Birthday"),
		(None, 0, "Josh", "Portrait", "30th Birthday"),
		(None, 0, "Linz", "Portrait", "35th Birthday"),
		
	]

	alertData = [
		(None, "Outage Coming up on the 4th", "active", time.time(), time.time() + 2),
		(None, "Callies Birthday Coming up!!", "active", time.time(), time.time() + 0.5),

	]

	db.executemany('INSERT INTO images VALUES (?,?,?,?,?,?,?)', imageData)
	db.executemany('INSERT INTO tags VALUES (?,?,?)', tagData)
	db.executemany('INSERT INTO sub_tags VALUES (?,?,?,?)', subTagData)
	db.executemany('INSERT INTO event_tags VALUES (?,?,?,?,?)', eventTagData)
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

	if not os.path.isdir(locations.queue_save_location()):
		try:
			os.mkdir( locations.queue_save_location() )
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


def insert_image_record(*args, **kwargs):

	db_connection = connect_to_database()
	db = db_connection.cursor()

	name = kwargs.get('name')	
	image_location = kwargs.get('image_location')
	thumb_location = kwargs.get('thumb_location')
	date_added = get_time()
	date_taken =  kwargs.get('date_taken')
	caption = kwargs.get('caption')

	imageData = [
		(None, name, image_location, thumb_location, date_added, date_taken, caption),
	]

	try:
		db.executemany('INSERT INTO images VALUES (?,?,?,?,?,?,?)', imageData)
		db_connection.commit()
		db_connection.close()
	except Exception, err:
		for error in err:			
			log("Database: Unable to insert image record - " + str(error))
			db_connection.close()

#Get a list of all tags in the DB
def get_tags():
	db_connection = connect_to_database()
	db = db_connection.cursor()
	try:		
		db.execute('''SELECT DISTINCT tag from tags''')
		the_tags = db.fetchall()
		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:
			for pretty_tag in ugly_tag:
				returned_list.append(pretty_tag.encode('utf-8'))

		return(returned_list)

	except Exception, err:
		db_connection.close()
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error) )
			return (False)

def get_sub_tags():
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:		
		db.execute('''SELECT DISTINCT parent_tag, sub_tag FROM sub_tags''')
		the_tags = db.fetchall()
		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:
			returned_list.append( [ ugly_tag[0].encode('utf-8'), ugly_tag[1].encode('utf-8') ] )										

		return(returned_list)

	except Exception, err:
		db_connection.close()
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error) )
			return (False)

def get_event_tags():
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:		
		db.execute('''SELECT DISTINCT parent_tag, parent_sub_tag, event_tag FROM event_tags''')
		the_tags = db.fetchall()
		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:			
			returned_list.append([ ugly_tag[0].encode('utf-8'), ugly_tag[1].encode('utf-8'), ugly_tag[2].encode('utf-8') ])

		return(returned_list)

	except Exception, err:
		db_connection.close()
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error) )
			return (False)