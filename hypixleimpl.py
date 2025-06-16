import requests, time

apiKey = "fdcee071-edf1-43f1-bd96-45aa9144634b"
mayorUrl = "https://api.hypixel.net/v2/resources/skyblock/election"

lastUpdated = 0
cachedData = None

def getMayorData():
    global lastUpdated, cachedData

    # get the mayor data from hypixle api
    response = requests.get(mayorUrl, headers={"API-Key": apiKey})
    responseFormatted = response.json()


    if responseFormatted["success"]:
        return responseFormatted
    else:
        print(f"Error: {responseFormatted['cause']} \n\n (probably invalid api key)")
    
        


