import urllib.request
import re

rePages = re.compile(r'>\d*</a>')
reTeams = re.compile(r'<strong>.+ acquire<\/strong>')
teamNames = []

with open('teams.txt') as ts:
        for n in ts:
            n.strip()
            n = n.replace('\n', '')
            n = n.replace('\r', '')
            teamNames.append(n)

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

#gets all the trades for the team and year specified
#if no team is specified, all trades for all teams will be gathered in the specified year
#if no year is specified, all trades from 2000 onward will be gathered for the specified team
#if no year AND no team is specifed, all trades for all teams from 2000 onward will be gathered
def get_team_trades(year = None, teamName = None):
    teams = []
    years = []
    teamTrades = []
    if (teamName == None):
        for i in set(teamNames).difference(defunct):
            teams.append(i.strip())
    else:
        teams.append(teamName.strip().replace(' ', '_'))
    
    if (year == None):
        for i in range(2000, 2020):
            years.append(str(i) + "-" + str(i+1))
    else:
        years.append(year)
    for y in years:
        for t in teams:

            pages = get_num_pages(team_url.format(t, y, 1))
            if (pages == 0): pages = 1

            for i in range(1, pages + 1):
                with urllib.request.urlopen(team_url.format(t, y, i)) as data:
                    html = data.read()

                for groups in re.findall(reTeams, html.decode()):
                    line = re.sub(r'(acquire)|(<(\/)?strong>)', '', groups)
                    line.strip()
                    if (line not in defunct):

                        if line in update:
                            line = update[line]

                        teamTrades.append(line)
            if (teamTrades):
                with open('Trades/' + t + ' ' + str(y) + '.csv', 'w') as f:
                    print("Reading {} for {}\n".format(t,y))
                    for team in teamTrades:
                        if team.strip().replace(' ', '_') != t.strip():
                            f.write(team + '\n')
            teamTrades[:] = [] # empties the trade list for the next loop

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

def menu():
    print("Please select an option:")
    print("1: 1 year")
    print("2: Range of years")
    print("3: Team Menu")

if __name__ == "__main__":
    
    # menu()
    # get_year_trades("2018-19")
    # get_team_trades("2018-19")
    get_team_trades(None, "Toronto Maples Leafs")
