import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import src.logger as logger
import src.database as database
import src.pictureConverter as pictureConverter
import src.locations as locations


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
    
        

def startServer():

  if database.verify_database_existence():
    database.verify_folder_existence()  #If the images and thumbnails folder don't exist create them
    cherrypy.quickstart(web_server(), config=conf)    
  else:
    database.create_fresh_tables()
    startServer()


startServer()

