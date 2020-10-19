# -*- coding: utf-8 -*-
"""ratingMoodleSurvey.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kcnslms_4DgyII_3yf9akgyHIWJX_Aig
"""

!pip install wit
!pip install df2gspread

class Reader:

  def readSheet(self):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import pandas as pd
    import requests
    WIT_ACCESS_TOKEN = 'ICX6YP2D6NJV3VKIFF56ZGTQ4PW53TRN'
    from wit import Wit
    cliente = Wit(access_token=WIT_ACCESS_TOKEN)

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cliente_secret.json', scope)
    client = gspread.authorize(creds)
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("SP1encuesta").sheet1
    # Extract and print all of the values
    opinion = sheet.col_values(24)
    course = sheet.col_values(2)

    data = pd.DataFrame([])
    for i in range(1,len(opinion)):
      message = opinion[i]
      resp = cliente.message(message)
      if resp['traits'] != {}:
       data = data.append(pd.DataFrame({'Curso': course[i],'Valor': str(resp['traits']['sentiment'][0]['confidence']),'Clase':str(resp['traits']['sentiment'][0]['value'])}, index=[0]), ignore_index=True)
      #ver el codigo de abajo sirve para ajustar el training de NLP de Wit.ai
      #else:
        #print (str(resp))
    return data

class Writer:

  def writeSheet(self,data):
    import gspread
    from df2gspread import df2gspread as d2g
    from oauth2client.service_account import ServiceAccountCredentials
    import pandas as pd

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cliente_secret.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_key = '1-dmyQYJDvYmKHk3wLo7n_2116XDQIQya16jrC77d9U0'
    wks_name = 'ratings'
    d2g.upload(data, spreadsheet_key, wks_name, credentials=creds, row_names=True, clean=True)

values = Reader()
courseRate = Writer()
val = values.readSheet()
courseRate.writeSheet(val)