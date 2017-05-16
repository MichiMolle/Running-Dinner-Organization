# Running-Dinner-Organization
A couple of python-scripts that help with the organization of a running-dinner. It consists of 3 seperate scripts, which all read from or write to a csv-file containing the relevant information about the dinner's participants.

## participant-coords.py
Needs to be run before dinner-magic.py and send-mails.py. The script determines the longitude and latitude of a the participants adress which is later needed to display it on a map. For this script to work you need to obtain a Key for the google-maps API. To get that follow this link:

The obtained coordinates will be added to the ***participants.csv***-file.

## dinner-magic.py
The second script helps planning individual routes for a dinner by showing all adresses on a google-map, with courses as well as vegetarian/vegan diet teams indicated by color or symbols.

The script takes the needed information from the ***participants.csv*** and creates a ***map.html*** in the root directory.

## send-mails.py
The third script reads from ***participants.csv*** and sends automated emails to your participants containing all relevant information about their dinner experience (which course do they have, where will they be for which course, do their guests have allergies or special diets).
