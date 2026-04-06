##Code for Daniel Neau's Honors Thesis: 
##The Correlation of Public Transit Time and Voting Turnout; A Study in Worcester, Massachusetts and Baton Rouge, Louisiana
##Clark University Graduate School of Geography, School of Climate Enviorment and Society
##Defended on April 6th, 2026

##Import nescisary repositories
import googlemaps
import pandas as pd
from datetime import datetime
import pytz
import calendar
import os
import re

##Set timezones for Worcester and Baton Rouge, and set the arrival time to the polls time to be July 29th 2025 at 7:59 am
eastern = pytz.timezone('US/Eastern')
central = pytz.timezone('US/Central')
arrival_worcester = eastern.localize(datetime(2025, 7, 29, 19, 59 ))
worcester_timestapmp = calendar.timegm(arrival_worcester.astimezone(pytz.utc).timetuple())
arrival_br = central.localize(datetime(2025, 7, 29, 19, 59))
br_timestapmp = calendar.timegm(arrival_br.astimezone(pytz.utc).timetuple())

##Need to use a Google Maps API key for this code to run replace "Akey" with your API Key
gmaps=googlemaps.Client(key="Akey")

##Calculate travel time by public transit from the centroid to the precinct's plling place in Worcester, recording the number of miles traveled, time traveled (in both seconds and minutes with seconds), as well as if the transit mode is walking or tranist
##If no route found will print a warning and put 'no route' in the modes column
worcester = pd.read_csv("WCentroids.csv")
wpolling = pd.read_csv("PollingPlaces.csv")
worcester['LatLon'] = worcester['Lat'].astype(str) + ',' + worcester['Lon'].astype(str)
worcester['Meters'] = None
worcester['Miles'] = None
worcester['Seconds'] = None
worcester['TravelDistance'] = None
worcester['TravelTime'] = None
worcester['Mode'] = None
for idx in worcester.index:
    o = worcester.loc[idx,'LatLon']
    des = wpolling.loc[idx, 'ADRESS']
    try:
        direction = gmaps.directions(o, des, mode="transit", arrival_time=worcester_timestapmp)
        if direction:
            element = direction[0]['legs'][0]
            dMiles = element['distance']['value']/1609.344
            textMiles = f"{round(dMiles,3)} mi"
            seconds = element['duration']['value']
            duration = element['duration']['text']
            modes = []
            for step in element['steps']:
                mode = step['travel_mode'].lower()
                modes.append(mode)
            worcester.loc[idx, 'Miles'] = dMiles
            worcester.loc[idx, 'Seconds'] = seconds
            worcester.loc[idx, 'TravelDistance'] = textMiles
            worcester.loc[idx, 'TravelTime'] = duration
            worcester.loc[idx, 'Mode'] = ", ".join(modes)
        else:
            print(f"Warning at row {idx}: no directions found.")
            worcester.loc[idx, 'modes'] = 'no route'
    except Exception as e:
        print(f"Error at row {idx}: {e}")
os.makedirs(os.path.dirname('results/Worcesteroutput.csv'), exist_ok=True)
worcester.to_csv('results/Worcesteroutput.csv', index=False)

##Calculate travel time by public transit from the centroid to the precinct's plling place in Baton Rouge, recording the number of miles traveled, time traveled (in both seconds and minutes with seconds), as well as if the transit mode is walking or tranist
##If no route found will print a warning and put 'no route' in the modes column
br = pd.read_csv("BRCentroid")
brP = pd.read_csv("BRCCentroid")
br['LatLon'] = br['Lat'].astype(str) + ',' + br['Lon'].astype(str)
br['Meters'] = None
br['Miles'] = None
br['Seconds'] = None
br['TravelDistance'] = None
br['TravelTime'] = None
br['Direct'] = None
br['Mode'] = None
for idx in br.index:
    o = br.loc[idx,'LatLon']
    des = brP.loc[idx, 'ADRESS']
    try:
        direction = gmaps.directions(o, des, mode="transit", arrival_time=br_timestapmp)
        if direction:
            element = direction[0]['legs'][0]
            dMiles = element['distance']['value']/1609.344
            textMiles = f"{round(dMiles,3)} mi"
            seconds = element['duration']['value']
            duration = element['duration']['text']
            modes = []
            for step in element['steps']:
                mode = step['travel_mode'].lower()
                modes.append(mode)
            br.loc[idx, 'Miles'] = dMiles
            br.loc[idx, 'Seconds'] = seconds
            br.loc[idx, 'TravelDistance'] = textMiles
            br.loc[idx, 'TravelTime'] = duration
            br.loc[idx, 'Mode'] = ", ".join(modes)
        else:
            print(f"Warning at row {idx}: no directions found.")
            br.loc[idx, 'modes'] = 'no route'
    except Exception as e:
        print(f"Error at row {idx}: {e}")
os.makedirs(os.path.dirname('results/Worcesteroutput.csv'), exist_ok=True)
br.to_csv('results/BRoutput.csv', index=False)