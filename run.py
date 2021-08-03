import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import csv

csv_file =  open("ghalamchi.csv", 'w')
csv_writer = csv.writer(csv_file, delimiter=",")
beshmar=0
Years = [99,98,97,96,95]
Depts = [1,2,3,4,5]
for year in Years:
    for dept in Depts:
        u = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedUpdateUni',data= {'year': year, 'dept': dept, 'ReshteId': 0})
        u = re.findall(":(\d*),", u.text)
        Universities = list(map(int, u))
        for uni in Universities:
            r = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedUpdateReshte',data= {'year': year, 'dept' : dept , 'uniId': uni})
            r = re.findall(":(\d*),", r.text)
            Reshtes = list(map(int, r))
            for reshte in Reshtes:
                html_doc = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedShowSuperiors',data= {'dept': str(dept), 'sahmieh': '0', 'rank': '0', 'reshte': str(reshte), 'year': str(year), 'univercity': str(uni), 'type': '2' })
                workbookid = re.findall("\('(.*)'", html_doc.text)
                workbookid = list(map(str, workbookid))
                time.sleep(0.5)
                soup = BeautifulSoup(html_doc.text, 'html.parser')
                soup = soup.find('table')
                soup = soup.find_all('tr')[1:]
                for count0,row in enumerate(soup):
                    Karname = requests.post('https://www.kanoon.ir/Public/SuperiorsRankBasedShowWorkBook',data= {'stdCounter':workbookid[count0],'dept':'1','year':'99'})
                    soup = BeautifulSoup(Karname.text, 'html.parser')
                    counter = 1
                    listKarname = []
                    for i in soup.find_all("td")[2:]:
                        if counter % 2 == 0 :
                            listKarname.append((i.text).replace(' ',''))
                        counter += 1
                    listKarname = list(map(int, listKarname))
                    for count, td in enumerate(row):
                        if count == 1:
                            miangine_taraz_kanooni = (td.text).rstrip()
                        elif count == 3:
                            goorooh = (td.text).rstrip()
                        elif count == 5:
                            rotbe_keshvari = (td.text).rstrip()
                        elif count == 7:
                            rotbe_sahmie = (td.text).rstrip()
                        elif count == 9:
                            sahmie_mantaghe = (td.text).rstrip()
                        elif count == 11:
                            jensiat = (td.text).rstrip()
                        elif count == 13:
                            shahr = (td.text).rstrip()
                        elif count == 15:
                            reshte_ghabooli = (td.text).rstrip()
                    final_list_row = [listKarname,miangine_taraz_kanooni + goorooh ,  rotbe_keshvari , rotbe_sahmie ,sahmie_mantaghe , jensiat , shahr , reshte_ghabooli, year , dept , uni , reshte]
                    print(final_list_row)
                    csv_writer.writerow(final_list_row)
                    beshmar += 1
                    time.sleep(0.1)
                    print(beshmar)
csv_file.close()
