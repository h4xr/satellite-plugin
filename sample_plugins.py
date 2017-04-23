'''
File: sample_plugins.py
Description: Stores some example plugins
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 23/04/2017
'''

from StatsdPlugin import StatsdPlugin
import subprocess

class SampleTest(StatsdPlugin):

    def passenger_stats_plugin(self):
        '''
        Collects the Passenger Statistics
        Params:
         - result_dict: A dictionary in which the results needs to be stored
        Returns: None
        '''

        process_data = subprocess.check_output(['passenger-status']).split('\n')
        for item in process_data:
            if "Requests in top-level queue" in item:
                val = item.split(':')[1].strip()

        self.store_results('passenger_top_level_queue', val)

if __name__ == '__main__':
    try:
        plugin = SampleTest()
        plugin.start()
    except Exception, e:
        print str(e)
        plugin.stop()
        print "Exiting"
