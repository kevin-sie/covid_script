from selenium import webdriver
import time
from calendar_setup import create_event


def get_creds():
    file = open("credentials.txt", "r")
    user = file.readline()
    user_pass = file.readline()
    file.close()
    return user.strip(), user_pass


def login(creds):
    global driver
    driver = webdriver.Chrome()
    driver.get('https://uma.force.com/campushealth/login')
    time.sleep(3)
    email = driver.find_element_by_id("i0116")
    email.send_keys(creds[0])
    next_btn = driver.find_element_by_id("idSIButton9")
    next_btn.click()
    time.sleep(3)
    password = driver.find_element_by_id("i0118")
    password.send_keys(creds[1])
    password.submit()
    time.sleep(2)
    stay_signed_in = driver.find_element_by_id("idSIButton9")
    stay_signed_in.click()


def reserve(location, day):
    time.sleep(5)
    radios = driver.find_elements_by_class_name("slds-radio--faux")
    radios[location].click()  # choose walk-in at Mullins
    radios[day].click()  # choose Monday option *NEED TO ADD FRIDAY OPTION*
    driver.find_elements_by_css_selector("button[title='Next']")[0].click()
    time.sleep(5)
    driver.find_elements_by_class_name("slds-radio--faux")[8].click()  # should choose the 9th option (1:00 PM)
    driver.find_elements_by_css_selector("button[title='Next']")[0].click()
    date_text = driver.find_elements_by_css_selector("div[dir='ltr']")[16].text
    # the text is time option (^ prev comment) + 8
    time.sleep(5)
    driver.find_element_by_css_selector("button[title='Finish']").click()
    return date_text


def reserve_appt():
    location = 0
    day_one = 8  # 8 = Monday
    day_two = 12  # 12 = Friday
    return reserve(location, day_one), reserve(location, day_two)


# def symptom_check():
#     driver.find_element_by_css_selector()


def main():
    login(get_creds())
    res = reserve_appt()
    for reservation in res:
        create_event(reservation)


if __name__ == "__main__":
    main()
