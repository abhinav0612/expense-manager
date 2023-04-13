import json
import requests


def make_api_call(url, headers, method, data=None, query_params=None):
    method_dict = {
        "GET": requests.get,
        "POST": requests.post,
        "PATCH": requests.patch,
        "DELETE": requests.delete
    }
    response = None
    error_message = None
    try:
        if method not in ['GET', 'POST', 'PATCH', 'DELETE']:
            print('HTTP method not suported.')
            return
        if method == "GET":
            response = method_dict[method](
                url=url, headers=headers, params=query_params)
        else:
            response = method_dict[method](url=url, headers=headers, data=json.dumps(data))
        # Raises HTTPError exception for HTTP codes 400-599.
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.HTTPError as err:
        error_message = 'HTTPError error occured while fetching data.'
        print(f'{error_message} Error: {err}')
    except requests.exceptions.ConnectionError as err:
        error_message = 'Connection error occured while fetching data.'
        print(f'{error_message} Error: {err}')
    except requests.exceptions.Timeout as err:
        error_message = 'Timeout error occured while fetching data.'
        print(f'{error_message} Error: {err}')
    except Exception as err:
        error_message = 'Exception occured while fetching data.'
        print(f'{error_message} Error: {err}')
    finally:
        data = {
            "results": response
        }
        if error_message:
            data['error'] = error_message

        return data
