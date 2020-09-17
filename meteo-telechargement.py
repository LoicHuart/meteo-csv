import os
import glob
import shutil
from datetime import datetime
import time
import gzip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds

destination = "C:\\Users\\loic\\Desktop\\Nouveau dossier\\meteo"
source_sans_extention = "C:\\Users\\loic\\Downloads\\"
source = source_sans_extention+"*.gz"
driver = webdriver.Chrome('C:\\Nouveaudossier\\chromedriver')

driver.get("http://rp5.md/Archives_m%C3%A9t%C3%A9o_%C3%A0_Charleville")

#click sur le bouton "Télécharger les archives météo"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[7]/div[5]").click()

#determine la date de debut(dateA) et la date de fin (dateB)
#dateA
dateActuel = datetime.now()

#dateActuel = datetime(2017,3,5,0,0,0,0)
if dateActuel.month == 1 :
    dateA = dateActuel.replace(month=12, day=dateActuel.day-(dateActuel.day-1),year=dateActuel.year-1)
else:
    dateA = dateActuel.replace(month=dateActuel.month-1, day=dateActuel.day-(dateActuel.day-1))
dateAstr= '{day}.{month}.{year}'.format(day=dateA.day, month=dateA.month, year=dateA.year)

#dateB
def last_day_of_month(year, month):

    last_days = [31, 30, 29, 28, 27]
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date()
    return None
if dateActuel.month == 1 :
    dateB = dateActuel.replace(month=12,year=dateActuel.year-1)
    dateBstr = last_day_of_month(dateB.year, dateB.month)
else:
    dateB =dateActuel.replace(month=dateActuel.month-1)
    dateBstr = last_day_of_month(dateB.year, dateB.month)

dateBstr= '{day}.{month}.{year}'.format(day=dateBstr.day, month=dateBstr.month, year=dateBstr.year)

#ecrit la date de debut
dateA = driver.find_element_by_name("ArchDate1")
dateA.clear()
dateA.send_keys(dateAstr)


#ecrit le date de fin
dateB = driver.find_element_by_name("ArchDate2")
dateB.clear()
dateB.send_keys(dateBstr)


#click sur la case "tous les jours"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[9]/div[1]/form[1]/table[2]/tbody[1]/tr[1]/td[2]/label[1]/span[1]").click()

#click sur la case "CSV"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[9]/div[1]/form[1]/table[2]/tbody[1]/tr[2]/td[3]/label[1]/span[1]").click()

#click sur la case "UTF-8"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[9]/div[1]/form[1]/table[2]/tbody[1]/tr[3]/td[3]/label[1]/span[1]").click()

#click sur le bouton "Choisir vers un fichier GZ (archives)"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[9]/div[1]/form[1]/table[2]/tbody[1]/tr[3]/td[6]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[1]").click()
time.sleep(5)

#click sur le bouton "Télécharger"
driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[9]/div[1]/form[1]/table[2]/tbody[1]/tr[3]/td[6]/table[1]/tbody[1]/tr[1]/td[2]/span[1]/a[1]").click()
download_wait(source_sans_extention)

time.sleep(5)

#determine le dernier fichier dans le dossier de telechargement
list_of_files = glob.glob(source)
latest_file = max(list_of_files, key=os.path.getctime)

#deplace le fichier dans le repertoire voulu
nomFichier = os.path.basename(latest_file)          #monFichier.csv.gz
nomFichierSansExtention = nomFichier.split(".gz")   #monFichier.csv
lienFichier= os.path.join(destination,nomFichier)
if os.path.exists(lienFichier) is True:
    os.remove(lienFichier)
shutil.move(latest_file,destination)

#decompresse le fichier
with gzip.open(lienFichier, 'rb') as f_in:
    with open(os.path.join(destination,nomFichierSansExtention[0]), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
os.remove(lienFichier)
driver.close()

