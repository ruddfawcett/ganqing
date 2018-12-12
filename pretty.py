#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
import json
import urllib.request

emotions = csv.DictReader(open('chinese_emotions_original.csv'))
next(emotions)

words = []

for emotion in emotions:
    char_info = emotion["Emotion word"].replace("‘",'').replace("’",'').split(' ')
    zh = char_info[0]

    type1_p = emotion["MC2"].split(', ')[0].split(' ')[1].replace('(', '').replace(')', '')
    type2_p = emotion["MC2"].split(', ')[1].split(' ')[1].replace('(', '').replace(')', '')

    if type1_p == 'NA': type1_p = 0
    if type2_p == 'NA': type2_p = 0

    entry = {
        'zh': zh,
        'pinyin': char_info[1],
        'eng': char_info[2],
        'rad': 0,
        'mean_intensity': emotion["MC1"].split(' ')[0],
        'mean_intensity_sd': emotion["MC1"].split(' ')[1].replace('(', '').replace(')', ''),
        'type1': emotion["MC2"].split(', ')[0].split(' ')[0],
        'type1_p': type1_p,
        'type2': emotion["MC2"].split(', ')[1].split(' ')[0],
        'type2_p': type2_p,
        'pos': emotion["MC3"].split(', ')[0],
        'neg': emotion["MC3"].split(', ')[1],
        'neu': emotion["MC3"].split(', ')[2]
    }

    rad_check = json.loads(urllib.request.urlopen(f'http://localhost:3000/?ch={urllib.parse.quote(zh)}').read())

    entry.update(rad_check)
    words.append(entry)

master_db = pd.DataFrame(words, columns=words[0].keys())
master_db.set_index('pinyin', inplace=True)
master_db.to_csv('emotions_modified.csv')
