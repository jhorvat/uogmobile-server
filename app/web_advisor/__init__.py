import os
import constants

_basedir = os.path.abspath(os.path.dirname(__file__)) # Get this file's directory rather than pwd

for f in os.listdir("{}/scripts".format(_basedir)): # Loop through the scripts folder
    filename, file_extension = os.path.splitext(f)

    if file_extension and file_extension == ".js": # Any JS files added to the JS_SCRIPTS dictionary in constants.py
        with open("{}/scripts/{}".format(_basedir, f), "r") as open_file:
            constants.JS_SCRIPTS[filename] = open_file.read()
