#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        DeltaTauToNexus.py
#
# description : Python source for the DeltaTauToNexus and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                DeltaTauToNexus are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  $
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys
import h5py
import csv
import os
import time
from threading import Thread, Lock


class WaitingCSVFileThread(Thread):
    def __init__(self, mother):
        Thread.__init__(self)
        
        self.mother = mother
	self.mother.info_stream("init WaitingCSVFile Thread")
        self.start_asked = False
        
################################################################################
    def get_recordingmanager_sessioncounter(self):
        
        session_counter = long(self.mother.session_counter_attribute_proxy.read().value)
        self.mother.attr_currentSessionCounter_read = session_counter
        return session_counter

################################################################################
    def get_csv_file(self,index):
        self.mother.info_stream("In get_csv_file")

        while 1:
            print "self.start_asked",self.start_asked
            if self.start_asked == False:
                return
            csv_filenames = os.listdir(self.mother.attr_csvInputDirectory_read)
            for f in csv_filenames:
                # avoid the temp file from the ftpclient ("temp_fileblabla.csv.1246436")
                if (f.find('temp') == -1) and (f.find('csv.') == -1) : #ie "temp" and "csv." are not in the filename
                    if int(f[f.rfind('-')+1:f.rfind('csv')-1]) == int(index):
                        print ("found csv_file : ", f)
                        return f

            # csv file is not yet arrived: wait 1 sec
            self.mother.info_stream("csv_file not yet arrived, waiting 1 sec...")
            self.mother.set_status("Process is running\ncsv_file not yet arrived, waiting ...")
            time.sleep(0.5)

