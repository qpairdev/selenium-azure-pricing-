from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from selenium.webdriver.firefox.options import Options
import Azure_test

# Start Browser

browser = webdriver.Firefox()
url = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/"
browser.get(url)

# Connect to database
mydb = mysql.connector.connect(
    host="qpairboto.cnryqwkkelel.us-east-1.rds.amazonaws.com",
    user="rivetcopt",
    passwd="rivetcopt",
    database="copt"
    )
cursor = mydb.cursor()
sql = "DROP TABLE IF EXISTS Test"
cursor.execute(sql)

# Create Table
sql = """
    CREATE TABLE Test(
    OS varchar(50),
    Region varchar(50),
    PricingBy varchar(50),
    Category varchar(50),
    CategorySubType varchar(50),
    InstanceType varchar(50),
    Active_vCPU varchar(50),
    Underlying_vCPU varchar(50),
    vCPU varchar(50),
    Core varchar(50),
    RAM varchar(20),
    GPU varchar(30),
    NVMeDisk varchar(30),
    TemporaryStorage varchar(20),
    PayAsYouGo varchar(50),
    OneYear varchar(50),
    OneYearSavings varchar(50),
    ThreeYear varchar(50),
    ThreeYearSavings varchar(50),
    AzureHybrid varchar(50),
    AzureHybridSavings varchar(50)
    )
    """
cursor.execute(sql)
print("Table Created")



url_option_list=[]

# Find list of the  OS
os_list_elem = browser.find_element_by_xpath("//*[@id='vm-type']")

# Wait for element clickable
WebDriverWait(browser, 30).until(EC.element_to_be_clickable, (By.XPATH,f"//*[@id='vm-type']"))

# Click on the OS List
os_list_elem.click()

optgroups = BeautifulSoup(os_list_elem.get_attribute('innerHTML'), "html5lib").findAll('optgroup')

for i, optgroup in enumerate(optgroups):
    # Wait for optgroup element presence
    WebDriverWait(browser, 30).until(EC.presence_of_element_located, (By.XPATH, f"//*[@id='vm-type']/optgroup[{i+1!r}]"))
    
    for j,option in enumerate(optgroup.findAll('option')):

        # Wait for optgroup element presence
        WebDriverWait(browser, 30).until(EC.presence_of_element_located, (By.XPATH, f"//*[@id='vm-type']/optgroup[{i+1!r}]/option[{j+1!r}]"))
        option_elem = browser.find_element_by_xpath(f"//*[@id='vm-type']/optgroup[{i+1!r}]/option[{j+1!r}]")
        option_elem.click()
        url_option_list.append({'name':option.text.strip(),'url':browser.current_url})

browser.close()

for url_option in url_option_list:
     success = Azure_test.run_scraping(url_option['url'], url_option['name'])
     if success == True:
         print("Successfully Scarped for {}".format(url_option['name']))

mydb.close()