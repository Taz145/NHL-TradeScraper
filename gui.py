from trade_scraper import *
import _tkinter
from tkinter import *
from tkinter import ttk


root = Tk()
year_val = IntVar(root)
team_val = StringVar(root)

def close_window():
    root.destroy()

def get_trades():
    y = str(year_val.get()) + '-' + str(((year_val.get())%100+1)).zfill(2)
    get_team_trades(y, team_val.get())

def main_setup():
    teamNames = []
    with open('teams.txt') as ts:
        for n in ts:
            n.strip()
            n = n.replace('\n', '')
            n = n.replace('\r', '')
            teamNames.append(n)

    # root = Tk()
    root.title("NHL Trade Scraper")


    year_menu_options = []
    for i in range(2000,2021):
        year_menu_options.append(i)

    
    year_val.set(year_menu_options[0])

    year_menu = OptionMenu(root, year_val, *year_menu_options)
    year_menu.pack()


    team_val.set(teamNames[0])

    team_menu = OptionMenu(root, team_val, *teamNames)
    team_menu.pack()

    scrape_button = Button(root, text="Get Trades!", command=get_trades)
    scrape_button.pack()

    exit_button = Button(root, text = "Quit", command=close_window)
    exit_button.pack()
    # team_name = StringVar()
    root.mainloop()

if __name__ == "__main__":
    main_setup()