import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
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
                    }
        }

def isAllowedInAdminArea(header):   
  keys = locations.readKeys()    
  try:
    if header['Remote-Addr'] in keys:      
      return (True)
    else:
      return (False)
  except:
    return (False)



class main_site(object):

  @cherrypy.expose	
  def index(self, *args, **kwargs):    
  	#Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/index.html')
    random_images = database.get_image_for_every_main_tag()
    main_tags = database.get_tags()
    blog = database.get_blogs()

    #Render the mako template
    self.mako_template_render = mako_template.render(images = random_images, main_tags = main_tags, blog = blog) 

    return self.mako_template_render

  @cherrypy.expose
  def p(self, *args, **kwargs): 
    mako_template = Template(filename='static/templates/index_data.tmpl')
    blog = database.get_blogs()
    main_tag = args[0]
    
    try:
      event_tag = args[2]      
      sub_tag = args[1]
      imageIDList = []      

      #SQL Offset number for DB Query
      try:
        offset = int(args[3])
      except:
        offset = 0      

      if event_tag == "Misc":
        images = database.get_latest_12_images_by_tag(main_tag, sub_tag, False, offset)        
      else:
        images = database.get_latest_12_images_by_tag(main_tag, sub_tag, event_tag, offset)      

      for image in images:        
        imageIDList.append(image[0])     

      if len(images) > 0:
        self.mako_template_render = mako_template.render(event_main_tag = main_tag, event_sub_tag = sub_tag,
                                                        imageIDList = imageIDList, event_tag = event_tag, 
                                                        images = images, display_type = "Event", offset = offset,
                                                        blog = blog)
          
        return self.mako_template_render
      else:
        return ( self.default() )

    except:      
      try:
        sub_tag = args[1]      
        event_tags = database.get_event_tags(sub_tag)
        images = database.get_image_for_each_event_tag(sub_tag)      
        misc_images = database.get_image_for_misc_sub_tag(main_tag, sub_tag)       
        
        if len(images) > 0 or len(misc_images) > 0:
          self.mako_template_render = mako_template.render(parent_main_tag = main_tag, parent_sub_tag = sub_tag, 
                                      event_tags = event_tags, images = images, misc_images = misc_images, display_type = "Sub",
                                      blog = blog)
          
          return self.mako_template_render
        else:
          return ( self.default() )

      except:      
        try:   
          sub_tags = database.get_sub_tags(main_tag)
          images = database.get_image_for_each_sub_tag(main_tag)          
          
          if len(images) > 0:            
            self.mako_template_render = mako_template.render(main_tag = main_tag, sub_tags = sub_tags, 
                                        images = images, display_type = "Main", blog = blog)
            return self.mako_template_render
          else:         
            return ( self.default() )

        except Exception, err:
          for error in err:
            log("Unable to build Template: " + str(error) )
  
  @cherrypy.expose
  def admin(self, *args, **kwargs):    
    try:
      Headers = cherrypy.request.headers

      if isAllowedInAdminArea(Headers):
        nav_location = args[0].lower()
        if nav_location == "manage":
          return ( self.manage() )
        elif nav_location == "upload":
          return ( self.upload() )
        elif nav_location == "process":
          return (self.process() )
      else:
        return (self.default())

    except:      
      return (self.default())  
    
  def upload(self, **arguments):
    #Create the below template using upload.html (and looking up in the static folder)
    mako_template = Template(filename='static/upload.html')
    
    #Render the mako template
    self.mako_template_render = mako_template.render()                 

    return self.mako_template_render
  
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
  
  def manage(self, **arguments):
    #Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/manage.html')
    main_tags = database.get_tags()
    sub_tags = database.get_sub_tags()
    event_tags = database.get_event_tags()
    blogs = database.get_blogs("titles")    
    logs = database.get_top_30_logs()

    #Render the mako template
    self.mako_template_render = mako_template.render(main_tags = main_tags, sub_tags = sub_tags, 
                                                     event_tags = event_tags, logs = logs, blogs = blogs)

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

    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
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
          log("Unable to receive upload - " + error, "WEB", "MEDIUM")
    else:
      return (self.default())
  
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
    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
      if len(kwargs) > 0:          
        isImageDeleted = database.update_image_data(kwargs)

        if isImageDeleted:
          return ('<span id = "deleted" class = "ui-widget ui-widget-content">Image deleted</span>')
        else:
          return ('<span class = "ui-widget ui-widget-content">Image metadata updated</span>')
    else:
      return (self.default())

  @cherrypy.expose
  def updateBlogData(self, *arguments, **kwargs):    
    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):    
      try:
        if kwargs['postType'] == "update":
          succesfulUpdate = database.update_blog(kwargs)
        elif kwargs['postType'] == "insert":          
          succesfulUpdate = database.insert_blog(kwargs)
        elif kwargs['postType'] == "delete":
          succesfulUpdate = database.delete_blog_by_id(kwargs['blog_id'])

        if succesfulUpdate:
          return ('UPDATED')
        else:        
          return ("ERROR - UNABLE TO UPDATE")

      except Exception, err:
        for error in err:
          log("Couldn't update blog - " + error, "DATABASE", "SEVERE")

        return ("Error updating blog - contact admin")
    else:
      return (self.default())
  
  @cherrypy.expose
  def deleteTags(self, *arguments, **kwargs):

    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
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
    else:
      return(self.default())

  @cherrypy.expose
  def deleteProcessingPicture(self, *arguments, **kwargs):
    filesystem.delete_queued_image_and_thumbnail(kwargs['FileLocation'])

  @cherrypy.expose
  def manageTags(self, *arguments, **kwargs):
    def checkIfParamExists(name):
      try:
        return( arguments[0].get(name) )
      except:
        try:                
          return (kwargs[name])
        except:
          return ("")         
    
    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
      #Check to see if the POST passed just a main tag, or also a sub - if they were passed
      #Send them to mako for filtering.
      #When manage tags is called from within main it passes a tuple instead of a dict so check for that as well.
      tag_type = checkIfParamExists('tag_type')
      main_tag = checkIfParamExists('main_tag')
      sub_tag = checkIfParamExists('sub_tag')

      mako_template = Template(filename='static/templates/manage_images.tmpl')
      tags = database.get_tags()    
      sub_tags = database.get_sub_tags()
      event_tags = database.get_event_tags()
      
      #Render the mako template
      self.mako_template_render = mako_template.render(main_tags = tags, sub_tags = sub_tags, 
                      event_tags = event_tags, menu_location = "get_tags", tag_type = tag_type,
                      main_tag_query = main_tag, sub_tag_query = sub_tag)

      return self.mako_template_render
    else:
      return (self.default())

  @cherrypy.expose
  def manageBlogs(self, *arguments, **kwargs):
    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
      #Dirty double try :( -REFACTOR
      try:
        #If blog_id doesn't exist then a new entry is being created so no blog db values
        try:     
          blog = database.get_blogs("id", kwargs['blog_id'])                 
        except:
          blog = ""          

        perform_action = kwargs['perform_action']
        mako_template = Template(filename='static/templates/manage_blogs.tmpl')
        self.mako_template_render = mako_template.render(blog = blog, perform_action = perform_action)

        return (self.mako_template_render)

      except Exception, err:
        return ( self.default() )
        for error in err:
          log("Unable to Manage Blog - " + error, "WEB", "LOW")
    else:
      return (self.default())

  @cherrypy.expose
  def getModalPicture(self, *args, **kwargs):
    image = database.get_image_by_id( kwargs.get('image_id') )
    mako_template = Template(filename='static/templates/image_modal.tmpl')  
    
    self.mako_template_render = mako_template.render(image = image)

    return self.mako_template_render

  @cherrypy.expose
  def insertTag(self, *arguments, **kwargs):
    Headers = cherrypy.request.headers
    if isAllowedInAdminArea(Headers):
      database.insert_tag(0, kwargs)
      return ( self.manageTags(kwargs) )
    else:
      return (self.default())
  
  @cherrypy.expose
  def default(self, *arguments):
    #Create the below template using index.html (and looking up in the static folder)
    mako_template = Template(filename='static/404.html')
    arguments = arguments

    #Render the mako template
    self.mako_template_render = mako_template.render(passed = arguments) 

    return self.mako_template_render


def startServer():

  if database.verify_database_existence():
    try:
      #If the images /thumbnails / queue folders don't exist create them.
      database.verify_folder_existence()
      
      if server_mode is "debug":
        if len( database.get_tags() ) <= 1:
          database.create_test_data()

      cherrypy.quickstart(main_site(), config=conf)
    except Exception, err:
      for error in err:
        log("Unable to start Webserver" + str(error), "WEB", "SEVERE")

  else:
    database.create_fresh_tables()       
    startServer()

if __name__ == "__main__":
  startServer()