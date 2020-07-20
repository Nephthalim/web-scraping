class Television:
    def __init__(self, names, priceValue,rating):
        self.names = names
        self.priceValue = priceValue
        self.rating = rating


def find_rating(ratings):
    rating = []
    for i in ratings:
        full_stars = i.find_elements_by_class_name("fullStar_365cI")
        half_stars = i.find_elements_by_class_name("halfStar_2QJ5U")
        rating.append(len(half_stars)/2+len(full_stars))
    return(rating)


def show_more_items(driver, show_more, time):
    i = 0
    while i < 10:
        show_more.click()
        time.sleep(5)
        show_more = driver.find_element_by_class_name("button_2Xgu4")
        i += 1
    return None


def append_data(data, title, tv):
    data[title].append({
        "name": tv.names.text,
        "price": float(tv.priceValue.get_attribute("content")),
        "rating": tv.rating
    })
    return(data)

def clean_up(num_page_names,names):
    a = []
    for i in range(num_page_names):
        if names[i].text != "":
            b = names[i].text.replace(" ", "")
            b = b.replace("\n", "")
            a.append(b)
    a = list(dict.fromkeys(a))
    return (a)