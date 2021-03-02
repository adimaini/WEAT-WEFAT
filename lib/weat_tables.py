import numpy as np
import os
import pandas as pd
from . import weat



def get_tar_att_arrays(model, t1, a1, a2, algorithm, t2=None,):
    '''Get the target and attribute arrays from the word embeddings'''

    if algorithm == 'weat':
        tar1 = np.array([model[vector] for vector in t1])
        tar2 = np.array([model[vector] for vector in t2])
        att1 = np.array([model[vector] for vector in a1])
        att2 = np.array([model[vector] for vector in a2])
        
        return tar1, tar2, att1, att2
    
    elif algorithm == 'wefat':
        tar1 = np.array([model[vector] for vector in t1])
        att1 = np.array([model[vector] for vector in a1])
        att2 = np.array([model[vector] for vector in a2])
        
        return tar1, att1, att2



def get_matrices(filepath, model, algorithm):
    ''' get the matrices of targets and attributes from word embeddings'''
    data_file = pd.read_csv(filepath, sep=',\s*', engine='python',  header=None, index_col=0)
    
    if algorithm == 'weat':
        # get targets and attribute labels
        target_names = list(data_file.index)[:2]
        attribute_names = list(data_file.index)[2:]

        # get targets and attribute sets
        targets = data_file.loc[target_names]
        attributes = data_file.loc[attribute_names]

        # get arrays, one for each set of target and attribute
        tar1 = targets.loc[target_names[0]]
        tar2 = targets.loc[target_names[1]]
        att1 = attributes.loc[attribute_names[0]]
        att2 = attributes.loc[attribute_names[1]]

        # remove any NaN values that have been read due to mismatch of columns 
        tar1 = tar1[~pd.isna(tar1)]
        tar2 = tar2[~pd.isna(tar2)]
        att1 = att1[~pd.isna(att1)]
        att2 = att2[~pd.isna(att2)]

        # give numpy array of glove word embeddings for targets and attributes
        tar1, tar2, att1, att2 = get_tar_att_arrays(model, tar1, att1, att2, algorithm, t2 = tar2, )

        return target_names, attribute_names, tar1, tar2, att1, att2
    
    elif algorithm == 'wefat':
        # get targets and attribute labels
        target_names = list(data_file.index)[:1]
        attribute_names = list(data_file.index)[1:]

        # get targets and attribute sets
        targets = data_file.loc[target_names]
        attributes = data_file.loc[attribute_names]

        # get arrays, one for each set of target and attribute
        tar1 = targets.loc[target_names[0]]
        att1 = attributes.loc[attribute_names[0]]
        att2 = attributes.loc[attribute_names[1]]

        # remove any NaN values that have been read due to mismatch of columns 
        tar1 = tar1[~pd.isna(tar1)]
        att1 = att1[~pd.isna(att1)]
        att2 = att2[~pd.isna(att2)]
        
        # give numpy array of glove word embeddings for targets and attributes
        tar1, att1, att2 = get_tar_att_arrays(model, tar1, att1, att2, algorithm)

        return target_names, attribute_names, tar1, att1, att2



def output_values(filepath, model, algorithm): 
    ''' gets the matrices, calculates the effect sixe, and calculates the p-values'''

    if algorithm == 'weat':     
        alg_object = weat.Weat()
        
        # retrieve target names and attributes to form the table
        target_names, attribute_names, _, _, _, _ = get_matrices(filepath, model, algorithm)
        # retrive the word embeddings for the targets and attributes
        _, _, t1, t2, a1, a2 = get_matrices(filepath, model, algorithm)
        # calculate the effect size 
        effect_size = alg_object.effect_size(t1, t2, a1, a2)
        # calculate the p-value, test statistic, and permutations
        p_val, test_stat, distr = alg_object.p_value(t1, t2, a1, a2)
        
        
    elif algorithm =='wefat':
        alg_object = weat.Wefat()
        
        # retrieve target names and attributes to form the table
        target_names, attribute_names, _, _, _ = get_matrices(filepath, model, algorithm)
        # retrive the word embeddings for the targets and attributes
        _, _, targets, a1, a2 = get_matrices(filepath, model, algorithm)
        
        effect_size, p_val = list(), list()
        for target in targets:
            # calculate the effect size 
            eff_size = alg_object.effect_size(target, a1, a2)
            effect_size.append(eff_size)
            
            # calculate the p-value, test statistic, and permutations
            p_value, test_stat, distr = alg_object.p_value(target, a1, a2)
            p_val.append(p_value)

    
    return target_names, attribute_names, effect_size, p_val



def output_table(model, algorithm, filepath):
    '''created an output dataframe table that can be used'''

    print('Reading files...\n')
     
    _, _, e_s, p_value = output_values(filepath, model, algorithm)
    
    if algorithm == 'wefat':
        # get the targets from the first row of the file
        target = pd.read_csv(filepath, nrows=1, header=None).dropna(axis=1).values.flatten().tolist()
        # strip whitespaces around the target names
        target = list(map(str.strip, target))
        output_df = pd.DataFrame(data = list(zip(target, e_s, p_value)), columns = ['Target', 'Effect Size', 'P-Value'])
    
    elif algorithm =='weat':
        output_df = pd.DataFrame(data = {'Effect Size': e_s, 'P-Value': p_value}, index=[0])
        
    output_df['Effect Size'] = output_df['Effect Size'].round(decimals=2)

    print('Finished.')
    return output_df