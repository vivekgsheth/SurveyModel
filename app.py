

from flask import Flask, render_template,request
app = Flask(__name__)
'''

'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html'
page = requests.get(url)
page.text
soup = BeautifulSoup(page.text, 'html.parser')

review_text_elem = soup.find_all('div',{'class':'col-md-12'})

result = []
result=[li.string for li in review_text_elem[2].find('ul').findAll('li')]
#print(result)

danger_elem = soup.find_all('div',{'class':'warning-signs-public'})
danger=[]
danger=[li.string for li in danger_elem[0].find('ul').findAll('li')]
#print(danger)

@app.route("/")
def index():
	#Import Libraries
	return render_template('index.html',result=result,danger=danger)


@app.route('/thankyou')
def thank_you():
	final_res = []
	final_dan= []

	for i in result:
		final_res.append(request.args.get(i))
	print(final_res)	

	for i in danger:
		final_dan.append(request.args.get(i))
	print(final_dan)


	symptom=[]
	for i in range(len(result)):
		if final_res[i]=='yes':
			symptom.append(result[i])

	for i in range(len(danger)):
		if final_dan[i]=='yes':
			symptom.append(danger[i])

	mild=['Fever or chills', 'Cough', 'Fatigue','Muscle or body aches', 'Headache', 'Sore throat', 'Congestion or runny nose', 'New confusion']
	moderate=['Nausea or vomiting', 'Diarrhea']
	severe=['Shortness of breath or difficulty breathing','New loss of taste or smell', 'Trouble breathing', 'Persistent pain or pressure in the chest', 'Inability to wake or stay awake', 'Bluish lips or face']
	m=0
	mo=0
	s=0

	#1-2 mild symptom {you seems to be in safe zone}
	#more than 4 mild there are chances of mild corona (you don't seen to okay)
	#more than 2 mild and atleast one moderate -> considerable chances of corona

	#						if more than 4 mild and 1 or more severre-90%
	#           more than 4 mild 1-moderate and 1 or more from severe-95%
	#1 moderate and 1 or more severe-85%
	#more than 4 mild and 1 moderate- 60%
	#more than 4 mild and more than 1 moderate- 70%



	for i in symptom:
	  if i in mild:
	    m+=1
	  elif i in moderate:
	    mo+=1
	  elif i in severe:
	    s+=1 
	  else:
	    if i in result:
	    	mo+=1
	    	moderate.append(i)
	    else:
	    	s+=1
	    	severe.append(i)

	s_len=len(severe)
	mo_len=len(moderate)
	m_len=len(mild)
	temp=(s+m)/(s_len+m_len)

	print(m,mo,s,mo_len,s_len,m_len,temp)

	symp='Heya!'
	
	if m>4 and mo>0 and s>3:
		symp= "You seems to have 97% chances of Severe corona!! you are in emergency Situation"
	elif m>4 and mo>0 and s>0:
		symp= "You seems to have 95% chances of Severe corona"
	elif m>4 and mo==0 and s>0:
		symp= "You seems to have 90% chances of Severe corona"
	elif m>2 and mo>0 and s>0:
		symp= "You seems to have 90% chances of Severe corona"
	elif s>3:
		symp= "You seems to have 90% chances of Severe corona"
	elif m<4 and mo==0 and s>0:
		symp= "You seems to have 85% chances of Severe corona"
	elif m>2 and mo>0:
		symp= "You seems to have considerable chances of corona"
	elif m>3:
		symp= "You seems to have considerable chances of corona"
	elif m<=3 or mo>0:
		symp= "You seems to be safe for now"

	'''
	if s > (s_len/2):
		symp= "You have "+ str(round(temp*100,2)) +" % chances of Severe corona"
	elif m< (m_len/2) and s==0:		
		symp= "You seems to be safe!!It is not your fault that you are feeling this way, we are in a pandemic.Keep a Safe Distance to Slow the Spread"
	elif m < (m_len/2) and   s < (s_len/2):
		symp= "You have "+ str(round(temp*100,2)) +" % chances of considerable chances of mild corona"
	elif m > (s_len/2) and s< (s_len/2):
		symp= "You have "+ str(round(temp*100,2)) +" % chances of mild corona"
	'''
	print("---------------------------------")
	Values=[]
	for i in range(len(symptom)):
		Values.append(symptom[i].split(" or")[0])
	print(Values)
	print("------------------------------------")

	import pyodbc

	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb' 
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()

	temp=[]
	quest=[]
	for i in range(len(Values)):
  		temp.append('SYMPTOM'+str(i+1))
  		quest.append('?')

	temp.append('ID')
	quest.append('?')

	x = ",".join(temp)
	y = ",".join(quest)

	SQLCommand = ("INSERT INTO SURVEY ("+x+") VALUES ("+y+");")
	cursor = cnxn.cursor()	
	Values.append(5000)

	cursor.execute(SQLCommand,Values)
	cnxn.commit()

	return render_template('thankyou.html',symp = symp)


if __name__ == '__main__':
    app.run(debug=True)


