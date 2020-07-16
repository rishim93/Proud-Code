
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import requests
import json
import socket
import logging
import datetime
import sys
from collections import OrderedDict
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
LOG_FILENAME = 'api_main.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,format = LOG_FORMAT)
logger = logging.getLogger()


#logging.debug('Log File for API MAIN Run sequence with date time')
#logging.debug('-------------------------------------------------')
# logging.exception("")
# logging.critical("")
#logging.debug(datetime .datetime.now())



class Api_main:
    # socket.gethostbyname(socket.gethostname())
    #myip = socket.getfqdn()
    #ipname = myip[-10:]
    proxies = {'https': '<proxy server>'}
    ip = str(socket.gethostbyname(socket.gethostname()))
    #logging.debug("Class Api_main starting testValues:")


    def testValues(self):

        # self.label_R.grid_forget()
        # self.text_R.grid_forget()
        # self.text_R.delete(1.0,  END)

        self.labelDisplayCompany.grid(row=2, column=4, padx=5, pady=5)
        self.labelDisplayStreet.grid(row=3, column=4, padx=5, pady=5)
        self.labelDisplayCity.grid(row=4, column=4, padx=5, pady=5)
        self.labelDisplayCountry.grid(row=5, column=4, padx=5, pady=5)
        self.labelDisplayProv.grid(row=6, column=4, padx=5, pady=5)
        self.labelDisplayPostalCode.grid(row=7, column=4, padx=5, pady=5)
        self.labelDisplayPhone.grid(row=8, column=4, padx=5, pady=5)
        self.labelDisplayUrl.grid(row=9, column=4, padx=5, pady=5)
        self.labelDisplayEmail.grid(row=10, column=4, padx=5, pady=5)

        self.labelDisplayCompany.config(text=self.entryCompanyName.get())
        self.labelDisplayStreet.config(text=self.entrystreet.get())
        self.labelDisplayCity.config(text=self.entryCity.get())
        self.labelDisplayCountry.config(text=self.country.get())
        self.labelDisplayProv.config(text=self.province.get())
        self.labelDisplayPostalCode.config(text=self.entryPostalCode.get())
        self.labelDisplayPhone.config(text=self.entryPhone.get())
        self.labelDisplayUrl.config(text=self.entryUrl.get())
        self.labelDisplayEmail.config(text=self.entryEmail.get())

        # if (len(self.entryCompanyName.get()) == 0 and len(self.entryPhone.get()) == 0):
        #     messagebox.showinfo("Error", "Company name as well as Telephone cannot be empty")
        # else:

        Api_main.googleapiNameAddress(self)




    def googleapiNameAddress(self):

        FullNameAddress = '{} {} {} {} {}'.format(self.entryCompanyName.get(), self.entrystreet.get(),
                                                  self.entryCity.get(), self.province.get(),
                                                  self.country.get())

        FullNameAddress = FullNameAddress.replace(" ", "%20")

        key = '<google API key>'
        google_place_url = ('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}'
                            '&inputtype=textquery&fields=name,place_id&key={}'
                            .format(FullNameAddress, key))
        if Api_main.ip.startswith('10.171.'):
            req_place = requests.get(google_place_url, proxies=Api_main.proxies)
        else:
            req_place = requests.get(google_place_url)

        with open('json_google_place.txt', 'w') as jg:
            jg.write(req_place.text)

        json_place_data = json.loads(req_place.text)
        google_place_status = json_place_data["status"]


        self.textGoogle.delete('1.0', END)

        if google_place_status == 'OK':

            try:
                place_id = json_place_data["candidates"][0]["place_id"]
            except:
                print("No place id Found")
                return


            google_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid={}&fields=place_id,' \
                                'name,international_phone_number,formatted_address,address_component,website&key={}'\
                .format(place_id, key)

                req_detail = requests.get(google_detail_url)

            with open('json_google_detail.txt', 'w') as jg2:
                jg2.write(req_detail.text)

            json_detail_data = json.loads(req_detail.text)
            google_detail_status = json_detail_data["status"]
            if google_detail_status == 'OK':
                with open('googleapidata.txt', 'w') as gad:
                    try:
                        gad.write(
                            "Name: " + json_detail_data["result"]["name"] + "\n")
                    except:
                        pass

                    try:
                        for add in str(json_detail_data["result"]["formatted_address"]).split(','):
                            gad.write(add+"\n")
                        # gad.write("Address: " + json_detail_data["result"]["formatted_address"] + "\n")
                    except:
                        pass
                    try:
                        # REGION
                        gad.write(
                            "Region: " + json_detail_data["result"]["address_components"][1]["long_name"] + "\n")
                    except:
                        pass
                    try:
                        # PHONE
                        gad.write(
                            "Phone: " + json_detail_data["result"]["international_phone_number"] + "\n")
                    except:
                        pass
                    try:
                        # WEBSITE
                        gad.write("Website: " +
                                  json_detail_data["result"]["website"] + "\n")
                    except:
                        pass
                    gad.write("-X-X-X-X-X-X-X-X-X-X-X-X-X- \n\n")
            else:
                with open('googleapidata.txt', 'w') as gad:
                    gad.write("No results Found")

        else:
            with open('googleapidata.txt', 'w') as gad:
                gad.write("Zero results")
        self.labelGoogle.grid(row=1, column=3, padx=5, pady=5, sticky='NSEW')
        self.textGoogle.grid(row=2, column=3, padx=5, pady=5)
        with open('googleapidata.txt', 'r') as gad:

            self.textGoogle.insert(INSERT, gad.read())

        self.scrollG.grid(row=2, column=4, sticky='nsew')
        self.textGoogle['yscrollcommand'] = self.scrollG.set


    def changeOptions(self, selection):
        # -----------------------------------------------------------
        # PROVINCE
        # -----------------------------------------------------------
        self.province.set('None')


        self.DropProvince = OptionMenu(
            self.mainframe3, self.province, *self.countryChoices[selection].keys())


        self.DropProvince.grid(row=5, column=2, padx=5, pady=5)

    def __init__(self, master):  # init function for tkinter window

        self.frame = ttk.Frame(master)
        self.frame.grid(row=1, column=1)

        # -----------------------------------------------------------
        # COMPANY NAME
        # -----------------------------------------------------------

        self.labelCompanyName = ttk.Label(self.frame, text="Company Name:-")
        self.labelCompanyName.grid(row=2, column=1, padx=5, pady=5)

        self.entryCompanyName = ttk.Entry(self.frame)
        self.entryCompanyName.grid(row=2, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # Street address
        # -----------------------------------------------------------

        self.labelstreet = ttk.Label(self.frame, text="Street Address:-")
        self.labelstreet.grid(row=3, column=1, padx=5, pady=5)

        self.entrystreet = ttk.Entry(self.frame)
        self.entrystreet.grid(row=3, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # CITY
        # -----------------------------------------------------------

        self.labelCity = ttk.Label(self.frame, text="City :-")
        self.labelCity.grid(row=4, column=1, padx=5, pady=5)

        self.entryCity = ttk.Entry(self.frame)
        self.entryCity.grid(row=4, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # COUNTRY
        # -----------------------------------------------------------

        self.labelCountry = ttk.Label(self.frame, text="Country :-")
        self.labelCountry.grid(row=5, column=1, padx=5, pady=5)

        # Country Choices
        self.mainframe2 = Frame(self.frame)
        self.mainframe2.grid(column=0, row=0, sticky=W)
        self.mainframe2.columnconfigure(0, weight=1)
        self.mainframe2.rowconfigure(0, weight=1)
        self.mainframe2.grid(row=5, column=2)

        self.country = StringVar(self.mainframe2)
        self.country.set('None')

        self.countryChoices = {'CANADA': {'Alberta': 'AB',
                                          'British Columbia': 'BC',
                                          'Manitoba': 'MB',
                                          'Newfoundland and Labrador': 'NL',
                                          'New Brunswick': 'NB',
                                          'Nova Scotia': 'NS',
                                          'Ontario': 'ON',
                                          'Prince Edward Island': 'PE',
                                          'Quebec': 'QC',
                                          'Saskatchewan': 'SK'
                                          },
                                'USA': {'Alabama': 'AL',
                                       'Alaska': 'AK', 'Arizona': 'AZ',
                                       'Arkansas': 'AR', 'California': 'CA',
                                       'Colorado': 'CO', 'Connecticut': 'CT',
                                       'Delaware': 'DE', 'District of Columbia': 'DC',
                                       'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
                                       'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
                                       'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
                                       'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
                                       'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
                                       'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
                                       'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
                                       'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
                                       'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
                                       'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
                                       'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
                                       'American Samoa': 'AS', 'Guam': 'GU', 'Marshall Islands': 'MH',
                                       'Micronesia': 'FM', 'Northern Marianas': 'MP', 'Palau': 'PW',
                                       'Puerto Rico': 'PR', 'Virgin Islands': 'VI'}}

        #self.countryChoices = OrderedDict(self.countryChoices)












        self.countryChoice = OptionMenu(self.mainframe2,
                                        self.country,
                                        *self.countryChoices.keys(),
                                        command=self.changeOptions)
        self.countryChoice.grid(row=5, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # PROVINCE
        # -----------------------------------------------------------

        self.labelProvince = ttk.Label(self.frame, text="Province/states :-")
        self.labelProvince.grid(row=6, column=1, padx=5, pady=5)

        self.mainframe3 = Frame(self.frame)
        self.mainframe3.grid(column=0, row=0, sticky=W)
        self.mainframe3.columnconfigure(0, weight=1)
        self.mainframe3.rowconfigure(0, weight=1)
        self.mainframe3.grid(row=6, column=2)

        self.province = StringVar(self.mainframe3)

        # -----------------------------------------------------------
        # Postal Code
        # -----------------------------------------------------------

        self.labelPostalCode = ttk.Label(self.frame, text="Postal Code :-")
        self.labelPostalCode.grid(row=7, column=1, padx=5, pady=5)

        self.entryPostalCode = ttk.Entry(self.frame)
        self.entryPostalCode.grid(row=7, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # PHONE NUMBER
        # -----------------------------------------------------------

        self.labelPhone = ttk.Label(self.frame, text="Phone Number :-")
        self.labelPhone.grid(row=8, column=1, padx=5, pady=5)

        self.entryPhone = ttk.Entry(self.frame)
        self.entryPhone.grid(row=8, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # URL
        # -----------------------------------------------------------

        self.labelUrl = ttk.Label(self.frame, text="URL :-")
        self.labelUrl.grid(row=9, column=1, padx=5, pady=5)

        self.entryUrl = ttk.Entry(self.frame)
        self.entryUrl.grid(row=9, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # Email
        # -----------------------------------------------------------

        self.labelEmail = ttk.Label(self.frame, text="Email :-")
        self.labelEmail.grid(row=10, column=1, padx=5, pady=5)

        self.entryEmail = ttk.Entry(self.frame)
        self.entryEmail.grid(row=10, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # Result Count Values max
        # -----------------------------------------------------------

        self.labelcountResultMax = ttk.Label(
            self.frame, text="Result Count (5) :-")
        self.labelcountResultMax.grid(row=11, column=1, padx=5, pady=5)

        self.entrycountResultMax = ttk.Entry(self.frame)
        self.entrycountResultMax.grid(row=11, column=2, padx=5, pady=5)

        # -----------------------------------------------------------
        # LINE
        # -----------------------------------------------------------

        self.labelLine = ttk.Label(
            self.frame, text="-----------------------------------------")
        self.labelLine.grid(row=12, column=1, padx=5, pady=5)


        # -----------------------------------------------------------
        # BUTTON SEARCH
        # -----------------------------------------------------------

        # self.Search = ttk.Button(self.frame, text="Search", command=self.R_check)
        self.Search = ttk.Button(
            self.frame, text="Search", command=self.testValues)
        self.Search.grid(row=13, column=1, columnspan=3, padx=5, pady=5,
                         sticky='NSEW')

        # -----------------------------------------------------------
        # LABEL DISPLAY INFORMATION
        # -----------------------------------------------------------
        self.labelDisplayCompany = ttk.Label(self.frame)
        self.labelDisplayCity = ttk.Label(self.frame)
        self.labelDisplayProv = ttk.Label(self.frame)
        self.labelDisplayCountry = ttk.Label(self.frame)
        self.labelDisplayPhone = ttk.Label(self.frame)
        self.labelDisplayStreet = ttk.Label(self.frame)

        self.labelDisplayEmail = ttk.Label(self.frame)
        self.labelDisplayUrl = ttk.Label(self.frame)
        self.labelDisplayPostalCode = ttk.Label(self.frame)

        # -----------------------------------------------------------
        # Text Boxes and Labels For Result
        # -----------------------------------------------------------
        self.frame2 = ttk.Frame(master)
        self.frame2.grid(row=1, column=1)
        self.text_R = Text(self.frame2, width=43, height=20)
        self.textRelatednames = Text(self.frame2, width=43, height=20)
        self.textRelatedaddress = Text(self.frame2, width=43, height=20)
        self.textGoogle = Text(self.frame2, width=43, height=20)

        self.label_R = ttk.Label(self.frame2, text="Api_main API")
        self.labelGoogle = ttk.Label(self.frame2, text="Google API")
        self.labelRelatednames = ttk.Label(self.frame2, text = "RELATED API Names")
        self.labelRelatedaddress = ttk.Label(self.frame2, text="RELATED API Addresses")
        # -----------------------------------------------------------
        # ScrollBar
        # -----------------------------------------------------------


        self.scrollD = ttk.Scrollbar(self.frame2, command=self.text_R.yview)
        # self.scrollD.grid(row=0, column=1, sticky='nsew')
        # self.text_R['yscrollcommand'] = self.scrollD.set

        self.scrollG = ttk.Scrollbar(self.frame2, command=self.text_R.yview)
        self.scrollRnames = ttk.Scrollbar(self.frame2, command=self.textRelatednames.yview)
        self.scrollRaddress = ttk.Scrollbar(self.frame2, command=self.textRelatedaddress.yview)

def main():  # Main function
    root = Tk()
    root.title("Check Business Existence")
    #root.geometry('450x400+80+80')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # root.configure(background='black')
    Api_main(root)
    root.mainloop()


if __name__ == "__main__":
    main()
