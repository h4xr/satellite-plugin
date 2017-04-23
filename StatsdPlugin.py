'''
File: StatsdPlugin.py
Description: Provides an interface for writing StatsD Plugins, collecting their
             data and reporting it to the StatsD Server
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 23/04/2017
'''
import statsd
import threading

class StatsdPlugin:
    '''
    StatsdPlugin provides a wrapper to the plugins through which they can
    register to a common interface to run and provide data.
    '''

    def __init__(self, host='127.0.0.1', port=8125, application_name='Satellite6',run_interval=1):
        '''
        Initialize the object and set the host and port where the statsd server
        is running. If no argument is provided, the client tries to connect to
        the statsd server running on localhost port 8125 by default.
        Params:
         - host: The host address of statsd server (Default:127.0.0.1)
         - port: The port on which the statsd server is listening (Default:8125)
         - application_name: The name of the application which will be appended
                             to the results before sending statistics
         - run_interval: The time interval in seconds which the registered
                         methods should run to collectd data (Default:1s)
        Returns: None
        '''

        self.host = host
        self.port = port
        self.application_name = application_name
        self.run_interval = run_interval

        #Set if the threads should run or not
        self.__run_threads = True

        #Try connecting to the Statsd Server
        self.statsd_client = statsd.StatsClient(self.host, self.port)

        #Initialize the registered methods list
        self.registered_methods = []

        #Initialize the threads list
        self.threads = []

        #Initialize the result dictionary
        self.thread_results = {}

    def __build_thread(self, method):
        '''
        Builds a thread for execution
        Params:
         - method: The target method, that needs to be executed
        Returns: None
        '''

        t = threading.Thread(target=method, args=(self.thread_results,), daemon=True)
        self.threads.append(t)

    def __report_results(self):
        '''
        Reports the collected results to the statsd server
        Params: None
        Returns: None
        '''

        for key in self.thread_results:
            metric_name = self.application_name + "." + str(key)
            self.statsd_client.gauge(metric_name, self.thread_results[key])
        self.thread_results.clear()

    def register_method(self, method):
        '''
        Registers a method for execution and result collection
        Params:
         - method: The method which needs to be executed
        Raises: TypeError if the provided parameter is not a callable
        Return: True on success
        '''

        if not callable(method):
            raise TypeError("Provided method is not callable")

        self.__build_thread(method)
        self.registered_methods.append(method)
        return True

    def start(self):
        '''
        Start the thread execution
        Params: None
        Returns: None
        '''

        while self.__run_threads:
            for thread in self.threads:
                thread.start()

            for thread in self.threads:
                thread.join()

            self.__report_results()
            time.sleep(self.run_interval)

    def stop(self):
        '''
        Stops the thread execution and causes the program to exit
        Params: None
        Returns: None
        '''

        self.__run_threads = False
