import sqlite3
import os
import locations
import time
from logger import log
from logger import get_time
from random import randint

db_path = os.path.join(locations.current_folder(), '.database.db')

def tryToCloseDB(db_connection):
	try:
		db_connection.close()
	except:
		pass

def verify_database_existence():
	#Check to see if DB exists
	if (os.path.isfile(db_path) ):
		try:
			db_connection = sqlite3.connect(db_path)
			db_connection.close()
			return(True)
		except Exception, err:
			db_connection.close()
			for error in err:
				logger.log("DataBase: Unable to verify existence" + str(error), "DATABASE","SEVERE")
	else:
		return(False)
	
def create_fresh_tables():
	try:
		#If DB doesn't exist create its tables and keys
		db_connection = sqlite3.connect(db_path)
		db = db_connection.cursor()
			
		db.execute('''CREATE TABLE images 
				(id INTEGER PRIMARY KEY, name TEXT, image_location TEXT, thumb_location TEXT, date_added DATETIME,
					date_taken DATETIME NOT NULL, caption TEXT, width INTEGER, height INTEGER)''')

		#Create 3 Tag tables - primary / sub / and event
		db.execute('''CREATE TABLE tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, tag TEXT NOT NULL)''')	
		db.execute('''CREATE TABLE sub_tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, parent_tag TEXT NOT NULL, sub_tag TEXT NOT NULL)''')
		db.execute('''CREATE TABLE event_tags (id INTEGER PRIMARY KEY, image_id INTEGER NOT NULL, parent_tag TEXT NOT NULL, parent_sub_tag NOT NULL, event_tag NOT NULL)''')

		db.execute('''CREATE TABLE alerts (id INTEGER PRIMARY KEY, alert TEXT, status TEXT, date_added INTEGER, inactive_date INTEGER)''')
		db.execute('''CREATE TABLE blogs (id INTEGER PRIMARY KEY, title TEXT NOT NULL, post TEXT NOT NULL, author TEXT NOT NULL, date_added DATETIME NOT NULL DEFAULT CURRENT_DATE)''')

		db.execute('''CREATE TABLE processing_queue (id INTEGER PRIMARY KEY, image_name TEXT)''')
		db.execute('''CREATE TABLE logs (id INTEGER PRIMARY KEY, error_type TEXT, error TEXT, date_time_occured DATETIME NOT NULL, severity TEXT)''')

		#Create index on tags
		db.execute(''' CREATE INDEX tagIndex ON tags(tag ASC) ''')
		db.execute(''' CREATE INDEX subtagIndex ON sub_tags(sub_tag ASC) ''')
		db.execute(''' CREATE INDEX eventtagIndex ON event_tags(event_tag ASC) ''')
		db.execute(''' CREATE INDEX logTypeIndex ON logs(error_type DESC) ''')


		db_connection.commit()
		log("Database did not exist: Created DB", "DATABASE", "SEVERE")
		db_connection.close()
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to create DB Tables: " + str(error), "DAtABASE", "SEVERE")

