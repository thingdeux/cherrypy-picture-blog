from PIL import Image
import os
import sys
from database import get_latest_image_id
from logger import log
from locations import thumbnail_save_location
from locations import image_save_location
from locations import current_folder


testPictureLocation = "C:\Development\Python\Junk\Bro.jpg"

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
		save_location = os.path.join(thumbnail_save_location(), str(get_latest_image_id() ) + '.jpg')	
		picObject.save(save_location, "JPEG")
	except Exception, err:
		for error in err:
			log ("Thumbnail Save Error" + str(error) )


def create_watermark(picObject):
	try:
		save_location = os.path.join(image_save_location(), str(get_latest_image_id() ) + '.jpg')

		shrink_size = (1280,1024)
		picObject.thumbnail( shrink_size )
		#picObject = picObject.resize( shrink_size )
	
		watermark_image = Image.open(os.path.join(current_folder(), 'static/watermark.png')  )		
		watermark_image = watermark_image.convert('RGBA')
		
		if picObject.mode is not 'RGBA':
			picObject = picObject.convert('RGBA')
		
		#Find the bottom right corner of the image, and set the coordinate for the text on the bottom right
		pic_size_x, pic_size_y = picObject.size
		watermark_size_x, watermark_size_y = watermark_image.size	
		watermark_box = (pic_size_x - watermark_size_x, pic_size_y - watermark_size_y, pic_size_x, pic_size_y)
		
		#Transpose the watermark.png file over the image
		picObject.paste(watermark_image, watermark_box, watermark_image)
		picObject.save(save_location, "JPEG")

	except Exception, err:
		for error in err:
			log("Image: Unable to create watermark " + error)


def save_uploaded_image(picObject):
	#Insert Database record for images
	log("Yup")

def process_uploaded_image(location):
	try:
		the_image = return_image_object(location)		
		create_watermark(the_image)
		#convert_image_to_thumbnail(the_image)
		#save_uploaded_image(the_image)
	except:
		log ("Image: Unable to process - " + str(location) )


#process_uploaded_image('/Users/joshuajohnson/Pictures/IMG_7461 copy.jpg')

