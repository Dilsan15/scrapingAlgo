import os
from houseScraper import postingScraper
from neighScraper import neighScraper


# Filters to be used for scraping, need these to get maxium results
MAJOR_FILTER_OPTIONS = {

    "Property-Type": ["Single Family", "Condo / Townhouse"],

    "Property-Sub-Type": ["Residential Detached Single Family", "Lowrise Apartment", "Half Duplex", "Townhouse",
                          "Apartment High Rise", "Residential Attached", "Carriage", "4PLEX", "Duplex Side By Side",
                          "Detached Condominium", "Detached Single Family", "Stacked Townhouse",
                          "Duplex Front and Back", "Duplex Up And Down", "Tri-Plex"],

    "Property-Style": ["Bungalow", "Bi-Level", "Split Level", "1 and Half Storey", "2 Storey", "2+ Stories",
                       "Single Level Apartment", "Multi Level Apartment", "Loft", "Penthouse", ]

}

# Initate class which is located in other file, and pass in the filter options/ other parameters

PostingScraper = postingScraper(post_needed=10, driver_path=os.environ["DRIVER_PATH_ENV"], time_out=3, browser_vis=True,
                                filter_options=MAJOR_FILTER_OPTIONS)

# True indicates that it will scrape that section

scrape_web = True
scrape_neigh = True

# Code to scrape the edmontonrealestatepro, I used multiple if and for loops to get all the possible combinations of the
# filters

if scrape_web:

    scraping_list = list()

    for pst in range(len(MAJOR_FILTER_OPTIONS["Property-Sub-Type"])):

        for ps in range(len(MAJOR_FILTER_OPTIONS["Property-Style"])):
            print(MAJOR_FILTER_OPTIONS["Property-Sub-Type"][pst], end=" ")
            print(MAJOR_FILTER_OPTIONS["Property-Style"][ps], end=" ")

            PostingScraper.prepare_page()

            if PostingScraper.adjust_filters(pst, ps):
                PostingScraper.get_posting_links()
                scraping_list.extend(PostingScraper.scrape_posting())


            else:
                pass

    PostingScraper.save_csv(scraping_list)

    print("Done House Scraping")

# Start neigh scraper after done house scraping

if scrape_neigh:
    neighScraper = neighScraper(driver_path=os.environ["DRIVER_PATH_ENV"])
    neighScraper.get_neigh_links()

    neighScraper.save_to_csv(neighScraper.get_neigh_stats())

    print("Done Neigh Scraping")