def connect_to_database():
	try:
		#If DB doesn't exist create its tables and keys
		db_connection = sqlite3.connect(db_path)				
		return (db_connection)
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			logger.log("DATABASE","DataBase: Unable to connect" + str(error), "SEVERE")
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
		(None, 0, "Family"),		
		(None, 0, "Holidays"),
		(None, 0, "Friends")
	]

	subTagData = [
		(None, 0, "Kids", "Callie"),

		(None, 0, "Josh", "Portraits"),
		(None, 0, "Josh", "With Callie"),
		(None, 0, "Josh", "Photography"),
		(None, 0, "Josh", "Birthdays"),

		(None, 0, "Linz", "Portraits"),
		(None, 0, "Linz", "With Callie"),
		(None, 0, "Linz", "Photography"),
		(None, 0, "Linz", "Birthdays"),

		(None, 0, "Family", "Johnson"),
		(None, 0, "Family", "Zamudio"),
		(None, 0, "Family", "Brownell"),
		(None, 0, "Family", "Murello"),
		(None, 0, "Family", "Williams"),
		(None, 0, "Family", "Puppies"),

		(None, 0, "Holidays", "Christmas"),
		(None, 0, "Holidays", "New Years"),
		(None, 0, "Holidays", "Easter"),
		(None, 0, "Holidays", "Valentines Day"),
		(None, 0, "Holidays", "Dragon Day"),
		(None, 0, "Holidays", "Thanksgiving"),
		(None, 0, "Holidays", "4th of July"),
		(None, 0, "Holidays", "Halloween"),
		
		(None, 0, "Friends", "Childhood"),
		(None, 0, "Friends", "Adult"),
	]

	eventTagData = [		
		(None, 0, "Kids", "Callie", "Growing Girl"),
		(None, 0, "Kids", "Callie", "Birthdays"),				
		(None, 0, "Kids", "Callie", "Silly"),
		(None, 0, "Kids", "Callie", "Portraits"),

		(None, 0, "Family", "Zamudio", "Brandon and Dakota"),
		(None, 0, "Family", "Zamudio", "Roger"),
		(None, 0, "Family", "Zamudio", "Richie and Angie"),
		(None, 0, "Family", "Johnson", "I I I"),
		(None, 0, "Family", "Johnson", "Larry and Annette"),
		(None, 0, "Family", "Johnson", "Misty"),
		(None, 0, "Family", "Johnson", "Anthony and Latonya"),
		(None, 0, "Family", "Williams", "Teresa"),
		(None, 0, "Family", "Brownell", "Christine"),
						
		(None, 0, "Holidays", "Halloween", "2013"),
		(None, 0, "Holidays", "Halloween", "2014"),
		(None, 0, "Holidays", "Christmas", "2013"),
		(None, 0, "Holidays", "Christmas", "2014"),
		(None, 0, "Holidays", "New Years", "2013"),
		(None, 0, "Holidays", "New Years", "2014"),
		(None, 0, "Holidays", "Easter", "2013"),
		(None, 0, "Holidays", "Easter", "2014"),
		(None, 0, "Holidays", "Valentines Day", "2013"),
		(None, 0, "Holidays", "Valentines Day", "2014"),
		(None, 0, "Holidays", "Dragon Day", "2013"),
		(None, 0, "Holidays", "Dragon Day", "2014"),
		(None, 0, "Holidays", "Thanksgiving", "2013"),
		(None, 0, "Holidays", "Thanksgiving", "2014"),
		(None, 0, "Holidays", "4th of July", "2013"),
		(None, 0, "Holidays", "4th of July", "2014")

	]

	alertData = [
		(None, "Outage Coming up on the 4th", "active", time.time(), time.time() + 2),
		(None, "Callies Birthday Coming up!!", "active", time.time(), time.time() + 0.5)

	]

	#db.executemany('INSERT INTO images VALUES (?,?,?,?,?,?,?)', imageData)
	db.executemany('INSERT INTO tags VALUES (?,?,?)', tagData)
	db.executemany('INSERT INTO sub_tags VALUES (?,?,?,?)', subTagData)
	db.executemany('INSERT INTO event_tags VALUES (?,?,?,?,?)', eventTagData)
	#db.executemany('INSERT INTO alerts VALUES (?,?,?,?,?)', alertData)

	try:
		db_connection.commit()
		db_connection.close()
		log("DataBase: Inserted test data into db", "DATABASE", "INFO")
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("DataBase: Unable to insert test data - " + str(error), "DATABASE","INFO")					

def verify_folder_existence():

	if not os.path.isdir(locations.image_save_location()):
		try:
			os.mkdir( locations.image_save_location() )
		except OSError, err:
			for error in err:
				log(str(error), "FILESYSTEM", "SEVERE")

	if not os.path.isdir(locations.thumbnail_save_location()):		
		try:
			os.mkdir( locations.thumbnail_save_location() )
		except OSError, err:
			for error in err:
				log(str(error), "FILESYSTEM", "SEVERE")

	if not os.path.isdir(locations.queue_save_location()):
		try:
			os.mkdir( locations.queue_save_location() )
		except OSError, err:
			for error in err:
				log(str(error), "FILESYSTEM", "SEVERE")

def get_latest_image_id():
	db_connection = connect_to_database()
	db = db_connection.cursor()
	try:
		#Get the last primary key in the table and add 1 to it for the new image_id
		db.execute('''SELECT id FROM images ORDER BY ID DESC LIMIT 1''')
		the_count = db.fetchone()
		db_connection.close()

		return (the_count[0] + 1)
	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable to get images table count " + str(error), "DATABASE","SEVERE" )
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
	width = kwargs.get('width')
	height = kwargs.get('height')

	try:		
		db.execute('INSERT INTO images VALUES (?,?,?,?,?,?,?,?,?)', (None, name, image_location, thumb_location, date_added, date_taken, caption, width, height) )
		last_row = db.lastrowid
		db_connection.commit()	
		db_connection.close()
		return(last_row)	
	except Exception, err:
		tryToCloseDB(db_connection)

		for error in err:			
			log("Database: Unable to insert image record - " + str(error), "DATABASE","MEDIUM")			

