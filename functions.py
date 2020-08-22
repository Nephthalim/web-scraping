
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Television:
    def __init__(self, names, priceValue, rating):
        self.names = names
        self.priceValue = priceValue
        self.rating = rating
    def clean_up(self, num_page_names):
        
        a = []
        for i in range(num_page_names):
            if self.names[i].text != "":
                # print("Cleaing {}".format(i))
                b = self.names[i].text.replace(" ", "")
                b = b.replace("\n", "")
                a.append(b)
        a = list(dict.fromkeys(a))
        return (a)

def search_tv(driver):
    search_bar = driver.find_element_by_name("search")
    search_bar.send_keys("TV")
    search_button = driver.find_element_by_class_name("searchButton_T4-BG")
    search_button.click()

def find_rating(ratings):
    rating = []
    for i in ratings:
        full_stars = i.find_elements_by_class_name("fullStar_365cI")
        half_stars = i.find_elements_by_class_name("halfStar_2QJ5U")
        rating.append(len(half_stars)/2+len(full_stars))
    return(rating)

def show_more_items(driver):
    i = 0
    try:
        while i < 10:
            show_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "loadMore_3AoXT")))

            show_more.click()
            i += 1
    except ElementClickInterceptedException:
        show_more_items(driver)
    return None

def append_data(data, title, tv):
    data[title].append({
        "name": tv.names.text,
        "price": float(tv.priceValue.get_attribute("content")),
        "rating": tv.rating
    })
    return(data)


