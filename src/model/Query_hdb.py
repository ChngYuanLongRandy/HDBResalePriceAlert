from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# runs the query in the website with HDB town 
def run_query_hdb(driver: webdriver.Chrome, params:dict):
    print("running hdb")
    hdb_town = driver.find_element(By.NAME, params["town_title"])
    hdb_town.send_keys(params["town_val"])

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