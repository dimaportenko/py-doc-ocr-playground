import numpy as np
import pandas as pd
import cv2
import PIL
import pytesseract
import spacy

img_cv = cv2.imread('./Selected/052.jpeg')
# cv2.imshow('Bussiness Card', img_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img_pil = PIL.Image.open('./Selected/052.jpeg')

text_cv = pytesseract.image_to_string(img_cv)
# print(text_cv)

text_pil = pytesseract.image_to_string(img_pil)
# print(text_pil)

data = pytesseract.image_to_data(img_cv)

dataList = list(map(lambda x: x.split('\t'), data.split('\n')))
df = pd.DataFrame(dataList[1:], columns=dataList[0])

print(df)

df.dropna(inplace=True)

# col_int = ['level',	'page_num', 'block_num', 'par_num',	'line_num',	'word_num',	'left',	'top', 'width',	'height', 'conf', 'text']
col_int = ['level','page_num','block_num','par_num','line_num','word_num','left','top','width','height', 'conf']
df[col_int] = df[col_int].astype(float).astype(int)

image = img_cv.copy()

for l, x, y, w, h, c, txt in df[['level', 'left', 'top', 'width', 'height', 'conf', 'text']].values:
# for l, x, y, w, h, txt in zip(df['level'], df['left'], df['top'], df['width'], df['height'], df['text']):
    # print(txt)

    if l == 5:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.putText(image, txt, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.imshow('Bussiness Card', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
