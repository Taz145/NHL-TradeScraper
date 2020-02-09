#! python3

import urllib.request
import re

url = "http://nhltradetracker.com/user/team_list"
re1 = re.compile(r'>[a-zA-Z ]+<\/a>')

teams = []

with urllib.request.urlopen(url) as data:
    html = data.read()

for names in re.findall(re1, html.decode()):
    names = names.replace('</a>', '')
    names = names.replace('>', '')
    names = names.replace(' ', '_')
    teams.append(names + '\n')

with open('teams.txt', 'w') as file:
    for n in teams:
        file.write(n)
