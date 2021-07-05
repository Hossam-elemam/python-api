import cv2
import pytesseract
import re
from nltk.tokenize import line_tokenize, sent_tokenize, word_tokenize,TweetTokenizer
import mysql.connector
from flask import Flask, request, jsonify
import base64
import json
import sys
import json
import pymongo

host_name = "localhost"
username = "root"
password = ""
database_name = "medical"

#user_id = sys.argv[1]

def scan_image ( user_id):

    mydb = mysql.connector.connect(
         host=host_name,
         user=username,
         passwd=password,
         database=database_name
        )

    x = str (user_id)
    user_id = x
    # y =  str(user_image)
    # user_image = y
    mycursor = mydb.cursor()
    mycursor.execute("SELECT image FROM users WHERE UserId=" + user_id)
    image1 = mycursor.fetchone()
    image = str(image1)

    # request_data = request.get_data()
    # user_image = {'user_image':request_data["base64"]}
    imgdata = base64.b64decode(image)
    filename = 'some_image.png'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

    pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image=cv2.imread('some_image.png')
    text=pytesseract.image_to_string(image)


    new_text=text[text.find("Collection"):]

    # \*step3_______________________________________________*\
    new_text = new_text.replace('Chemical Examination', '')
    new_text = new_text.replace('Microscopic Examination', '')
    new_text = new_text.replace('aes', '')
    new_text = new_text.replace('*', '')
    new_text = new_text.replace('“', '')
    new_text = new_text.replace('HPF', '')
    new_text = new_text.replace('fHPF', '')
    new_text = new_text.replace('”', '')
    new_text = new_text.replace('f', '')
    new_text = new_text.replace(',', '')
    new_text = new_text.replace('Sp .Gravity', 'Sp.Gravity')
    new_text = new_text.replace('Proteins ( Albumin )', 'Proteins')
    new_text = new_text.replace('Ketone Bodies', 'Ketone_Bodies')
    new_text = new_text.replace('Epithelial Cells', 'Epithelial_Cells')
    new_text = new_text.replace('Red Blood Cells', 'Red_Blood_Cells')
    new_text = new_text.replace(';', '')
    new_text = new_text.replace('Pus Cells', 'Pus_Cells')
    new_text = new_text.replace('Ova & Parasites', 'Ova_Parasites')
    new_text = new_text.replace('Lt ee epee', 'Nil ')
    new_text = new_text.replace('_ Nil', 'Nil')

    print("Result After Removing Unnisessery Words___________________________________________")

    new_text = new_text.lower()
    token = line_tokenize(new_text)
    print(new_text)
    Dict = {}
    token = line_tokenize(new_text)
    for lines in token:
        words = word_tokenize(lines)

    for elem in token:
        elem_words = elem.split()
        Dict[elem_words[0]] = elem_words[1]

    print(Dict)
    mylist = list(Dict.items())
    print (type(Dict))
    print (type(mylist))



    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["urineAnalysis"]

    # take care ya hossam i put static user id
    # you should put the user id that come from flutter ya hossam
    user_id = 14
    analysis_result = [
        { '_id': user_id, "color": "yellow", "Bictric": "Null"},
    ]
    print (type(analysis_result))

    x = mycol.insert_one(Dict)

    #print(x.inserted_ids)
    del Dict["_id"]
    y = mycol.find_one()
    print(y)

    return Dict

#scan_image (14)






