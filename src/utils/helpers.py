from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from bets.cherry_bet import CherryBet
import time
import os

def get_driver():
    # Set up the WebDriver
    driver = webdriver.Chrome()
    driver.get(os.getenv("GAME_URL"))
    return driver

def login(driver: WebDriver):
    # Find the login form element by id
    loginForm = driver.find_element(By.ID, "login-modal-component__title")

    # Check if the login form is displayed
    if loginForm:
        # Find the username input element by id
        username_input = driver.find_element(By.ID, "txtUsername")

        # Get the username from the environment variable
        username = os.getenv("USERNAME")

        # Enter the username
        username_input.send_keys(username)

        # Find the password input element by id
        password_input = driver.find_element(By.ID, "txtPassword")

        # Get the password from the environment variable
        password = os.getenv("PASSWORD")

        # Enter the password
        password_input.send_keys(password)

        # Find the button element using XPath
        button = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'login-modal-component__login-button') and @type='submit']"
        )

        # Click the button
        button.click()
        
        # Delay for 10 seconds
        time.sleep(10)

def switch_to_game_frame(driver: WebDriver):
        # Find game frame element by class name and switch to it
        game_frame = driver.find_element(By.CLASS_NAME, "inline-games-page-component__game-frame")
        driver.switch_to.frame(game_frame)
        driver.switch_to.frame(0)

def get_bet():
    bet_type = os.getenv("BETTING_TYPE")
    switcher = {
        'CHERRY_BET': CherryBet
    }
    return switcher.get(bet_type, "Invalid bet type")