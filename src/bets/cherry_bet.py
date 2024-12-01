from interfaces.bets_interface import BetsInterface
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class CherryBet(BetsInterface):
    def find_element(driver: WebDriver):        
        interactive_overlays = driver.find_elements(By.CLASS_NAME, "interactive-overlay--Rm6da")

        # Cherry overlay is the first interactive overlay
        return interactive_overlays[0]
    
    def get_clicks_multiplier(number_of_losses):
        return 2 ** number_of_losses
