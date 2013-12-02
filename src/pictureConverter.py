from PIL import Image
import os
import sys
from database import get_latest_image_id
from database import insert_image_record
from logger import log
from locations import thumbnail_save_location
from locations import image_save_location
from locations import current_folder


class WebsiteImage:
	def __init__(self, location):		
		self.location = location		

		try:
			self.picObject = self.return_image_object()
			self.watermarked_image = self.create_watermark()
			self.thumbnail = self.convert_image_to_thumbnail()
			self.date_taken = self.get_date_taken()

		except Exception, err:
			for error in err:
				log("Image: Unable to process image - " + str(error))

		try:
			self.save_uploaded_images()
			#insert_image_record(self.image_location, self.thumb_location)
		except Exception, err:
			for error in err:
				log("Image: Unable to save images" + str(error))

	def return_image_object(self):
		try:
			pictureObject = Image.open(self.location)
			return (pictureObject)
		except Exception, err:
			for error in err:
				log ("Unable to open picture" + str(err))
				return (False)

	def convert_image_to_thumbnail(self):
			
		try:
			picObject = self.picObject
			thumbnail_size = (100,100)			
			picObject.thumbnail( thumbnail_size )
			
			#Get latest DB id and append to the filename 		
			return(picObject)

		except Exception, err:
			for error in err:
				log ("Thumbnail Save Error" + str(error) )


	def create_watermark(self):
		try:
			picObject = self.picObject
			shrink_size = (1280,1024)
			picObject.thumbnail( shrink_size )		
		
			watermark_image = Image.open(os.path.join(current_folder(), 'static/watermark.png')  )	
			watermark_image = watermark_image.convert('RGBA')
			
			#Convert the picture to RGBA if it's not already
			if picObject.mode is not 'RGBA':
				picObject = picObject.convert('RGBA')
			
			#Find the bottom right corner of the image, and set the coordinate for the text on the bottom right
			pic_size_x, pic_size_y = picObject.size
			watermark_size_x, watermark_size_y = watermark_image.size	
			watermark_box = (pic_size_x - watermark_size_x, pic_size_y - watermark_size_y, pic_size_x, pic_size_y)
			
			#Transpose the watermark.png file over the image
			picObject.paste(watermark_image, watermark_box, watermark_image)
			
			return(picObject)

		except Exception, err:
			for error in err:
				log("Image: Unable to create watermark " + error)

	def save_uploaded_images(self):	
		self.thumb_location = os.path.join(thumbnail_save_location(), str(get_latest_image_id() ) + '.jpg')	
		self.image_location = os.path.join(image_save_location(), str(get_latest_image_id() ) + '.jpg')

		try:		
			self.watermarked_image.save(self.image_location, "JPEG")	
			self.thumbnail.save(self.thumb_location, "JPEG")
		except Exception, err:
			for error in err:
				log("Image: Unable to save images " + str(error))

	def get_date_taken(self):
		exif_data = self.picObject._getexif()

		#Get the 'date taken' exif data and return it
		return ( exif_data.get(36867) )		


WebsiteImage('C:\Users\Thing2\Pictures\Blackup.jpg')

