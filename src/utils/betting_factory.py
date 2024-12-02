
import os
from bets.cherry_bet import CherryBet

def get_bet():
    bet_type = os.getenv("BETTING_TYPE")
    switcher = {
        'CHERRY_BET': CherryBet
    }
    return switcher.get(bet_type, "Invalid bet type")