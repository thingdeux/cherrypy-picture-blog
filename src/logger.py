import time

def log(error="Undefined Error", error_type = "GENERIC", severity="INFO"):	
	
	current_time = time.asctime(time.localtime(time.time()))	
	
	try:
		from database import connect_to_database
		db_connection = connect_to_database()
		db = db_connection.cursor()

		db.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?)', (None, error_type, error, current_time, severity,) )
		db_connection.commit()
		db_connection.close()

		#For debug purposes also print
		print ("REMOVE ME IN PROD: " + error)

	except Exception, err:		
		db_connection.close()

		for error in err:
			#This will change for debugging it's print	
			print("Unable to add error to DB: " + error)

def get_time():
	return(  time.asctime(time.localtime(time.time()))  )