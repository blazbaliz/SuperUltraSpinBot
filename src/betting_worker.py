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

    def _can_place_bets(self):
        try:
            dealer_message = self.driver.find_element(By.CLASS_NAME, "game-table__controls-panel-centered")

            # If container text contains "Place your bets" return true
            if "PLACE YOUR BETS" in dealer_message.text:
                return True
            
            return False
        except:
            return False


    def _find_cherry(self):
        interactive_overlays = self.driver.find_elements(By.CLASS_NAME, "interactive-overlay--Rm6da")

        # Cherry overlay is the first interactive overlay
        return interactive_overlays[0]

    def _deposit(self):
        cherry = self._find_cherry()

        # Calculate the number of clicks based on the number of losses
        clicks = 2 ** self._nmbr_of_loses
        print("number of clicks: ", clicks)
        for _ in range(clicks):
            cherry.click()
            time.sleep(0.05)
            print("Clicking cherry")

    def _get_driver(self):
        # Set up the WebDriver
        driver = webdriver.Chrome()
        driver.get("https://livecasino.bet365.com/Play/SuperMegaUltra")
        return driver
    
    def _get_balance(self):
        balance = self.driver.find_element(By.CLASS_NAME, "balance__value")
        return balance.text

    def _check_new_round_data(self):  
        new_balance = self._get_balance()

        if new_balance >= self._balance:
            self._nmbr_of_loses = 0
        else:
            self._nmbr_of_loses += 1
        print("Number of losses: ", self._nmbr_of_loses)

        self._balance = new_balance

    def _set_chip_level(self):
        # Find the chip level element by class name
        chips = self.driver.find_elements(By.CLASS_NAME, "chip__label")
        chips[0].click()
        print(chips)

    def start_betting(self):
        # Set up the WebDriver
        self.driver = self._get_driver()

        self._login()

        self._switch_to_game_frame()

        self._balance = self._get_balance()
        self._nmbr_of_loses = 0

        while not self._can_place_bets():
            time.sleep(1)
        
        time.sleep(1)
        self._set_chip_level()

        while True:
            while not self._can_place_bets():
                time.sleep(1)
            
            self._check_new_round_data()  

            # Wait one second after waiting ends so the new round can start
            time.sleep(1)
            self._deposit()
            
            while self._can_place_bets():
                time.sleep(1)
        
        # this is currently uncallable
        self.driver.quit()