def insert_tag(image_id, tagData):	
	db_connection = connect_to_database()
	db = db_connection.cursor()		
		
	if tagData['tag_type'] == 'main':		
		db.execute('INSERT INTO tags VALUES (?, ?, ?)', (None, image_id, tagData['main_tag']) )				
	elif tagData['tag_type'] == 'sub':
		db.execute('INSERT INTO sub_tags VALUES (?, ?, ?, ?)', (None, image_id, tagData['main_tag'], tagData['sub_tag']) )
	elif tagData['tag_type'] == 'event':
		db.execute('INSERT INTO event_tags VALUES (?, ?, ?, ?, ?)', (None, image_id, tagData['main_tag'], tagData['sub_tag'], tagData['event_tag']) )

	try:
		db_connection.commit()
		db_connection.close()
	except Exception, err:
		tryToCloseDB(db_connection)		
		for error in err:
			log("Unable to add tags: " + str(error), "DATABASE","MEDIUM")

def insert_blog(*args):
	try:		
		author = args[0]['author']
		title = args[0]['title']
		date_added = args[0]['date_added']
		post = args[0]['post']
		
		db_connection = connect_to_database()
		db = db_connection.cursor()
		db.execute('''INSERT INTO blogs VALUES (?,?,?,?,?)''', (None, title, post, author, date_added,))

		db_connection.commit()
		db_connection.close()
		return (True)		
	except Exception, err:
		for error in err:
			log("Unable to insert post - " + str(error), "DATABASE", "SEVERE")
		return (False)

#Get a list of all tags in the DB
def get_tags():
	db_connection = connect_to_database()
	db = db_connection.cursor()
	try:		
		db.execute('''SELECT DISTINCT tag from tags ORDER BY(id) ASC''')
		the_tags = db.fetchall()
		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:
			for pretty_tag in ugly_tag:
				returned_list.append(pretty_tag.encode('utf-8'))

		return(returned_list)

	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error), "DATABASE","SEVERE" )
			return (False)

#Get a list of all sub tags in the DB
def get_sub_tags(parent_tag = False):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:
		if parent_tag == False:
			db.execute('''SELECT DISTINCT parent_tag, sub_tag FROM sub_tags ORDER BY(sub_tag) ASC''')
			the_tags = db.fetchall()
		else:			
			db.execute('''SELECT DISTINCT parent_tag, sub_tag FROM sub_tags WHERE parent_tag = ? ORDER BY(sub_tag) ASC''', (parent_tag,) )
			the_tags = db.fetchall()			

		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:
			returned_list.append( [ ugly_tag[0].encode('utf-8'), ugly_tag[1].encode('utf-8') ] )										

		return(returned_list)

	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error), "DATABASE","SEVERE" )
			return (False)

#Get a list of all event tags in the DB
def get_event_tags(sub_tag = False):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:
		if sub_tag == False:	
			db.execute('''SELECT DISTINCT parent_tag, parent_sub_tag, event_tag FROM event_tags ORDER BY(event_tag) ASC''')
			the_tags = db.fetchall()
		else:
			db.execute('''SELECT DISTINCT parent_tag, parent_sub_tag, event_tag FROM event_tags WHERE parent_sub_tag = ? ORDER BY(event_tag) ASC''', (sub_tag,))
			the_tags = db.fetchall()

		db_connection.close()

		returned_list = []
		#Make the DB records prettier/easier to work with by removing unicode tags and commas
		for ugly_tag in the_tags:			
			returned_list.append([ ugly_tag[0].encode('utf-8'), ugly_tag[1].encode('utf-8'), ugly_tag[2].encode('utf-8') ])

		return(returned_list)

	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable to get tags: " + str(error), "DATABASE","SEVERE" )
			return (False)

