import requests
import os
import pandas as pd
from datetime import datetime
import bs4
import json
import boto3

#AURORA API
AURORA_API_URL = "http://aurorawatch-api.lancs.ac.uk/0.2.5/status/project/awn/sum-activity.xml"

#WEATHER API
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_API_PARAMS = {
	"latitude": os.environ['WEATHER_API_LAT'],
	"longitude": os.environ['WEATHER_API_LON'],
	"hourly": "cloud_cover",
	"daily": "sunset",
	"timezone": "Europe/London",
	"forecast_days": 1
}

#ALERTS
SNS_TOPIC = os.environ['SNS_TOPIC']
NOTIFICATIONS_ENABLED = os.environ['NOTIFICATIONS_ENABLED']
SNS_CLIENT = boto3.client('sns')
ALERT_ON_HIGH_ACTIVITY = False
ALERT_ON_BAD_CONDITIONS = False
ALERT_ON_PRE_SUNSET = False

# #THRESHOLDS
AURORA_ACTIVITY_THRESHOLD = int(os.environ['AURORA_ACTIVITY_THRESHOLD'])
CLOUDS_THRESHOLD = int(os.environ['CLOUD_THRESHOLD'])

def publish(message):
    SNS_CLIENT.publish(
        TopicArn = os.environ['SNS_TOPIC'],
        Subject = "Aurora Alert",
        Message = message
    )
    print(message)

#Get hourly forecast and sunset time
def get_visibility():
    response = requests.get(WEATHER_API_URL, params=WEATHER_API_PARAMS).content
    data = json.loads(response)
    df = pd.DataFrame(data['hourly'])

    sunset = ''.join(data['daily']['sunset'])
    sunset = datetime.strptime(sunset, '%Y-%m-%dT%H:%M').strftime('%H:%M')
    return df, sunset

def main(event, context):
    # Get cloudiness and sunset time
    clouds_df, sunset = get_visibility()

    #Get aurora activity data
    response = requests.get(AURORA_API_URL)
    activity_xml = bs4.BeautifulSoup(response.text, "xml")
    activity_bs = activity_xml.find_all('activity')

    now = datetime.today()
    prev_hour = datetime.strftime(now.replace(second=0, microsecond=0, minute=0), '%Y-%m-%dT%H:%M:%S%z')
    message = ""

    #Loop over each activity and add any times that have aurora activity higher than the threshold to the relevant arrays dependent on the visibility conditions.
    for activity in activity_bs:
        period = activity.find('datetime').get_text()
        print(period)
        if period > prev_hour:
            value = activity.find('value').get_text()
            period = datetime.strptime(period, '%Y-%m-%dT%H:%M:%S%z')
            period = period.strftime('%H:%M')
            cloud_cover = clouds_df[clouds_df['time'].str.contains(period)]['cloud_cover'].values[0]
            if float(value) > AURORA_ACTIVITY_THRESHOLD and sunset < period and int(cloud_cover) < CLOUDS_THRESHOLD:
                message = message + "The chance of seeing the aurora is high."
            elif float(value) > AURORA_ACTIVITY_THRESHOLD and sunset > period and ALERT_ON_PRE_SUNSET:
                message = message + "Aurora activity is high but the sun has not set yet."
            elif float(value) > AURORA_ACTIVITY_THRESHOLD and int(cloud_cover) > CLOUDS_THRESHOLD and ALERT_ON_BAD_CONDITIONS:
                message = message + "Aurora activity is high but it is quite cloudy so the chances of seeing the aurora are low"
        
    if message == "":
        message = "No chance of seeing Aurora"
    elif message != "" and NOTIFICATIONS_ENABLED == "true":
        publish(message)
    else:
        print(message)