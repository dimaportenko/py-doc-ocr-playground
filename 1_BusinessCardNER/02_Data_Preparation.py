import numpy as np
import pandas as pd
import cv2
import pytesseract

import os
from glob import glob
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

imgPaths = glob('./Selected/*.jpeg')
# print(imgPaths)

allBusinessCard = pd.DataFrame(columns=['id', 'text'])

for imgPath in tqdm(imgPaths,desc='BusinessCard'):

    _, filename = os.path.split(imgPath)
    # print(filename)

# extract data and text
    image = cv2.imread(imgPath)
    data = pytesseract.image_to_data(image)
    dataList = list(map(lambda x: x.split('\t'), data.split('\n')))
    df = pd.DataFrame(dataList[1:], columns=dataList[0])
    df.dropna(inplace=True)

    df['conf'] = df['conf'].astype(float).astype(int)
# useFullData = df[df['conf'] > 30]
    useFullData = df.query('conf > 30')
# print (useFullData)

    businessCard = pd.DataFrame()
    businessCard['text'] = useFullData['text']
    businessCard['id'] = filename

    # print(businessCard)

    # allBusinessCard = allBusinessCard.append(businessCard, ignore_index=True)
    allBusinessCard = pd.concat([allBusinessCard, businessCard], ignore_index=True)

print(allBusinessCard)
allBusinessCard.to_csv('allBusinessCard.csv', index=False)
