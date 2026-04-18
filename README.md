# Flask Official Docs/ Flask Quickstart documentation
#    https://flask.palletsprojects.com/
# ctrl F or scroll down to find all information below



what i did to set up aka refernce page.....
################
##### app.py #####
################

#Example from docs:
@app.route("/")
def hello_world():
    return "Hello, World!"

#Handling JSON request for GPS route
request.get_json()

#jsonify returning data
return jsonify({...})


Trying to build:
GET /                  is server turned on
GET /bus-location      send GPS data
GET /attendance        send student data
POST /gps              receive data from frontend

USED AI TO CREATE DATA FILL IN FOR DEMO

###########################
#### requirements.txt  ####
############################

# same site (flask.palletsprojects.com)






###########################
# Alicorn Backend Demo Setup
############################

1. Download or clone repo
2. Open terminal in folder
    - go to app.y folder, click file path, type cmd

## Install dependencies
  - in command promt type
        pip install -r requirements.txt

## Run server
python app.py

## Open in browser for testing
http://127.0.0.1:5000/
http://127.0.0.1:5000/bus-location
http://127.0.0.1:5000/attendance
http://127.0.0.1:5000/students

this makes:
your computer the server
flask backend running on it
browser - client connecting to it


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cite pip documentation and Python Docs

now intall with this:    pip install -r requirements.txt


