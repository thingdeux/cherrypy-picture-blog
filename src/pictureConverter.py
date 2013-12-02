from PIL import Image
import os
import sys
from database import get_latest_image_id
from logger import log
from locations import thumbnail_save_location
from locations import image_save_location


testPictureLocation = "C:\Development\Python\Junk\Bro.jpg"
outputlocation = "C:\Development\Python\Junk\gest.jpg"

def return_image_object(location):
	try:
		picObject = Image.open(location)
		return (picObject)
	except Exception, err:
		for error in err:
			log ("Unable to open picture" + str(err))
			return (False)

def convert_image_to_thumbnail(picObject):	
		
	try:
		thumbnail_size = (100,100)
		picObject.thumbnail( thumbnail_size )
		
		#Get latest DB id and append to the filename 
		save_location = os.path.join(thumbnail_save_location(), str(get_latest_image_id) + '.jpg')		
		picObject.save(save_location, "JPEG")
	except Exception, err:
		for error in err:
			log ("Thumbnail Save Error" + str(error) )


#def create_watermark(location):


#print(thumbnail_save_location())
#testImage = return_image_object('/Users/joshuajohnson/Pictures/DarthDucku.jpg')
#convert_image_to_thumbnail(testImage)





#locations.image_save_location()
#locations.thumbnail_save_location()