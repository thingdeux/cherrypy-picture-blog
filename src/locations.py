import os

def current_folder():
	the_current_folder = os.path.dirname(os.path.abspath(__file__))	
	return (the_current_folder.rstrip('src'))

def image_save_location():
	current_folder = os.path.dirname(os.path.abspath(__file__))
	os.path.join(current_folder, 'images')

def thumbnail_save_location():
	current_folder = os.path.dirname(os.path.abspath(__file__))
	os.path.join(current_folder, 'thumbnails')