
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from interfaces.bets_interface import BetsInterface
import time
import os

class BettingWorker:

    def __init__(self, driver: WebDriver, bet: BetsInterface):
        self._bet = bet
        self.driver = driver
        
    def _can_place_bets(self):
        try:
            dealer_message = self.driver.find_element(By.CLASS_NAME, "game-table__controls-panel-centered")

            # If container text contains "Place your bets" return true
            if "PLACE YOUR BETS" in dealer_message.text:
                return True
            
            return False
        except:
            return False

    def _deposit(self):
        betting_element = self._bet.find_element(self.driver)

        # Calculate the number of clicks based on the number of losses
        clicks = self._bet.get_clicks_multiplier(self._nmbr_of_loses)
        print("number of clicks: ", clicks)
        for _ in range(clicks):
            betting_element.click()
            time.sleep(0.02)
            print("Clicking on betting element")

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

        # Click the first chip
        chips[int(os.getenv("CHIP_INDEX"))].click()

    def start_betting(self):

        self._balance = self._get_balance()
        self._nmbr_of_loses = 0

        while not self._can_place_bets():
            time.sleep(1)
        
        time.sleep(1)
        self._set_chip_level()

        while True:
            # While placing bets is not possible, wait
            while not self._can_place_bets():
                time.sleep(1)
            
            self._check_new_round_data()  

            # Wait one second after waiting ends so the new round can start
            time.sleep(1)
            
            self._deposit()
            
            # Wait for the new round to start
            while self._can_place_bets():
                time.sleep(1)