def check_for_processing_image(passed_image_name):
	db_connection = connect_to_database()
	db = db_connection.cursor()	

	try:		
		db.execute('SELECT image_name FROM processing_queue WHERE image_name = ?', (passed_image_name,) )
		processing_queue = db.fetchall()
		db_connection.close()

		if len(processing_queue) > 0:			
			return (1); #If the passed image_name is currently being processed return true.
		else:			
			return (0);
		
		
	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable query processing queue: " + str(error), "DATABASE","SEVERE" )
			return (1)

def insert_currently_processing_job(image_name):
	db_connection = connect_to_database()
	db = db_connection.cursor()
		
	db.execute('INSERT INTO processing_queue VALUES (?, ?)', (None, str(image_name) ) )

	try:
		db_connection.commit()
		db_connection.close()
	except Exception, err:
		for error in err:
			log("Unable to add job to processing_queue tags: " + str(error), "DATABASE","SEVERE")

def delete_currently_processing_job(image):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:		
		db.execute('DELETE FROM processing_queue WHERE image_name = ?', (image,) )
		db_connection.commit()
		db_connection.close()
		return (True)

	except Exception, err:
		tryToCloseDB(db_connection)
		
		for error in err:
			log("DataBase: Unable to delete processing job: " + str(error), "DATABASE","SEVERE" )
			return (False)

def get_images_by_tag(*args, **kwargs):
	tags = args[0]

	#Check to see if the argument contains an event_tag or just a sub
	try:
		event_tag = tags['event_tag']
		sub_tag = tags['sub_tag']
	except:
		event_tag = False
		try:
			sub_tag = tags['sub_tag']
		except:
			sub_tag = False		

	#Main will always exist
	main_tag = tags['main_tag']
	
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:		
		if event_tag:			
			db.execute('SELECT * from images WHERE id IN (SELECT image_id FROM event_tags WHERE parent_tag == (?) AND parent_sub_tag == (?) AND event_tag == (?) ) ORDER BY (date_taken) ASC', (main_tag, sub_tag, event_tag,) )			
		elif sub_tag:
			db.execute('SELECT * from images WHERE id IN (SELECT image_id FROM sub_tags WHERE parent_tag == (?) AND sub_tag == (?) ) ORDER BY (date_taken) ASC', (main_tag, sub_tag,) )			
		elif main_tag:
			db.execute('SELECT * from images WHERE id IN (SELECT image_id FROM tags WHERE tag == (?) )  ORDER BY (date_taken) ASC', (main_tag,) )	
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to query images: " + str(error), "DATABASE","SEVERE")

		return ("")

	query = db.fetchall()	
	db_connection.close()

	return ( query )

def get_image_by_id(image_id):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:
		db.execute('SELECT * FROM images WHERE id == (?)', (image_id,) )
	except Exception, err:
		db.connection.close()
		for error in err:
			log("Unable to get image by ID: " + str(error), "DATABASE","HIGH")	
		return ("")

	query = db.fetchall()
	db.connection.close()

	return (query)

def get_image_tags_by_image_id(image_id):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:
		db.execute('SELECT id, tag FROM tags WHERE image_id == (?)', (image_id,) )
		main_tags = db.fetchall()
		db.execute('SELECT id, parent_tag, sub_tag FROM sub_tags WHERE image_id == (?)', (image_id,) )
		sub_tags = db.fetchall()
		db.execute('SELECT id, parent_tag, parent_sub_tag, event_tag FROM event_tags WHERE image_id == (?)', (image_id,) )
		event_tags = db.fetchall()
		db.connection.close()

	except Exception, err:
		tryToCloseDB(db_connection)

		for error in err:
			log("Unable to get image by ID: " + str(error), "DATABASE","HIGH")		
		return ("")

	returnedList = [
						main_tags,
						sub_tags,
						event_tags
					]

	return(returnedList)

def does_image_have_at_least_one_tag(image_id):
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:
		db.execute('SELECT COUNT(*) FROM sub_tags WHERE image_id == ?', (image_id,) )
		sub_count = db.fetchone()[0]
		db.execute('SELECT COUNT(*) FROM event_tags WHERE image_id == ?', (image_id,) )
		event_count = db.fetchone()[0]	

		if (sub_count + event_count) <= 0:			
			update_image_data({
								'image_id': image_id,
								'delete_requested': 1
							})
			return (False)
		else:
			return (True)

		db_connection.close()
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:			
			log("Unable to determine if image has at least one tag: " + str(error), "DATABASE","MEDIUM")
			return (True)

