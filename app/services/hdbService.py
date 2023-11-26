from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import yaml

config_path = "app/config/config.yaml"
with open(config_path, 'r') as yaml_file:
    configData = yaml.load(yaml_file, Loader=yaml.FullLoader)


filepath = "hdb.csv"

# def main_hdb():
#     driver = start_driver()
#     run_query_success(driver, params_hdb)
#     if params_hdb["street_val"]:
#         df = write_to_dataframe_street(driver, headers_street)
#         save_dataframe(df, filepath, headers_street)
#     else:
#         df = write_to_dataframe_hdb(driver, headers_hdb)
#         save_dataframe(df, filepath, headers_hdb)
#     send_email(df)

def get_results(params:dict, headers: list, format:str ="json"):
    print("Starting get results method")
    print(f"Params are :{params}")
    try:
        driver = start_driver(params)
        run_query_success(driver, params)
        if params["street_val"]:
            df = write_to_dataframe_street(driver, headers)
        else:
            df = write_to_dataframe_hdb(driver, headers)
        if format.lower() == "df":
            return df
        elif format.lower() == "json":
            return df.to_json(orient='records')
    except Exception as ex:
        print(f"Unable to process due to {ex}")

# start the driver, returns a webdriver chrome object
def start_driver(params:dict) -> webdriver.Chrome:

    # # Set up Chrome options
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Run in headless mode
    # driver = webdriver.Chrome(options=chrome_options)
    try:
        # service = webdriver.ChromeService(executable_path=r'/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(r'/usr/local/bin/chromedriver')
        driver.get(params["hdb_link"])
        assert params["hdb_title"] in driver.title
    except Exception as ex: 
        print(f"Unable to start driver due to exception {ex}")
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
    blk_from_field = driver.find_element(By.NAME , params["blk_from_title"])
    blk_from_field.send_keys(params["blk_from_val"])
    blk_to_field = driver.find_element(By.NAME , params["blk_to_title"])
    blk_to_field.send_keys(params["blk_to_val"])

    
# runs the base query that is similar to both hdb or street query
def run_base_query(driver: webdriver.Chrome, params:dict):
    radio = driver.find_element(By.ID, params["user_profile_title"])
    radio.click()
    flat_type = driver.find_element(By.NAME, params["flat_type_title"])
    flat_type.send_keys(params["flat_type_val"])

    date_range_field = driver.find_element(By.ID , params["date_range_title"])
    date_range_field.send_keys("last 6")
    # date_range_field.send_keys("last 12")

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
        resale_price = tr[6].text
        resale_date = tr[7].text
        data.append([block, hdb_town, storey, floor_area, flat_model, lease_commence, remaining_lease, resale_price, resale_date])
    
    return pd.DataFrame(data, columns=headers)


# saves file locally
def save_dataframe(df:pd.DataFrame, filepath:str, headers:str) ->None:
    try:
        print("saving to csv...")
        print(df.head())
        df.to_csv(filepath, columns=headers, index=False)
    except Exception as ex:
        print("unable to save due to {}",ex)

# sends an email
def send_email(df:pd.DataFrame):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = 'hdbresalealertservice@gmail.com'
    receiver_email  = 'chngyuanlong@gmail.com'
    password = "qcbx wfzf eysm xlxk"
    html_table = df.to_html(index=False)
    # Attach HTML content to the email
    message = MIMEMultipart()
    html_body = f'<html><body>{html_table}</body></html>'
    message.attach(MIMEText(html_body, 'html'))
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "HDB Resale Alert"
    try:
        print(f"attempting to send email with following params -> from: {message['From']} To: {message['To']} Subject: {message['Subject']}")
        print(f"With email body : {html_body}")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent!")
    except Exception as ex:
        print(f"Unable to send email due to {ex} ")

# if (__name__ == "__main__") :
#     main_hdb()