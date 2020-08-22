import json, time
from functions import Television,append_data,find_rating,search_tv,show_more_items
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

start_time = time.time()

tele = Television(None, None, None)

driver = webdriver.Firefox()
driver.get("https://www.bestbuy.ca/en-ca")

search_tv(driver)
show_more_items(driver)
print("----- Showing More Items")


names = driver.find_elements_by_class_name("productItemName_3IZ3c")
priceValue = driver.find_elements_by_xpath("//meta[@itemprop='price']")
ratings = driver.find_elements_by_class_name("starRateContainer_3dnAH")


rating =find_rating(ratings)
print("----- Finding Ratings")

tele = Television(names, priceValue, rating)
num_page_names = len(tele.names)


with open("results.json", "w") as json_file:
    data = {}
    data["TV's"] = []
    data["Cheapest TV"] = []
    data["Best Rated TV"] = []
    min_price = 99999
    max_rating = 0
    # clean up any repeated items
    print("----- Cleaning up")
    cleaned = tele.clean_up(num_page_names)
    

    j = 0
    k = 0
    tv = []
    print("----- Appending Data")
    for i in range(len(cleaned)-1):
        if names[i].text != "":
            tv.append(Television(
                tele.names[i], tele.priceValue[i], tele.rating[i]))
            if float(priceValue[i].get_attribute("content")) < min_price:
                min_price = float(priceValue[i].get_attribute("content"))
                j = len(tv)-1
            if rating[i] > max_rating:
                max_rating = rating[i]
                k = len(tv)-1
            append_data(data, "TV's", tv[len(tv)-1])

    append_data(data, "Cheapest TV", tv[j])
    append_data(data, "Best Rated TV", tv[k])

    json.dump(data, json_file, sort_keys=True, indent=2)

driver.close()

print("----- {:.2f} seconds".format(time.time() - start_time))
