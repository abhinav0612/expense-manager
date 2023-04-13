import constants as Constants

from datetime import datetime, timedelta

from constants import ExpenseAction
from network import make_api_call

def get_text_before_symbol(original_text):
    try:
        symbols = ['@', '$', '#']
        break_point = -1
        for index, char in enumerate(original_text):
            if char in symbols:
                break_point = index
                break
        if break_point != -1:
            return original_text[:break_point]
        return original_text
    except Exception as e:
        print(f'Exception occured in get_text_before_symbol. Error: {e}')


def get_param_value(expense_text, separator_symbol):
    try:
        splitted_text_list = expense_text.split(separator_symbol)
        if len(splitted_text_list) > 1:
            return get_text_before_symbol(splitted_text_list[1])
    except Exception as e:
        print(f'Exception occured in get_param_value. Error: {e}')


def get_expense_params(expense_text):
    expense_params = {}
    try:
        expense_params['amount'] = get_param_value(expense_text, '$')
        expense_params['category'] = get_param_value(expense_text, '#')
        expense_params['description'] = get_text_before_symbol(expense_text)
        expense_params['expense_date'] = get_param_value(expense_text, '@')
    except Exception as e:
        print(f'Exception occured in get_expense_params. Error: {e}')
        expense_params['error'] = True
    return expense_params


def check_date_format(date_str):
    valid_date = False
    try:
        datetime_obj = datetime.strptime(date_str, '%d-%m-%Y')
        valid_date = True
    except:
        pass
    return valid_date


def get_action_type(user_text):
    try:
        if user_text.startswith('summary'):
            return Constants.Action.SUMMARY
        elif user_text.startswith('trends'):
            return Constants.Action.TRENDS
        elif user_text.startswith('analysis'):
            return Constants.Action.ANALYSIS
        else:
            return Constants.Action.EXPENSE
    except Exception as e:
        print(
            f'Exception occured in get_action_type. Error: {e}')
    
def get_expense_action_type(user_command, replied_to_message_id):
    try:
        if replied_to_message_id:
            if user_command.startswith('delete'):
                return Constants.ExpenseAction.DELETE
            else:
                return Constants.ExpenseAction.UPDATE
        else:
            return Constants.ExpenseAction.ADD
    except Exception as e:
        print(
            f'Exception occured in get_expense_action_type. Error: {e}')


def get_start_and_end_date_for_sumary(user_command):
    results = {
        "start_date_str": None,
        "end_date_str": None
    }
    duration_phase = None    # current or last
    duration_type = None     # day, week, month or year
    start_date = None
    end_date = None
    try:
        args = user_command.split(' ')
        if len(args) == 2:
            if args[1] == 'today':
                duration_phase = 'current'
                duration_type = 'day'
            elif args[1] == 'yesterday':
                duration_phase = 'last'
                duration_type = 'day'
        elif len(args) == 3:
            if args[1] in ['last', 'current']:
                if args[2] in ['day', 'week', 'month', 'year']:
                    duration_phase = args[1]
                    duration_type = args[2]
        elif len(args) == 5:
            if args[1] == 'from' and args[3] == 'to':
                if check_date_format(args[2]) and check_date_format(args[4]):
                    start_date = args[2]
                    end_date = args[4]
                else:
                    results['error'] = "Start and End date format incorrect."
                    return results
        if duration_phase and duration_type:
            current_date = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0)
            if duration_type == 'day':
                if duration_phase == 'current':
                    start_date = current_date
                    end_date = current_date
                else:
                    start_date = current_date - timedelta(days=1)
                    end_date = current_date - timedelta(seconds=1)
            elif duration_type == 'week':
                if duration_phase == 'current':
                    start_date = current_date - \
                        timedelta(days=current_date.weekday())
                    end_date = start_date + timedelta(days=6)
                else:
                    start_date = current_date - \
                        timedelta(days=current_date.weekday() + 7)
                    end_date = current_date - \
                        timedelta(days=current_date.weekday() + 1)
            elif duration_type == 'month':
                if duration_phase == 'current':
                    start_date = current_date.replace(day=1)
                    end_date = start_date.replace(year=current_date.year + 1, month=1) - timedelta(
                        days=1) if current_date.month == 12 else start_date.replace(month=start_date.month + 1) - timedelta(days=1)
                else:
                    start_date = current_date.replace(
                        year=current_date.year - 1, month=12) if current_date.month == 1 else current_date.replace(month=current_date.month - 1, day=1)
                    end_date = current_date.replace(day=1) - timedelta(days=1)
            else:
                if duration_phase == 'current':
                    start_date = current_date.replace(month=1, day=1)
                    end_date = start_date.replace(month=12, day=31)
                else:
                    start_date = datetime(
                        year=current_date.year - 1, month=1, day=1)
                    end_date = start_date.replace(month=12, day=31)
            results['start_date_str'] = start_date.strftime(
                Constants.DATE_TIME_FORMATTER)
            results['end_date_str'] = end_date.strftime(
                Constants.DATE_TIME_FORMATTER)
        elif start_date and end_date:
            results['start_date_str'] = start_date
            results['end_date_str'] = end_date
        else:
            results['error'] = "Invalid command."
    except Exception as e:
        print(
            f'Exception occured in get_start_and_end_date_for_sumary. Error: {e}')
    return results


def handle_expense_command(command, user_id, message_id, replied_to_message_id, source):
    try:
        expense_action = get_expense_action_type(command, replied_to_message_id)
        url = Constants.BASE_URL + '/expense/'
        headers = {'Content-Type': 'application/json'}
        if expense_action == ExpenseAction.ADD:
            expense_params = get_expense_params(command)
            body = {'user_id': user_id, 'message_id': message_id, 'source': source, **expense_params}
            resp = make_api_call(url=url, headers=headers, method='POST', data=body)
        elif expense_action == ExpenseAction.UPDATE:
            expense_params = get_expense_params(command)
            body = {'user_id': user_id, 'message_id': replied_to_message_id, **expense_params}
            resp = make_api_call(url=url, headers=headers, method='PATCH', data=body)
        elif expense_action == ExpenseAction.DELETE:
            body = {'user_id': user_id, 'message_id': replied_to_message_id}
            resp = make_api_call(url=url, headers=headers, method='DELETE', data=body)
        print(resp)
    except Exception as e:
        print(f'Exception occured in handle_expense_command. Error: {e}')

def handle_trends_command(command, user_id, message_id, replied_to_message_id, source):
    try:
        ...
    except Exception as e:
        print(f'Exception occured in handle_trends_command. Error: {e}')

def handle_summary_command(command, user_id, message_id, replied_to_message_id, source):
    try:
        url = Constants.BASE_URL + '/summary/'
        headers = {'Content-Type': 'application/json'}
        dates_dict = get_start_and_end_date_for_sumary(command)
        if 'error' in dates_dict:
            # TODO Custom class
            print(dates_dict['error'])
            return
        
        params = {'user_id': user_id, 'start_date': dates_dict['start_date_str'], 'end_date': dates_dict['end_date_str']}
        resp = make_api_call(url=url, headers=headers, method='GET', query_params=params)
        print(resp)
    except Exception as e:
        print(f'Exception occured in handle_expense_command. Error: {e}')

def handle_analysis_command(command, user_id, message_id, replied_to_message_id, source):
    ...