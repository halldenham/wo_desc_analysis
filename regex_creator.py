# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 11:59:26 2017

@author: dh1023
"""

import pandas as pd

# import data
raw_phrase_s = r'C:\Users\dh1023\Desktop\Python\wo_code_analysis' \
              '\wo_code_to_phrase_key_input.xlsx'
raw_phrases = pd.read_excel(raw_phrase_s)

'''
create a regex to combine two phrases
regex example to combine "toilet" and "clogged" would be:
\btoilet\b.*\bclogged\b

But, if there's only 1 phrase, then only have that be the criteria.
Example: "hydrastation" and a blank second phrase would only result in
\bhydrastation\b
'''
# set second phrase values to "blank" for use in if statement
phrases = raw_phrases.copy()
blank_er = 'blank_error' # blank error so replace with string
phrases['Second Phrase'] = phrases['Second Phrase'].fillna(blank_er)

# flip first and second phrase to create total list of possibilities
# but don't do it if there's NaN in the second column (aka it is a one-word
# phrase, so it doesn't need to be flipped)
phrases_flip = raw_phrases.dropna(subset=['Second Phrase']).copy()
# rename the columns to "flip" them
phrases_flip = phrases_flip.rename(columns = {
        'Second Phrase':'First Phrase', 'First Phrase':'Second Phrase'})

# append the flipped data to the phrases df
frames = [phrases, phrases_flip]
phrases_join = pd.concat(frames)

    
def regex_func(regex_data):
    if regex_data['Second Phrase'] == blank_er:
        return r'\b' + regex_data['First Phrase'] + r'\b'
    else:
        return r'\b' + regex_data['First Phrase'] + \
                       r'\b.*\b' + regex_data['Second Phrase'] + r'\b'


phrases_join['regex_key'] = phrases_join.apply(regex_func, axis=1)


phrases_join.to_excel('wo_code_to_phrase_key.xlsx', index=False)
print('Done')


##############################################################
##################### old code ###############################
##############################################################

#if phrases['Second Phrase'] == blank:
#    phrases['regex_key'] = r'\b' + phrases['First Phrase'] + r'\b'
#else:
#    phrases['regex_key'] = r'\b' + phrases['First Phrase'] + \
#                       r'\b.*\b' + phrases['Second Phrase'] + r'\b'

#frame = pd.DataFrame(np.random.randn(4, 3), columns=list('abc'))
#frame[['b','c']].apply(lambda x: x['c'] if x['c']>0 else x['b'], axis=1)

#phrases[['First Phrase','Second Phrase']].apply(lambda x: x['First Phrase'] if x['First Phrase']=='1' else x['Second Phrase'], axis=1)
#phrases.apply(lambda x: x['First Phrase'] if x['First Phrase']=='1' else x['Second Phrase'], axis=1)
#phrases.apply(lambda x: x['First Phrase'] if x['Second Phrase'] == 'blank_er' else x['Second Phrase'], axis=1)

#phrases.apply(lambda x: x['First Phrase'] if x['Second Phrase']==1, axis=1)

#phrases['regex_key'] = r'\b' + phrases['First Phrase'] + \
#                       r'\b.*\b' + phrases['Second Phrase'] + r'\b'