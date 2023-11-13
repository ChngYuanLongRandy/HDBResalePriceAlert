from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = 'hdbresalealertservice@gmail.com'
receiver_email  = 'chngyuanlong@gmail.com'
password = "qcbx wfzf eysm xlxk"
message = """\
Subject: Hi there

This message is sent from Python."""

hdb_link = "https://services2.hdb.gov.sg/webapp/BB33RTIS/BB33SComparator"
hdb_title = "Resale Flat Prices"
user_profile_title = "userProfileB"
flat_type_title = "FLAT_TYPE"
flat_type_val = Keys.NUMPAD4
town_title = "NME_NEWTOWN"
# town_val = None
town_val = "a"
street_title = "NME_STREET"
street_val = None
# street_val = "Ang Mo Kio Ave 3"
date_range_title = "dteRange"
submit_btn_id = "btnSubmit"

params_hdb = {"hdb_link":hdb_link,
          "hdb_title":hdb_title,
          "user_profile_title":user_profile_title,
          "flat_type_title":flat_type_title,
          "flat_type_val":flat_type_val,
          "town_title":town_title,
          "town_val":town_val,
          "street_title":street_title,
          "street_val":street_val,
          "date_range_title":date_range_title,
          "submit_btn_id":submit_btn_id}

# for HDB Town
headers_hdb = [
    "Block",
    "Street Name",
    "Storey",
    "Floor Area (sqm)" , 
    "Flat Model",
    "Lease Commence Date",
    "Remaining Lease",
    "Resale Price",
    "Resale Registration Date"
    ]

filepath = "hdb.csv"

def main_street():
    driver = start_driver()
    run_query_success(driver, params_hdb)
    df = write_to_dataframe_hdb(driver, headers_hdb)
    save_dataframe(df, filepath, headers_hdb)

def main_hdb():
    driver = start_driver()
    run_query_success(driver, params_hdb)
    df = write_to_dataframe_hdb(driver, headers_hdb)
    save_dataframe(df, filepath, headers_hdb)
    send_email({"information":df.iloc[1:5]})

# start the driver, returns a webdriver chrome object
def start_driver() -> webdriver.Chrome:
    driver = webdriver.Chrome()
    driver.get(hdb_link)
    assert hdb_title in driver.title
    return driver

# runs the query in the website with HDB town 
def run_query_hdb(driver: webdriver.Chrome, params:dict):
    print("running hdb")
    hdb_town = driver.find_element(By.NAME, params["town_title"])
    hdb_town.send_keys(params["town_val"])


# runs the query in the website with Street Name
def run_query_street(driver: webdriver.Chrome, params:dict):
    print("running street")
    street_field = driver.find_element(By.NAME , params["street_title"])
    street_field.send_keys(params["street_val"])

    
# runs the base query that is similar to both hdb or street query
def run_base_query(driver: webdriver.Chrome, params:dict):
    radio = driver.find_element(By.ID, params["user_profile_title"])
    radio.click()
    flat_type = driver.find_element(By.NAME, params["flat_type_title"])
    flat_type.send_keys(params["flat_type_val"])

    date_range_field = driver.find_element(By.ID , params["date_range_title"])
    date_range_field.send_keys("last 12")

# master query function
# returns all records in chronological order
def run_query(driver: webdriver.Chrome, params: dict):
    if params["street_val"]:
        run_query_street(driver, params)
    else:
        run_query_hdb(driver, params)
    run_base_query(driver, params)
    submit_btn = driver.find_element(By.ID, params["submit_btn_id"])
    submit_btn.click()

# Runs the query twice which for some reason will then only be able to generate the results
def run_query_success(driver: webdriver.Chrome, params:dict):
    run_query(driver, params)
    run_query(driver, params)

# writes the hdb data from the HDB category coupled with the headers and returns a pd.dataframe
def write_to_dataframe_hdb(driver:webdriver.Chrome, headers:list)->pd.DataFrame:
    addresses = driver.find_elements(By.XPATH, '//tr[@height="30"]')
    # we only need half of them as the rest of them are repeated but not shown (ie the values are hidden)
    addresses = addresses[:int(len(addresses)/2)]
    data = []
    for address in addresses:
        tr = address.find_elements(By.XPATH,".//child::td")        
        block = tr[0].text
        street_name = tr[1].text
        storey = tr[2].text
        floor_area,flat_model = tr[3].text.split("\n")
        lease_commence = tr[4].text
        remaining_lease = tr[5].text.split("\n")[0]
        resale_price = tr[6].text
        resale_date = tr[7].text
        data.append([block, street_name, storey, floor_area, flat_model, lease_commence, remaining_lease, resale_price, resale_date])
    
    return pd.DataFrame(data, columns=headers)

# saves file locally
def save_dataframe(df:pd.DataFrame, filepath:str, headers:str) ->None:
    print("saving to csv...")
    df.to_csv(filepath, columns=headers_hdb, index=False)

# sends an email
def send_email(data:dict):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

if (__name__ == "__main__") :
    main_hdb()