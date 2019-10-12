import requests
import time
import csv
from bs4 import BeautifulSoup

setTimeout = 1 #pause code to not spam the site (true = 1, false = 0)
timeout    = 0.5 #time to pause code in s
minPage    = 1 #first page
maxPage    = 52 #last page
url        = 'https://www.posta.hr'
urlPath    = '/pretrazivanje-postanskih-ureda/263?pojam=&page='
fileName   = 'postanski_uredi.csv'

#Open csv file
with open( fileName, 'w') as csvfile:

    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Poštanski broj', 'Poštanski ured', 'Adresa', 'Mjesto'])

    #loop throu url pages
    for page in range(minPage, maxPage + 1 ):

        page = str(page)

        if setTimeout:
            time.sleep(timeout)

        fullUrl  = url + urlPath + page
        response = requests.get(fullUrl)

        if response.status_code == 200:
            print('Dohvaćanje podataka sa stranice ' + page + '!')

        elif response.status_code == 404 :
            exit()

        #parse response text to HTML and get table body
        table = BeautifulSoup(response.text, "html5lib").find('tbody')

        #Check if data (td) exists
        if table.findAll('td'):
            for row in table.findAll('tr'):

                data = []
                for td in row.findAll( 'td' ):
                    if td.get_text():
                        split = td.get_text().split(',', 1)

                        if len(split) > 1:

                            leftSplit     = split[0].split(' ', 1)
                            postanskiBroj = leftSplit[0]
                            mjesto        = leftSplit[1]
                            adresa        = split[1].strip()

                            data = [postanskiBroj, mjesto, adresa]

                        else:
                            data.append(split[0])

                if data:
                    filewriter.writerow(data) #store collected data in csv file

                    if setTimeout:
                        time.sleep(timeout) #pause code to not spam the site

            print('Podaci sa stranice ' + page + ' su uspješno uneseni!')

            if int(page) == maxPage:
                print('Kraj skripte!')

        else:
            print('Nema pronađenih podataka na stranici ' + page + '!', 'Kraj skripte!' , sep='\n')
            exit()





