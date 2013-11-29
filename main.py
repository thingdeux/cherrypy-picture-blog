import cherrypy
import os
from mako.template import Template
from mako.lookup import TemplateLookup

current_folder = os.path.dirname(os.path.abspath(__file__))

cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
                         'server.socket_port': 1234,
                         })


conf = {         
        '/static': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'static')
                    },
         '/static/css': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'static/css')
                        },
         '/js': { 'tools.staticdir.on' : True,
                      'tools.staticdir.dir': os.path.join(current_folder, 'js')
                    },
         '/js/lib': { 'tools.staticdir.on' : True,
                          'tools.staticdir.dir': os.path.join(current_folder, 'js/lib')
                        },
        'favicon.ico': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': os.path.join(current_folder, "/static/favicon.ico")
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
    
        

cherrypy.quickstart(web_server(), config=conf)