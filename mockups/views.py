import requests
from pandas.io.json import json_normalize
import json
import csv
import time
import pandas as pd
import os

from datetime import timedelta

from django.shortcuts import render, redirect
from .models import Usuario
import re


def principal(request):
     todos_usuarios = Usuario.objects.all()
     usuario1 = todos_usuarios[0]
     usuario1.id_strava = None
     usuario1.save()
     request.session['code_strava'] = ""

     uri = request.get_full_path()
     print(uri)
     m = re.search('code=(.+?)&', uri)
     if m:
          code = m.group(1)
          request.session['code_strava'] = code
          print(code)
     if not request.session['code_strava'] == "":
          return redirect('resumen-usuario-strava')

     context = {}
     return render(request, 'principal.html', context)


def resumen_usuario_strava(request):

     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
     STATIC_FOLDER = THIS_FOLDER + "/static/"

     todos_usuarios = Usuario.objects.all()
     usuario1 = todos_usuarios[0]

     if not usuario1.id_strava:#user has no id_strava

          if not request.session['code_strava'] == "":#i already ask for code!

               code_from_oauth = request.session['code_strava']
               #exchange user code for user tokens
               # Make Strava auth API call with your
               # client_code, client_secret and code
               response = requests.post(
                                   url = 'https://www.strava.com/oauth/token',
                                   data = {
                                        'client_id': 63232,
                                        'client_secret': '042d93e39aa4abe4ea68fe237c6ac15bdca3261a',
                                        'code': code_from_oauth,
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

               #get id_strava from tokens
               usuario1.id_strava = strava_tokens['athlete'].get('id')
               #save id in database
               usuario1.save()

          else:#otherwhise i should ask for it
               return redirect('https://www.strava.com/oauth/authorize?client_id=63232&response_type=code&redirect_uri=http://desarrolloqueridoapp.pythonanywhere.com&approval_prompt=force&scope=profile:read_all,activity:read_all')

     else:#user has id_strava

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

     url = 'https://www.strava.com/api/v3/athletes/'+ str(usuario1.id_strava) +'/activities' #put athlete id
     access_token = strava_tokens['access_token']

     # Create the dataframe ready for the API call to store your activity data
     activities = pd.DataFrame(
                              columns = [
                                        "name",
                                        "start_date_local",
                                        "type",
                                        "distance",
                                        "moving_time",
                                        "elapsed_time",
                                        "total_elevation_gain"
                                        ]
                              )

     #get 1 page with last 5 activities from Strava and filtering
     page = 1
     # get page of activities from Strava
     r = requests.get(url + '?access_token=' + access_token + '&per_page=5' + '&page=' + str(page)) #***pages***
     r = r.json()

     if(r):# if results in page 1
          for x in range(len(r)):
               activities.loc[x + (page-1)*5,'name'] = r[x]['name']
               activities.loc[x + (page-1)*5,'start_date_local'] = r[x]['start_date_local']
               activities.loc[x + (page-1)*5,'type'] = r[x]['type']
               activities.loc[x + (page-1)*5,'distance'] = r[x]['distance']
               activities.loc[x + (page-1)*5,'moving_time'] = r[x]['moving_time']
               activities.loc[x + (page-1)*5,'elapsed_time'] = r[x]['elapsed_time']
               activities.loc[x + (page-1)*5,'total_elevation_gain'] = r[x]['total_elevation_gain']

     # Export your activities file as a csv
     # to the folder you're running this script in
     activities.to_csv(STATIC_FOLDER + 'strava_activities.csv')

     #cleanning the data to display it on html table
     for ind in activities.index:
          #convert distance from m to km
          dist_frame = activities.loc[activities.index == ind, ['distance']]
          dist_val = dist_frame.at[ind, 'distance']
          activities.loc[activities.index == ind, ['distance']] = round(dist_val/1000, 2)

          #convert time from secs to hours:min
          mov_time_frame = activities.loc[activities.index == ind, ['moving_time']]
          mov_time_val = mov_time_frame.at[ind, 'moving_time']
          mov_time_val = mov_time_val/60
          str_mtv = str(timedelta(minutes=mov_time_val))[:-3]
          activities.loc[activities.index == ind, ['moving_time']] = str_mtv

          #convert time from secs to hours:min
          ela_time_frame = activities.loc[activities.index == ind, ['elapsed_time']]
          ela_time_val = ela_time_frame.at[ind, 'elapsed_time']
          ela_time_val = ela_time_val/60
          str_etv = str(timedelta(minutes=ela_time_val))[:-3]
          activities.loc[activities.index == ind, ['elapsed_time']] = str_etv

     #removing index
     cleanned_data = []
     for act in activities.to_records():
          new_act = list(act)
          new_act.pop(0)
          cleanned_data.append(new_act)

     context = {}
     context['strava_data'] = cleanned_data
     return render(request, 'resumen-usuario.html', context)

def resumen_usuario(request):

     THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
     STATIC_FOLDER = THIS_FOLDER + "/static/"
    
     # read csv only for test
     activities = pd.read_csv(STATIC_FOLDER + 'strava_activities_for_test.csv')

     #cleanning the data to display it on html table
     for ind in activities.index:
          #convert distance from m to km
          dist_frame = activities.loc[activities.index == ind, ['distance']]
          dist_val = dist_frame.at[ind, 'distance']
          activities.loc[activities.index == ind, ['distance']] = round(dist_val/1000, 2)

          #convert time from secs to hours:min
          mov_time_frame = activities.loc[activities.index == ind, ['moving_time']]
          mov_time_val = mov_time_frame.at[ind, 'moving_time']
          mov_time_val = mov_time_val/60
          str_mtv = str(timedelta(minutes=mov_time_val))[:-3]
          activities.loc[activities.index == ind, ['moving_time']] = str_mtv

          #convert time from secs to hours:min
          ela_time_frame = activities.loc[activities.index == ind, ['elapsed_time']]
          ela_time_val = ela_time_frame.at[ind, 'elapsed_time']
          ela_time_val = ela_time_val/60
          str_etv = str(timedelta(minutes=ela_time_val))[:-3]
          activities.loc[activities.index == ind, ['elapsed_time']] = str_etv

     #removing index
     cleanned_data = []
     for act in activities.to_records():
          new_act = list(act)
          new_act.pop(0)
          cleanned_data.append(new_act)

     context = {}
     context['strava_data'] = cleanned_data
     return render(request, 'resumen-usuario.html', context)
