import requests
from pandas.io.json import json_normalize
import json
import csv
import time
import pandas as pd
import os

from django.shortcuts import render

def principal(request):
     context = {}
     return render(request, 'principal.html', context)

def resumen_usuario(request):

     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
     STATIC_FOLDER = THIS_FOLDER + "/static/"
     try:
          # Get the tokens from file to connect to Strava
          with open(STATIC_FOLDER + 'strava_tokens.json') as json_file:
               strava_tokens = json.load(json_file)
          print("terminé el try")
     except:
          print("entré al except")
          # Make Strava auth API call with your 
          # client_code, client_secret and code
          response = requests.post(
                              url = 'https://www.strava.com/oauth/token',
                              data = {
                                   'client_id': 63232,
                                   'client_secret': '042d93e39aa4abe4ea68fe237c6ac15bdca3261a',
                                   'code': '4ef1c6b0961c6de3bce26cb5fbf391de3856bdad',
                                   'grant_type': 'authorization_code'
                                   }
                         )
          #Save json response as a variable
          strava_tokens = response.json()
          # Save tokens to file
          with open(STATIC_FOLDER + 'strava_tokens.json', 'w') as outfile:
               json.dump(strava_tokens, outfile)

          # Get the tokens from file to connect to Strava
          with open(STATIC_FOLDER + 'strava_tokens.json') as json_file:
               strava_tokens = json.load(json_file)

     # If access_token has expired then 
     # use the refresh_token to get the new access_token
     if strava_tokens['expires_at'] < time.time():
          print("entré en el if")
          # Make Strava auth API call with current refresh token
          response = requests.post(
                                   url = 'https://www.strava.com/oauth/token',
                                   data = {
                                   'client_id': 63232,
                                   'client_secret': '042d93e39aa4abe4ea68fe237c6ac15bdca3261a',
                                   'grant_type': 'refresh_token',
                                   'refresh_token': strava_tokens['refresh_token']
                                   }
                                   )
          # Save response as json in new variable
          new_strava_tokens = response.json()
          # Save new tokens to file
          with open(STATIC_FOLDER + 'strava_tokens.json', 'w') as outfile:
               json.dump(new_strava_tokens, outfile)
          # Use new Strava tokens from now
          strava_tokens = new_strava_tokens
     else:
          print("no entré en el if")


     url = "https://www.strava.com/api/v3/activities"
     access_token = strava_tokens['access_token']

     # Create the dataframe ready for the API call to store your activity data
     activities = pd.DataFrame(
                              columns = [
                                        "id",
                                        "name",
                                        "start_date_local",
                                        "type",
                                        "distance",
                                        "moving_time",
                                        "elapsed_time",
                                        "total_elevation_gain",
                                        "end_latlng",
                                        "external_id"
                                        ]
                              )


     #OPTION: get 1 page with last 10 activities from Strava and filtering
     page = 1
     # get page of activities from Strava
     r = requests.get(url + '?access_token=' + access_token + '&per_page=10' + '&page=' + str(page)) #***pages***
     r = r.json()

     if(r):# if results in page 1
          for x in range(len(r)):
               activities.loc[x + (page-1)*10,'id'] = r[x]['id']
               activities.loc[x + (page-1)*10,'name'] = r[x]['name']
               activities.loc[x + (page-1)*10,'start_date_local'] = r[x]['start_date_local']
               activities.loc[x + (page-1)*10,'type'] = r[x]['type']
               activities.loc[x + (page-1)*10,'distance'] = r[x]['distance']
               activities.loc[x + (page-1)*10,'moving_time'] = r[x]['moving_time']
               activities.loc[x + (page-1)*10,'elapsed_time'] = r[x]['elapsed_time']
               activities.loc[x + (page-1)*10,'total_elevation_gain'] = r[x]['total_elevation_gain']
               activities.loc[x + (page-1)*10,'end_latlng'] = r[x]['end_latlng']
               activities.loc[x + (page-1)*10,'external_id'] = r[x]['external_id']

     # Export your activities file as a csv 
     # to the folder you're running this script in
     activities.to_csv(STATIC_FOLDER + 'strava_activities.csv')


     """
     #OPTION: getting all activities in pages of 200 entries drom Strava and filtering
     page = 1
     while True:
     
          # get page of activities from Strava
          r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page)) #***pages***
          r = r.json()

          # if no results then exit loop
          if (not r):
               break
          
          # otherwise add new data to dataframe
          for x in range(len(r)):
               activities.loc[x + (page-1)*200,'id'] = r[x]['id']
               activities.loc[x + (page-1)*200,'name'] = r[x]['name']
               activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
               activities.loc[x + (page-1)*200,'type'] = r[x]['type']
               activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
               activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
               activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
               activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
               activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
               activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']

          # increment page
          page += 1
     
     # Export your activities file as a csv 
     # to the folder you're running this script in
     activities.to_csv('strava_activities.csv')


     #OPTION: Get first page of activities from Strava with all fields
     r = requests.get(
          url + '?access_token=' + access_token,
          )
     r = r.json()
    
     df = json_normalize(r)
     df.to_csv('strava_activities_all_fields.csv')
     """
     
     context = {}
     return render(request, 'resumen-usuario.html', context)
