# import required libraries
import requests
from collections import defaultdict
import datetime



payload = ""
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}



# Enter State and District Name
stateName = input("Enter State Name: ").lower()
districtName = input("Enter District Name: ").lower()

# try catch to caught the error occured by apis
try:
    # Get id of current state by api
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    responseStates = requests.request("GET", url, headers=headers, data=payload)
    states = responseStates.json()



    state = dict()
    for ind in states['states']:
        state[ind['state_name'].lower()] = ind['state_id']

    # print invalid state name, if state name is not in the state list
    if stateName not in state:
        print("Invalid State Name: ")
        print("Exiting....")
        exit()


    # Get District for given states by api
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(state[stateName])

    responseDist = requests.request("GET", url, headers=headers, data=payload)

    dists = responseDist.json()

    dist = dict()
    for ind in dists['districts']:
        dist[ind['district_name'].lower()] = ind['district_id']

    # print invalid district name, if district name not in the district list of states
    if districtName not in dist:
            print("Invalid District Name: ")
            print("Exiting....")
            exit()
    districtId = dist[districtName]

    # Enter Minimum age
    minmAge = int(input("Enter Minimum Age (18/45) :"))

    while minmAge not in [18,45]:
        print("Invalid Minimum Age ")
        print("Please Try Again ")
        minmAge = int(input("Enter Minimum Age (18/45) :"))


    # Get Availability for next 15 days
    currDate = datetime.datetime.today() # datetime.timedelta(days=1)
    for i in range(15):
        currDate += datetime.timedelta(days=1)
        
        dateStr = currDate.strftime('%d-%m-%Y')

        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+str(districtId)+"&date="+dateStr


        response = requests.request("GET", url, headers=headers, data=payload)

        medicals = response.json()

        length  = len(medicals['sessions'])
        data = medicals['sessions']
        
        print(dateStr)
        print("===========================")
        flag = True
        for i in range(length):
            curr = data[i]
            if curr['min_age_limit'] == minmAge and curr['available_capacity'] > 0:
                flag = False
                print("-> ",curr['name'],",",curr['block_name'],"Vaccine:",curr['vaccine'],"      Available**: ",curr['available_capacity'])
        if flag:
            print("Sorry😢! No vaccine available")
            print()
except:
  print("Sorry! Cowin public API is not working currently. Try Again Later")





