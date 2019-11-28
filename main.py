from flask import Flask, request
from json import dumps
from google.cloud import vision
from google.cloud.vision import types
import os
import io
import re
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import request
import sys
import numpy as np
import pickle
from PIL import Image
import flask
app = Flask(__name__)
bootstrap = Bootstrap(app)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"





      
def get_date(imagefiles):
	#image_file='Receipts/0349ff40.jpeg'
	
	date_list=[]
	for image_file in imagefiles:
		#print("image_file----",image_file)
		img_name=re.findall("\S+[.]\S+",str(image_file))
		print("name of image----------",img_name)
		try:
			img = Image.open(image_file)
			buffer = io.BytesIO()
			img.save(buffer, "JPEG")
			content = buffer.getvalue()
			client = vision.ImageAnnotatorClient()
			
			        
			content_image = types.Image(content=content)
			response = client.document_text_detection(image=content_image)
			document = response.full_text_annotation
			ygh=[]

			for text in response.text_annotations:
			    ygh.append(text.description)
			k=ygh[0].replace("\n"," ")
			print(k.lower())
			date=re.findall("\d{1,2}\s{0,2}[-\\\/]\d{1,2}\s{0,2}[-\\\/]\s{0,2}\d{2,4}",k)
			print(date)
			if date:
				date_list.append([img_name[0],date[0]])
			else:
				date1=re.findall("\d{1,2}\s{0,2}[/\-\,]\s{0,2}[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]\s{0,2}[/\,\-\|]\d{2,4}"
					,k.lower())
				#print(date1)
				if date1:
					#print(date1)
					date_list.append([img_name[0],date1[0]])
				else:
					date2=re.findall("((jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s{0,2}\d{1,2}\s{0,2}[,\-\.\']\s{0,2}\d{2,4})"
						,k.lower())
					#print(date2[0][0])
					if date2:
						#rint(date2[0][0])
						date_list.append([img_name[0],date2[0][0]])
					else:
						date3=re.findall("(\d+[-\/\d](jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s{0,2}['\-\/]\s{0,2}\d{2,4})",k.lower())
						
						if date3:
							#print(date3)
							date_list.append([img_name[0],date3[0][0]])
						else:
							print("none")
							date_list.append([img_name[0],"null"])
							count+=1
		except:
			pass

	
	return date_list


	



@app.route("/")
def index():
    return render_template("upload.html")


@app.route('/result', methods=["GET", "POST"])
def uploadfile():
	if request.method == "POST":
		#file = request.files['file']
		uploaded_files = flask.request.files.getlist("file")
		print("uploadfile",uploadfile)
		if uploaded_files:
			return str("Date found is :")+str(get_date(uploaded_files))
		else:
			return "please ulpoad an image"
	




if __name__ == '__main__':
   app.run(debug = True)