def delete_image_tags(*args):	

	try:		
		data = args[0]
		image_id = data['image_id']
		sub_tag_id = data['sub_tag_id']
		
		try:			
			event_tag_id = data['event_tag_id']
			#Cast number_of_event_tags into an int so we can use math operations on it
			event_tag_length = int( data['number_of_event_tags'] )
		except:
			event_tag_id = False
		
		db_connection = connect_to_database()
		db = db_connection.cursor()

		if event_tag_id:
			#Make sure no other event tags are present before removing from the sub_tags table
			if event_tag_length <= 1:
				db.execute('DELETE FROM sub_tags WHERE id = ?', (sub_tag_id,) )				

			db.execute('DELETE FROM event_tags WHERE id = ?', (event_tag_id,) )						
		elif not event_tag_id:
			db.execute('DELETE FROM sub_tags WHERE id = ?', (sub_tag_id,) )	

		db_connection.commit()
		db_connection.close()
		
		if does_image_have_at_least_one_tag(image_id):
			return (True)
		else:
			return (False)
		
	except Exception, err:
		try:
			db_connection
			tryToCloseDB(db_connection)
		except:
			no_db = True
		for error in err:
			log("Unable to delete tag: " + str(error), "DATABASE","MEDIUM")
			return (True)

def delete_blog_by_id(blog_id):
	try:				
		db_connection = connect_to_database()
		db = db_connection.cursor()
		db.execute( 'DELETE FROM blogs WHERE id == ?', (blog_id,) )

		db_connection.commit()
		db_connection.close()
		return (True)		
	except Exception, err:
		for error in err:
			log("Unable to delete blog - " + str(error), "DATABASE", "SEVERE")
		return (False)
			
def update_image_data(*args, **kwargs):	
	if args:
		data = args[0]
	else:
		data = kwargs
	
	try:
		image_id = data['image_id']

		#Deletion request, delete image and all metadata
		if data['delete_requested']:
			db_connection = connect_to_database()
			db = db_connection.cursor()

			try:
				import filesystem
				#Delete image file and thumbnail
				db.execute('SELECT image_location, thumb_location FROM images WHERE id = ?', (image_id,) )
				locations = db.fetchall()[0]
				#First element is image location, second is thumbnail location
				filesystem.delete_file( locations[0] )
				filesystem.delete_file( locations[1] )

				#Clean up all image metadata
				db.execute('DELETE FROM images WHERE id == ?', (image_id,)  )
				db.execute('DELETE FROM tags WHERE image_id == ?', (image_id,)  )
				db.execute('DELETE FROM sub_tags WHERE image_id == ?', (image_id,)  )
				db.execute('DELETE FROM event_tags WHERE image_id == ?', (image_id,)  )
				db_connection.commit()		
				db_connection.close()
				return(True)  #BOOL Flag for isImageDeleted cherrypyFunction

			except Exception, err:
				tryToCloseDB(db_connection)
				return ("ERROR")
				for error in err:
					log("Unable to delete image " + image_id + " - " + str(error), "DATABASE","MEDIUM")					

	#Not a deletion request, update image metadata
	except:
		db_connection = connect_to_database()
		db = db_connection.cursor()		

		try:
			name = data['name']
			caption = data['caption']
			date_taken = data['date_taken']
			db.execute('''UPDATE images SET name = ?, caption = ?, date_taken = ? WHERE id == ?''', (name,caption,date_taken,image_id,))
			db_connection.commit()
			db_connection.close()
		except Exception, err:
			tryToCloseDB(db_connection)
			for error in err:				
				log("Unable to update Image #" + str(image_id) + ": " + str(error), "DATABASE","MEDIUM")

		return (False) #BOOL Flag for isImageDeleted cherrypyFunction

def update_blog(*args):
	try:
		blog_id = args[0]['id']
		author = args[0]['author']
		title = args[0]['title']
		date_added = args[0]['date_added']
		post = args[0]['post']
		
		db_connection = connect_to_database()
		db = db_connection.cursor()
		db.execute('''UPDATE blogs SET author = ?, title = ?, date_added = ?, post = ? WHERE id == ?''', (author,title,date_added, post,blog_id,))

		db_connection.commit()
		db_connection.close()
		return (True)		
	except Exception, err:
		for error in err:
			log("Unable to update post - " + str(error), "DATABASE", "SEVERE")
		return (False)

