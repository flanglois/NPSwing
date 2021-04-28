# Author: FL 26/04/2021
from argparse import ArgumentParser
import h5py
import csv
import numpy as np
import os
import random
from os import walk


#Gate_index;Calc-Gated_Sample-X;Calc-Gated_Sample-Z;Calc-Gated_Sample-Rz;Calc-Gated_Sample-Rx;Calc-Gated_Sample-Rs;Calc-Gated_FZPCS-X;Calc-Gated_FZPCS-Z;Calc-Gated_FZPCS-Rx;Calc-Gated_FZPCS-Rz;Raw-Gated_Sample-Xe;Raw-Gated_Sample-Xi;Raw-Gated_Sample-Ze;Raw-Gated_Sample-Zi;Raw-Gated_Sample-Zo;Raw-Gated_FZPCS-Xe;Raw-Gated_FZPCS-Xi;Raw-Gated_FZPCS-Ze;Raw-Gated_FZPCS-Zi;
#------------------------------------------------------------------------------
# Main Entry point
#------------------------------------------------------------------------------
if __name__ == "__main__":

    # command line parsing
    parser = ArgumentParser(description="NP Swing hdf5 script")
    parser.add_argument("-d1","--csv_input_directory",help="Directory where the CSV files will arrive (eg from FtpClient")
    parser.add_argument("-d2","--nxs_output_directory",help="Directory where the NXS files will be written")
    parser.add_argument("-num1","--num1",help="start number")
    parser.add_argument("-num2","--num2",help="end number")

    args = parser.parse_args()
    
    if args.csv_input_directory:
        csv_input_directory = args.csv_input_directory
    else:
        raise BaseException("No CSV input directory specified")

    if args.nxs_output_directory:
        nxs_output_directory = args.nxs_output_directory
    else:
        raise BaseException("No NXS output directory specified")
    
    if args.num1:
        num1 = int(args.num1)
    if args.num2:
        num2 = int(args.num2)

    print "csv_input_directory = ", csv_input_directory
    print "nxs_output_directory = ", nxs_output_directory
    
    # get csv filenames 
    (_,_,csv_filenames) = walk(csv_input_directory).next()

    print "csv_filenames = ", csv_filenames

    columns_dict = { "0":"Gate_index",
                    "1":"Calc-Gated_Sample-X"}

    while num1 <= num2:
        print "num1 = ", num1
        the_csv_file = ""
        the_nxs_file = ""
        for f in csv_filenames:
            if int(f[f.rfind('-')+1:f.rfind('.')]) == int(num1):
                the_csv_file = f
                the_nxs_file = os.path.splitext(f)[0]+'.nxs'
                break

        print "csv_file = ", the_csv_file
        print "nxs_file = ", the_nxs_file

        num1+=1

        #==========================================================================   
        # read csv file and 
        calc_gated_sample_tx    = []
        calc_gated_sample_tz    = []
        calc_gated_fzp_tx       = []
        calc_gated_fzp_tz       = []
        substraction_tx         = []
        substraction_tz         = []
        substraction_noisy100tx = []
        substraction_noisy100tz = []
        substraction_noisy50tx  = []
        substraction_noisy50tz  = []
        substraction_noisy25tx  = []
        substraction_noisy25tz  = []
        substraction_noisy10tx  = []
        substraction_noisy10tz  = []

        with open(csv_input_directory + '/' + the_csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for a_row in csv_reader:
                if line_count == 0:
                    print("Column names are: ", (a_row))
                    line_count += 1
                else:
                    try:
                        # print("line_count = ",line_count)
                        # print("a_row[0] = ",a_row[0])
                        # print("a_row[1] = ",a_row[1])
                        # print("a_row[2] = ",a_row[2])
                        
                        calc_gated_sample_tx.append(float(a_row[1]))
                        calc_gated_sample_tz.append(float(a_row[2]))
                        calc_gated_fzp_tx.append(float(a_row[6]))
                        calc_gated_fzp_tz.append(float(a_row[7]))
                        substraction_tx.append(float(a_row[1]) - float(a_row[6])) 
#                       substraction_tz.append(float(a_row[2]) - float(a_row[7]))
#   Probleme avec Ze et Zo. On utilise gated_Zi pour le sample 
                        substraction_tz.append(float(a_row[13]) - float(a_row[7])) 
#    Probleme avec la premiere valeur calc. On utilise les valeurs raw Xe et raw Ze pour sample et FZP
#                       substraction_tx.append(-float(a_row[10]) + float(a_row[15])) 
#                       substraction_tz.append(float(a_row[12]) - float(a_row[17])) 
                        substraction_noisy100tx.append(random.gauss((float(a_row[1]) - float(a_row[6])),1E-6*100)) 
                        substraction_noisy100tz.append(random.gauss((float(a_row[2]) - float(a_row[7])),1E-6*100)) 
                        substraction_noisy50tx.append(random.gauss((float(a_row[1]) - float(a_row[6])),1E-6*50)) 
                        substraction_noisy50tz.append(random.gauss((float(a_row[2]) - float(a_row[7])),1E-6*50)) 
                        substraction_noisy25tx.append(random.gauss((float(a_row[1]) - float(a_row[6])),1E-6*25)) 
                        substraction_noisy25tz.append(random.gauss((float(a_row[2]) - float(a_row[7])),1E-6*25)) 
                        substraction_noisy10tx.append(random.gauss((float(a_row[1]) - float(a_row[6])),1E-6*10)) 
                        substraction_noisy10tz.append(random.gauss((float(a_row[2]) - float(a_row[7])),1E-6*10)) 
                        line_count += 1
                    except :
                        pass
                        #print ("maybe end of the file...", )
            
            print "\ncalc_gated_sample_tx: ",calc_gated_sample_tx
            print('nb lines',line_count)
            
        #==========================================================================   
        # create nxs file
        f = h5py.File(nxs_output_directory +'/'+ the_nxs_file, 'a')
        f.create_group("/entry/scan_data")
        
        #==========================================================================       
        
 #       calc_gated_sample_tx_nx = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_sample_tx", data=calc_gated_sample_tx)
 #       calc_gated_sample_tz_nx = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_sample_tz", data=calc_gated_sample_tz)
 #       calc_gated_fzp_tx_nx    = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_fzp_tx", data=calc_gated_fzp_tx)
 #       calc_gated_fzp_tz_nx    = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_fzp_tz", data=calc_gated_fzp_tz)
        substraction_tx_nx      = f["/entry/scan_data"].create_dataset(u"historised_relative_sample_tx", data=substraction_tx)
        substraction_tz_nx      = f['/entry/scan_data'].create_dataset(u"historised_relative_sample_tz", data=substraction_tz)
 #       substraction_noisytx_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy100tx", data=substraction_noisy100tx)
 #       substraction_noisytz_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy100tz", data=substraction_noisy100tz)
 #       substraction_noisytx_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy50tx", data=substraction_noisy50tx)
 #       substraction_noisytz_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy50tz", data=substraction_noisy50tz)
 #       substraction_noisytx_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy25tx", data=substraction_noisy25tx)
 #       substraction_noisytz_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy25tz", data=substraction_noisy25tz)
 #       substraction_noisytx_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy10tx", data=substraction_noisy10tx)
 #       substraction_noisytz_nx      = f['/'+key_top[0]+'/scan_data'].create_dataset(u"historised_relative_sample_noisy10tz", data=substraction_noisy10tz)
        f.close()
        print "done"

 
