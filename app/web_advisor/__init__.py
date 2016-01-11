import os
import constants

_basedir = os.path.abspath(os.path.dirname(__file__))

for f in os.listdir("{}/scripts".format(_basedir)):
    filename, file_extension = os.path.splitext(f)

    if file_extension and file_extension == ".js":
        with open("{}/scripts/{}".format(_basedir, f), "r") as open_file:
            constants.JS_SCRIPTS[filename] = open_file.read()