################################################################################
    def create_nxs_data_file(self,csv_file_name):
        
        try:
    
            if self.start_asked == False:
                return

            #------------------------------------------------
            #1 open / read csv file
            
            # declare the arrays
            gate_index              = []
            calc_gated_sample_tx    = []
            calc_gated_sample_tz    = []
            calc_gated_sample_rz    = []
            calc_gated_sample_rx    = []
            calc_gated_sample_rs    = []

            calc_gated_fzp_cs_tx    = []
            calc_gated_fzp_cs_tz    = []
            calc_gated_fzp_cs_rx    = []
            calc_gated_fzp_cs_rz    = []
            
            raw_gated_sample_txe    = []
            raw_gated_sample_txi    = []
            raw_gated_sample_tze    = []
            raw_gated_sample_tzi    = []
            raw_gated_sample_tzo    = []

            raw_gated_fzp_cs_txe    = []
            raw_gated_fzp_cs_txi    = []
            raw_gated_fzp_cs_tze    = []
            raw_gated_fzp_cs_tzi    = []

            std_gated_sample_txe    = []
            std_gated_sample_txi    = []
            std_gated_sample_tze    = []
            std_gated_sample_tzi    = []
            std_gated_sample_tzo    = []

            std_gated_fzp_cs_txe    = []
            std_gated_fzp_cs_txi    = []
            std_gated_fzp_cs_tze    = []
            std_gated_fzp_cs_tzi    = []

            substraction_calc_gated_tx = []
            substraction_calc_gated_tz = []

            # Open and Parse the CSV file
	    
	        # Waiting 0.2 sec before opening the csv file to be sure that it is there
            self.mother.info_stream("Waiting 0.2 sec before opening the csv file to be sure that it is there")
            time.sleep(0.2)
            with open(self.mother.attr_csvInputDirectory_read + '/' + csv_file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0
                selected_columns = self.mother.selected_columns
                for row in csv_reader:
                    # 1st line are the names of the columns
                    if line_count == 0:
                        print ("Column names are: ", (row))
                        line_count += 1
                    # then the real data
                    else:
                        #try:
                        for column in range (len(selected_columns)):
                            if selected_columns[column] == 0:  
                                gate_index.append(float(row[0]))
                                
                            if selected_columns[column] == 1:                   
                                calc_gated_sample_tx.append(float(row[1]))
                            if selected_columns[column] == 2:               
                                calc_gated_sample_tz.append(float(row[2]))
                            if selected_columns[column] == 3:
                                calc_gated_sample_rz.append(float(row[3]))
                            if selected_columns[column] == 4:
                                calc_gated_sample_rx.append(float(row[4]))
                            if selected_columns[column] == 5:
                                calc_gated_sample_rs.append(float(row[5]))
                            
                            if selected_columns[column] == 6:
                                calc_gated_fzp_cs_tx.append(float(row[6]))
                            if selected_columns[column] == 7:
                                calc_gated_fzp_cs_tz.append(float(row[7]))
                            if selected_columns[column] == 8:
                                calc_gated_fzp_cs_rx.append(float(row[8]))
                            if selected_columns[column] == 9:
                                calc_gated_fzp_cs_rz.append(float(row[9]))

                            if selected_columns[column] == 10:
                                raw_gated_sample_txe.append(float(row[10]))
                            if selected_columns[column] == 11:
                                raw_gated_sample_txi.append(float(row[11]))
                            if selected_columns[column] == 12:
                                raw_gated_sample_tze.append(float(row[12]))
                            if selected_columns[column] == 13:
                                raw_gated_sample_tzi.append(float(row[13]))
                            if selected_columns[column] == 14:
                                raw_gated_sample_tzo.append(float(row[14]))

                            if selected_columns[column] == 15:
                                raw_gated_fzp_cs_txe.append(float(row[15]))
                            if selected_columns[column] == 16:
                                raw_gated_fzp_cs_txi.append(float(row[16]))
                            if selected_columns[column] == 17:
                                raw_gated_fzp_cs_tze.append(float(row[17]))
                            if selected_columns[column] == 18:
                                raw_gated_fzp_cs_tzi.append(float(row[18]))

                            if selected_columns[column] == 19:
                                std_gated_sample_txe.append(float(row[19]))
                            if selected_columns[column] == 20:
                                std_gated_sample_txi.append(float(row[20]))
                            if selected_columns[column] == 21:
                                std_gated_sample_tze.append(float(row[21]))
                            if selected_columns[column] == 22:
                                std_gated_sample_tzi.append(float(row[22]))
                            if selected_columns[column] == 23:
                                std_gated_sample_tzo.append(float(row[23]))

                            if selected_columns[column] == 24:
                                std_gated_fzp_cs_txe.append(float(row[24]))
                            if selected_columns[column] == 25:
                                std_gated_fzp_cs_txi.append(float(row[25]))
                            if selected_columns[column] == 26:
                                std_gated_fzp_cs_tze.append(float(row[26]))
                            if selected_columns[column] == 27:
                                std_gated_fzp_cs_tzi.append(float(row[27]))

                        # computed substractions for tx and tz
                        substraction_calc_gated_tx.append(float(row[1]) - float(row[6]))
                        substraction_calc_gated_tz.append(float(row[2]) - float(row[7]))

                        line_count += 1
                        #except :
                        #    pass
                            #print ("maybe end of the file...", )
                
                #print ("\ncalc_gated_sample_tx: ",calc_gated_sample_tx)
               	print ("nb lines",line_count)

            #------------------------------------------------
            #2 create nxs file

            nxs_filename = "data_from_deltatau_000001.nxs"
            print ( "nxs_file = ", nxs_filename)
            f = h5py.File(self.mother.attr_nxsOutputDirectory_read +'/'+ nxs_filename, 'x') # 'x' means fail if file exist
            scan_data_entry = "/entry/scan_data"
            f.create_group(scan_data_entry)

            #------------------------------------------------
            #3 populate nxs file   
            # get size from substraction array as it is always selected
            size = len(substraction_calc_gated_tx)

            for column in range (0, len(selected_columns)):
                if selected_columns[column] == 0:
                    dset = f[scan_data_entry].create_dataset(u"gate_index", data=gate_index)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                    
                if selected_columns[column] == 1:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_sample_tx", data=calc_gated_sample_tx)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 2:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_sample_tz", data=calc_gated_sample_tz)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 3:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_sample_rz", data=calc_gated_sample_rz)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 4:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_sample_rx", data=calc_gated_sample_rx)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 5:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_sample_rs", data=calc_gated_sample_rs)
                    dset.attrs["buf_size"] = "["+str(size)+"]"

                if selected_columns[column] == 6:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_tx", data=calc_gated_fzp_cs_tx)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 7:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_tz", data=calc_gated_fzp_cs_tz)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 8:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_rx", data=calc_gated_fzp_cs_rx)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 9:
                    dset = f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_rz", data=calc_gated_fzp_cs_rz)
                    dset.attrs["buf_size"] = "["+str(size)+"]"

                if selected_columns[column] == 10:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_sample_txe", data=raw_gated_sample_txe)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 11:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_sample_txi", data=raw_gated_sample_txi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 12:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_sample_tze", data=raw_gated_sample_tze)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 13:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_sample_tzi", data=raw_gated_sample_tzi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 14:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_sample_tzo", data=raw_gated_sample_tzo)
                    dset.attrs["buf_size"] = "["+str(size)+"]"

                if selected_columns[column] == 15:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_txe", data=raw_gated_fzp_cs_txe)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 16:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_txi", data=raw_gated_fzp_cs_txi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 17:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_tze", data=raw_gated_fzp_cs_tze)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 18:
                    dset = f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_tzi", data=raw_gated_fzp_cs_tzi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"

                if selected_columns[column] == 19:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_sample_txe", data=std_gated_sample_txe)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 20:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_sample_txi", data=std_gated_sample_txi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 21:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_sample_tze", data=std_gated_sample_tze)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 22:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_sample_tzi", data=std_gated_sample_tzi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 23:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_sample_tzo", data=std_gated_sample_tzo)
                    dset.attrs["buf_size"] = "["+str(size)+"]"

                if selected_columns[column] == 24:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_txe", data=std_gated_fzp_cs_txe)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 25:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_txi", data=std_gated_fzp_cs_txi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 26:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_tze", data=std_gated_fzp_cs_tze)
                    dset.attrs["buf_size"] = "["+str(size)+"]"
                if selected_columns[column] == 27:
                    dset = f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_tzi", data=std_gated_fzp_cs_tzi)
                    dset.attrs["buf_size"] = "["+str(size)+"]"


            # computed substractions for tx and tz
            dset = f[scan_data_entry].create_dataset(u"historised_relative_sample_tx", data=substraction_calc_gated_tx)
            dset.attrs["buf_size"] = "["+str(size)+"]"
            dset = f[scan_data_entry].create_dataset(u"historised_relative_sample_tz", data=substraction_calc_gated_tz)
            dset.attrs["buf_size"] = "["+str(size)+"]"

            f.close()

            self.mother.info_stream("done")
            
        except Exception, e:
            print ("-------> An unforeseen exception occured....", e )
            self.error_occured = True
            self.error_msg = e
            
        
        
