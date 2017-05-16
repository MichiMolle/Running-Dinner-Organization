import csv
import requests
import copy
import time

class Person:
    def __init__(self, person_id, first_name, last_name, email, eating, allergies):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.eating = eating
        self.allergies = allergies
        
class Team:
    def __init__(self, team_id, adress, appetizer_id, main_course_id, dessert_id, latitude, longitude):
        self.team_id = team_id
        self.adress = adress
        self.appetizer_id = appetizer_id
        self.main_course_id = main_course_id
        self.dessert_id = dessert_id
        self.latitude = latitude
        self.longitude = longitude 
        self.eating = "normal"
        self.course = ""
        self.members = []
        self.guests = []
        
    def add_member(self, member):
        self.members.append(member)
    
    def add_guests(self, guests):
        self.guests.append(guests)

teams = []

def team_id_exists(id):
    team_exists = False
    for team in teams:
        if(team.team_id == id):
            team_exists = True
    return team_exists
    
def get_team_by_id(id):
    for team in teams:
        if(int(team.team_id) == int(id)):
            t = team
            break
        else:
            t = None
    return t

with open('participants.csv') as dinnerfile:
    filereader= csv.reader(dinnerfile, delimiter=',')
    
    test = 0
    firstline = True
    for row in filereader:
        if(firstline == True):
            firstline = False
        else:
            if(team_id_exists(int(row[1])) == False):
                if(row[13] == ''):
                    row[13] = 0
                if(row[14] == ''):
                    row[14] = 0
                if(row[15] == ''):
                    row[15] = 0
                t1 = Team(int(row[1]),row[8],row[13],row[14],row[15],row[16],row[17])
                teams.append(t1)
                person = Person(row[0],row[2],row[3],row[4],row[9],row[12])
                if(row[9] == "Vegetarisch" or row[9] == "Vegan"):
                    t1.eating = row[9]
                t1.add_member(person)
            else:
                t1 = get_team_by_id(int(row[1]))
                person = Person(row[0],row[2],row[3],row[4],row[9],row[12])
                if(row[9] == "Vegetarisch" or row[9] == "Vegan"):
                    if(t1.eating != "Vegan"):
                        t1.eating = row[9]
                t1.add_member(person)


teamo = copy.deepcopy(teams)
    
for team in teamo:
    if(int(team.team_id) != int(team.appetizer_id) and team.appetizer_id != 0):
            t = get_team_by_id(int(team.appetizer_id))
            t.add_guests(team.team_id)
    if(int(team.team_id) != int(team.main_course_id) and team.main_course_id != 0):
            t = get_team_by_id(team.main_course_id)
            t.add_guests(team.team_id)
    if(int(team.team_id) != int(team.dessert_id) and team.dessert_id != 0):
            t = get_team_by_id(int(team.dessert_id))
            t.add_guests(team.team_id)

javascript = ""
for team in teams:
    img_file = ""
    if(int(team.team_id) == int(team.appetizer_id)):
        img_file = "vorspeise.png"
        team.course = "Vorspeise"
    elif(int(team.team_id) == int(team.main_course_id)):
        img_file = "hauptgang.png"
        team.course = "Hauptgang"
    elif(int(team.team_id) == int(team.dessert_id)):
        img_file = "nachspeise.png"
        team.course = "Nachspeise"
    else:
        img_file = "keingang.png"
        
    if(team.eating == "normal"):
        img_path = "omni"
    elif(team.eating == "Vegetarisch"):
        img_path = "vegie"
    else:
        img_path = "vegan"
        
    team_name = ""
    for member in team.members:
        if(team_name == ""):
            team_name = member.last_name + " & "
        else:
            team_name = team_name + member.last_name
        print(team_name)
    
    ap_team = get_team_by_id(int(team.appetizer_id))
    if(ap_team!=None):
        vorspeise = str(team.appetizer_id)
        if(ap_team.guests!=None):
            for guest in ap_team.guests:
                vorspeise = vorspeise + ", (" + str(guest) + ")" 
    
    mc_team = get_team_by_id(int(team.main_course_id))
    if(mc_team!=None):
        hauptgang = str(team.main_course_id)
        if(ap_team.guests!=None):
            for guest in mc_team.guests:
                hauptgang = hauptgang + ", (" + str(guest) + ")" 
        
    d_team = get_team_by_id(int(team.dessert_id))
    if(d_team!=None):
        dessert = str(team.dessert_id)
        if(ap_team.guests!=None):
            for guest in d_team.guests:
                dessert = dessert + ", (" + str(guest) + ")" 
        
    if(team.course == "Vorspeise" and team.guests!=None):
        for guest in team.guests:
            team.appetizer_id = team.appetizer_id + "," + str(guest)
    if(team.course == "Hauptgang" and team.guests!=None):
        for guest in team.guests:
            team.main_course_id = team.main_course_id + "," + str(guest)
    if(team.course == "Nachspeise" and team.guests!=None):
        for guest in team.guests:
            team.dessert_id = team.dessert_id + "," + str(guest)
    
    img = "'res/img/"+img_path+"/"+img_file+"'"
    
    script = "var marker = new google.maps.Marker({position: {lat:"+str(team.latitude)+", lng:"+str(team.longitude)+"}, \nmap: map,\nlabel: '"+str(team.team_id)+"',\nicon: "+img+", \ntitle: 'Team: "+team_name+"\\nVorspeise:"+vorspeise+"\\nHauptgang:"+hauptgang+"\\nNachspeise:"+dessert+"'\n});\n"
    javascript = javascript + script
    
templatefile = open('res/template.html','r')
htmltext = templatefile.read()

htmltext = htmltext.replace("#MARKERS#", javascript)
htmlfile = open("dinner.html",'w') 
htmlfile.write(htmltext)
htmlfile.close()

