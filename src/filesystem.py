import os
import logger
import locations

def delete_file(filename):
	test = "test"

def get_queue_directory_list():
	returned_list = []     

	for image_file in os.listdir(locations.queue_save_location()):
	    filename_without_extension = image_file.split('.')[0]
	    location = os.path.join(locations.queue_save_location(), image_file)
	    
	    returned_list.append(filename_without_extension)

	return (returned_list)	

def get_queued_directory_locations():
	returned_list = []     

	for image_file in os.listdir( locations.queue_save_location() ):
		location = os.path.join(locations.queue_save_location(), image_file)

		returned_list.append(location)

	return (returned_list)