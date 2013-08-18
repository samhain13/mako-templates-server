# Modified Mako Templates Test Server

A simple webserver for testing Mako templates for HTML and JSON.  
It also has the ability to serve static files. But please do not  
use this in a production environment, unless you're crazy.  
  
makoserv.py is just a jacked-up version of the run_wsgi.py script  
that comes with a standard Mako install. Modifications are marked  
by “S13: description of mod”.
  
  
## Usage
Install Mako:

    $ pip install mako
  
Go to your project's directory:

    $ cd /path/to/your/project/directory

Start serving on http://0.0.0.0:5000:

    /path/to/your/project/directory$ python /path/to/makoserv.py

Or serve on a custom ipaddress and port (both are required):

    /path/to/your/project/directory$ python /path/to/makoserv.py <ip_address>:<port_number>


## Cached Templates

Cached/temporary files are stored in /tmp/makoserv in Ubuntu,  
that directory is defined in the “temp” variable in line 14.  
Change that when using makoser.py in other OSes.