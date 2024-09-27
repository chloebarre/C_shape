
import glob
import os
import pickle
import re
import numpy as np
import pandas as pd
from function_features import *
import sys
from choose_version import choose, chooselabel
from constants import VARIABLE
import h5py
import argparse

def main(arg_str):

    version = 20180409
    arg_parser = argparse.ArgumentParser(
        description='Larvae behavior analysis')

    arg_parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + str(version))
    arg_parser.add_argument('--id', required=True, action='store', type=int,
                            help='A simulation identifier to be added to the output file')
    arg_parser.add_argument('-n', '--name', action='store',
                            type=str)
    arg_parser.add_argument('-a', '--ac',
                            action='store', type=str)
    arg_parser.add_argument('-s', '--start',
                            action='store', type=int)
    arg_parser.add_argument('-e', '--end',
                            action='store', type=int)

    arg_parser.add_argument(
        '-b', '--behav', action='store', type=str)

    input_args = arg_parser.parse_args(arg_str.split())

    #float(input_args.start)

    ac = input_args.ac
    behav = input_args.behav
    Line = input_args.name
    #t_start = 30.0
    #float(Line.split('s1x')[0][-2:])
    #t_end = 45.0
    #float(Line.split('s1x')[0][-2:]) + 15.0
    #t_start = float(Line.split('s1x')[0][-2:])
    #t_start = 60.0
    t_start = 0.0
    t_end = 150.0
    t_activation = 60.0

    # labels_ =['crawl_weak', 'crawl_strong', 'bend_weak', 'bend_strong', 'stop_weak',  'stop_strong', 'hunch_weak', 'hunch_large',\
    # 'back crawl weak', 'back_crawl_strong', 'roll weak', 'roll strong']


    labels_ = ['run_large', 'bend_large', 'stop_large', 'hunch_large', 'back_crawl_large', 'roll_large','small_motion']

    feats = ['S_smooth_5', 'S_deriv_smooth_5', 'eig_smooth_5', 'eig_deriv_smooth_5', 'motion_velocity_norm_smooth_5',
         'head_velocity_norm_smooth_5', 'tail_velocity_norm_smooth_5', 'long_diff_', 'projection_head', 'projection_tail','theta_head','theta_tail']
    feats_before = ['S_smooth_5','eig_smooth_5','head_velocity_norm_smooth_5','motion_velocity_norm_smooth_5','tail_velocity_norm_smooth_5']
    feats_after = ['S_smooth_5','eig_smooth_5','head_velocity_norm_smooth_5','motion_velocity_norm_smooth_5','tail_velocity_norm_smooth_5']

    Index_df = ['time','Larva','Date','Line','behav','S_smooth_5 max','S_smooth_5 min','S_deriv_smooth_5 max','S_deriv_smooth_5 min','eig_smooth_5 max',
     'eig_smooth_5 min','eig_deriv_smooth_5 max','eig_deriv_smooth_5 min','motion_velocity_norm_smooth_5 max','motion_velocity_norm_smooth_5 min','head_velocity_norm_smooth_5 max',
     'head_velocity_norm_smooth_5 min','tail_velocity_norm_smooth_5 max','tail_velocity_norm_smooth_5 min','long_diff_ max',
     'long_diff_ min','projection_head max','projection_head min','projection_tail max','projection_tail min','theta_head max','theta_head min','theta_tail max','theta_tail min',
     'S_smooth_5_before','eig_smooth_5_before','eig_deriv_smooth_5_before','head_velocity_norm_smooth_5_before','motion_velocity_norm_smooth_5_before','S_smooth_5_after','eig_smooth_5_after','head_velocity_norm_smooth_5_after','motion_velocity_norm_smooth_5_after']

    var = choose(ac)

    id = input_args.id
    path_=var.path
#    var.time_start = t_start
#    var.time_end = t_end
    if not os.path.exists('output/'+str(ac)+'/'+str(behav)+'/Data_'+str(ac)+'_'+str(behav)+'_'  + Line.split('/')[0]+Line.split('/')[-1] + '_23_02.pkl'):
        
        #behav_number = labels_.index(behav)/2+0.5
        behav_number = labels_.index(behav)+1
        df = pd.DataFrame({'index':Index_df}).set_index('index')
        nb_of_behaviour = -1
        subdirs = list(os.listdir(path_ + Line + '/'))
        print(Line)
        print(subdirs)

        Files = []

        for date in [j for j in subdirs if '.' not in j ]:
            print(date)
            #if date == '20191126_162650':
            try :
                print(date)
                name_file = path_ + Line + '/' + date +'/trx.mat'
                f = h5py.File(name_file, 'r')
                trx = f.get('trx')
            except :
                print('Nop',Line,date)
                continue
            df,nb_of_behaviour = obtaining_features(trx,f,df,nb_of_behaviour,behav_number,t_start,t_activation,t_end,feats,feats_before,feats_after)
            print(Line,date,df.shape)
            f.close()

        fichier_w = open('output/'+str(ac)+'/'+str(behav)+'/Data_'+str(ac)+'_'+str(behav)+'_'  + Line.split('/')[0]+Line.split('/')[-1] + '.pkl', 'wb')
        pickle.dump((df), fichier_w)
