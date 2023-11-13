from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# writes the hdb data from the Street category coupled with the headers and returns a pd.dataframe
def write_to_dataframe_street(driver:webdriver.Chrome, headers:list)->pd.DataFrame:
    addresses = driver.find_elements(By.XPATH, '//div[@class="grid-container hide-for-small-only"]//tr')
    # we only need the second to the last
    addresses = addresses[1:len(addresses)]
    data = []
    for address in addresses:
        tr = address.find_elements(By.TAG_NAME,"td")      
        block = tr[1].text
        hdb_town = tr[0].text
        storey = tr[2].text
        floor_area,flat_model = tr[3].text.split("\n")
        lease_commence = tr[4].text
        remaining_lease = tr[5].text.split("\n")[0]
        print(remaining_lease)
        resale_price = tr[6].text
        resale_date = tr[7].text
        data.append([block, hdb_town, storey, floor_area, flat_model, lease_commence, remaining_lease, resale_price, resale_date])
    
    return pd.DataFrame(data, columns=headers)

# runs the query in the website with Street Name
def run_query_street(driver: webdriver.Chrome, params:dict):
    print("running street")
    street_field = driver.find_element(By.NAME , params["street_title"])
    street_field.send_keys(params["street_val"])