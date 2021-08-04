from bs4.element import Declaration
import requests
import time
import re
import csv
from bs4 import BeautifulSoup

csv_file =  open("ghalamchi.csv", 'w')
csv_writer = csv.writer(csv_file, delimiter=",")

Years = [99,98,97,96,95]
Depts = [1,2,3,4,5]

for year in Years:
    for dept in Depts:
        u = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedUpdateUni',data= {'year': year, 'dept': dept, 'ReshteId': 0})
        u = re.findall(":(\d*),", u.text)
        Universities = list(map(int, u))
        Universities = [31]
        for uni in Universities:
            r = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedUpdateReshte',data= {'year': year, 'dept' : dept , 'uniId': uni})
            r = re.findall(":(\d*),", r.text)
            Reshtes = list(map(int, r))
            for reshte in Reshtes:
                html_doc = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors',data= {'dept': str(dept), 'sahmieh': '0', 'rank': '0', 'reshte': str(reshte), 'year': str(year), 'univercity': str(uni), 'type': '2' })
                workbookid = re.findall("\('(.*)'", html_doc.text)
                workbookid = list(map(str, workbookid))
                soup = BeautifulSoup(html_doc.text, 'html.parser')
                soup = soup.find('table')
                if type(soup)=='NoneType' :
                    print('ERROR ON {} {} {} {}'.format(year,dept,uni,reshte))
                elif soup == None:
                    print('ERROR')
                else:
                    soup = soup.find_all('tr')[1:]
                    for count0,row in enumerate(soup):
                        for count, td in enumerate(row):
                            if count == 1:
                                miangine_taraz_kanooni = (td.text).rstrip()
                            elif count == 3:
                                goorooh = (td.text).rstrip()
                            elif count == 5:
                                rotbeK = (td.text).rstrip()
                            elif count == 7:
                                rotbeS = (td.text).rstrip()
                            elif count == 9:
                                sahmieM = (td.text).rstrip()
                            elif count == 11:
                                jensiat = (td.text).rstrip()
                            elif count == 13:
                                shahr = (td.text).rstrip()
                            elif count == 15:
                                DayNight = (td.text).rstrip()
                                Regexx = re.findall(".*\s|\s", DayNight)[0]
                                DayNight = DayNight[len(Regexx):]
                        #Karname
                        Karname = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedShowWorkBook',data= {'stdCounter':workbookid[count0],'dept':str(dept),'year':str(year)})
                        soup = BeautifulSoup(Karname.text, 'html.parser')
                        counter = 1
                        listKarname = []
                        for i in soup.find_all("td")[2:]:
                            if counter % 2 == 0 :
                                listKarname.append((i.text).replace(' ',''))
                            counter += 1
                        listKarname = list(map(int, listKarname))

                        #return all data from row
                        final_list_row = [year,dept,uni,reshte,rotbeK,rotbeS,sahmieM,jensiat,shahr,miangine_taraz_kanooni,goorooh,DayNight,listKarname]
                        print(final_list_row)

                        csv_writer.writerow(final_list_row)

                        #time.sleep(0.5)

csv_file.close()
