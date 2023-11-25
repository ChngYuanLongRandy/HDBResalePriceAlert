from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from model import Query_hdb, Query_street

class Query:

    def __init__(self, params:dict) -> None:
        self.params = params["params"]
        self.driver = self.__start_driver__()
        self.query_type = "street" if self.params["street_val"] else "town"
        self.headers_street = params["headers_street"]
        self.headers_hdb = params["headers_hdb"]

    # start the driver, returns a webdriver chrome object
    def __start_driver__(self) -> webdriver.Chrome:
        driver = webdriver.Chrome()
        driver.get(self.params["hdb_link"])
        assert self.params["hdb_title"] in driver.title
        return driver


    # runs the base query that is similar to both hdb or street query
    def run_base_query(self,driver: webdriver.Chrome, params:dict):
        radio = driver.find_element(By.ID, params["user_profile_title"])
        radio.click()
        flat_type = driver.find_element(By.NAME, params["flat_type_title"])
        flat_type.send_keys(params["flat_type_val"])

        date_range_field = driver.find_element(By.ID , params["date_range_title"])
        date_range_field.send_keys("last 12")

    # master query function
    # returns all records in chronological order
    def run_query(self):
        if self.params["street_val"]:
            Query_street.run_query_street(self.driver, self.params)
        else:
            Query_hdb.run_query_hdb(self.driver, self.params)
        self.run_base_query(self.driver, self.params)
        submit_btn = self.driver.find_element(By.ID, self.params["submit_btn_id"])
        submit_btn.click()

    # Runs the query twice which for some reason will then only be able to generate the results
    def run_query_success(self):
        self.run_query()
        self.run_query()

    # master write dataframe function
    def write_to_dataframe(self) -> pd.DataFrame:
        if self.query_type == "street":
            print('params["street_val"] is true')
            return Query_street.write_to_dataframe_street(self.driver, self.headers_street)
        else:
            print('params["street_val"] is false')
            return Query_hdb.write_to_dataframe_hdb(self.driver, self.headers_hdb)