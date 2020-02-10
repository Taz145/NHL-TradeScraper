from trade_scraper import *
import _tkinter
from tkinter import *
from tkinter import ttk

class scraperMenu:

    root = Tk()
    year_val1 = IntVar()
    year_val2 = IntVar()
    team_val = StringVar()
    range_option = IntVar()

    range_option = IntVar()

    year_menu_options = []
    team_menu_options = get_team_names()

    year_menu1 = None
    year_menu2 = None
    range_button = None
    team_menu = None
    scrape_button = None
    exit_buton = None

    def get_trades(self):
        y = []
        if (self.range_option.get() == 0):
            y.append(str(self.year_val1.get()) + '-' + str((self.year_val1.get()%100) + 1).zfill(2))
        else:
            for i in range (self.year_val1.get(), self.year_val2.get()):
                y.append( str(i) + '-' + str((i %100) + 1).zfill(2))
        get_team_trades(y, self.team_val.get())

    def toggle_range(self):
        if (self.range_option.get() == 0):
            self.year_menu2.configure(state = "disabled")
        else:
            self.year_menu2.configure(state = "normal")
    
    def close_window(self):
        self.root.destroy()
    
    def __init__(self):

        for i in range(2000,2021):
            self.year_menu_options.append(i)
        
        self.root.title("NHL Trade Scraper")
        self.year_val1.set(self.year_menu_options[0])
        self.year_val2.set(self.year_menu_options[0])

        self.year_menu1 = OptionMenu(self.root, self.year_val1, *self.year_menu_options)
        self.year_menu2 = OptionMenu(self.root, self.year_val2, *self.year_menu_options)

        self.year_menu2.configure(state = "disabled")

        self.year_menu1.pack()
        self.year_menu2.pack()

        self.range_button = Checkbutton(self.root, text="Range of Years", variable = self.range_option, command = self.toggle_range, onvalue=1,offvalue=0)

        self.range_button.pack()

        self.team_val.set(self.team_menu_options[0])
        self.team_menu = OptionMenu(self.root, self.team_val, *self.team_menu_options)
        self.team_menu.pack()

        self.scrape_button = Button(self.root, text="Get Trades!", command=self.get_trades)
        self.scrape_button.pack()

        self.exit_button = Button(self.root, text = "Quit", command=self.close_window)
        self.exit_button.pack()

        self.root.mainloop()

if __name__ == "__main__":
    m = scraperMenu()
