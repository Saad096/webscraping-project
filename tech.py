from datetime import datetime

from xmlrpc.client import DateTime
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
import os
import pandas as pd
import random
import os
from selenium.webdriver.common.keys import Keys
import json

driver=""
txp=""


if __name__ == '__main__':

    print("Opening Browser  . . . ")
    driver = uc.Chrome("/home/saad/Desktop/Selenium Work/About Software INstalletion/chromedriver_linux64/chromedriver")
    driver.get("https://skillsfunding.service.gov.uk/home")
    sleep(5)
    driver.find_element(By.NAME,"username").send_keys("dev@inspiremiddlesexcollege.org")
    driver.find_element(By.NAME,"password").send_keys("EInspire1234$$")
    driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
    sleep(5)
    driver.get("https://recruit.providers.apprenticeships.education.gov.uk/10038183/vacancies/?Filter=All&SearchTerm=")
    page=0

    link_list=[]

    while True:

        page = page + 1

        print("Page No: "+str(page))

        

        driver.get("https://recruit.providers.apprenticeships.education.gov.uk/10038183/vacancies/?filter=All&page=" + str(page))

        sleep(5)

        temp = driver.find_elements(By.XPATH,"//h3[contains(@class,'govuk-heading-m')]")

        if len(temp) > 0  and temp[0].text == "0 vacancies":
            break

        temp=driver.find_elements(By.XPATH,"//tr")

        count=0

        for item in temp:
            data=item.find_elements(By.XPATH,"td")
            if len(data) > 5 and data[5].text == "LIVE":
                data=data[6].find_elements(By.XPATH,"a")
                if len(data) > 0 :
                    data=data[0].get_attribute("href")
                    link_list.append(data)



    person_links=[]
    count=0
    for link in link_list:
        driver.get(link)

        temp = driver.find_elements(By.XPATH,"//table")
        if len(temp) > 0 :
            temp=temp[-1].find_elements(By.XPATH,"tbody")
            temp=temp[0].find_elements(By.XPATH,"tr")
            for item in temp:
                data=item.find_element(By.XPATH,"td")
                data=data.find_elements(By.XPATH,"a")
                if len(data)>0:
                    data=data[0].get_attribute("href")
                    person_links.append(data)
                
            count = count + 1

            print(str(count)+ " / " +str(len(link_list)))


    data_list=[]

    count=0

    for link in person_links:

        data_structure={
            "Name":"Name",
            "Application_Id":"Application_Id",
            "Location":"Location",
            "Number":"Number",
            "E_Mail":"E_Mail",
            "Q1":"Q1",
            "Q2":"Q2",
            "Q3":"Q3"
        }
        try:
            driver.get(link)

            name_=driver.find_element(By.XPATH,"//h1[contains(@class,'govuk-heading-xl govuk-!-margin-bottom-0')]")
            data_structure["Name"]=name_.text

            app_id_=driver.find_element(By.XPATH,"//p[contains(@class,'govuk-body govuk-!-margin-bottom-6')]")
            data_structure["Application_Id"]=app_id_.text.replace("Application ID: ","")

            about_=driver.find_elements(By.XPATH,"//div[contains(@class,'panel panel-border-narrow')]//p")
            
            data_structure["Location"]=about_[0].text.replace('\n',',')

            temp=about_[1].text.split("\n")

            if len(temp) > 0:
                data_structure["Number"]=temp[0]
            if len(temp) > 1:
                data_structure["E_Mail"]=temp[1]
            
            temp=driver.find_elements(By.XPATH,"//div[contains(@class,'govuk-form-group')]")

            if len(temp) > 0:
                data_structure["Q1"]=temp[0].text.replace('\n',' ')
            if len(temp) > 1:
                data_structure["Q2"]=temp[1].text.replace('\n',' ')
            if len(temp) > 2:
                data_structure["Q3"]=temp[2].text.replace('\n',' ')
            
            data_list.append(data_structure)
        except:
            pass
        count = count + 1
        print(str(count)+ " / " +str(len(person_links)))

    print("Writing . . . ")

    
    with open("mydata1.json", "w") as f:
        json.dump(data_list,f)
    
    print("Completed")

    exit()
        