def get_top_30_logs():
	try:
		db_connection = connect_to_database()
		db = db_connection.cursor()

		db.execute("SELECT error_type, error, date_time_occured, severity FROM logs ORDER BY (id) DESC LIMIT 30")
		logs = db.fetchall()		
		db_connection.close()

		return(logs)
	except Exception, err:
		tryToCloseDB(db_connection)
		return ("")
		for error in err:
			log("Unable to get logs: " + str(error), "DATABASE", "LOW")

def get_latest_12_images_by_tag(main_tag, sub_tag, event_tag = False, offset = 0):	
	try:
		db_connection = connect_to_database()
		db = db_connection.cursor()
		if event_tag == False:
			db.execute('''SELECT images.id, images.name, images.thumb_location  FROM images 
						  INNER JOIN sub_tags ON images.id = sub_tags.image_id WHERE images.id NOT IN 
						  (SELECT image_id from event_tags WHERE parent_tag = (?) AND parent_sub_tag = (?) )
						  AND sub_tags.parent_tag = (?) AND sub_tags.sub_tag =(?) 
						  ORDER BY (images.date_taken) DESC LIMIT 12 OFFSET ?''', (main_tag, sub_tag, main_tag, sub_tag, offset,))
		else:
			db.execute('''SELECT images.id, images.name, images.thumb_location  FROM images 
							INNER JOIN event_tags ON images.id = event_tags.image_id WHERE event_tags.parent_tag = ? 
							AND event_tags.parent_sub_tag = ? AND event_tags.event_tag = ? ORDER BY (images.date_taken) DESC LIMIT 12 OFFSET ?''', (main_tag, sub_tag,event_tag, offset,))	

		latest_10 = db.fetchall()
		db_connection.close()

		return ( latest_10 )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest 10 images: " + str(error), "DATABASE", "SEVERE")

def get_latest_images(number_of_images = 5):
	try:
		db_connection = connect_to_database()
		db = db_connection.cursor()
		db.execute('''SELECT * FROM images ORDER BY ID DESC LIMIT ?''', (number_of_images,))		

		latest_images = db.fetchall()
		db_connection.close()

		return ( latest_images )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest images: " + str(error), "DATABASE", "SEVERE")	

def get_random_image_id_by_tag(db_cursor = False, **kwargs):	
	def query_db_for_acceptable_images(dbcur, tag):
		#If the key main_tag is passed it's a main tag query
		#If the key parent_tag and sub_tag are passed (and not main_tag) it's a sub tag query
		#If the key event_tag is passed (and neither of the previous two) it's an event query
		#If the key 'misc_parent_tag' is passed it's a query for sub_tags that don't have event tags
		try:			
			main_tag = tag['main_tag']			
			dbcur.execute('''SELECT images.id FROM images INNER JOIN tags ON images.id = tags.image_id WHERE
			 tags.tag = ? AND images.width > 720 AND images.height > 800 AND images.height <= 900 AND 
			 (images.width - images.height) > 280''', (main_tag,))
			return ( dbcur.fetchall() )
		except:
			try:				
				sub_tag = tag['sub_tag']
				parent_tag = tag['parent_tag']											
				dbcur.execute( '''SELECT images.id FROM images INNER JOIN sub_tags ON images.id = sub_tags.image_id WHERE
				 				sub_tags.sub_tag = ? AND sub_tags.parent_tag = ? AND images.width > 720 AND images.height > 800 AND
				 				 images.height <= 900 AND (images.width - images.height) > 280''', (sub_tag,parent_tag,) )							

				return ( dbcur.fetchall() )
			except:
				try:					
					event_tag = tag['event_tag']
					parent_sub = tag['parent_sub_tag']
					parent_tag = tag['parent_tag']					
					dbcur.execute('''SELECT images.id FROM images INNER JOIN event_tags ON images.id = event_tags.image_id WHERE 
									event_tags.event_tag = ? AND event_tags.parent_sub_tag = ? AND event_tags.parent_tag = ? AND
									images.width > 720 AND images.height > 800 AND images.height <= 900 AND (images.width - images.height) > 280''', 
									(event_tag,parent_sub, parent_tag))
					return ( dbcur.fetchall() )
				except:
					try:
						misc_parent_tag = tag['misc_parent_tag']
						misc_sub_tag = tag['misc_sub_tag']
						dbcur.execute('''SELECT images.id FROM images INNER JOIN sub_tags ON images.id = sub_tags.image_id WHERE 
										sub_tags.parent_tag = ? AND sub_tags.sub_tag = ? AND images.width > 720 AND 
										images.height > 800 AND images.height <= 900 and (images.width - images.height) > 280 AND 
										image_id NOT IN (SELECT image_id FROM event_tags WHERE parent_tag = ? AND parent_sub_tag = ? )''',
										(misc_parent_tag, misc_sub_tag, misc_parent_tag, misc_sub_tag,) )
						return ( dbcur.fetchall() )

					except Exception, err:
						for error in err:
							log("Unable to query db for acceptable images: " + str(error), "DATABASE", "MEDIUM")
						return ("")

	def return_random_number(db):
		try:			
			image_id_list = query_db_for_acceptable_images(db, kwargs)			
			#Select a random record from 1 to length of results and return the id
			try: 
				random_image = randint(1, (len(image_id_list) - 1) )								
			except:
				if len(image_id_list) >= 1:
					random_image = 0
				else:
					return(False)			
			
			return (  get_image_by_id(image_id_list[random_image][0])  )
		except:					
			return(False)
		
	if db_cursor == False:
		try:
			db_connection = connect_to_database()
			db_cursor = db_connection.cursor()
			random_id =  return_random_number(db_cursor)
			db_connection.close()

			#No random image could be found
			if random_id == False:
				return(False)
			else:
				return (random_id)

		except Exception, err:
			tryToCloseDB(db_connection)
			for error in err:
				log("Unable to get random Image_id  " + str(error), "DATABASE", "SEVERE")
			return(False)			
	else:
		return ( return_random_number(db_cursor) )

