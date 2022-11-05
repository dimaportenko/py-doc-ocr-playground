import numpy as np
import pandas as pd
import string
import re

with open('./businessCard.txt', mode='r', encoding='utf8', errors='ignore') as f:
    text = f.read()


# print(text)
data = list(map(lambda x:x.split('\t'), text.split('\n')))
df = pd.DataFrame(data[1:], columns=data[0])
# print(df.head())

whitespace = string.whitespace
punctuation = '!#$%&\'()*+:;<=>?[\\]^`{!}~'
tableWhitespace = str.maketrans('', '', whitespace)
tablePunctuation = str.maketrans('', '', punctuation)

def cleanText(txt):
    text = str(txt)
    text = text.lower()
    removewhitespace = text.translate(tableWhitespace)
    removepunctuation = removewhitespace.translate(tablePunctuation)

    return str(removepunctuation)

df['text'] = df['text'].apply(cleanText)
# dataClean = df[df['text'] != '']
dataClean = df.query('text != ""')
dataClean.dropna(inplace=True)

print(dataClean.head(10))

group = dataClean.groupby(by='id')
cards = group.groups.keys()
print(cards)

allCardsData = []
for card in cards: 
    cardData = []
    grouparray = group.get_group('000.jpeg')[['text', 'tag']].values
    content = ''
    annotations = {'entities':[]}
    start = 0
    end = 0

    for text, label in grouparray:
        text = str(text)
        stringLength = len(text) + 1

        start = end
        end = start + stringLength

        if label != 'O':
            annotations['entities'].append((start, end, label))

        content = content + text + ' '
    
    cardData = (content, annotations)
    allCardsData.append(cardData)

# print(annotations)
# print(content)

# print(content.find('info@laurelseducation.com') + len('info@laurelseducation.com'))

# print(allCardsData)


card_data_df = pd.DataFrame(allCardsData,columns=['text','labels'])
card_data_df['isNull'] = card_data_df['labels'].apply(lambda x: 'Null' if len(x['entities']) ==0 
                                                      else 'Clean')
card_data_df.query('isNull == "Null"')

card_data_df.dropna(inplace=True)
clean_data = card_data_df.query('isNull == "Clean"')[['text','labels']]

allCardsData = list(map(lambda x: tuple(x), clean_data.values.tolist()))

import random

random.shuffle(allCardsData)

print(len(allCardsData))

TrainData = allCardsData[:240]
TestData = allCardsData[240:]

import pickle

pickle.dump(TrainData, open('./data/TrainData.pickle', 'wb'))
pickle.dump(TestData, open('./data/TestData.pickle', 'wb'))
