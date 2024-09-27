import pandas as pd
import pickle
import numpy as np
import copy
import glob


def used_classifier(CLF_HCSO,CLF_CHT,DF):
    Index_RF =  ['S_smooth_5 max','S_smooth_5 min','S_deriv_smooth_5 max','S_deriv_smooth_5 min','eig_smooth_5 max',
 'eig_smooth_5 min','eig_deriv_smooth_5 max','eig_deriv_smooth_5 min','motion_velocity_norm_smooth_5 max','motion_velocity_norm_smooth_5 min','head_velocity_norm_smooth_5 max',
 'head_velocity_norm_smooth_5 min','tail_velocity_norm_smooth_5 max','tail_velocity_norm_smooth_5 min','long_diff_ max',
 'long_diff_ min','projection_head max','projection_head min','projection_tail max','projection_tail min','theta_head max','theta_head min','theta_tail max','theta_tail min']

    DF = DF.reset_index(drop=True)
    X_pred=DF[Index_RF]
    DF_prediction=pd.DataFrame({'index':list(DF.index),'time':list(DF['time']),'Date':list(DF['Date']),'Line':list(DF['Line']),'Larva':list(DF['Larva']),'prediction':np.arange(len(X_pred)),'probabilities':np.arange(len(X_pred))}).set_index('index')

    for clf in CLF_HCSO:
        #print(clf)
        y_pred=clf.predict(X_pred)
        DF_prediction['test'+str(str(CLF_HCSO.index(clf)))]=pd.Series(list(y_pred),index=list(X_pred.index))    

    for i in range(len(DF_prediction.index[:])) :
        DF_prediction.iloc[i,4]=DF_prediction.iloc[i,6:].value_counts().index[0]
        DF_prediction.iloc[i,5]=DF_prediction.iloc[i,6:].value_counts()[0]/sum(DF_prediction.iloc[i,6:].value_counts())

    DF_N=DF.loc[list(DF_prediction[DF_prediction.prediction=='Other'].index)]
    X_pred=DF_N[Index_RF]
    DF_prediction_=pd.DataFrame({'index':list(DF_N.index),'time':DF_N['time'],'Date':list(DF_N['Date']),'Line':list(DF_N['Line']),'Larva':list(DF_N['Larva']),'prediction':np.arange(len(X_pred)),'probabilities':np.arange(len(X_pred))}).set_index('index')

    for clf in CLF_CHT:
        y_pred=clf.predict(X_pred)
        DF_prediction_['test'+str(CLF_CHT.index(clf))]=pd.Series(list(y_pred),index=list(X_pred.index))  
        
    for i in range(len(DF_prediction_.index) ):
        DF_prediction_.iloc[i,4]=DF_prediction_.iloc[i,6:].value_counts().index[0]
        DF_prediction_.iloc[i,5]=DF_prediction_.iloc[i,6:].value_counts()[0]/sum(DF_prediction_.iloc[i,6:].value_counts())
    DF_final_prediction = pd.concat((DF_prediction[~(DF_prediction.prediction=='Other')].iloc[:,:6],DF_prediction_.iloc[:,:6])) 
    return DF_final_prediction

def load_and_concat_files(path_pattern):
    files = glob.glob(path_pattern)
    df_combined = None
    
    for idx, file in enumerate(files):
        try:
            df = pd.read_pickle(file)
            if idx == 0:
                df_combined = copy.deepcopy(df)
            else:
                df_combined = pd.concat([df_combined, df], axis=1)
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    return df_combined.T if df_combined is not None else None


fichier_w = open(path_in + 'Random_forest_22_11.pkl', 'rb')
(CLF_HCSO,CLF_CHT) = pickle.load(fichier_w)

Features = pd.DataFrame({})
    # Define your paths
base_path = path_data+'/CSHAPE_Maxime/Dataframe_feats_hunch/output/t2/'
name_pattern = '*' + name + '*.pkl'

# Process each directory
df_hunch_weak_t2 = load_and_concat_files(base_path + 'hunch_weak/' + name_pattern)
df_bend_t2 = load_and_concat_files(base_path + 'bend_large/' + name_pattern)
df_hunch = load_and_concat_files(base_path + 'hunch_large/' + name_pattern)

DF = pd.concat([df_hunch,df_bend_t2,df_hunch_weak_t2]).reset_index(drop = True) 
Features = pd.concat([Features,DF])

DF_prediction = used_classifier(CLF_HCSO,CLF_CHT,DF)


DF_prediction.to_csv(path_out+'DF_prediction.csv')