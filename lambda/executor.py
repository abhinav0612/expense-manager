
from argparse import Action
import constants as Constants
from constants import Action
from utils import (
    get_action_type,
    handle_expense_command,
    handle_summary_command,
    handle_analysis_command,
    handle_trends_command
)



def execute(event):
    try:
        action_to_handler = {
            Action.SUMMARY: handle_summary_command,
            Action.TRENDS: handle_trends_command,
            Action.ANALYSIS: handle_analysis_command,
            Action.EXPENSE: handle_expense_command,
        }

        message_id = '1111'
        replied_to_message_id = None
        user_id = '12345'
        user_command = 'clothes#shopping$2000@04-09-2022'
        source = 'Telegram'

        action = get_action_type(user_command)
        action_to_handler[action](user_command, user_id, message_id, replied_to_message_id, source)
    except Exception as e:
        print(f'Exception occured in execute. Error: {e}')