# Load selenium components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import boto3
import time

# Establish chrome driver and go to idaho site URL
url = "https://idbop.mylicense.com/verification/Search.aspx"
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--silent")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
        options=chrome_options)
driver.get(url)
#print(driver.title)
# Search with Last Name L and License Type Pharmacist
driver.find_element_by_name("t_web_lookup__last_name").send_keys('L')
Select(driver.find_element_by_name("t_web_lookup__license_type_name")).select_by_visible_text("Pharmacist")
time.sleep(2)
sch_button = driver.find_element_by_name("sch_button")
sch_button.click()

# Search all href on the first page and append to an array
suburl = []
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
     href = elem.get_attribute('href')
     if href is not None and "Details.aspx" in href:
             suburl.append(href)
            # print(href)
# Open a file to write
with open ('/saswati/log/idaho_license_details.csv','w') as file:
    file.write("First_Name; Middle_Name; Last_Name; License_Number; License_Type; Status; Org_Issue_Date; Expiry_Date; Renewed \n")

# Loop through each suburl - scrape information and write to the file
for i in suburl:
    driver.get(i)
    first_name = driver.find_element_by_xpath("//span[@id='_ctl27__ctl1_first_name']").text
    middle_name = driver.find_element_by_xpath("//span[@id='_ctl27__ctl1_m_name']").text
    last_name = driver.find_element_by_xpath("//span[@id='_ctl27__ctl1_last_name']").text
    license_number = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_license_no']").text
    license_type = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_license_type']").text
    status = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_status']").text
    org_issue_dt = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_issue_date']").text
    exp_date = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_expiry']").text
    renewed = driver.find_element_by_xpath("//span[@id='_ctl36__ctl1_last_ren']").text
    with open('/saswati/log/idaho_license_details.csv','a') as file:
        file.write(first_name + ";" + middle_name + ";" + last_name + ";" + license_number + ";"
                                   + license_type + ";" + status + ";" + org_issue_dt + ";" + exp_date + ";" + renewed + "\n")
    #btn_close = driver.find_element_by_xpath("//*[@id='btn_close']")
    #driver.implicitly_wait(5)
    #btn_close.click()

# Close file and driver
file.close()
driver.close()
REGION = 'us-east-1'
ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxx'
SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
PATH_IN_COMPUTER = '/saswati/log/idaho_license_details.csv'
BUCKET_NAME = 'saswatiassignment'
KEY = 'output/idaho_license_details.csv' # file path in S3

s3_resource = boto3.resource(
            's3',
            region_name = REGION,
            aws_access_key_id = ACCESS_KEY_ID,
            aws_secret_access_key = SECRET_ACCESS_KEY
 )
s3_resource.Bucket(BUCKET_NAME).put_object(
            Key = KEY,
            Body = open(PATH_IN_COMPUTER, 'rb')
)