def get_image_for_every_main_tag():
	try:
		db_connection = connect_to_database()
		db = db_connection.cursor()
		
		db.execute('SELECT tag FROM tags WHERE image_id = 0 ORDER BY(id) ASC')
		main_tags = db.fetchall()		
		returned_list_of_dicts = {}

		for tag in main_tags:
			random_image = get_random_image_id_by_tag(db, main_tag = tag[0])

			#If a random image has been returned add it to the dictionary else skip over it
			if random_image == False:
				pass
			else:
				returned_list_of_dicts[ tag[0] ] = random_image

		db_connection.close()

		return ( returned_list_of_dicts )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest images " + str(error), "DATABASE", "SEVERE")

def get_image_for_each_sub_tag(main_tag):
	try:		
		sub_tags = get_sub_tags(main_tag)		
		db_connection = connect_to_database()
		db = db_connection.cursor()					
		returned_list_of_dicts = {}

		for parent_tag, sub_tag in sub_tags:						
			random_image = get_random_image_id_by_tag(db, parent_tag = main_tag, sub_tag = sub_tag)			
			if random_image == False:
				pass
			else:
				returned_list_of_dicts[ sub_tag ] = random_image

		db_connection.close()

		return ( returned_list_of_dicts )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest images " + str(error), "DATABASE", "SEVERE")

def get_image_for_each_event_tag(sub_tag):
	try:		
		event_tags = get_event_tags(sub_tag)		
		db_connection = connect_to_database()
		db = db_connection.cursor()					
		returned_list_of_dicts = {}

		for parent_tag, sub_tag, event_tag in event_tags:						
			random_image = get_random_image_id_by_tag(db, parent_tag = parent_tag, parent_sub_tag = sub_tag, event_tag = event_tag)

			if random_image == False:				
				pass
			else:							
				returned_list_of_dicts[ event_tag ] = random_image

		db_connection.close()

		return ( returned_list_of_dicts )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest images " + str(error), "DATABASE", "SEVERE")	

def get_image_for_misc_sub_tag(main_tag, sub_tag):
	try:				
		db_connection = connect_to_database()
		db = db_connection.cursor()					
		returned_list_of_dicts = {}
		
		random_image = get_random_image_id_by_tag(db, misc_parent_tag = main_tag, misc_sub_tag = sub_tag)
		
		if random_image == False:
			pass
		else:
			returned_list_of_dicts[ "Misc" ] = random_image

		db_connection.close()

		return ( returned_list_of_dicts )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest images " + str(error), "DATABASE", "SEVERE")

