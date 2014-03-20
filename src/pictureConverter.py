from PIL import Image
import os
import sys
from database import get_latest_image_id
from database import insert_image_record
from logger import log
from locations import thumbnail_save_location
from locations import image_save_location
from locations import current_folder
from locations import queue_save_location


class WebsiteImage:
	def __init__(self, location, *args, **kwargs):
		if args:
			self.location = os.path.join(queue_save_location(), location)
			self.postData = args[0]		
		else:			
			self.location = location

		try:
			self.picObject = self.return_image_object()

			if self.picObject:
				self.watermarked_image = self.create_watermark()
				self.thumbnail = self.convert_image_to_thumbnail()
				self.size = self.get_image_height_and_width()					

				try:
					isUploaded = self.save_uploaded_images()
					
					if isUploaded:
						self.picture_row_id = insert_image_record(name = self.postData.picture_name, 
							image_location=self.image_location, thumb_location=self.thumb_location,
							date_taken=self.postData.date_taken, caption=self.postData.picture_caption, 
							width = self.size[0], height = self.size[1])
						
						self.isSuccesful = True

				except Exception, err:
					self.isSuccesful = False
					for error in err:
						log("Image: Unable to save images" + str(error), "CONVERTER", "MEDIUM")

		except Exception, err:
			self.isSuccesful = False
			for error in err:
				log("Image: Unable to process image - " + str(error), "CONVERTER", "MEDIUM")



	def return_image_object(self):
		try:
			pictureObject = Image.open(self.location)
			return (pictureObject)
		except Exception, err:
			self.isSuccesful = False
			for error in err:				
				log("Unable to open picture - " + str(err), "CONVERTER", "MEDIUM")
				return (False)

	def convert_image_to_thumbnail(self):
			
		try:
			picThumb = self.picObject
			thumbnail_size = (150,125)			
			
			#Create blank canvas
			picObject = Image.new( self.picObject.mode, thumbnail_size)
			#Turn the copy of the passed Image Object into a thumbnail
			picThumb.thumbnail(thumbnail_size, Image.ANTIALIAS)

			#Find the difference between the two to create black background behind cropped image (if not widescreen format)
			x_offset= (picObject.size[0] - picThumb.size[0]) // 2
			y_offset= (picObject.size[1] - picThumb.size[1]) // 2

			#Create new image with black background pasted behind the resize
			picObject.paste(picThumb, (x_offset, y_offset))
						
			return(picObject)

		except Exception, err:
			self.isSuccesful = False
			for error in err:
				log("Thumbnail Save Error" + str(error), "CONVERTER", "MEDIUM" )

	def create_watermark(self):
		try:
			picObject = self.picObject
			shrink_size = (1280,1024)
			picObject.thumbnail( shrink_size, Image.ANTIALIAS )		
		
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
			self.isSuccesful = False
			for error in err:
				log("Unable to create watermark " + str(error), "CONVERTER", "MEDIUM")

	def save_uploaded_images(self):			

		self.thumb_location = os.path.join(thumbnail_save_location(), str(get_latest_image_id() ) + '.jpg')
		self.image_location = os.path.join(image_save_location(), str(get_latest_image_id() ) + '.jpg')			

		try:		
			self.watermarked_image.save(self.image_location, "JPEG")	
			self.thumbnail.save(self.thumb_location, "JPEG")
			return (True)
		except Exception, err:
			self.isSuccesful = False
			for error in err:
				log("Unable to save images " + str(error), "CONVERTER", "MEDIUM")

			return (False)

	def get_image_height_and_width(self):
		try:
			return (self.watermarked_image.size)
		except:
			return ( (0,0) )


def create_queue_thumbnail(file_location,save_location):	
	try:
		#Break the location into chunks then take the filename
		filename_chunks = file_location.split('/')
		filename = filename_chunks[len(filename_chunks) - 1]
		filename = filename.split('.')[0]
		
		size = 260, 260
		queue_image = Image.open(file_location)
		queue_image.thumbnail(size, Image.ANTIALIAS)		
		queue_image.save(os.path.join(save_location, filename + ".thumbnail" ), "JPEG")

	except Exception, err:
		for error in err:
			log ("Thumbnail Save Error: " + str(error), "CONVERTER", "MEDIUM" )

def get_date_exif(image_name):
	try:
		filename = os.path.join(queue_save_location(), image_name)
		
		queue_image = Image.open(filename)
		exif_data = queue_image._getexif()
		formatted_date = exif_data.get(36867).split(':')		

		built_date_string = formatted_date[1] + "/" + formatted_date[2].split(' ')[0] + "/" + formatted_date[0]
				
		#Get the 'date taken' exif data and return it if available
		return (  built_date_string )				
	except:				
		return("01/01/84")
	

