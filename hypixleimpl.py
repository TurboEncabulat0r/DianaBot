import requests

apiKey = "fdcee071-edf1-43f1-bd96-45aa9144634b"

class ApiFailure(Exception):
    pass

def getMayorData():
    url = "https://api.hypixel.net/v2/resources/skyblock/election"
    """
    {
        "success": true,
        "lastUpdated": 0,
        "mayor": {},
        "current": {}
    }
    """

    
    response = requests.get(url, headers={"API-Key": apiKey})
    responseFormatted = response.json()


    if responseFormatted["success"]:
        return responseFormatted
    else:
        raise ApiFailure()
    
        


