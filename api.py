import sys
from importlib.resources import Resource
from flask_cors import CORS, cross_origin
import pytesseract
from nltk.tokenize import line_tokenize, word_tokenize
from flask import Flask, request, jsonify
import json
import base64
import cv2
from main import scan_image


# declared an empty variable for reassignment
responseName = ''
response64 = ''

# creating the instance of our flask application
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/image": {"origins": "http://localhost"}})


@cross_origin(origin='localhost',headers=['Content- Type'])

# route to entertain our post and get request from flutter app
@app.route('/image', methods=['GET','POST'])
def image():

    request_data = request.data  # getting the response data
    #request_data = json.loads(request_data) # converting it from json to key value pair
    #response_json = request_data.decode('utf-8').replace('\0', '')
    #responseahmed = json.loads(request_data)
   # userid = request_data['user_id']
    # fetching the global response variable to manipulate inside the function
   # global responseName, response64

    # checking the request type we get from the app
    if (request.method == 'POST'):
        try:
            request_data = request.data  # getting the response data
            #request_data = json.loads(request_data)  # converting it from json to key value pair
            #response_json = request_data.decode('utf-8').replace('\0', '')
            #responseahmed = json.loads(request_data)

            print(request_data)


        except Exception as e:
             print(e)

        print(request_data)

        userid = request.form["user_id"]
        #userimage = request_data['user_image']

        # here enter your function
        response = scan_image(userid)  # re-assigning response with the name we got from the user
        print("**************")
        print (response)
        return jsonify(response) #jsonify({'result':response})  # to avoid a type error
       # obj={"result":userid}
        #result=obj.json()
        #print(result)

        #return
    else:

        return "no image"
            #request.form["user_id"]
        #return jsonify() # sending data back to your frontend app


if __name__ == "__main__":
    app.run(debug=True)

class StaticFiles(Resource):
    def get(self):
        return(request.base_url)