import os
import logging
from time import sleep

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from helper.timer import timer

PATH_TO_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "download")


class SysthagLib(ABC):
    """
    The SysthagLib Class defines a template method that contains a skeleton of
    some algorithm, composed of calls to (usually) abstract primitive
    operations.

    Concrete subclasses should implement these operations, but leave the
    template method itself intact.
    """

    def template_method(self, get_url, execution, personal_information) -> None:
        """
        The template method defines the skeleton of an algorithm.
        """
        browser = self.selenium_options(execution)
        self.polytech_douala(browser, get_url)
        self.pre_registration_step_1(browser)
        self.pre_registration_step_2(browser, personal_information)
        self.pre_registration_step_3(browser)

    # These operations already have implementations.

    @timer
    def selenium_options(self, execution) -> webdriver:
        logging.info('settings options for selenium...')
        preferences = {"download.default_directory": PATH_TO_DOWNLOAD_FOLDER,
                       "safebrowsing.enabled": True,
                       "directory_upgrade": True}

        chrome_options = Options()
        useragent = UserAgent()

        chrome_options.add_experimental_option("prefs", preferences)
        chrome_options.add_argument(f'user-agent={useragent}')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--no-sandbox")

        chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.headless = True

        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        if execution == 'headless':
            logging.info('running bot in headless mode')
            chrome_options.add_argument("--" + execution)
            browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            browser.set_window_size(1920, 1080)
            browser.maximize_window()
            return browser
        elif execution == 'interface':
            logging.info('running bot in ui mode')
            browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            return browser
        else:
            logging.error(f'{execution} is not currently supported. Please choose between interface or headless.')
            raise ValueError(f'{execution} is not currently supported')

    def polytech_douala(self, browser, get_url) -> None:
        logging.info('home page...')
        browser.get(get_url)
        sleep(3)

        logging.info('pre-registration...')
        pre_registration = browser.find_element_by_link_text("PREINSCRIPTION")
        pre_registration.click()
        sleep(3)

        logging.info('select polytech douala University...')
        polytech = browser.find_element_by_id("j_idt80:7:ecol")
        polytech.click()
        print("AbstractClass says: I am doing the bulk of the work")

    def pre_registration_step_1(self, browser) -> None:
        logging.info('preregistration page STEP1: General terms and conditions of use...')
        sleep(4)
        btn_next = browser.find_element_by_id('boutNext')
        btn_next.click()

    def pre_registration_step_2(self, browser, personal_information) -> None:
        logging.info('preregistration page STEP2: Personal information...')
        logging.info(f'personal information: {personal_information}')
        lastname = str(personal_information['lastname'])
        firstname = str(personal_information['firstname'])
        birthday = str(personal_information['birthday'])
        birthplace = str(personal_information['birthplace'])
        phone_number = str(personal_information['phone_number'])
        city_of_residence = str(personal_information['city_of_residence'])
        sleep(4)

        lastname_btn = browser.find_element_by_name('name')
        lastname_btn.clear()
        lastname_btn.send_keys(lastname)
        sleep(2)

        firstname_btn = browser.find_element_by_name('surname')
        firstname_btn.clear()
        firstname_btn.send_keys(firstname)
        sleep(2)

        birthday_btn = browser.find_element_by_name('date_input')
        birthday_btn.clear()
        birthday_btn.send_keys(birthday)
        sleep(2)

        birthplace_btn = browser.find_element_by_name('lieuNaiss')
        birthplace_btn.clear()
        birthplace_btn.send_keys(birthplace)
        sleep(2)

        city_of_residence_btn = browser.find_element_by_name('villeResid')
        city_of_residence_btn.clear()
        city_of_residence_btn.send_keys(city_of_residence)
        sleep(2)

        phone_number_btn = browser.find_element_by_name('phone')
        phone_number_btn.clear()
        phone_number_btn.send_keys(phone_number)
        sleep(2)

        btn_next = browser.find_element_by_id('boutNext')
        btn_next.click()
        sleep(60)

    def pre_registration_step_3(self, browser):
        logging.info('preregistration page STEP3: Education...')
    # These operations have to be implemented in subclasses.

    # @abstractmethod
    # def required_operations1(self) -> None:
    #     pass
    #
    # @abstractmethod
    # def required_operations2(self) -> None:
    #     pass

    # These are "hooks." Subclasses may override them, but it's not mandatory
    # since the hooks already have default (but empty) implementation. Hooks
    # provide additional extension points in some crucial places of the
    # algorithm.

    # def hook1(self) -> None:
    #     pass
    #
    # def hook2(self) -> None:
    #     pass
