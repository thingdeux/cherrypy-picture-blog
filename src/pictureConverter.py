from PIL import Image
import os
import sys
from logger import log

testPictureLocation = "C:\Development\Python\Junk\Bro.jpg"
outputlocation = "C:\Development\Python\Junk\gest.jpg"

def return_image_object(location):
	try:
		picObject = Image.open(location)
		return (picObject)
	except:
		log ("Unable to open picture")
		return (False)

def convert_image_to_thumbnail(picObject):
	thumbnail_size = (100,100)
		
	try:			
		picObject.thumbnail( thumbnail_size )
		picObject.save(outputlocation, "JPEG")
	except Exception, err:
		for error in err:
			log ("Thumbnail Save Error - " + str(error) )


#def create_watermark(location):



#testImage = return_image_object(testPictureLocation)
#print(testImage)