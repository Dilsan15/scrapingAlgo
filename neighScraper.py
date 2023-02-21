import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class neighScraper:

    def __init__(self, driver_path):

        # Basic setup

        self.all_links = []

        option = webdriver.ChromeOptions()

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/108.0.0.0 Safari/537.36 '

        option.add_argument(f'user-agent={user_agent}')

        option.add_argument('--deny-permission-prompts')
        option.add_argument('--disable-geolocation')

        option.page_load_strategy = 'eager'

        sel_service = Service(driver_path)
        self.driver = webdriver.Chrome(service=sel_service, options=option)
        self.driver.maximize_window()

        self.driver.get("https://www.areavibes.com/edmonton-ab/neighborhoods/")

    def get_neigh_links(self):

        # Get all the links to the neighbourhoods in Edmonton

        time.sleep(2)
        all_links = self.driver.find_element(By.ID, "quick-search-src").find_elements(By.TAG_NAME,
                                                                                      "a")

        self.all_links = list(map(lambda x: x.get_attribute("href"), all_links))
        print(self.all_links)
        print(len(self.all_links))

    def get_neigh_stats(self):

        # Get all the stats for each neighbourhood that we have links for

        all_stats = []

        for i in self.all_links:
            temp_dict = {}

            self.driver.get(i + "livability/")
            time.sleep(1)

            comp_ranks = self.driver.find_element(By.CLASS_NAME, "liv-box-digest").find_elements(By.TAG_NAME, "b")
            all_fact_boxes = self.driver.find_elements(By.CLASS_NAME, "facts-box-body")

            temp_dict["neigh_name"] = " ".join(i.split("/")[4].split("+"))
            temp_dict["total_liv_score"] = self.driver.find_element(By.CLASS_NAME, "ndx5__").text

            temp_dict["edmonton_rank"] = comp_ranks[0].text
            temp_dict["alberta_rank"] = comp_ranks[1].text
            temp_dict["percent_rank"] = comp_ranks[2].text
            temp_dict["ammenities_grade"] = self.driver.find_element(By.ID, "amenities-jmp").find_element(By.TAG_NAME,
                                                                                                          "i").text
            temp_dict["cost_of_living_percent"] = all_fact_boxes[0].find_element(By.TAG_NAME, "em").text
            temp_dict["crime_rate"] = all_fact_boxes[3].find_element(By.TAG_NAME, "em").text
            temp_dict["median_income"] = all_fact_boxes[6].find_element(By.TAG_NAME, "em").text
            temp_dict["in_labor_force"] = all_fact_boxes[7].find_element(By.TAG_NAME, "em").text
            temp_dict["unemployment_rate"] = all_fact_boxes[8].find_element(By.TAG_NAME, "em").text
            temp_dict["median_house_val"] = all_fact_boxes[9].find_element(By.TAG_NAME, "em").text
            temp_dict["home_owner_percent"] = all_fact_boxes[11].find_element(By.TAG_NAME, "em").text
            temp_dict["high_school_percent"] = all_fact_boxes[12].find_element(By.TAG_NAME, "em").text
            temp_dict["bach_degree"] = all_fact_boxes[13].find_element(By.TAG_NAME, "em").text
            temp_dict["test_scores"] = all_fact_boxes[14].find_element(By.TAG_NAME, "em").text

            self.driver.get(i + "demographics/")
            time.sleep(1)

            demo_table_tr = self.driver.find_element(By.CLASS_NAME, "av-default").find_elements(By.TAG_NAME, "tr")

            temp_dict["area_pop"] = demo_table_tr[1].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["pop_dense"] = demo_table_tr[2].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["med_age"] = demo_table_tr[3].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["male_to_fem"] = demo_table_tr[4].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["marri_coup"] = demo_table_tr[5].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["fam_w_kids"] = demo_table_tr[6].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["eng_only"] = demo_table_tr[7].find_elements(By.TAG_NAME, "td")[1].text

            temp_dict["french_only"] = demo_table_tr[8].find_elements(By.TAG_NAME, "td")[1].text

            print(temp_dict)

            all_stats.append(temp_dict)
            print(f"{len(all_stats)}/{len(self.all_links)}")

        return all_stats

    def save_to_csv(self, all_info):

        # Takes all the information collected and saves it to a csv file

        df = pd.DataFrame(all_info)
        df.to_csv("data/neigh_data_Feb15_2023.csv", index=False)
