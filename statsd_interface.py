'''
File: StatsdClient.py
Description: Implements mechanism for reporting stats to collectd
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 20/04/2017
'''
import os

class StatsdClient:
    '''
    StatsdClient implements functionality for reporting client data
    to te statsd server
    '''

    REQUEST_TYPES = {
       'gauge' : 'g',
       'counter': 'c',
       'timer': 'ms'
    }

    def __init__(self, host="127.0.0.1", port=8125):
        '''
        Initialize the statsd client for reporting the statistics
        to the server.
        Params:
         - host: The address to the remote statsd server (Default: 127.0.0.1)
         - port: The port where the statsd server is running (Default: 8125)
        Returns: None
        '''

        self.host = "127.0.0.1"
        self.port = port

    def __prepare_request(self, request_type):
        '''
        Prepares a request for reporting to statsd server
        Params:
         - request_type: The typeof request to be made
        Returns: True on success, False on error
        '''

        if request_type not in self.REQUEST_TYPES:
            return False

        self.request = "%s.%s:%s|" + self.REQUEST_TYPES[type] + "%s"
        return True

    def connect(self, host, port):
        '''
        Connect to the remote StatsD server
        Params:
         - host: The host address of the StatsD server
         - port: The port on which the StatsD server is listening
        Returns: None
        '''

        self.host = host
        self.port = port

    def gauge(self, application_name, metric_name, metric_value):
        '''
        Prepares a Gauge value to be sent to the server
        Params:
         - application_name: Name of the application for which data is recorded
         - metric_name: Name of metric which is being recorded
         - metric_value: The value that needs to be sent
        Returns: True on success/False on Failure
        '''

        self.__prepare_request()
