import sys

#app's path
sys.path.insert(0,"C:\\WebAutoTestProject\\website")

from website.index import app as application

#Initialize WSGI app object
#application = index