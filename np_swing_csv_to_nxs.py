# Author: FL 26/04/2021
"""
A script used for NP Swing to transform csv files comming from the deltatau controller
and write them into a nexus file that will be merged by the DataMerger
"""
from argparse import ArgumentParser
import h5py
import csv
import os
import random
import time
from PyTango import *

################################################################################
def get_recordingmanager_sessioncounter():
    
    session_counter = recording_mgr_proxy.sessionCounter
    return session_counter

################################################################################
def get_csv_filename(index):

    while 1:
        csv_filenames = os.listdir(csv_input_directory)
        for f in csv_filenames:
            if int(f[f.rfind('-')+1:f.rfind('.')]) == int(index):
                print "found csv_file : ", f
                return f

        # csv file is not yet arrived: wait 5 sec
        print "csv_file not yet arrived, waiting 5 sec..."
        time.sleep(5)

################################################################################
def create_nxs_data_file(csv_file_name):

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
    with open(csv_input_directory + '/' + csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            # 1st line are the names of the columns
            if line_count == 0:
                print("Column names are: ", (row))
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
        
        print "\ncalc_gated_sample_tx: ",calc_gated_sample_tx
        print('nb lines',line_count)

    #------------------------------------------------
    #2 create nxs file

    nxs_filename = "data_from_deltatau_000001.nxs"
    print "nxs_file = ", nxs_filename
    f = h5py.File(nxs_output_directory +'/'+ nxs_filename, 'x') # 'x' means fail if file exist
    scan_data_entry = "/entry/scan_data"
    f.create_group(scan_data_entry)

    #------------------------------------------------
    #3 populate nxs file   

    for column in range (0, len(selected_columns)):
        if selected_columns[column] == 0:
            f[scan_data_entry].create_dataset(u"gate_index", data=gate_index)

        if selected_columns[column] == 1:
            f[scan_data_entry].create_dataset(u"calc_gated_sample_tx", data=calc_gated_sample_tx)
        if selected_columns[column] == 2:
            f[scan_data_entry].create_dataset(u"calc_gated_sample_tz", data=calc_gated_sample_tz)
        if selected_columns[column] == 3:
            f[scan_data_entry].create_dataset(u"calc_gated_sample_rz", data=calc_gated_sample_rz)
        if selected_columns[column] == 4:
            f[scan_data_entry].create_dataset(u"calc_gated_sample_rx", data=calc_gated_sample_rx)
        if selected_columns[column] == 5:
            f[scan_data_entry].create_dataset(u"calc_gated_sample_rs", data=calc_gated_sample_rs)

        if selected_columns[column] == 6:
            f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_tx", data=calc_gated_fzp_cs_tx)
        if selected_columns[column] == 7:
            f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_tz", data=calc_gated_fzp_cs_tz)
        if selected_columns[column] == 8:
            f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_rx", data=calc_gated_fzp_cs_rx)
        if selected_columns[column] == 9:
            f[scan_data_entry].create_dataset(u"calc_gated_fzp_cs_rz", data=calc_gated_fzp_cs_rz)

        if selected_columns[column] == 10:
            f[scan_data_entry].create_dataset(u"raw_gated_sample_txe", data=raw_gated_sample_txe)
        if selected_columns[column] == 11:
            f[scan_data_entry].create_dataset(u"raw_gated_sample_txi", data=raw_gated_sample_txi)
        if selected_columns[column] == 12:
            f[scan_data_entry].create_dataset(u"raw_gated_sample_tze", data=raw_gated_sample_tze)
        if selected_columns[column] == 13:
            f[scan_data_entry].create_dataset(u"raw_gated_sample_tzi", data=raw_gated_sample_tzi)
        if selected_columns[column] == 14:
            f[scan_data_entry].create_dataset(u"raw_gated_sample_tzo", data=raw_gated_sample_tzo)

        if selected_columns[column] == 15:
            f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_txe", data=raw_gated_fzp_cs_txe)
        if selected_columns[column] == 16:
            f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_txi", data=raw_gated_fzp_cs_txi)
        if selected_columns[column] == 17:
            f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_tze", data=raw_gated_fzp_cs_tze)
        if selected_columns[column] == 18:
            f[scan_data_entry].create_dataset(u"raw_gated_fzp_cs_tzi", data=raw_gated_fzp_cs_tzi)

        if selected_columns[column] == 19:
            f[scan_data_entry].create_dataset(u"std_gated_sample_txe", data=std_gated_sample_txe)
        if selected_columns[column] == 20:
            f[scan_data_entry].create_dataset(u"std_gated_sample_txi", data=std_gated_sample_txi)
        if selected_columns[column] == 21:
            f[scan_data_entry].create_dataset(u"std_gated_sample_tze", data=std_gated_sample_tze)
        if selected_columns[column] == 22:
            f[scan_data_entry].create_dataset(u"std_gated_sample_tzi", data=std_gated_sample_tzi)
        if selected_columns[column] == 23:
            f[scan_data_entry].create_dataset(u"std_gated_sample_tzo", data=std_gated_sample_tzo)

        if selected_columns[column] == 24:
            f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_txe", data=std_gated_fzp_cs_txe)
        if selected_columns[column] == 25:
            f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_txi", data=std_gated_fzp_cs_txi)
        if selected_columns[column] == 26:
            f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_tze", data=std_gated_fzp_cs_tze)
        if selected_columns[column] == 27:
            f[scan_data_entry].create_dataset(u"std_gated_fzp_cs_tzi", data=std_gated_fzp_cs_tzi)


    # computed substractions for tx and tz
    f[scan_data_entry].create_dataset(u"historised_relative_sample_tx", data=substraction_calc_gated_tx)
    f[scan_data_entry].create_dataset(u"historised_relative_sample_tz", data=substraction_calc_gated_tz)

    fname = f.filename
    f.close()
    
    # for debug purpose: ie simulate the DataMerger Process
    #os.remove(fname) 
    print "done"


#Gate_index;Calc-Gated_Sample-X;Calc-Gated_Sample-Z;Calc-Gated_Sample-Rz;Calc-Gated_Sample-Rx;Calc-Gated_Sample-Rs;Calc-Gated_FZPCS-X;Calc-Gated_FZPCS-Z;Calc-Gated_FZPCS-Rx;Calc-Gated_FZPCS-Rz;Raw-Gated_Sample-Xe;Raw-Gated_Sample-Xi;Raw-Gated_Sample-Ze;Raw-Gated_Sample-Zi;Raw-Gated_Sample-Zo;Raw-Gated_FZPCS-Xe;Raw-Gated_FZPCS-Xi;Raw-Gated_FZPCS-Ze;Raw-Gated_FZPCS-Zi;
#------------------------------------------------------------------------------
# Main Entry point
#------------------------------------------------------------------------------
if __name__ == "__main__":

    # command line parsing
    parser = ArgumentParser(description="NP Swing hdf5 script")
    parser.add_argument("-d1","--csv_input_directory",help="Directory where the CSV files will arrive (eg from FtpClient")
    parser.add_argument("-d2","--nxs_output_directory",help="Directory where the NXS files will be written")
    parser.add_argument("-col","--selected_columns",help="Selected columns that will be written into the nxs file: eg: [1,2,4,78] \
                                                            0 being the first column ie: Index)")

    args = parser.parse_args()
    
    # csv directory
    if args.csv_input_directory:
        csv_input_directory = args.csv_input_directory
        print "csv_input_directory = ", csv_input_directory
    else:
        raise BaseException("No CSV input directory specified")

    # nxs directory
    if args.nxs_output_directory:
        nxs_output_directory = args.nxs_output_directory
        print "nxs_output_directory = ", nxs_output_directory
    else:
        raise BaseException("No NXS output directory specified")

    # selected columns default columns: 1,2,6,7
    selected_columns = "1,2,6,7" # mandatory to compute the "substractions" data
    if args.selected_columns:
        selected_columns = args.selected_columns
    selected_columns += "1,2,6,7"
    
    # transform the string to a list
    selected_columns = list(selected_columns.split(",")) 
    # transform list of str to list of int
    selected_columns = list(map(int,selected_columns))

    recording_mgr_proxy = DeviceProxy("flyscan/core/recording-manager.1")

    ################################################################################
    # Main loop for each csv file
    while 1:

        #1 get the session counter from RecordingManager, then check that the CSV as the good session counter 
        session_counter = get_recordingmanager_sessioncounter()
        print "session_counter = ", session_counter

        #2 find the csv file with this index
        csv_file_name = get_csv_file(session_counter)

        #3 create the nxs file corresponding and copy csv data into it, the nxs file should be ending with 00001.nxs
        create_nxs_data_file(csv_file_name)
