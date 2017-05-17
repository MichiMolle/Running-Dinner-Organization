import requests
import csv

lines = []

api_key = ""

with open('participants.csv') as dinnerfile:
    filereader= csv.reader(dinnerfile, delimiter=',')

    firstline = True
    for row in filereader:
        if(firstline == True):
            firstline = False
        else:
         response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+str(row[7])+'+Bamberg&key='+api_key)

         response = response.json()
         longitude = response['results'][0]['geometry']['location']['lng']
         latitude = response['results'][0]['geometry']['location']['lat']
            
         print(str(latitude) + ","+str(longitude))
         row.extend([str(latitude),str(longitude),"\n"])
         lines.append(row)

with open('participants.csv', 'w') as file:
    file.write('Person-ID,Team-ID,Vorname,Nachname,Email,Kochpartner,Kochpartner-ID,Adresse,Essgewohnheiten,Bachelor in Bamberg,Beginn Master,Allergien,Vorspeise-ID,Hauptgang-ID,Nachspeise-ID,LAT,LNG\n')
    for line in lines:
        file.write(",".join(line))
        


