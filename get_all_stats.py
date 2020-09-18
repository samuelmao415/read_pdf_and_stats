import pandas as pd
import re
import numpy as np

from urllib.request import urlopen
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import  LAParams
import logging
import re

def readPdf(pdf_file):
    logging.propagate = False
    logging.getLogger().setLevel(logging.ERROR)
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr=rsrcmgr, outfp=retstr, laparams=laparams)

    process_pdf(rsrcmgr=rsrcmgr, device=device, fp=pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()

    return content

def search_key(body, key, backward, forward):

    #key: keyword
    #backward: positions going back
    res = [i for i in range(len(body)) if body.startswith(key, i)]
    if res:
        end = [body[res - backward:res + forward] + '||' for res in res]
    else:
        end = ''
#     print(f' 总共 {len(end)} 次 提到了 {key}')
#     print(f'展示: {end}')
    return([key, len(end), end])

import glob
import pandas as pd

# Get a list of all the csv files
# files = list(glob.glob('.//./*.pdf'))

import os

#we shall store all the file names in this list
files = []
path = input('path:')
for root, dirs, filelist in os.walk(path):
    for file in filelist:
        #append the file name to the list
        if file.endswith('pdf'):
            files.append(os.path.join(root,file))

print(files)



#print all the file names

def read_file(file, key, backward, forward):
    df = pd.DataFrame()

    pdf_file = open(file,'rb') #local
    try:
        content = readPdf(pdf_file)
        s = r'(\n|\r|\xa0|/s/|\t|&nbsp;|&#\d*;|\x0c|\…|\u3000)'
        body = re.sub(s,'',content)
        pdf_file.close()
        key_word_list = search_key(body = body, key = key, backward = backward, forward = forward)
    #     print(key_word_list)
        df['file'] = [file]
        df['key'] = [key_word_list[0]]
        df['metioned_times'] = [key_word_list[1]]
        df['cases'] = [key_word_list[2]]

        df['city'] = file.split('/')[-2]
    except Exception as exception:
        print(f'error: {file}')

    return(df)

# key = '社会'
key = input('key to search:')
backward = int(input('backward:'))
forward = int(input('forward:'))


df = pd.DataFrame()
for i in range(len(files)):
    individual_result = read_file(file = files[i], key = key, backward = backward, forward = forward)
#     print(individual_result)
    df = df.append(individual_result)

# exg = read_file(file = file, key=key, backward = backward, forward = forward)

import os
d = os.getcwd()

# dir_name = d.split('/')[-2]
# df['city'] = [dir_name]* df.shape[0]
  #generate a unique file name based on the id and record
file_name= key + '.csv'

#create the CSV
df.to_csv(path+file_name, index = False)
