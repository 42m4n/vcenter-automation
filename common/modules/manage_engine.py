import requests
import urllib3
from loguru import logger
from common.configs import ManageEngineConf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ManageEngine:
    print('ManageEngine')

    def __init__(self):
        self.udf_fields_mapping = ManageEngineConf.udf_fields_mapping
        self.ticket_base_api = f"{ManageEngineConf.manage_engine_address}/api/v3/requests"
        self.headers = {"authtoken": f"{ManageEngineConf.manage_engine_token}"}

    def add_note_to_ticket(self, ticket_id, message):
        print('add_note_to_ticket')

        comment_input_data = {
            "note": {
                "description": message,
                "show_to_requester": True,
                "mark_first_response": False,
                "add_to_linked_requests": True
            }
        }
        self.send_request(ticket_id, comment_input_data, method='ADD_NOTE')
        print('add_note_to_ticket Finish')
        logger.info(f'Note added for ticket {ticket_id}')

    def change_ticket_status(self, ticket_id, status):
        status_input_data = {
            "request": {
                "status": {
                    "id": status
                }
            }}
        self.send_request(ticket_id, status_input_data, method='CHANGE_STATUS')
        logger.info(f'Note added for ticket {ticket_id}')

    def send_request(self, ticket_id, data, method):
        url = f'{self.ticket_base_api}/{ticket_id}'
        comment_url = f"{url}/notes"

        data = {'input_data': str(data)}

        try:
            print('send_request')
            if method == 'ADD_NOTE':
                print('ADD_NOTE')
                response = requests.post(comment_url, headers=self.headers, data=data, verify=False)
                logger.info(f'Add note request sent to Manage Engine ')
                print('ADD_NOTE Sent')
                response.raise_for_status()

            elif method == 'CHANGE_STATUS':

                response = requests.put(url, headers=self.headers, data=data, verify=False)
                logger.info(f'Change status request sent to Manage Engine ')

                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print('EXCEPTION AT SEND MANAGE ENGINE REQUEST')
            print(e)
            logger.error(f'Send request to Manage Engine failed cause: {e}')
            raise e
