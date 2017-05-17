def send_email(recipient, subject, body):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    fromaddr = "fromadress"
    toaddr = recipient
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    import smtplib
    server = smtplib.SMTP('server', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("mailadress", "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("done")

import csv
import copy

templatefile = open('res/mail-template.txt','r')
templatetext = templatefile.read()

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
        self.eating = "Alles"
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
                if(row[12] == ''):
                    row[12] = 0
                if(row[13] == ''):
                    row[13] = 0
                if(row[14] == ''):
                    row[14] = 0
                t1 = Team(int(row[1]),row[7],row[12],row[13],row[14],row[15],row[16])
                teams.append(t1)
                person = Person(row[0],row[2],row[3],row[4],row[8],row[11])
                if(row[8] == "Vegetarisch" or row[8] == "Vegan"):
                    t1.eating = row[8]
                t1.add_member(person)
            else:
                t1 = get_team_by_id(int(row[1]))
                person = Person(row[0],row[2],row[3],row[4],row[8],row[11])
                if(row[8] == "Vegetarisch" or row[8] == "Vegan"):
                    if(t1.eating != "Vegan"):
                        t1.eating = row[8]
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

for team in teams:
    if(int(team.team_id) == int(team.appetizer_id)):
        team.course = "Vorspeise"
    elif(int(team.team_id) == int(team.main_course_id)):
        team.course = "Hauptgang"
    elif(int(team.team_id) == int(team.dessert_id)):
        team.course = "Nachspeise"
        
    team_name = ""
    for member in team.members:
        if(team_name == ""):
            team_name = member.last_name + " & "
        else:
            team_name = team_name + member.last_name
    
    ap_team = get_team_by_id(int(team.appetizer_id))
    vorspeise = str(team.appetizer_id)
    for guest in ap_team.guests:
        vorspeise = vorspeise + ", (" + str(guest) + ")" 
    
    mc_team = get_team_by_id(int(team.main_course_id))
    hauptgang = str(team.main_course_id)
    for guest in mc_team.guests:
        hauptgang = hauptgang + ", (" + str(guest) + ")" 
        
    d_team = get_team_by_id(int(team.dessert_id))
    dessert = str(team.dessert_id)
    for guest in d_team.guests:
        dessert = dessert + ", (" + str(guest) + ")" 
        
teama = copy.deepcopy(teams)

for team in teama:    
    
    vegancount = 0
    vegiecount = 0
    allergies = "Allergien: "
    eatingstyle = "Essgewohnheiten: "
    
    for guest in team.guests:
        t = get_team_by_id(int(guest))
        for t_member in t.members:
            if(t_member.allergies != "none"):
                allergies = allergies + '"'+  t_member.allergies + '"'
            if(t_member.eating == "Vegan"):
                vegancount = vegancount + 1
            elif(t_member.eating == "Vegetarisch"):
                vegiecount = vegiecount + 1
        
    if(vegiecount != 0):
        eatingstyle = eatingstyle + str(vegiecount) + "x Vegetarisch "
    if(vegancount != 0):
        eatingstyle = eatingstyle + str(vegancount) + "x Vegan "
    if(vegiecount == 0 and vegancount == 0):
        eatingstyle = eatingstyle + "Keine Besonderheiten"
        
    if(allergies == "Allergien: "):
        allergies = allergies + "Keine Allergien"
            
    if(int(team.appetizer_id) != int(team.team_id)):
        a_team = get_team_by_id(int(team.appetizer_id))
        a_team_name = a_team.members[0].first_name + " " + a_team.members[0].last_name + " & " + a_team.members[1].first_name + " " + a_team.members[1].last_name
    else:
        a_team = copy.deepcopy(team)
        a_team_name = "euch"
    
    if(int(team.team_id) != int(team.main_course_id)):
        mc_team = get_team_by_id(int(team.main_course_id))   
        mc_team_name = mc_team.members[0].first_name + " " + mc_team.members[0].last_name + " & " + mc_team.members[1].first_name + " " + mc_team.members[1].last_name
    else:
        mc_team = copy.deepcopy(team)
        mc_team_name = "euch"
    
    if(int(team.team_id) != int(team.dessert_id)):
        d_team = get_team_by_id(int(team.dessert_id))   
        d_team_name = d_team.members[0].first_name + " " + d_team.members[0].last_name + " & " + d_team.members[1].first_name + " " + d_team.members[1].last_name
    else:
        d_team = copy.deepcopy(team)
        d_team_name = "euch"
        

    
    member_index = 0
    for member in team.members:
        text = templatetext.replace("#VORNAME#", member.first_name)
        
        if(member_index == 0):
            partner = team.members[1].first_name + " " + team.members[1].last_name + " (" + team.members[1].email+")"
            member_index = 1
        else:
            partner = team.members[0].first_name + " " + team.members[0].last_name + " (" + team.members[0].email+")"

        
        text = text.replace("#PARTNER#", partner)
        text = text.replace("#VORSPEISENAME#", a_team_name)
        text = text.replace("#VORSPEISEADRESSE#", a_team.adress)
        text = text.replace("#HAUPTGANGNAME#", mc_team_name)
        text = text.replace("#HAUPTGANGADRESSE#", mc_team.adress)
        text = text.replace("#DESSERTNAME#", d_team_name)
        text = text.replace("#DESSERTADRESSE#", d_team.adress)
        text = text.replace("#ESSGEWOHNHEITEN#", eatingstyle)
        text = text.replace("#ALLERGIEN#", allergies)
        
        
        send_email(member.email, "", text)