################################################################################
    def run(self):
        self.mother.info_stream("start WaitingCSVFile thread")
        
        while 1:
            if self.start_asked:
            
                self.error_occured = False
        
                #1 get the session counter from RecordingManager, then check that the CSV as the good session counter 
                session_counter = self.get_recordingmanager_sessioncounter()
                self.mother.info_stream("session_counter =  %s" % session_counter)

                #2 find the csv file with this index
                csv_file_name = self.get_csv_file(session_counter)

                #3 create the nxs file corresponding and copy csv data into it, the nxs file should be ending with 00001.nxs
                self.create_nxs_data_file(csv_file_name)
                
                self.start_asked = False
                
                if self.error_occured:
                    self.mother.set_state(PyTango.DevState.ALARM)
                    self.mother.set_status("Error occured:\n" + str(self.error_msg))
                else:
                    self.mother.set_state(PyTango.DevState.STANDBY)
                    self.mother.set_status("Ready to Start processing")
        

#==================================================================
#   DeltaTauToNexus Class Description:
#
#         DeltaTauToNexus transform CSV data files from the DeltaTau controller to Nexus files ready to be merged by the DataMerger
#
#==================================================================
#     Device States Description:
#
#   DevState.RUNNING :  The Process is RUNNING
#   DevState.STANDBY :  The Process is STANDBY
#==================================================================

