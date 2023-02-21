import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class postingScraper:

    def __init__(self, post_needed, driver_path, time_out, browser_vis, filter_options):

        # Basic setup

        self.post_needed = post_needed
        self.time_out = time_out
        self.filter_options = filter_options
        self.links_collected = []
        self.links_scraped = []

        sel_service = Service(driver_path)
        option = webdriver.ChromeOptions()

        option.add_argument('--deny-permission-prompts')
        option.add_argument('--disable-geolocation')

        if not browser_vis:
            option.add_argument("--headless")
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/108.0.0.0 Safari/537.36 '
            option.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(service=sel_service, options=option)
        self.driver.maximize_window()

    def prepare_page(self):

        # Go to the page and click the search button

        self.driver.get("https://www.edmontonrealestate.pro/")
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, "quick-search__button--submit").click()

    def adjust_filters(self, *iter):
        # adjust the filters on the website

        self.driver.find_element(By.CLASS_NAME, "hybrid__button--filter").click()
        filter_op = self.driver.find_element(By.CLASS_NAME, "filter")

        time.sleep(2)

        all_fields = self.driver.find_element(By.CLASS_NAME, "filter__fields")

        for field in all_fields.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')[::-1]:

            if field.is_selected():
                field.click()
                time.sleep(1)

        self.driver.execute_script("arguments[0].scrollTo(0, 0);", filter_op)
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollTo(0, 300);", filter_op)
        time.sleep(1)

        try:

            for type in self.filter_options['Property-Type']:
                prop_type_fil = self.driver.find_element(By.CSS_SELECTOR, f"input[value='{type}']")
                prop_type_fil.click()
                time.sleep(2)

            prop_style = all_fields.find_element(By.CSS_SELECTOR,
                                                 f"input[value='{self.filter_options['Property-Style'][iter[1]]}']")
            prop_style.click()
            time.sleep(2)

            prop_sub_type = all_fields.find_element(By.CSS_SELECTOR,
                                                    f"input[value='{self.filter_options['Property-Sub-Type'][iter[0]]}']")
            prop_sub_type.click()
            time.sleep(2)

            self.driver.find_element(By.CLASS_NAME, "filter__actions").find_elements(By.TAG_NAME, "button")[1].click()
            time.sleep(4)

            return True


        except Exception as e:
            print(e)

    def get_posting_links(self):

        # Scroll down and collect the links of the postings

        def adjust_filters(self, *iter):

            self.driver.find_element(By.CLASS_NAME, "hybrid__button--filter").click()
            filter_op = self.driver.find_element(By.CLASS_NAME, "filter")

            time.sleep(2)

            all_fields = self.driver.find_element(By.CLASS_NAME, "filter__fields")

            for field in all_fields.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')[::-1]:

                if field.is_selected():
                    field.click()
                    time.sleep(1)

            self.driver.execute_script("arguments[0].scrollTo(0, 0);", filter_op)
            time.sleep(2)
            self.driver.execute_script("arguments[0].scrollTo(0, 300);", filter_op)
            time.sleep(1)

            try:

                for type in self.filter_options['Property-Type']:
                    prop_type_fil = self.driver.find_element(By.CSS_SELECTOR, f"input[value='{type}']")
                    prop_type_fil.click()
                    time.sleep(2)

                prop_style = all_fields.find_element(By.CSS_SELECTOR,
                                                     f"input[value='{self.filter_options['Property-Style'][iter[1]]}']")
                prop_style.click()
                time.sleep(2)

                prop_sub_type = all_fields.find_element(By.CSS_SELECTOR,
                                                        f"input[value='{self.filter_options['Property-Sub-Type'][iter[0]]}']")
                prop_sub_type.click()
                time.sleep(2)

                self.driver.find_element(By.CLASS_NAME, "filter__actions").find_elements(By.TAG_NAME, "button")[
                    1].click()
                time.sleep(4)

                return True


            except Exception as e:
                print(e)

        while True:

            self.links_collected.extend([hidLink.get_attribute("href") for hidLink in
                                         self.driver.find_elements(By.CLASS_NAME, "hybrid__teaser__card")])

            self.links_collected = list(set(self.links_collected))

            try:

                load_more = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div/section[1]/div[3]/button')

                self.go_to_element(load_more.location_once_scrolled_into_view,
                                   self.driver.find_element(By.CLASS_NAME, "filter"), -10)

                time.sleep(1)

                load_more.click()


            except:
                print(f"# of links collected == {len(self.links_collected)}")
                break

    def scrape_posting(self):

        # go thourgh the links collected and scrape the data

        all_info = []

        for link in self.links_collected:

            if link not in self.links_scraped:
                self.driver.get(link)

                try:

                    temp_dic = {}

                    temp_dic["Link"] = link

                    temp_dic["House Description"] = \
                        self.driver.find_element(By.CLASS_NAME, "block--lightest").find_element(By.TAG_NAME, "p").text

                    for i in self.driver.find_elements(By.TAG_NAME, "tbody"):

                        for j in i.find_elements(By.TAG_NAME, "tr"):
                            temp_dic[j.find_element(By.TAG_NAME, "th").text] = j.find_element(By.TAG_NAME, "td").text

                    all_info.append(temp_dic)
                    self.links_scraped.append(link)
                    self.links_collected.remove(link)


                except:
                    pass

            self.links_scraped.extend(link)

        return all_info

    def go_to_element(self, web_element_locations, slide_element, adj):

        # Scrolls to the element specified, with an adjustment. Reduced redundancy in class methods

        self.driver.execute_script(
            f"arguments[0].scrollTo({web_element_locations['x']}, {int(web_element_locations['y']) + (adj)})",
            slide_element
        )

    def save_csv(self, data):
        # Saves the data to a csv file
        df = pd.DataFrame(data)
        df.to_csv(f'data/edmonton_housing_data_Feb15_2023.csv', mode='w', index=False)
