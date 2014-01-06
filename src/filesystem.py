import os
import logger
import locations

def delete_file(filename):
	test = "test"


def get_queue_directory_list():
	returned_list = []     

	for image_file in os.listdir(locations.queue_save_location()):		
	    filename_without_extension = image_file.split('.')

	    #Exclude the .thumbnail files
	    if 'thumbnail' not in filename_without_extension[1]:
	    	
		    image_location = os.path.join(locations.queue_save_location(), image_file)
		    thumbnail_location = os.path.join("/queue", filename_without_extension[0] + ".thumbnail")		    
		    
		    #Create list with the filename (for displaying on the site) and actual file system location (for backend work)
		    inner_list = []
		    inner_list.append(filename_without_extension[0])
		    inner_list.append(image_location)
		    inner_list.append(thumbnail_location)
		    
		    returned_list.append(inner_list)

	return (returned_list)	


def get_queued_directory_locations():
	returned_list = []     

	for image_file in os.listdir( locations.queue_save_location() ):
		location = os.path.join(locations.queue_save_location(), image_file)

		returned_list.append(location)

	return (returned_list)