def get_misc_count_by_tag(*args, **kwargs):
	tags = args[0]

	#Check to see if the argument contains an event_tag or just a sub
	try:		
		sub_tag = tags['sub_tag']		
		main_tag = tags['main_tag']
	except:				
		return (False)
		
	db_connection = connect_to_database()
	db = db_connection.cursor()

	try:				
		
		db.execute('''SELECT count(*) FROM images INNER JOIN sub_tags ON images.id = sub_tags.image_id WHERE 
									sub_tags.parent_tag = ? AND sub_tags.sub_tag = ? AND 
									image_id NOT IN (SELECT image_id FROM event_tags WHERE parent_tag = ? AND parent_sub_tag = ? )''',
									(main_tag, sub_tag, main_tag, sub_tag,) )

		to_return = db.fetchall()		

		return ( to_return[0][0] )		
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to misc count images: " + str(error), "DATABASE","SEVERE")

		return ("")

	query = db.fetchall()	
	db_connection.close()

	return ( query )

def sanitizeInputString(string):
	try:
		passedString = str(string)
		strippedString = passedString.replace("'","").replace(";","").replace("\"", "").replace("=","").replace("*","")
		return ( strippedString )
	except:
		return ("")

def get_latest_alert():
	try:				
		db_connection = connect_to_database()
		db = db_connection.cursor()									
		db.execute("SELECT * FROM alerts ORDER BY (id) LIMIT 1")

		returned_alert = db.fetchall()
		db_connection.close()

		return ( returned_alert )

	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest alert " + str(error), "DATABASE", "SEVERE")

def get_blogs(query_type = "latest", blog_id = False):
	try:
		db_connection = connect_to_database()
		db = db_connection.cursor()
		if query_type == "latest":
			db.execute("SELECT * FROM blogs ORDER BY (id) DESC LIMIT 1")
		elif query_type == "titles":
			db.execute("SELECT id, title FROM blogs ORDER BY (id) DESC")
		elif query_type == "id":
			db.execute("SELECT * FROM blogs WHERE id == ? ORDER BY (id) DESC", (blog_id,))


		returned_blog = db.fetchall()
		db_connection.close()

		return ( returned_blog )
	except Exception, err:
		tryToCloseDB(db_connection)
		for error in err:
			log("Unable to get latest blog " + str(error), "DATABASE", "SEVERE")

#Class used for breaking down data from process submission POST
class Posted_Data:
	def __init__(self, data, dataType):

		self.postedData = data		
		self.dataType = dataType

		if "process" in dataType:
			try:
				insert_currently_processing_job(self.postedData['picture_name'])
				self.image_processor()				
			except Exception, err:
				self.isSuccesful = False
				for error in err:
					log("Unable to completely process image: " + str(error), "DATABASE","MEDIUM")

	def image_processor(self):

		def parse_tags():
			def break_tags_apart(tagsString):
				tagsList = tagsString.split(';')

				#Return tag dictionaries with tag info passed from POST
				if len(tagsList) == 3:
					tagDict = {'tag_type': 'event','event_tag': tagsList[2],'sub_tag': tagsList[1],'main_tag': tagsList[0]}
					return (tagDict)
				elif len(tagsList) == 2:
					#Set sub_tag on photo
					tagDict = {'tag_type': 'sub','sub_tag': tagsList[1],'main_tag': tagsList[0]}
					return (tagDict)
				elif len(tagsList) == 1:
					tagDict = {'tag_type': 'main','main_tag': tagsList[0]}
					return (tagDict)

			tagList = []
			for field, data in self.postedData.iteritems():				
				if "event_tag_selection" in field or "tag_selection" in field or "sub_tag_selection" in field:
					#Handler for multiple tags being selected
					if isinstance(data, list):
						tempTagList = []
						for tags in data:
							tempTagList.append( break_tags_apart(tags) )

						#Write one clean dictionary per tag hierarchy to the tag list
						for tag in tempTagList:														
							tagList.append(tag)

					else:          
						tagList.append( break_tags_apart(data) )
			return ( tagList )
		
		self.tagList = parse_tags()  #List of tag dictionaries
		self.picture_name = self.postedData['picture_name']
		self.picture_caption = self.postedData['picture_caption']
		self.file_location = self.postedData['FileLocation']
		self.date_taken = self.postedData['picture_date']
		import pictureConverter
		convertedPicture = pictureConverter.WebsiteImage(self.file_location, self)

		#If PIL has processed the image
		if convertedPicture.isSuccesful == True:
			for tag in self.tagList:			
				insert_tag( convertedPicture.picture_row_id, tag )				
			self.isSuccesful = True
		else:
			self.isSuccesful = False
