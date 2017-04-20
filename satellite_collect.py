import subprocess
import statsd
import os

def send_stats(name,value):
    '''
    Send the stats to the statsd server
    Params:
     - name: Name of the value to send
     - value: Value associated with the key
    Returns: None
    '''

    statsd_connection = statsd.Connection(
                        host = 'localhost',
                        port = 8125,
                      )
    raw_data  = statsd.Raw('SatelliteServer')
    raw_data.send(name, value)
    #os.system('echo "passenger.requests.topLevel:%s|c" | nc -w 1 -u 127.0.0.1 8125' %(value))
#    raw_data = statsd.Gauge('SatelliteServer', statsd_connection)
#    out = raw_data.send(name, value)
#    print out


def collect_passenger_stats(data=None):
    '''
    Collects the statistics from passenger-status and reports them
    to the statsd service plugin
    Params:
     - data: Any mock data that needs to be sent to the handler
    Returns: None
    '''

    process_data = subprocess.check_output(['passenger-status']).split('\n')
    for item in process_data:
        if "Requests in top-level queue" in item:
            val = item.split(':')[1].strip()
    send_stats('passengerRequests', val)
    
if __name__ == '__main__':
    
    while True:
        collect_passenger_stats()
    
