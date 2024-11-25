from unicodedata import digit
from attr import NOTHING
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

class BettingWorker:
    def _login(self):
        # Find the login form element by id
        loginForm = self.driver.find_element(By.ID, "login-modal-component__title")

        # Check if the login form is displayed
        if loginForm:
            # Find the username input element by id
            username_input = self.driver.find_element(By.ID, "txtUsername")

            # Get the username from the environment variable
            username = os.getenv("USERNAME")

            # Enter the username
            username_input.send_keys(username)

            # Find the password input element by id
            password_input = self.driver.find_element(By.ID, "txtPassword")

            # Get the password from the environment variable
            password = os.getenv("PASSWORD")

            # Enter the password
            password_input.send_keys(password)

            # Find the button element using XPath
            button = self.driver.find_element(
                By.XPATH,
                "//button[contains(@class, 'login-modal-component__login-button') and @type='submit']"
            )

            # Click the button
            button.click()
            
            # Delay for 10 seconds
            time.sleep(10)


    def _switch_to_game_frame(self):
        # Find game frame element by class name and switch to it
        game_frame = self.driver.find_element(By.CLASS_NAME, "inline-games-page-component__game-frame")
        self.driver.switch_to.frame(game_frame)
        self.driver.switch_to.frame(0)

    def _waiting_for_next_round(self):
        dealer_message_text = self.driver.find_element(By.CLASS_NAME, "dealer-message-text")

        # If container text contains "Wait" return true
        if dealer_message_text.text == "":
            return False
        
        return True

    def _find_cherry(self):
        interactive_overlays = self.driver.find_elements(By.CLASS_NAME, "interactive-overlay--Rm6da")

        # Cherry overlay is the first interactive overlay
        return interactive_overlays[0]

    def _deposit(self):
        cherry = self._find_cherry()
        cherry.click()

    def _get_driver(self):
        # Set up the WebDriver
        driver = webdriver.Chrome()
        driver.get("https://livecasino.bet365.com/Play/SuperMegaUltra")
        return driver

    def start_betting(self):
        # Set up the WebDriver
        self.driver = self._get_driver()

        self._login()

        self._switch_to_game_frame()

        while self._waiting_for_next_round():
            time.sleep(1)

        # Wait one second after waiting ends so the new round can start
        time.sleep(1)
        self._deposit()
        
        while not self._waiting_for_next_round():
            time.sleep(1)

        self.driver.quit()
