import json,time
from functions import show_more_items, append_data, Television, find_rating, clean_up
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Firefox()
driver.get("https://www.bestbuy.ca/en-ca")
search_bar = driver.find_element_by_name("search")

search_bar.send_keys("TV")
search_button = driver.find_element_by_class_name("searchButton_T4-BG")
search_button.click()

WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
    (By.CLASS_NAME, "productItemName_3IZ3c")))

time.sleep(5)
show_more = driver.find_element_by_class_name("button_1Yg9v")

# click show more
show_more_items(driver, show_more, time)


names = driver.find_elements_by_class_name("productItemName_3IZ3c")
time.sleep(10)
ratings = driver.find_elements_by_class_name("container_SSA6h")
priceValue = driver.find_elements_by_xpath("//meta[@itemprop='price']")

time.sleep(10)

num_page_names = len(names)

# get the ratings
rating = find_rating(ratings)
time.sleep(10)

with open("results.json", "w") as json_file:
    data = {}
    data["TV's"] = []
    data["Cheapest TV"] = []
    data["Best Rated TV"] = []
    min_price = 99999
    max_rating = 0


    # clean up any repeated items
    a = clean_up(num_page_names, names)

    j = 0
    k = 0
    tv = []
    for i in range(len(a)):
        if names[i].text != "":
            tv.append(Television(names[i], priceValue[i], rating[i]))
            if float(priceValue[i].get_attribute("content")) < min_price:
                min_price = float(priceValue[i].get_attribute("content"))
                j = i

            if rating[i] > max_rating:
                max_rating = rating[i]
                k = i
            # append data to dictionary
            append_data(data, "TV's", tv[i])

    append_data(data, "Cheapest TV", tv[j])
    append_data(data, "Best Rated TV", tv[k])

    json.dump(data, json_file, sort_keys=True, indent=2)

driver.close()
