import logging
import random
import time
from typing import Optional, List

from config.settings import headers, url_volunteer, minimum_time, maximum_time
from controllers.logincontroller import LoginController
from controllers.logincontrollerinterface import LoginControllerInterface
from models.sessionmanager import SessionManager
from bs4 import BeautifulSoup


class MessagingService:

    def __init__(self, loginController: Optional[LoginControllerInterface] = None):

        self.recipients = None
        self.phoneNumber = None
        self.message = None
        self.password = None
        self.username = None
        self.notifier = None
        self.delay_to_start_sending = random.uniform(10.141516, 29.141516)
        self.loginController = loginController if loginController else LoginController()

    def send_messages(self, notifier, username: str, password: str, message: str, phoneNumber: str,
                      recipients: List[str]) -> None:
        self.notifier = notifier
        self.username = username
        self.password = password
        self.message = message
        self.phoneNumber = phoneNumber
        self.recipients = recipients
        self.loginController.logout()
        current_recipient = 0
        self.notifier.notify_starting_messaging(self.delay_to_start_sending)
        time.sleep(self.delay_to_start_sending)
        for recipient in self.recipients:
            self.__send_message(recipient)
            current_recipient += 1
            self.notifier.notify_progress_message_sending(current_recipient)
            if current_recipient != len(self.recipients):
                time.sleep(random.uniform(minimum_time, maximum_time))

    def __send_message(self, volunteer_id: str) -> bool:
        self.loginController.login(self.username, self.password)
        url = f'{url_volunteer}{volunteer_id}?showMessage=1'
        try:
            response = SessionManager.get_session().get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                message_token = soup.find('input', {'name': 'message[_token]'})['value']
                message_loaded = soup.find('input', {'name': 'message[loaded]'})['value']
                data = {
                    'message[body]': self.message,
                    'message[phoneNumber]': self.phoneNumber,
                    'message[dusdat]': '',
                    'message[_token]': message_token,
                    'message[loaded]': message_loaded}
            else:
                logging.error(f'Error while sending message to volunteer with id {volunteer_id}: '
                              f'Could not get message page')
                return False
            response = SessionManager.get_session().post(url, data=data, headers=headers)
            if response.status_code != 200:
                logging.error(f'Error while sending message to volunteer with id {volunteer_id}: '
                              f'Could not send message')
                return False
            return True

        except Exception as e:
            logging.error(f'Error while sending message to volunteer with id {volunteer_id}: {e.__str__()}')
            return False
        finally:
            self.loginController.logout()
