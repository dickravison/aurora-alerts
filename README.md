# aurora-alerts

This is used to send alerts if it's likely that the Aurora Borealis is able to be seen. This deploys the function to AWS Lambda and uses AWS Eventbridge to invoke the function once a day.

It uses the [AuroraWatch API](https://aurorawatch.lancs.ac.uk/) for measuring Aurora activity. It uses the [Open-Meteo API](https://open-meteo.com/) to determine if the weather conditions are ideal. It retrieves how cloudy it is and what time sunset is from this API.

Need to add some error handling to this still.