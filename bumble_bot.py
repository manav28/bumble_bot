from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import os
import urllib.request as url
from uuid import uuid4
from getpass import getpass
import json

from buttons import buttons
from fields import fields

class BumbleBot():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(927, 1016)
        self.driver.set_window_position(993, 27)
        self.driver.get("https://bumble.com/get-started")
        sleep(5)
    
    def enter_text(self, xpath, text):
        element = self.driver.find_element_by_xpath(xpath)
        element.send_keys(text)
    
    def click(self, class_name=None, xpath=None):
        if class_name:
            element = self.driver.find_element_by_class_name(class_name)
        elif xpath:
            element = self.driver.find_element_by_xpath(xpath)
        
        element.click()
    
    def login(self, store_credentials=False):
        try:
            with open('../secrets.json', 'r') as f:
                secrets = json.load(f)
                phone_number = secrets["phone_number"]
                password = secrets["password"]

        except FileNotFoundError:
            secrets = {}
            phone_number = input("Enter phone number: ")
            secrets["phone_number"] = phone_number
            password = getpass("Enter password: ")
            secrets["password"] = password
            if store_credentials:
                with open('../secrets.json', 'w') as f:
                    json.dump(secrets, f)

        # Phone number button
        phone_number_button = buttons["phone_number"]
        self.click(xpath=phone_number_button)

        # Enter phone number
        phone_number_field = fields["phone_number_field"]
        self.enter_text(phone_number_field, phone_number)

        # Continue button
        continue_button = buttons["continue_button"]
        self.click(xpath=continue_button)
        sleep(2)

        # Enter Password
        password_field = fields["password_field"]
        self.enter_text(password_field, password)

        # Sign In!
        sign_in_button = buttons["sign_in"]
        self.click(xpath=sign_in_button)
    
    def like(self, save=False):
        like = buttons["like"]
        if save:
            self.save_images("likes")
        self.click(class_name=like)
    
    def dislike(self, save=False):
        dislike = buttons["dislike"]
        if save:
            self.save_images("dislikes")
        self.click(class_name=dislike)
    
    def generate_folder_name(self):
        class_name = "encounters-story-profile__name"
        text = self.driver.find_element_by_class_name(class_name).text
        text = text.replace(' ', '')
        name, age = text.split(',')
        uid = uuid4().hex
        folder_name = name + '_' + uid
        return folder_name

    def save_images(self, label=""):
        class_name = "media-box__picture-image"
        images = self.driver.find_elements_by_class_name(class_name)

        image_number = 1
        folder_name = self.generate_folder_name()
        os.mkdir(os.path.join(label, folder_name))

        for img in images:
            src = img.get_attribute("src")
            path = os.path.join(label, folder_name, "image_" + str(image_number) + ".png")
            url.urlretrieve(src, path)
            image_number += 1
    
    def logout(self):
        # Profile icon
        profile_icon = buttons["profile_icon"]
        self.click(xpath=profile_icon)
        sleep(1)

        # Logout button
        logout_button = buttons["logout"]
        self.click(xpath=logout_button)
        sleep(1)

        # Confirm logout
        confirm_logout = buttons["confirm_logout"]
        self.click(xpath=confirm_logout)
        sleep(3)

        self.driver.close()

if __name__ == "__main__":
    bot = BumbleBot()
    bot.login()
    sleep(5)
    while True:
        try:
            bot.like()
        except NoSuchElementException:
            bot.driver.refresh()
        sleep(2)