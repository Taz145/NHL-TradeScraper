import urllib.request
import re

# Regex to get the total number of pages
rePages = re.compile(r'>\d*</a>')
# Regex to get the team names involved in a trade
reTeams = re.compile(r'<strong>.+ acquire<\/strong>')
teamNames = []

# teams that no longer exist and will be skipped in counting trades
#TODO add filters for that this list IS used when valid years are given
defunct = {"Hamilton_Tigers", "Montreal_Maroons", "New York_Americans",
           "Philadelphia_Quakers", "Pittsburgh_Pirates", "Quebec_Bulldogs"}

# dict of teams that have changed ts to their current ts.
# Used to count trades properly
update = {'Atlanta_Flames': 'Calgary_Flames',
          'Atlanta_Thrashers': 'Winnipeg_Jets',
          'Cleveland_Barons': 'Dallas_Stars',
          'Colorado_Rockies': 'New_Jersey_Devils',
          'Detroit_Cougars': 'Detroit_Red_Wings',
          'Detroit_Falcons': 'Detroit_Red_Wings',
          'Hartford_Whalers': 'Carolina_Hurricanes',
          'Kansas_City_Scouts': 'New_Jersey_Devils',
          'Minnesota_North_Stars': 'Dallas_Stars',
          'Quebec_Nordiques': 'Colorado_Avalanche',
          'Toronto_Arenas': 'Toronto_Maple_Leafs'}

#urls for each specification of trade gathering
url = "http://nhltradetracker.com/user/trade_list_by_season/{}/{}"
team_url = "http://nhltradetracker.com/user/trade_list_by_season_team/{}/{}/{}"
all_team_url = "http://nhltradetracker.com/user/trade_list_by_team/{}}/1"

def get_team_names():
    t = []
    with open('teams.txt') as ts:
            for n in ts:
                n.strip()
                n = n.replace('\n', '')
                n = n.replace('\r', '')
                t.append(n)
    return t

#gets all the trades for the team and year specified
def get_team_trades(year, teamName):
    teamTrades = []
    for y in year:
        print("Getting trades for {} in {}".format(teamName, y))
        pages = get_num_pages(team_url.format(teamName, y, 1))
        if (pages == 0): pages = 1

        for i in range(1, pages + 1):
            with urllib.request.urlopen(team_url.format(teamName, y, i)) as data:
                html = data.read()

            for groups in re.findall(reTeams, html.decode()):
                line = re.sub(r'(acquire)|(<(\/)?strong>)', '', groups)
                line.strip()
                if (line not in defunct):

                    if line in update:
                        line = update[line]

                    teamTrades.append(line)
    if (teamTrades):
        if len(year) > 1:
            filename = 'Trades/' + teamName + ' ' + year[0] + '-' + year[len(year)-1] + '.csv'
        else:
            filename = 'Trades/' + teamName + ' ' + year[0] + '.csv'
        with open(filename, 'w') as f:
            for team in teamTrades:
                if team.strip().replace(' ', '_') != teamName.strip():
                    f.write(team + '\n')


#gets all the trades for the year specified
#output file is a csv with all tuples being the trading pairs
def get_year_trades(year):
    pages = get_num_pages(url.format(year, 1))
    trades = []
    print("Reading all trades from {}".format(year))
    for i in range(1, pages + 1):
        with urllib.request.urlopen(url.format(year, i)) as data:
            html = data.read()

        for groups in re.findall(reTeams, html.decode()):
            line = re.sub(r'(acquire)|(<(\/)?strong>)', '', groups)
            line.strip()
            if (line not in defunct):
                if line in update:
                    line = update[line]
                trades.append(line)
    with open('Trades/' + str(year) + '.csv', 'w') as f:
        for i in range(1, len(trades), 2):
            f.write(trades[i - 1] + ',' + trades[i] + '\n')

#gets the total number of pages the trades are listed on
def get_num_pages(url):
    pageMax = 0
    with urllib.request.urlopen(url) as data:
        html = data.read()

    for pages in re.findall(rePages, html.decode()):
        pages = re.sub(r'\D', '', pages)
        if pages != '':
            if pageMax < int(pages):
                pageMax = int(pages)
    return pageMax
