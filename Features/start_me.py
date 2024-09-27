# This function creates the argument list and launches job managers

import numpy
import glob
import re
import argparse
from os import path
import os    # for file operations
import socket   # for netowrk hostname
import numpy
import argparse  # for command-line arguments
import subprocess   # for launching detached processes on a local PC
import sys      # to set exit codes
# Constants
from constants import *


# Define arguments
arg_parser = argparse.ArgumentParser(
    description='Job manager. You must choose whether to resume simulations or restart and regenerate the arguments file')
arg_parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + str(version))
mode_group = arg_parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('--restart', action='store_true')
mode_group.add_argument('--resume', action='store_true')
arg_parser.add_argument('--ac', action='store', type=str)
# arg_parser.add_argument('--end', action='store', type=int)
# arg_parser.add_argument('--start', action='store', type=int)
arg_parser.add_argument('--behav', action='store', type=str)
#state = 'large'
#ac = 't15'

# Identify the system where the code is running
hostname = socket.gethostname()
if hostname.startswith('maestro-submit'):
    script_name = 'sbatch_tars.sh'
    jobs_count = jobs_count_tars
elif hostname == 'patmos':
    script_name = 'sbatch_t_bayes.sh'
    jobs_count = jobs_count_t_bayes
elif hostname == 'onsager-dbc':
    script_name = 'job_manager.py'
    jobs_count = jobs_count_onsager
elif hostname == "thales.dbc.pasteur.fr":
    script_name = 'job_manager.py'
    jobs_count = jobs_count_chloe
else:
    print('Unidentified hostname "' + hostname +
          '". Unable to choose the right code version to launch. Aborting.')
    exit()


# Analyze if need to restart or resume
input_args = arg_parser.parse_args()
bl_restart = input_args.restart
# end = int(input_args.end)
# start = int(input_args.start)
end = 150
start = 0
print(end,start)
ac = input_args.ac
behav = input_args.behav
# If restart is required, regenerate all files
if bl_restart:
    print("Creating arguments list...")

    # Clear the arguments file
    try:
        os.remove(args_file)
    except:
        pass

    # Clean the logs and output folders
    for folder in ([logs_folder]):
        if os.path.isdir(folder):
            print("Cleaning up the folder: '" + folder + "'.")
            cmd = "rm -rfv " + folder
            try:
                os.system(cmd)
            except Exception as e:
                print(e)

        # Recreate the folder
        try:
            os.makedirs(folder)
        except Exception as e:
            print(e)

    # Clean slurm files in the root folder
    cmd = "rm -fv ./slurm-*"
    try:
        os.system(cmd)
    except Exception as e:
        print(e)
    if ac =='t2' or ac == 't0' or ac =='t7':
        path_ = r'/pasteur/zeus/projets/p02/hecatonchire/tihana/' + ac + '/'
    if ac == 't15' :
        path_ = r'/pasteur/zeus/projets/p02/hecatonchire/screens/' + ac + '/'

    Liste_set = []
    f = open("DataMaxT2_miss2.txt","r")

#    f = open("DataMaxT2_20221027.txt","r")
    #f = open("DataMaxT7.txt","r")
    for x in f:
        Liste_set.append(x.split('\n')[0])
    Dossier = Liste_set

#[#''FCF_attP2@UAS_TNT_2_0003/p_5_60s1x30s0s#n#n#n']


    Dossier =  ['GMR_SS00740@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n','GMR_SS00740@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n']

    
    
    #['FCF_attP2@UAS_GtACR1_450/p_4_60s1x30s0s#n#n#n','FCF_attP2@UAS_GtACR1_450/p_5_60s1x30s0s#n#n#n',
            #    'FCF_attP2@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED10_60s1x30s0s#n#n','FCF_attP2@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
            #    'GMR_11A07@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n','GMR_11A07@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED10_60s1x30s0s#n#n',
            #    'FCF_attP2-40@UAS_GtACR1_450/p_4_60s1x30s0s#n#n#n','FCF_attP2-40@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
            #    'FCF_attP2-40@UAS_GtACR1_450/p_5_60s1x30s0s#n#n#n','FCF_attP2-40@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
            #    'GMR_SS00739@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n','GMR_SS00739@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
            #    'GMR_SS00740@UAS_GtACR1_450/p_4_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n','GMR_SS00740@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n'
            #    ]
    
