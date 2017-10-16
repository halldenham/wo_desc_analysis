# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:42:23 2017

@author: dh1023
"""

import pandas as pd
import numpy as np
import re

'''
This script will reference a dictionary of regular expressions that are
associated with particular "WO Types"

The initial thought is to scan the WO description to see if it matches any
of the RegEx in the dictionary, then list all distinct WO Type matches     
'''

'''
############################################################################
compile all the regex's into a usable format (dataframe)
'''
# import and create dataframe of the reference/dictionary of wo codes
path_phrase_dict = r'C:\Users\dh1023\Desktop\Python\wo_code_analysis' \
                    '\wo_code_to_phrase_key.xlsx'
raw_phrase_dict = pd.read_excel(path_phrase_dict)

# find all the distinct wo codes
distinct_codes = list(raw_phrase_dict['WO Code'].unique())

# create an empty dataframe
regex_df = pd.DataFrame(columns =['wo_code','regex_list'])
# fill dataframe with wo code and corresponding regex
i = 0
while i < len(distinct_codes):
    # for each distinct wo code, loop through and compile a 
    # list of regex then append that list to a dataframe
    
    # select the regex corresponding with that wo code from the dataframe
    regex_list = raw_phrase_dict[
                 raw_phrase_dict['WO Code'] == distinct_codes[i]]
    # compile the regex's in to a list
    compiled_regex_list = re.compile(r'\b(?:%s)\b' % '|'.join(
            regex_list.loc[:,'regex_key']), re.IGNORECASE)
    # write the regex's and correspodning code in to a dataframe
    regex_df.loc[i,'wo_code'] = distinct_codes[i]
    regex_df.loc[i,'regex_list'] = compiled_regex_list
    
    i = i + 1



'''
############################################################################
create a function to run the regex's through the wo data and return codes
'''
def regex_phrase3(x):    
# find if there's any matches to current regex and return previous and 
# current WO code matches

    # search through the WO descriptions for matching regex
    m = re.search(regex_exp, x['WO Description'])
    
    # if there is a matching regex 
    if m:
        if x['code1'] == None:
            # return the wo code in first slot
            return regex_code, None, None
        elif x['code2'] == None:
            # return the wo code in second slot
            return x['code1'], regex_code, None
        elif x['code3'] == None:
            # return the wo code in third slot
            return x['code1'], x['code2'], regex_code
        else:
            # if more than 3 codes, return "more codes" in third slot
            return x['code1'], x['code2'], 'more codes'
    
    # if there's no match, return current codes
    else:
        return x['code1'], x['code2'], x['code3']



'''
############################################################################
create a loop to run each series of regex phrases through the wo description
'''
# import data
path_wo_data = r'C:\Users\dh1023\Desktop\Python\3. Reference Files or ' \
                'Standards\Generic_WO_Report_SR entered and completed ' \
                'Aug2015 to Aug2017.xlsx'
raw_wo_data = pd.read_excel(path_wo_data, sheetname='Fewer Columns')

# clean data -- drop blank wo descriptions for regex later on
wo_data = raw_wo_data.dropna(subset=['WO Description']).copy()

# create a dataframe of just the description and blank columns for the codes
wo_desc = wo_data.loc[:,{'WO Description', 'WO_Num'}].copy()
wo_desc['code1'] = None
wo_desc['code2'] = None
wo_desc['code3'] = None

print('starting loop')
ii = 0
while ii < len(regex_df):
    regex_exp = regex_df.loc[ii,'regex_list']
    regex_code = regex_df.loc[ii,'wo_code']
    
    # results of the regex code function in a df
    df0 = pd.DataFrame(wo_desc.apply(regex_phrase3, axis=1).tolist(), 
                       columns=['code1', 'code2', 'code3'])
    # drop the old code 1, 2, 3 from wo_desc df
    wo_desc = wo_desc.drop(['code1', 'code2', 'code3'], axis=1)
    # add the results back to the wo_desc df
    wo_desc = pd.concat([wo_desc, df0], axis=1, join_axes=[wo_desc.index])
    ii = ii +1

# drop the duplicate columns, and add the WO code columns to original data
wo_codes = wo_desc.drop(['WO Description', 'WO_Num'], axis=1)
wo_data = pd.concat([wo_data, wo_codes], axis=1, join_axes=[wo_data.index])

# if there is a keyword associated with the WO, overwrite the code1
# whether or not it's null or filled with the word "equipment"
wo_data['code1'] = np.where(wo_data['Equip Keyword'].notnull(), 
       'equipment', wo_data['code1'])

# export full wo data
wo_data.to_excel('wo_code_results.xlsx', index=False)

# export wo data without any codes
wo_data_no_code = wo_data.copy()
# select data where "results" column has no value
wo_data_no_code = wo_data_no_code[wo_data_no_code['code1'].isnull()]
wo_data_no_code.to_excel('no_wo_code_results.xlsx', index=False)