class DeltaTauToNexus(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        DeltaTauToNexus.init_device(self)

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        self.info_stream("[Device delete_device method] for device %s" % self.get_name())
        self.th.start_asked = False
              
#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.info_stream("In %s::init_device()" % self.get_name())
        self.get_device_properties(self.get_device_class())
        
        self.set_state(PyTango.DevState.STANDBY)
        self.set_status("Ready to Start processing")
          
        self.th = WaitingCSVFileThread(self)
        self.th.start_asked = False
        self.th.start()
        
        self.session_counter_attribute_proxy = PyTango.AttributeProxy(self.SessionCounterAttributeName)
        self.attr_currentSessionCounter_read = long(self.session_counter_attribute_proxy.read().value)

#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")

#==================================================================
#
#    DeltaTauToNexus read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self,data):
        self.debug_stream("In read_attr_hardware()")

#------------------------------------------------------------------
#    Read csvInputDirectory attribute
#------------------------------------------------------------------
    def read_csvInputDirectory(self, attr):
        self.debug_stream("In read_csvInputDirectory()")
        
        #    Add your own code here
        
        #attr_csvInputDirectory_read = "Hello Tango world"
        attr.set_value(self.attr_csvInputDirectory_read)


#------------------------------------------------------------------
#    Write csvInputDirectory attribute
#------------------------------------------------------------------
    def write_csvInputDirectory(self, attr):
        self.info_stream("In write_csvInputDirectory()")
        self.attr_csvInputDirectory_read = attr.get_write_value()


#---- csvInputDirectory attribute State Machine -----------------
    def is_csvInputDirectory_allowed(self, req_type):
        """if self.get_state() in [PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False"""
        return True


#------------------------------------------------------------------
#    Read nxsOutputDirectory attribute
#------------------------------------------------------------------
    def read_nxsOutputDirectory(self, attr):
        self.debug_stream("In read_nxsOutputDirectory()")
        
        #    Add your own code here

        attr.set_value(self.attr_nxsOutputDirectory_read)


#------------------------------------------------------------------
#    Write nxsOutputDirectory attribute
#------------------------------------------------------------------
    def write_nxsOutputDirectory(self, attr):
        self.info_stream("In write_nxsOutputDirectory()")
        self.attr_nxsOutputDirectory_read = attr.get_write_value()
        

#---- nxsOutputDirectory attribute State Machine -----------------
    def is_nxsOutputDirectory_allowed(self, req_type):
        """if self.get_state() in [PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False"""
        return True


#------------------------------------------------------------------
#    Read selectedColumns attribute
#------------------------------------------------------------------
    def read_selectedColumns(self, attr):
        self.debug_stream("In read_selectedColumns()")
        
        #    Add your own code here
        
        attr.set_value(self.attr_selectedColumns_read)


#------------------------------------------------------------------
#    Write selectedColumns attribute
#------------------------------------------------------------------
    def write_selectedColumns(self, attr):        
        self.info_stream("In write_selectedColumns()")
        self.attr_selectedColumns_read = attr.get_write_value()
        
        # selected columns default columns: 1,2
        self.selected_columns = "1,2" # mandatory to compute the "substractions" data
        # transform the string to a list
        self.selected_columns = list(self.attr_selectedColumns_read.split(",")) 
        # transform list of str to list of int
        self.selected_columns = list(map(int,self.selected_columns))


#---- selectedColumns attribute State Machine -----------------
    def is_selectedColumns_allowed(self, req_type):
        """if self.get_state() in [PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False"""
        return True
        
#------------------------------------------------------------------
#    Read currentSessionCounter attribute
#------------------------------------------------------------------
    def read_currentSessionCounter(self, attr):
        self.debug_stream("In read_currentSessionCounter()")
        
        #    Add your own code here
        #self.attr_currentSessionCounter_read = self.get_recordingmanager_sessioncounter()
        attr.set_value(self.attr_currentSessionCounter_read)
        
#---- currentSessionCounter attribute State Machine -----------------
    def is_currentSessionCounter_allowed(self, req_type):
        """if self.get_state() in [PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False"""
        return True



#==================================================================
#
#    DeltaTauToNexus command methods
#
#==================================================================


#------------------------------------------------------------------
#    Start command:
#
#    Description: Start the Process
#                
#------------------------------------------------------------------
    def Start(self):
        self.info_stream("In Start()")
        self.set_state(PyTango.DevState.RUNNING)
        self.set_status("Process is running") 
        
        self.th.start_asked = True


#---- Start command State Machine -----------------
    def is_Start_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            #    End of Generated Code
            #    Re-Start of Generated Code
            return False
        return True
        
#------------------------------------------------------------------
#    Abort command:
#
#    Description: Abort the Process
#                
#------------------------------------------------------------------
    def Abort(self):
        self.info_stream("In Abort()")
        
        self.th.start_asked = False
        self.set_state(PyTango.DevState.STANDBY)
        self.set_status("Ready to Start processing") 


#---- Abort command State Machine -----------------
    def is_Abort_allowed(self):
        if self.get_state() in [PyTango.DevState.STANDBY]:
            #    End of Generated Code
            #    Re-Abort of Generated Code
            return False
        return True


#==================================================================
#
#    DeltaTauToNexusClass class definition
#
#==================================================================
class DeltaTauToNexusClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        'SessionCounterAttributeName':
            [PyTango.DevString,
            "Name of the session counter attribure",
            [ "flyscan/core/recording-manager.1/sessionCounter" ] ],
        }


    #    Command definitions
    cmd_list = {
        'Start':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],

        'Abort':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        }


    #    Attribute definitions
    attr_list = {
        'csvInputDirectory':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true",
            } ],
        'nxsOutputDirectory':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true",
            } ],
        'selectedColumns':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true",
            } ],
        'currentSessionCounter':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ],
            {
               
            } ],   
        }


#------------------------------------------------------------------
#    DeltaTauToNexusClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print "In DeltaTauToNexusClass  constructor"

#==================================================================
#
#    DeltaTauToNexus class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        py = PyTango.Util(sys.argv)
        py.add_TgClass(DeltaTauToNexusClass,DeltaTauToNexus,'DeltaTauToNexus')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e