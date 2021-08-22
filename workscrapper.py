from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import Select
import bs4
import re
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from playsound import playsound  

def workscrap():
    with open('D:\PY Programs\workscrapper\cred.json') as data_file: #Username and password are stored in json file.
        data = json.load(data_file)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://venus.wis.ntu.edu.sg/PortalServices/ServiceListModule/LaunchService.aspx?type=1&launchSvc=https%3A%2F%2Fvenus%2Ewis%2Entu%2Eedu%2Esg%2FWSS2%2FStudent%2FLogin%2Easpx")
    username_input = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input")
    username_input.send_keys(data['username']) 
    ddelement= Select(driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/select'))
    ddelement.select_by_value('STUDENT')
    okbutton = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[4]/td/input[1]")
    okbutton.click()
    password_input = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input")
    password_input.send_keys(data['password'])
    button = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input[1]")
    button.click()
    assignment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_detail_menuControlStud1_tvCoordt3"]' )))
    assignment.click()
    post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_detail_gvAvailableJob"]/tbody/tr[1]/th[8]/a' )))
    post.click()
    while True:
        jobdata = open(r"D:\PY Programs\workscrapper\jobdata.txt","r") #list of saved job postings as to identify latest ones
        job = jobdata.readlines()
        jobdata.close()
        photo = False
        while photo == False:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)
            sleep(2)
            original_window = driver.current_window_handle
            html = driver.page_source
            soup = bs4.BeautifulSoup(html,'html.parser')
            joblist = re.findall('(WS-.*)</a>',str(soup))
            for i in joblist:
                new_string = i + "\n"
                if new_string not in job:
                    try:
                        jobindex = str(joblist.index(i) + 2)
                        xpath = "//*[@id='ctl00_detail_gvAvailableJob_ctl0" + jobindex + "_lbJobNo']"
                        wscode = driver.find_element_by_xpath(xpath)
                        wscode.click()
                        sleep(2)
                        for window_handle in driver.window_handles:
                            if window_handle != original_window:
                                driver.switch_to.window(window_handle)
                                break
                        print(driver.window_handles)
                        direct = (r"C:\Users\User\Desktop\%s.png" % i)
                        driver.get_screenshot_as_file(direct) #Screenshot web page as png and save to desktop.
                        driver.close()
                        driver.switch_to_window(original_window)
                        photo = True
                    except NoSuchElementException:
                        break
            driver.refresh()

        jobdata = open(r"D:\PY Programs\workscrapper\jobdata.txt","w") #update job posting list
        for i in joblist:
            jobdata.write(i + "\n")
        jobdata.close()
        
        #Following lines can be added to play sound to alert user when there are new jobs.
        # if photo == True:
        #     playsound("D:\PY Programs\workscrapper\jobaudio.mp3")
        


    
