import requests
import csv
import sys
import os

#LATEST_NAV_DOWNLOAD_LINK = r"http://portal.amfiindia.com/spages/NAV0.txt"
LATEST_NAV_DOWNLOAD_LINK = r"http://portal.amfiindia.com/spages/NAVOpen.txt"
#ALTERNATE_LINK = r"https://www.amfiindia.com/spages/NAVAll.txt"
LATEST_PORTFOLIO_FILEPATH = "TotalPortfolio.csv"

folder_path = sys.path[0] + os.sep

class MFTracker(object):
    def __init__(self):
        self.latest_nav_download_filepath = None
        self.all_schemes_info = list()
        self.all_schemes_nav = dict()
        self.related_scheme_rows = list()
        self.portfolio_worth = 0

    def choose_portfolio(self):
        csvs_dict = dict(enumerate([csv_filename for csv_filename in os.listdir(folder_path) if csv_filename.__contains__('.csv')]))
        print("-------------------------------------------------------------------")
        print("\n")
        for item, value in csvs_dict.items():
            print("Enter {0} for Calculating Portfolio : {1}".format(item, value))
        print("\n")
        print("-------------------------------------------------------------------")
        global LATEST_PORTFOLIO_FILEPATH
        while True:
            option = input("Enter Your Option Now :: ")
            print("Option Entered")
            print(option)
            if int(option) in csvs_dict:
                LATEST_PORTFOLIO_FILEPATH = csvs_dict[int(option)]
                break
            else:
                print("Try Again, the option seems invalid...")
    
    def download_latest_nav_statement(self):
        url = LATEST_NAV_DOWNLOAD_LINK
        local_filename = url.split('/')[-1]
        local_filename = folder_path + local_filename
        try:
            response = requests.get(url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk: 
                        f.write(chunk)
        except Exception as e:
            print("Fallback initiated , Exception Occured :: %s"%str(e))
            self.latest_nav_download_filepath = local_filename
        self.latest_nav_download_filepath = local_filename			
        return local_filename

    def get_scheme_codes(self):
        with open(folder_path+LATEST_PORTFOLIO_FILEPATH,"r") as file_handle:
            CSVDictReader = csv.DictReader(file_handle)
            for row in CSVDictReader:
                self.all_schemes_nav[row["scheme_code"]] = 0
                self.all_schemes_info.append((row["scheme_code"],row["no_of_units"]))
            #print self.all_schemes_info
            #print self.all_schemes_nav

    def read_latest_nav_file(self):
        with open(self.latest_nav_download_filepath,"r") as file_handle:
            CSVDictReader = csv.DictReader(file_handle,delimiter = ";")
            for row in CSVDictReader:
                if(row["Scheme Code"] in self.all_schemes_nav):
                    self.related_scheme_rows.append(row)
        #print self.related_scheme_rows

    def add_balances(self):
        global LATEST_PORTFOLIO_FILEPATH
        if "balances.json" in os.listdir(folder_path):
            import json
            balance_json = json.load(open(folder_path+"balances.json"))
            if balance_json["portfolio"] == LATEST_PORTFOLIO_FILEPATH:
                print("Adding Balances in Calculation.....")
                self.portfolio_worth = int(balance_json["amount"])

    def calculate(self):
        for row_info in self.all_schemes_info:
            for scheme in self.related_scheme_rows:
                if scheme["Scheme Code"] == row_info[0]:
                    print("-> Current NAV Of Invested " + scheme["Scheme Name"] + " on " + scheme["Date"] + " for "+ row_info[1] +" units = " + str(float(row_info[1])*float(scheme["Net Asset Value"])))
                    self.portfolio_worth = self.portfolio_worth + (float(row_info[1])*float(scheme["Net Asset Value"]))

        print("Your Total Portfolio Net Worth = "+str(self.portfolio_worth))
        if self.portfolio_worth > 10000000:
            print("Your worth in an understandable way : " + str(int(self.portfolio_worth/10000000) )+ " Crores " + str(int(self.portfolio_worth%10000000)/100000 ) + " Lakhs "  + str(int(self.portfolio_worth%100000)/1000) + " Thousands ")
        else:
            print("Your worth in an understandable way : " + str(int(self.portfolio_worth/100000) )+ " Lakhs " + str(int(self.portfolio_worth%100000)/1000) + " Thousands " )

mf_tracker = MFTracker()
mf_tracker.choose_portfolio()
print("Downloading Latest NAV Statement of Mutual Funds .......")
mf_tracker.download_latest_nav_statement()
mf_tracker.get_scheme_codes()
mf_tracker.read_latest_nav_file()
mf_tracker.add_balances()
mf_tracker.calculate()
