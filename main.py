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
    
    #Render the mako template
    self.mako_template_render = mako_template.render()                   

    return self.mako_template_render



  @cherrypy.expose
  def uploadPicture(self, **kwargs):
    #Takes a binary file and places it in the 'queue' folder for image processing
    def write_uploaded_image_file(location):
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


    try:
      #Object of each file passed to the server via post
      uploadObj = kwargs.get('file[]')

      for cherrypyObj in uploadObj:        
        #Save each file in the queue_save_location folder as its own filename

        #If a duplicate filename is found append a number to the file and write it anyhow      
        if not os.path.isfile( os.path.join(locations.queue_save_location(), cherrypyObj.filename) ):
          file_location = os.path.join(locations.queue_save_location(), cherrypyObj.filename)          
          write_uploaded_image_file( file_location ) 
          #Create Thumbnail for queue process page             
          pictureConverter.create_queue_thumbnail( file_location,locations.queue_save_location() )          

        else:
          #Find out how many files exist with the same name and append a count of the files to the filename - super hacky!!   
          #Known "problem" of fuzzy matching between already existing files.  Not serious as copy will be made either way.
          count = get_duplicate_image_file_count(locations.queue_save_location(), cherrypyObj.filename)
          filename_with_count = cherrypyObj.filename.replace('.', '-' + str(count) + '.')
          file_location = os.path.join(locations.queue_save_location(),  filename_with_count)     
          write_uploaded_image_file( file_location )
          #Create Thumbnail for queue process page          
          pictureConverter.create_queue_thumbnail( file_location, locations.queue_save_location() )          

    except Exception, err:
      for error in err:
        log("Unable to receive upload - " + error)
  
  @cherrypy.expose
  def processPicture(self, **kwargs):    
    for field, data in kwargs.iteritems():
      print (str(field) + ": " + str(data) )

  @cherrypy.expose
  def deletePicture(self, **kwargs):
    print kwargs

def startServer():

  if database.verify_database_existence():
    try:
      database.verify_folder_existence()  #If the images and thumbnails folder don't exist create them.
      
      if server_mode is "debug":
        if database.get_latest_image_id() is 1:
          database.create_test_data()

      cherrypy.quickstart(web_server(), config=conf)
    except Exception, err:
      for error in err:
        log("Unable to start Webserver" + str(error))

  else:
    database.create_fresh_tables()       
    startServer()



startServer()