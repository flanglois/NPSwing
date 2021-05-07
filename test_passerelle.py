from PyTango import *
import time

def start():
    recording_mgr_proxy = DeviceProxy("flyscan/core/recording-manager.1")
    session_counter_proxy = AttributeProxy("flyscan/core/recording-manager.1/sessionCounter") 
    while 1:
        print "session counter = ", recording_mgr_proxy.sessionCounter
        print "session counter proxy = ", session_counter_proxy.read().value
        print "csv_file not yet arrived, waiting 5 sec..."
        time.sleep(5)


#------------------------------------------------------------------------------
# Main Entry point
#------------------------------------------------------------------------------
if __name__ == "__main__":

    start()