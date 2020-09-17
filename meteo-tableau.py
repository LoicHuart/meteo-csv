import csv
from selenium import webdriver
from datetime import datetime
import os

driver = webdriver.Chrome('C:\\Nouveaudossier\\chromedriver')
driver.get("http://rp5.md/Archives_m%C3%A9t%C3%A9o_%C3%A0_Charleville")
destination = "C:\\Users\\loic\\Desktop\\pythonTableau\\"

table = driver.find_element_by_xpath("/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[8]/table[1]")
#renome le ficher
dateActuel = datetime.now()
dateActuelStr= '{year}.{month}.{day}.{hour}.{minute}.{second}.csv'.format(year=dateActuel.year, month=dateActuel.month, day=dateActuel.day, hour=dateActuel.hour, minute=dateActuel.minute, second=dateActuel.second)
lienFichier= os.path.join(destination,dateActuelStr)


with open(lienFichier, 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    for row in table.find_elements_by_css_selector('tr'):
        #ecrit dans la console le nom des class de chaque ligne du tableau
        print("class = ",row.find_element_by_css_selector('td').get_attribute("class"))

        #test si c'est une ligne avec la date ou non,
        #si il y a la date il l'ecrit ,
        #sinon il n'y a pas la date il l'ecrit en laissant une case vide au debut de la ligne
        if (row.find_element_by_css_selector('td').get_attribute("class")=="cl_dt"):
            wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
        else:
            wr.writerow([""]+[d.text for d in row.find_elements_by_css_selector('td')])

driver.close()