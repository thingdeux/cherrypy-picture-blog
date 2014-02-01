import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import src.logger as logger
from src.logger import log
import src.database as database
import src.pictureConverter as pictureConverter
import src.locations as locations
import src.filesystem as filesystem

server_mode = "debug"

cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 1234,
                         })


conf = {        
        '/static': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(locations.current_folder(), 'static')
                    },
         '/static/css': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(locations.current_folder(), 'static/css')
                        },
         '/js': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(locations.current_folder(), 'js')
                    },
         '/queue': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(locations.current_folder(), 'queue'),
                      'tools.staticdir.content_types': {'jpg': 'image/jpeg'}
                        },
          '/images': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(locations.current_folder(), 'images'),
                      'tools.staticdir.content_types': {'jpg': 'image/jpeg'}
                        },
          '/thumbnails': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(locations.current_folder(), 'thumbnails'),
                      'tools.staticdir.content_types': {'jpg': 'image/jpeg'}
                        },
         '/js/lib': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(locations.current_folder(), 'js/lib')
                        },
        'favicon.ico': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': os.path.join(locations.current_folder(), "static/favicon.ico")
                    },

        }


class web_server(object):

  @cherrypy.expose	
  def index(self, **arguments):
  	#Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/index.html')
    
    #Render the mako template
    self.mako_template_render = mako_template.render()                    

    return self.mako_template_render

  @cherrypy.expose
  def upload(self, **arguments):
    #Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/upload.html')
    
    #Render the mako template
    self.mako_template_render = mako_template.render()                 

    return self.mako_template_render

  @cherrypy.expose
  def process(self, **arguments):
    #Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/process.html')
    queued_files = filesystem.get_queue_directory_list()
    tags = database.get_tags()    
    sub_tags = database.get_sub_tags()
    event_tags = database.get_event_tags()
    
    #Render the mako template
    self.mako_template_render = mako_template.render(queued_files = queued_files, tags = tags, sub_tags = sub_tags, event_tags = event_tags)

    return self.mako_template_render

  @cherrypy.expose
  def manage(self, **arguments):
    #Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/manage.html')
    main_tags = database.get_tags()
    sub_tags = database.get_sub_tags()
    event_tags = database.get_event_tags()

    #Render the mako template
    self.mako_template_render = mako_template.render(main_tags = main_tags, sub_tags = sub_tags, event_tags = event_tags)

    return self.mako_template_render

  @cherrypy.expose
  def uploadPicture(self, **kwargs):
    #Takes a binary file and places it in the 'queue' folder for image processing
    def write_uploaded_image_file(location, cherrypyObj):
      tempFile = open(location, 'wb')
      tempFile.write(cherrypyObj.file.read())
      tempFile.close()

    def get_duplicate_image_file_count(location, filename):
      filename_found_count = 0
      filename_without_extension = filename.split('.')[0]

      for image_file in os.listdir(location):        

        if filename_without_extension in image_file:
          filename_found_count = filename_found_count + 1

      return (filename_found_count)

    def uploadImage(passedImage):
      #Save each file in the queue_save_location folder as its own filename        
      #If a duplicate filename is found append a number to the file and write it anyhow      
      if not os.path.isfile( os.path.join(locations.queue_save_location(), passedImage.filename) ):
        file_location = os.path.join(locations.queue_save_location(), passedImage.filename)          
        write_uploaded_image_file( file_location, passedImage ) 
        #Create Thumbnail for queue process page             
        pictureConverter.create_queue_thumbnail( file_location,locations.queue_save_location() )          

      else:
        #Find out how many files exist with the same name and append a count of the files to the filename - super hacky!!   
        #Known "problem" of fuzzy matching between already existing files.  Not serious as copy will be made either way.
        count = get_duplicate_image_file_count(locations.queue_save_location(), passedImage.filename)
        filename_with_count = passedImage.filename.replace('.', '-' + str(count) + '.')
        file_location = os.path.join(locations.queue_save_location(),  filename_with_count)     
        write_uploaded_image_file( file_location, passedImage )
        #Create Thumbnail for queue process page          
        pictureConverter.create_queue_thumbnail( file_location, locations.queue_save_location() )

    try:      
      #Object of each file passed to the server via post
      uploadObj = kwargs.get('file[]')

      try:
        imageCount = len(uploadObj)
                
        for image in uploadObj:
          uploadImage(image)

      except:        
        uploadImage(uploadObj)

    except Exception, err:
      for error in err:
        log("Unable to receive upload - " + error)
  
  @cherrypy.expose
  def processPicture(self, **kwargs):
    sentPOST = database.Posted_Data(kwargs, "process")

    if sentPOST.isSuccesful == True:
      #Delete job from queue
      if ( database.delete_currently_processing_job(sentPOST.picture_name) ):
        filesystem.delete_queued_image_and_thumbnail(kwargs['FileLocation'])      
    
  @cherrypy.expose
  def checkProcessingQueue(self, *arguments, **kwargs):
    #Take a GET request with the image_name passed as a parameter and check to see if its being ..
    #  ...  processed
    if len(arguments) > 0:
      processing_image = arguments[0]
    else:
      processing_image = ""

    return ( str( database.check_for_processing_image(processing_image) ) )

  @cherrypy.expose
  def getPictures(self, *arguments, **kwargs):    
    returned_data = database.get_images_by_tag( kwargs )
    mako_template = Template(filename='static/templates/manage_images.tmpl')    

    self.mako_template_render = mako_template.render(image_data = returned_data, menu_location = "list")

    return self.mako_template_render

  @cherrypy.expose
  def getOnePicture(self, *arguments, **kwargs):   
    image_id = kwargs.keys()[0]
    returned_data = database.get_image_by_id ( image_id )
    tag_data = database.get_image_tags_by_image_id( image_id )
    main_tags = tag_data[0]
    sub_tags = tag_data[1]
    event_tags = tag_data[2]

    mako_template = Template(filename='static/templates/manage_images.tmpl')

    self.mako_template_render = mako_template.render(image_data = returned_data, main_tags = main_tags, 
                                sub_tags = sub_tags, event_tags = event_tags, menu_location = "selected")

    return self.mako_template_render

  @cherrypy.expose
  def updateImageData(self, *arguments, **kwargs):
    if len(kwargs) > 0:          
      isImageDeleted = database.update_image_data(kwargs)

      if isImageDeleted:
        return ('<span id = "deleted" class = "ui-widget ui-widget-content">Image deleted</span>')
      else:
        return ('<span class = "ui-widget ui-widget-content">Image metadata updated</span>')      
  
  @cherrypy.expose
  def deleteTags(self, *arguments, **kwargs):
    isImageStillActive = database.delete_image_tags(kwargs)    
    
    if isImageStillActive:
      image_id = kwargs['image_id']      
      returned_data = database.get_image_by_id ( image_id )
      tag_data = database.get_image_tags_by_image_id( image_id )
      main_tags = tag_data[0]
      sub_tags = tag_data[1]
      event_tags = tag_data[2]

      mako_template = Template(filename='static/templates/manage_images.tmpl')    

      self.mako_template_render = mako_template.render(image_data = returned_data, main_tags = main_tags, 
                                  sub_tags = sub_tags, event_tags = event_tags, menu_location = "selected")

      return self.mako_template_render
      
    else:      
      return ('<span id = "deleted" class = "ui-widget ui-widget-content">Image Deleted</span>')

  @cherrypy.expose
  def deleteProcessingPicture(self, *arguments, **kwargs):
    filesystem.delete_queued_image_and_thumbnail(kwargs['FileLocation'])

  @cherrypy.expose
  def manageTags(self, *arguments, **kwargs):    
    mako_template = Template(filename='static/templates/manage_images.tmpl')
    tags = database.get_tags()    
    sub_tags = database.get_sub_tags()
    event_tags = database.get_event_tags()
    
    #Render the mako template
    self.mako_template_render = mako_template.render(main_tags = tags, sub_tags = sub_tags, event_tags = event_tags, menu_location = "get_tags", tag_type = kwargs['tag_type'])

    return self.mako_template_render

def startServer():

  if database.verify_database_existence():
    try:
      database.verify_folder_existence()  #If the images /thumbnails / queue folders don't exist create them.
      
      if server_mode is "debug":
        if len( database.get_tags() ) <= 1:
          database.create_test_data()

      cherrypy.quickstart(web_server(), config=conf)
    except Exception, err:
      for error in err:
        log("Unable to start Webserver" + str(error))

  else:
    database.create_fresh_tables()       
    startServer()


startServer()