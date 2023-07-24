import threading
from typing import List

from services.locationautocompleteservice import LocationAutocompleteService
from services.messagingservice import MessagingService
from services.servicemanagerinterface import ServiceManagerInterface
from services.volunteerservice import VolunteerService


class ServiceManager(ServiceManagerInterface):
    """
    This class is responsible for managing all the services.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.volunteer_service = VolunteerService()
        self.__observers = []
        self.location_autocomplete_service = LocationAutocompleteService()
        self.messaging_service = MessagingService()

    def subscribe(self, observer):
        """
        Subscribe to the service manager.
        """
        self.__observers.append(observer)

    def notify_location_auto_complete(self, data):
        """
        Notify all the subscribers about the auto complete data.
        """
        for observer in self.__observers:
            observer.notify('notify_location_auto_complete', data)

    def notify_total_volunteers(self, data):
        """
        Notify all the subscribers about the total volunteers data.
        """
        for observer in self.__observers:
            observer.notify('notify_amount_of_volunteer', data)

    def get_location_data(self, location):
        """
        Get the location data by using the LocationAutocompleteService.
        """
        threading.Thread(target=self.__get_location_data_in_thread, args=(location,)).start()

    def __get_location_data_in_thread(self, location):
        """
        This private method is used to get the location data in a separate thread.
        """
        data = self.location_autocomplete_service.get_location_autocomplete(location)
        self.notify_location_auto_complete(data)

    def get_amount_of_volunteer(self, checkbox_vars, location_ids_types, location, distance):
        """
        Get the amount of volunteers by using the VolunteerService.
        """
        threading.Thread(target=self.__get_amount_of_volunteer_in_thread,
                         args=(checkbox_vars, location_ids_types, location, distance)).start()

    def get_volunteers(self, checkbox_vars, location_ids_types, location, distance):
        """
        Get all the volunteers by using the VolunteerService.
        """
        threading.Thread(target=self.__get_volunteers_in_thread,
                         args=(checkbox_vars, location_ids_types, location, distance)).start()

    def __get_amount_of_volunteer_in_thread(self, checkbox_vars, location_ids_types, location, distance):
        """
        This private method is used to get the amount of volunteers in a separate thread.
        """
        data = self.volunteer_service.get_amount_of_volunteer(checkbox_vars, location_ids_types, location, distance)
        self.notify_total_volunteers(data)

    def __get_volunteers_in_thread(self, checkbox_vars, location_ids_types, location, distance):
        """
        This private method is used to get all the volunteers in a separate thread.
        """
        data = self.volunteer_service.get_volunteers(self, checkbox_vars, location_ids_types, location, distance)
        self.notify_get_volunteers(data)

    def send_messages(self, username: str, password: str, message: str, phoneNumber: str, recipients: List[str]):
        """
        Send a message by using the MessagingService.
        """
        threading.Thread(target=self.__send_message_in_thread,
                         args=(username, password, message, phoneNumber, recipients)).start()

    def __send_message_in_thread(self, username: str, password: str, message: str, phoneNumber: str,
                                 recipients: List[str]):
        """
        This private method is used to send a message in a separate thread.
        """
        self.messaging_service.send_messages(self, username, password, message, phoneNumber, recipients)
        self.notify_message_sent()

    def notify_starting_messaging(self, data):
        """
        Notify all the subscribers about the starting messaging data.
        """
        for observer in self.__observers:
            observer.notify('notify_starting_messaging', data)

    def notify_progresse_get_volunteers(self, data):
        """
        Notify all the subscribers about the progress data.
        """
        for observer in self.__observers:
            observer.notify('notify_progresse_get_volunteers', data)

    def unsubscribe(self, observer):
        """
        Unsubscribe from the service manager.
        """
        self.__observers.remove(observer)

    def notify_get_volunteers(self, data):
        """
        Notify all the subscribers about the volunteers data.
        """
        for observer in self.__observers:
            observer.notify('notify_get_volunteers', data)

    def notify_message_sent(self):
        """
        Notify all the subscribers about the message sent data.
        """
        for observer in self.__observers:
            observer.notify('notify_message_sent', None)

    def notify_progress_message_sending(self, data):
        """
        Notify all the subscribers about the progress message sending data.
        """
        for observer in self.__observers:
            observer.notify('notify_progress_message_sending', data)
