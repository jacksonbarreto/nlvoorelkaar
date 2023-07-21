import threading

from services.locationautocompleteservice import LocationAutocompleteService
from services.servicemanagerinterface import ServiceManagerInterface


class ServiceManager(ServiceManagerInterface):
    """
    This class is responsible for managing all the services.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.__observers = []
        self.location_autocomplete_service = LocationAutocompleteService()

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
            observer.notify('notify_total_volunteers', data)

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

    def unsubscribe(self, observer):
        """
        Unsubscribe from the service manager.
        """
        self.__observers.remove(observer)