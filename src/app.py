from dotenv import load_dotenv
from utils.helpers import get_driver, login, switch_to_game_frame, get_bet
from betting_worker import BettingWorker

# Load environment variables from .env file
load_dotenv()

driver = get_driver()

login(driver)

switch_to_game_frame(driver)

bet = get_bet()

worker = BettingWorker(driver, bet)
worker.start_betting()

driver.quit()