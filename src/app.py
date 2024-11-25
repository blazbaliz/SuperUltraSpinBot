from dotenv import load_dotenv

from betting_worker import BettingWorker

# Load environment variables from .env file
load_dotenv()

worker = BettingWorker()
worker.start_betting()