#     ['FCF_attP2@UAS_GtACR1_450/p_5_60s1x30s0s#oi_redLED100_60s1x30s0s#n#n',
# 'GMR_11A07@UAS_GtACR1_450/p_5_60s1x30s0s#oi_redLED100_60s1x30s0s#n#n',
# 'EL-GAL4_R11F02-GAL80@FCF_attP2/p_5_60s1x30s0s#oi_redLED100_60s1x30s0s#n#n',
# 'EL-GAL4_R11F02-GAL80@UAS_GtACR1_450/p_5_60s1x30s0s#oi_redLED100_60s1x30s0s#n#n'] 
    
    # ['FCF_attP2@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
    # 'GMR_11A07@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
    # 'EL-GAL4_R11F02-GAL80@FCF_attP2/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n',
    # 'EL-GAL4_R11F02-GAL80@UAS_GtACR1_450/p_5_60s1x30s0s#oi_greenLED50_60s1x30s0s#n#n']
    
    # ['GMR_61D08@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#fe_90_0s1x60s0s#n',\
    # 'GMR_61D08@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#pd_90_0s1x60s0s#n',\
    # 'GMR_61D08@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#st_300_0s1x60s0s#n',\
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#fe_90_0s1x60s0s#n',\
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#pd_90_0s1x60s0s#n',\
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch17p5_60s1x30s0s#120s10x2s8s#st_300_0s1x60s0s#n',
    # 'GMR_61D08@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#fe_90_0s1x60s0s#n',
    # 'GMR_61D08@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#pd_90_0s1x60s0s#n',
    # 'GMR_61D08@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#st_300_0s1x60s0s#n',
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#fe_90_0s1x60s0s#n',
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#pd_90_0s1x60s0s#n',
    # 'FCF_attP2@20XUAS_CsChrimsom_mVenus/ch_17_60s1x30s0s#ch_17_120s10x2s8s#st_300_0s1x60s0s#n']
    #print(Liste_set)
    # dirs = [f for f in [i for i in list(os.listdir(
    #     path_)) if '.mat' not in i] if path.isdir(path_ + f)]
    # Dossier = []
    # for ff in dirs:
    #     if '.mat' not in ff:
    #         if ff not in [i.split('/')[0] for i in Liste_set ]:
    #             if not os.path.isfile('output/'+str(ac)+'/df_'+str(ac)+'_'+str(behav)+'_Before_' + str(ff) + '_t.pkl'):
    #                 Dossier.append(ff)
    #Dossier = [''GMR_11A07@20XUAS_CsChrimsom_mVenus',''FCF_attP2@20XUAS_CsChrimsom_mVenus']
    #print((files))
    #Dossier = [j for j in Liste_set if '30s1' in j]
    #Dossier = [''GMR_SS01935@UAS_Chrimson_Venus_X_0070/r_LED100_30s2x15s30s#n#n#n',',''GMR_SS01934@UAS_Chrimson_Venus_X_0070/r_LED100_30s2x15s30s#n#n#n',']

 #    Dossier = [''FCF_attP2-40@'FCF_attP2-40/p_4_60s1x30s0s#p_4_120s10x2s8s#n#n',
 # ''GMR_11A07@20XUAS_CsChrimsom_mVenus/p_4_60s1x30s0s#ch_17_60s1x30s0s#n#n',
 # ''GMR_11A07@UAS_TNT_2_0003/p_6_60s1x30s0s#n#n#n']
    #Dossier = Liste_set

    #Dossier = [''GMR_20B01@UAS_Chrimson_Venus/X_0070/p_8_45s1x30s0s#r_LED100_45s1x30s0s#n#n',''GMR_SS00739@UAS_Chrimson_Venus/X_0070/p_8_45s1x30s0s#r_LED100_45s1x30s0s#n#n']
    print(Dossier)
    id = 0
    with open(args_file, 'w') as file_object:
        for files in Dossier:
            id += 1
            args_string = '-n=%s --id=%i -s=%i -e=%i -a=%s -b=%s\n' % (
                files, id, start, end, ac, behav)
            file_object.write(args_string)

    # Create lock file
    with open(args_lock, 'w'):
        pass

    print("Argument list created. Launching sbatch...")

    line_count = id
else:
    print("Resuming simulation with the same arguments file")


# Launch job

if script_name == 'job_manager.py':
    cmd_str = 'python3 %s' % (script_name)
    popens = []
    pids = []
    for j in range(1, jobs_count + 1):
        cur_popen = subprocess.Popen(["python3", script_name])
        popens.append(cur_popen)
        pids.append(cur_popen.pid)
    print("Launched %i local job managers" % (jobs_count))
    print("PIDs: ")
    print(pids)

    # Collect exit codes
    for j in range(jobs_count):
        popens[j].wait()
    print("All job managers finished successfully")

else:
    # -o /dev/null
    cmd_str = 'sbatch --array=1-%i %s' % (jobs_count, script_name)
    os.system(cmd_str)
