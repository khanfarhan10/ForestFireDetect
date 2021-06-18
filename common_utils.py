!pip install kaggle


import os
def get_size(path = os.getcwd()):
    print("Calculating Size: ",path)
    total_size = 0
    #if path is directory--
    if os.path.isdir(path):
      print("Path type : Directory/Folder")
      for dirpath, dirnames, filenames in os.walk(path):
          for f in filenames:
              fp = os.path.join(dirpath, f)
              # skip if it is symbolic link
              if not os.path.islink(fp):
                  total_size += os.path.getsize(fp)
    #if path is a file---
    elif os.path.isfile(path):
      print("Path type : File")
      total_size=os.path.getsize(path)
    else:
      print("Path Type : Special File (Socket, FIFO, Device File)" )
      total_size=0
    bytesize=total_size
    print(bytesize, 'bytes')
    print(bytesize/(1024), 'kilobytes')
    print(bytesize/(1024*1024), 'megabytes')
    print(bytesize/(1024*1024*1024), 'gegabytes')
    return total_size


x=get_size("/content/examples")



import os
os.makedirs("/content/.kaggle/")

import json
token = {"username":"farhanhaikhan","key":"f2c0df223af325f0d811a0f18b0c02ca"}
with open('/content/.kaggle/kaggle.json', 'a+') as file:
    json.dump(token, file)

import shutil
os.makedirs("/.kaggle/")
src="/content/.kaggle/kaggle.json"
des="/.kaggle/kaggle.json"
shutil.copy(src,des)


os.makedirs("/root/.kaggle/")
!cp /content/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle config set -n path -v /content

#https://towardsdatascience.com/setting-up-kaggle-in-google-colab-ebb281b61463

!kaggle competitions download -c digit-recognizer

!kaggle datasets download -d tawsifurrahman/covid19-radiography-database

!unzip -q covid19-radiography-database.zip -d /content/dataset



src="/content/Dataset.zip"
des="/content/DATA/"
get_ipython().system('unzip -q {} -d {}'.format(src,des))

import os
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
    return dir


import os
import zipfile
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
def zipper(dir_path,zip_path):
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dir_path, zipf)
    zipf.close()


zipper('/content/MAIN/Train',"Zipped_Data.zip")

MAIN="/content/DATA"
SLAVE="/content/final-dataset/"
create_dir(MAIN)
#we want directories such as
#DATA-> Train , Val-> Covid, Normal ,Viral_Pneumonia

TRAIN_PATH = "/content/DATA/Train"
VAL_PATH = "/content/DATA/Val"

create_dir(TRAIN_PATH)
create_dir(VAL_PATH)

from sklearn.model_selection import train_test_split
import random
def distribute(SRC_PATH="/content/final-dataset",TRAIN_PATH="/content/DATA/Train",VAL_PATH="/content/DATA/Val",current_class="abc",
               max_val=0,split_frac=0.8):
  SRC_CLASS_PATH=os.path.join(SRC_PATH,current_class)
  TRAIN_CLASS_PATH=os.path.join(TRAIN_PATH,current_class)
  VAL_CLASS_PATH=os.path.join(VAL_PATH,current_class)
  ITEMS=os.listdir(SRC_CLASS_PATH)
  if (max_val!=0):
    try:
      ITEMS=random.choices(ITEMS,k=max_val)
    except:
      ITEMS = random.sample(ITEMS, max_val)
    print("Length of ",current_class," trimmed to ",len(ITEMS))
  print("Length of ",current_class," ",len(ITEMS))
  random.seed(43) #make this expt reproducable
  x=ITEMS
  y=range(len(x))
  xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.2, random_state = 43)
  TRAIN_IMGS=xTrain
  VAL_IMGS=xTest

  print("Train : Val Lists ",len(TRAIN_IMGS)," : ",len(VAL_IMGS))

  for each_img in TRAIN_IMGS:
    src=os.path.join(SRC_CLASS_PATH,each_img)
    des=os.path.join(TRAIN_CLASS_PATH,each_img)
    shutil.copy(src,des)
  for each_img in VAL_IMGS:
    src=os.path.join(SRC_CLASS_PATH,each_img)
    des=os.path.join(VAL_CLASS_PATH,each_img)
    shutil.copy(src,des)

category_classes=["COVID-19","NORMAL","Viral Pneumonia"]
for each_class in category_classes:
  create_dir(os.path.join(TRAIN_PATH,each_class))
  create_dir(os.path.join(VAL_PATH,each_class))
  distribute(current_class=each_class,max_val=375)
#75/375 is 20%
#trim all datasets to 300:75 ratio


#other augmentation techniques : CVD_DATASET

#to delete some data
#shutil.rmtree("/content/DATA")




#COVID ZIPPER
from google.colab import drive
drive.mount('/content/drive')

import shutil
import os
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
    return dir

src="/content/drive/My Drive/NEW_DATA/FINAL_AUG_DATA"
des="/content/MAIN"

shutil.copytree(src,des)


def zipper(dir_path,zip_path):
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dir_path, zipf)
    zipf.close()


import os
import zipfile
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
def zipper(dir_path,zip_path):
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    zipdir(dir_path, zipf)
    zipf.close()


zipper('/content/MAIN/Train',"'Zipped_Dataset_Train.zip'")

zipf = zipfile.ZipFile('Zipped_Dataset_Train.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('/content/MAIN/Train', zipf)
zipf.close()

zipf = zipfile.ZipFile('Zipped_Dataset_Val.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('/content/MAIN/Val', zipf)
zipf.close()

import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
RES="/content/drive/My Drive/NEW_DATA/"
zip_file=find('*Zipped_Dataset_Val.zip', '/content/')
print(zip_file[0])
src=zip_file[0]
des=os.path.join(RES,"Zipped_Dataset_Val.zip")
shutil.copy(src,des)


zip_file2=find('*Zipped_Dataset_Train.zip', '/content/')
print(zip_file2[0])

src=zip_file2[0]
des=os.path.join(RES,"Zipped_Dataset_Train.zip")
shutil.copy(src,des)


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
dir="/content/drive/My Drive/NEW_DATA/FINAL_AUG_DATA"
bytesize=get_size(dir)
print(bytesize, 'bytes')
print(bytesize/(1024*1024), 'megabytes')
print(bytesize/(1024*1024*1024), 'gegabytes')

#download the dataset

#main_runner

#https://towardsdatascience.com/setting-up-kaggle-in-google-colab-ebb281b61463
#setting up kaggle in your colab

import os
os.makedirs("/content/.kaggle/")

import json
token = {"username":"farhanhaikhan","key":"f2c0df223af325f0d811a0f18b0c02ca"}
with open('/content/.kaggle/kaggle.json', 'a+') as file:
    json.dump(token, file)

import shutil
os.makedirs("/.kaggle/")
src="/content/.kaggle/kaggle.json"
des="/.kaggle/kaggle.json"
shutil.copy(src,des)


os.makedirs("/root/.kaggle/")
!cp /content/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle config set -n path -v /content

#https://towardsdatascience.com/setting-up-kaggle-in-google-colab-ebb281b61463

!pip install kaggle
!kaggle datasets download -d tawsifurrahman/covid19-radiography-database


!unzip -q covid19-radiography-database.zip -d /content/dataset

from PIL import Image
directory="/content/dataset/COVID-19 Radiography Database/COVID-19/"
output="/content/dataset_compressed/COVID-19 Radiography Database/COVID-19/"
os.makedirs(output)
list_files=os.listdir(directory)

for each in list_files:
  full_path=os.path.join(directory,each)
  foo = Image.open(full_path)
  x,y=foo.size
  x=round(x*0.8)
  y=round(y*0.8)
  foo = foo.resize((x,y),Image.ANTIALIAS)
  foo.save(os.path.join(output,each),optimize=True,quality=95)
"""
The normal chest X-ray (left panel) depicts clear lungs without any areas of abnormal opacification in the image. Bacterial pneumonia (middle) typically exhibits a focal lobar consolidation, in this case in the right upper lobe (white arrows), whereas viral pneumonia (right) manifests with a more diffuse ‘‘interstitial’’ pattern in both lungs.
"""

#auc roc curve
#intersection
#https://github.com/ieee8023/covid-chestxray-dataset
#https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia









#merge all notebooks in a directory!
import os, fnmatch
import io
import sys
import nbformat
from nbformat import v4 as nbf

#from IPython import nbformat #is deprecated
#finds files in a directory corresponding to a regex query
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result



#code to print a list vertically :)
def print_list(lst):
  for i in lst:
    print(i)

#function to merge multiple notebooks into one file
def merge_notebooks(filenames,output="output_finale.ipynb",start=True,end=True):
    merged = nbf.new_notebook()
    count=0
    for fname in filenames:
        count+=1
        with io.open(fname, 'r', encoding='utf-8') as f:
            print("Reading Notebook",count," : ",fname)
            nb = nbformat.read(f, as_version=4)
            if start:
              start_text = """## Start of notebook """+str(os.path.basename(fname))
              start_cells = [nbformat.v4.new_markdown_cell(start_text)]
              merged.cells.extend(start_cells)

            merged.cells.extend(nb.cells)
            print("Appending to Output Notebook",count," : ",fname)
            if end:
              end_text = """## End of notebook """+str(os.path.basename(fname))
              end_cells = [nbformat.v4.new_markdown_cell(end_text)]
              merged.cells.extend(end_cells)
    if not hasattr(merged.metadata, 'name'):
        merged.metadata.name = ''
    merged.metadata.name += "_merged"
    print("Merging to Output Notebook : ",output)
    with io.open(output, 'w', encoding='utf-8') as f:
      nbformat.write(merged, f)
      #print("Merged to Output Notebook : ",os.path.join(os.getcwd(),output))
      print("Merged to Output Notebook : ",output)
    #print(nbformat.writes(merged))
    #nbformat.writes(merged)
#sorted_list=sorted([notebook_files], key=str.lower)
#sort by basename
notebook_files=find('*.ipynb', '/content/')
notebook_files.sort(key=lambda x: os.path.basename(x))
print(len(notebook_files),"Notebook Files Found :")
print_list(notebook_files)
merge_notebooks(filenames=notebook_files,output="merged_output_notebook.ipynb")












#answer on stackoverflow 4 line indent code
filename="/content/db_code.txt"
with open(filename) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.rstrip() for x in content]

for e in content:
  print(str("    ")+e)

#finds files in a directory corresponding to a regex query
import os, fnmatch
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

zip_file=find('*covid19-radiography-database.zip', '/content/')
print(zip_file)

#scrape a table from a webpage
import requests
import pandas as pd

url = "http://www.inwea.org/wind-energy-in-india/wind-power-potential/"
html = requests.get(url).content
df_list = pd.read_html(html)
print(len(df_list))
df1,df2 = df_list
#Estimation of installable wind power potential at 80 m level,Estimation of installable wind power potential at 100 m level
df1.to_csv('small_data.csv')
df2.to_csv('big_data.csv')


df.to_csv('50-80.csv', index = False, header=True)


import os, fnmatch
import sqlite3
import pandas as pd

#creates a directory without throwing an error
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
  else:
    print("Directory already existed : ", dir)
  return dir

#finds files in a directory corresponding to a regex query
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result



#convert sqlite databases(.db,.sqlite) to pandas dataframe(excel with each table as a different sheet or individual csv sheets)
def save_db(dbpath=None,excel_path=None,csv_path=None,extension="*.sqlite",csvs=True,excels=True):
    if (excels==False and csvs==False):
      print("Atleast one of the parameters need to be true: csvs or excels")
      return -1

    #little code to find files by extension
    if dbpath==None:
      files=find(extension,os.getcwd())
      if len(files)>1:
        print("Multiple files found! Selecting the first one found!")
        print("To locate your file, set dbpath=<yourpath>")
      dbpath = find(extension,os.getcwd())[0] if dbpath==None else dbpath
      print("Reading database file from location :",dbpath)

    #path handling

    external_folder,base_name=os.path.split(os.path.abspath(dbpath))
    file_name=os.path.splitext(base_name)[0] #firstname without .
    exten=os.path.splitext(base_name)[-1]   #.file_extension

    internal_folder="Saved_Dataframes_"+file_name
    main_path=os.path.join(external_folder,internal_folder)
    create_dir(main_path)


    excel_path=os.path.join(main_path,"Excel_Multiple_Sheets.xlsx") if excel_path==None else excel_path
    csv_path=main_path if csv_path==None else csv_path

    db = sqlite3.connect(dbpath)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(len(tables),"Tables found :")

    if excels==True:
      #for writing to excel(xlsx) we will be needing this!
      try:
        import XlsxWriter
      except ModuleNotFoundError:
        !pip install XlsxWriter

    if (excels==True and csvs==True):
      writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing Excel Sheet ",i," : ",table_name)
          table.to_excel(writer, sheet_name=table_name, index=False)
          print("Parsing CSV File ",i," : ",table_name)
          table.to_csv(os.path.join(csv_path,table_name + '.csv'), index_label='index')

      writer.save()


    elif excels==True:
      writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing Excel Sheet ",i," : ",table_name)
          table.to_excel(writer, sheet_name=table_name, index=False)

      writer.save()

    elif csvs==True:
      i=0
      for table_name in tables:
          table_name = table_name[0]
          table = pd.read_sql_query("SELECT * from %s" % table_name, db)
          i+=1
          print("Parsing CSV File ",i," : ",table_name)
          table.to_csv(os.path.join(csv_path,table_name + '.csv'), index_label='index')
    cursor.close()
    db.close()
    return 0
save_db();

#mount the drive where we have the downloaded trained weights
from google.colab import drive
drive.mount('/content/drive',force_remount=True)


from google.colab import drive
drive.mount('/gdrive')


#common utility functions used everywhere
from IPython.display import FileLink
FileLink(r'/kaggle/input/lung-segmentation-unet/best_model.h5')


#creates a directory without throwing an error
def create_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
    print("Created Directory : ", dir)
  else:
    print("Directory already existed : ", dir)
  return dir
#counts the number of files in a directory
def count_no(dir):
  lst=os.listdir(dir)
  return len(lst)

def ListDiff(li1, li2):
    return (list(set(li1) - set(li2)))

import os
import zipfile
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
zipf = zipfile.ZipFile('Zipped_Dataset.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('/content/FINAL_AUG_DATA', zipf)
zipf.close()



get_ipython().system('unzip -q {} -d /content/kaggle_dir'.format(zip_file[0]))
print("Done Unzipping!")

#main_runner

#https://towardsdatascience.com/setting-up-kaggle-in-google-colab-ebb281b61463
#setting up kaggle in your colab

import os
os.makedirs("/content/.kaggle/")

import json
token = {"username":"farhanhaikhan","key":"f2c0df223af325f0d811a0f18b0c02ca"}
with open('/content/.kaggle/kaggle.json', 'a+') as file:
    json.dump(token, file)

import shutil
os.makedirs("/.kaggle/")
src="/content/.kaggle/kaggle.json"
des="/.kaggle/kaggle.json"
shutil.copy(src,des)


os.makedirs("/root/.kaggle/")
!cp /content/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle config set -n path -v{/content}


#############################
#download google drive file to kaggle_dir
#turn on the internet first

import gdown

url = 'https://drive.google.com/uc?id=1UP_Gv9D0nqTHaK7haudwPqjshW_XYEFz'

output = 'dataset.zip'

gdown.download(url, output, quiet=False)

####################

def print_dict(new_dict):
    #print ("Dictionary is :  ")
    #print("keys: values")
    for i in new_dict:
        print(i, " :", new_dict[i])
############################
!unzip -q /kaggle/working/dataset.zip -d /kaggle/working/data_aug
#############################
import shutil
shutil.rmtree("/kaggle/working/data_aug")
##############################
import shutil
src=""
des=""
shutil.copy(src,des)
###########################
import os

"""def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size
dir="/content/drive/My Drive/NEW_DATA/FINAL_AUG_DATA"
bytesize=get_size(dir)
print(bytesize, 'bytes')
print(bytesize/(1024*1024), 'megabytes')
print(bytesize/(1024*1024*1024), 'gegabytes')"""
##########################################################################
#listing directories
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

##############################################################################
os.path.getsize("best_model_todate")/(1024*1024) #megabytes
########################################################################
"""if os.path.isdir(path):
    print("\nIt is a directory")
elif os.path.isfile(path):
    print("\nIt is a normal file")
else:
    print("It is a special file (socket, FIFO, device file)" )"""
#https://www.w3resource.com/python-exercises/python-basic-exercise-85.php

import os
def get_size(path = os.getcwd()):
    print("Calculating Size: ",path)
    total_size = 0
    #if path is directory--
    if os.path.isdir(path):
      print("Path type : Directory/Folder")
      for dirpath, dirnames, filenames in os.walk(path):
          for f in filenames:
              fp = os.path.join(dirpath, f)
              # skip if it is symbolic link
              if not os.path.islink(fp):
                  total_size += os.path.getsize(fp)
    #if path is a file---
    elif os.path.isfile(path):
      print("Path type : File")
      total_size=os.path.getsize(path)
    else:
      print("Path Type : Special File (Socket, FIFO, Device File)" )
      total_size=0
    bytesize=total_size
    print(bytesize, 'bytes')
    print(bytesize/(1024), 'kilobytes')
    print(bytesize/(1024*1024), 'megabytes')
    print(bytesize/(1024*1024*1024), 'gegabytes')
    return total_size


x=get_size("/content/examples")





# -*- coding: utf-8 -*-
"""BeautifulSoup1.0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r3tWW0YZBHIGSwJYOkKXN3MolgT0LryS

#Getting the query from the search
"""

from bs4 import BeautifulSoup
import re
import requests
import random

req_name="snakes"
#request name that triggers everything in the following code
#reques name is the only expected input by the user


#function that returns google search results based upon a query
#here we want pinterest photo links only

def google_search_results(req_name):
  #https://hackernoon.com/how-to-scrape-google-with-python-bo7d2tal
  #https://github.com/getlinksc/scrape_google/blob/master/search.py

  # desktop user-agent
  USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
  # mobile user-agent
  MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

  query = req_name
  #https://www.google.com/search?q=tigers+photos+pinterest
  query = query.replace(' ', '+')
  URL = f"https://google.com/search?q={query}"
  #print(URL)
  headers = {"user-agent": USER_AGENT}
  resp = requests.get(URL, headers=headers)

  if resp.status_code == 200:
      soup = BeautifulSoup(resp.content, "html.parser")
      results = []
      for g in soup.find_all('div', class_='r'):
          anchors = g.find_all('a')
          if anchors:
              link = anchors[0]['href']
              title = g.find('h3').text
              item = {
                  "title": title,
                  "link": link
              }
              results.append(item)
  return results

#code to print a list vertically :)
def print_list(lst):
  for i in lst:
    print(i)


#extracts the urls from the search query
def extract_urls(search_res):
  urls=[]
  for site in search_res:
    urls.append(site["link"])
  return urls

#filters out the pinterest urls from the list of urls
#most probably not required as google searches keywords efficiently
def filter_pin_urls(urls):
  filtered_links=[]
  for url in urls:
    if(re.search("pinterest",url)):
      filtered_links.append(url)
  return filtered_links



#get links from google for pinterest pics
def get_img_url(req_name):
  search_res=google_search_results(req_name+" photos pinterest")
  #print_list(search_res)
  query_urls=extract_urls(search_res)
  filtered_urls=filter_pin_urls(query_urls)
  #print_list(filtered_urls)
  #print(len(filtered_urls))
  req_url=random.choice(filtered_urls)
  #print(req_url)
  return (req_url)


req_url=get_img_url(req_name)
print(req_url)

def get_all_hyperlinks(data):
  links=[]
  for link in data.findAll('a', attrs={'href': re.compile("^http://")}):
    #links.append()
    print (link.get('href'))

"""#IMAGE DOWNLOAD PART"""

import urllib.request
#handles getting all image webpage data as string
def get_data(url):
  html_page=urllib.request.urlopen(url)
  soup = BeautifulSoup(html_page)
  data=str(soup)
  return data

#find all image urls ending with jpg
def find_all_image_urls(s):
  #pinterest concentration
  #syntax
  #{"url":"https://i.pinimg.com/474x/2a/16/b0/2a16b0c151a32a58d735bb46f589f6f6.jpg"
  #lst = re.findall('"url":"http\S+jpg"', s)
  #lst = re.findall('"url":"http[^,]+jpg"', s)
  lst = re.findall('http[^,]+jpg', s)
  #todo ending with other extensions png etc
  return lst





#filter that searches for the word originals in the set of urls for pinterest specefically this is important
def filtered_urls(lst):
  new_lst=[]
  for i in lst:
    if(re.search("originals",i)):
      new_lst.append(i)
  return new_lst


string_data=get_data(req_url)
#print(string_data)
image_urls=find_all_image_urls(string_data)
unique_urls=set(image_urls)
orig_urls=filtered_urls(unique_urls)
print_list(orig_urls)
#.*\.ccf$
#todo add other file formats

# \S matches any non-whitespace character
# ^ Match the start of the string
# $ Match the end of the string


"""The matching pattern could be:

^([^,]+),
That means

^        starts with
[^,]     anything but a comma
+        repeated one or more times (use * (means zero or more) if the first field can be empty)
([^,]+)  remember that part
,        followed by a comma"""

#handles downloading all images on the list of images

import os


#name of the directory in which images will be saved
def dir_name(req_name):
  directory="/content"+"/"+req_name+"/"
  if not os.path.isdir(directory):
    os.makedirs(directory)
  return directory





#downloads the images from list of urls to given output directory
def download_images(urls,dir):
  #wget -P /var/cache/foobar/ [...]
  #wget --directory-prefix=/var/cache/foobar/ [...]\
  for url in urls:
    os.system('wget -P %s %s' %(dir,url))

dir=dir_name(req_name)
print(dir)
download_images(orig_urls,dir)

#downloads all the images from the given request name .
#Not recommended to use as will take up lots of internet and storage space
def download_all_imgs(query):
  search_res=google_search_results(query+" photos pinterest")
  #print_list(search_res)
  query_urls=extract_urls(search_res)
  filtered_links=filter_pin_urls(query_urls)
  for each_url in filtered_links:
    string_data=get_data(each_url)
    #print(string_data)
    image_urls=find_all_image_urls(string_data)
    unique_urls=set(image_urls)
    orig_urls=filtered_urls(unique_urls)
    #print_list(orig_urls)
    download_images(orig_urls,dir)


#download_all_imgs("linkin_park")
#download_all_imgs(req_name)

import os

# Get the list of all files and directories
# in the root directory
path = dir
dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")

# print the list
print_list(dir_list)

print("No of downloaded images :",len(dir_list))

#code to copy downloaded content to your personal drive
#mount drive before running this piece of code
import shutil
src_dir=dir
des_dir="/content/drive/My Drive/Linkin_Park"
#shutil.copytree(src_dir,des_dir)



#todo perhaps for other websites than pinterest, use filter good quality pics
from PIL import Image
#im = Image.open("texture.jpg")
#print (im.size)
#The size is given as a 2-tuple (width, height)
#getting image resolutions in python
#delete/filterout low resolution images

"""#GET TEXT PART"""

#!git clone https://github.com/hunkim/word-rnn-tensorflow.git
#https://medium.com/deep-writing/how-to-write-with-artificial-intelligence-45747ed073c
#checkout deep writing later

def filter_wiki_urls(urls):
  filtered_links=[]
  for url in urls:
    if(re.search("wikipedia",url)):
      filtered_links.append(url)
  return filtered_links

def filter_urls_with_keyword(urls,word):
  #if word is found in the list of urls then only return url
  filtered_links=[]
  for url in urls:
    if(re.search(word,url)):
      filtered_links.append(url)
  return filtered_links


#a text url generator using req_name as input
def get_txt_url(req_name):
  search_res=google_search_results(req_name+" wikipedia")
  #print_list(search_res)
  query_urls=extract_urls(search_res)
  filtered_urls=filter_wiki_urls(query_urls)
  #print_list(filtered_urls)
  #print(len(filtered_urls))
  #req_url=random.choice(filtered_urls)
  req_url=filtered_urls[0] #the first url
  #print(req_url)
  return (req_url)



# specify which URL/web page we are going to be scraping
# sampler text_url = "https://en.wikipedia.org/wiki/Tiger"
text_url=get_txt_url(req_name)

# open the url using urllib.request and put the HTML into the page variable
page = urllib.request.urlopen(text_url)

# parse the HTML from our URL into the BeautifulSoup parse tree format
soup = BeautifulSoup(page)
#print(soup)

#https://www.thepythoncode.com/article/access-wikipedia-python

!pip install wikipedia

import wikipedia
# print the summary of what python is
print(wikipedia.summary(req_name))
#wikipedia.summary(req_name, sentences=2)
#fixed number of sentences in wiki summary

#https://stackoverflow.com/questions/15228054/how-to-count-the-amount-of-sentences-in-a-paragraph-in-python
import re
par=wikipedia.summary(req_name)
text=re.split(r'[.!?]+', par)
#text contains list of lines in wikipedia search query for request name
print_list(text)
len(text)

result = wikipedia.search(req_name)
print_list(result)
#similar results as req_name

page = wikipedia.page(result[0])
title = page.title
print(page)
print()
print(title)
print()

categories = page.categories
print_list(categories)

# get the whole wikipedia page text (content)
content = page.content
content=str(content)

modified_content = content.replace('.','\n')
#https://stackoverflow.com/questions/1546226/what-is-a-simple-way-to-remove-multiple-spaces-in-a-string
single_spaces=re.sub(' +', ' ',modified_content)
lines_of_content=modified_content.splitlines()
#print(modified_contents)
#print_list(lines_of_content[1:100])


#cleanup the list (non uniform spacing between paras to uniform spacing)

#https://www.geeksforgeeks.org/python-remove-additional-spaces-in-list/
# Python3 code to demonstrate
# removing multiple spaces
# using list comprehension + enumerate()

# initializing list of lists
test_list = lines_of_content


# using list comprehension + enumerate()
# removing multiple spaces and keeping just one
res = [val for idx, val in enumerate(test_list)
	if val or (not val and test_list[idx - 1])]



#insert a basic intro"== Basic Introduction ==" at the beginning of the contents list

index=0
#beginning of the list
value="== Basic Introduction =="
res.insert(index, value)

print_list(res[0:])

#temp code to check if below works properly
abcdres="""Recent molecular studies support the monophyly of the clades of modern snakes, scolecophidians, typhlopids + anomalepidids, alethinophidians, core alethinophidians, uropeltids (Cylindrophis, Anomochilus, uropeltines), macrostomatans, booids, boids, pythonids and caenophidians

=== Families ===

=== Legless lizards ===

While snakes are limbless reptiles, which evolved from (and are grouped with) lizards, there are many other species of lizards which have lost their limbs independently and superficially look similar to snakes
 These include the slowworm and glass snake

== Biology ==

=== Size ===

==  Ki Re  ==
The now extinct Titanoboa cerrejonensis snakes were 12"""
#results expected 2,9
#lst = res.replace('.','\n')
#res=lst.splitlines()
#print(res)
#print(len(res))
#type(res)
#expected output 4,13

#print(res[4])
#print(res[13])

#function that keeps the last of repeated titles (deleted titles to be added later in a slide)

def isheading(line):
  return re.search("==",line)



def get_titles_to_keep(results):
  revres=results[::-1]
  #print_list(revres)
  titles_to_keep=[]
  for i in range(0,len(revres)):
    line=revres[i]
    #if empty line,do nothing
    if len(line.strip()) == 0 :
      #print("empty line found",i)
      continue
    #non empty line do what??
    #two cases possible
    #case1 title
    elif isheading(line):
      #print("Title line found",i,line,flag)
      if(flag==0):
        titles_to_keep.append(i)
      flag=flag+1
    #case2 normal topic content line
    else:
      #print("normal content found",i)
      flag=0
  length=len(revres)

  #print(titles_to_keep)

  #actually operating on reversed list
  actual_titles_to_keep = [length-x-1 for x in titles_to_keep]

  actual_titles_to_keep.sort()
  #print(actual_titles_to_keep)

  titles=[]
  for element_index in actual_titles_to_keep:
    #print(res[element_index])
    titles.append(results[element_index])
  return actual_titles_to_keep,titles


title_indexes,title_names=get_titles_to_keep(res)

print_list(title_indexes)
print_list(title_names)

#https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/

def merge_list_to_dict(test_keys,test_values):
  # using dictionary comprehension
  # to convert lists to dictionary
  merged_dict = {test_keys[i]: test_values[i] for i in range(len(test_keys))}
  return merged_dict


sub_headings=merge_list_to_dict(title_names,title_indexes)
print(sub_headings)

def getKeys(dict):
  return dict.keys()
def getVals(dict):
  return dict.values()
def convert_to_list(iterable):
  lst=[]
  for each in iterable:
    lst.append(each)
  return lst
#https://www.geeksforgeeks.org/python-create-list-of-numbers-with-given-range/
def createList(r1, r2):
  return list(range(r1, r2))

def rank_dict(input_dict):
  count=0
  list_of_keys=convert_to_list(getKeys(input_dict))
  list_of_ranks=createList(0,len(list_of_keys))
  ranked_dictionary=merge_list_to_dict(list_of_keys,list_of_ranks)
  #print(list_of_keys)
  return ranked_dictionary

ranked_sub_headings=rank_dict(sub_headings)
print(ranked_sub_headings)

def extract_all_titles(results):
  all_title_names=[]
  all_title_indexes=[]
  length=len(results)
  for i in range(length):
    line=results[i]
    if isheading(line):
      all_title_names.append(line)
      all_title_indexes.append(i)
  return all_title_names,all_title_indexes

all_title_names,all_title_indexes=extract_all_titles(res)
#print_list(all_title_names)
all_titles=merge_list_to_dict(all_title_names,all_title_indexes)
print(all_titles)
ranked_all_titles=rank_dict(all_titles)
print(ranked_all_titles)

#https://www.geeksforgeeks.org/python-difference-in-keys-of-two-dictionaries/

#returns a dict that gives the difference between two dictionaries keeping the values from first keeping as values
def dictdiffkeys(dict1,dict2):
  lst=[]
  for key in dict1.keys():
    if not key in dict2:
      # Printing difference in
      # keys in two dictionary
      lst.append(key)
  new_dict={}
  for each in lst:
    new_dict[each]=dict1[each]
  return new_dict


blank_titles=dictdiffkeys(ranked_all_titles,ranked_sub_headings)
print(blank_titles)

#https://stackoverflow.com/questions/32815640/how-to-get-the-difference-between-two-dictionaries-in-python
def dictdiff(dict1,dict2):
  set_1 = set(dict1.items())
  set_2 = set(dict2.items())
  newdict=dict(set_1 - set_2)
  return newdict


#special titles that get deleted
trimmed_titles=dictdiff(all_titles,sub_headings)
print(trimmed_titles)

def getKeys(dict):
    return dict.keys()
def getVals(dict):
    return dict.values()

def convert_to_list(iterable):
  lst=[]
  for each in iterable:
    lst.append(each)
  return lst


trimmed_titles_indexes=convert_to_list(getVals(trimmed_titles))
trimmed_titles_names=convert_to_list(getKeys(trimmed_titles))

print()
print(trimmed_titles_indexes)

from collections import OrderedDict
from operator import itemgetter

def sort_dict_by_val(InputDict):
  return dict( sorted(InputDict.items(), key=itemgetter(1),reverse=False))

#arranged_trimmed_titles= OrderedDict(sorted(trimmed_titles.items(), key=itemgetter(1)))
#arranged_trimmed_titles = dict( sorted(trimmed_titles.items(), key=itemgetter(1),reverse=False))
arranged_trimmed_titles=sort_dict_by_val(trimmed_titles)
print(arranged_trimmed_titles)

res[395]

import copy
#Note that you need to delete them in reverse order so that you don't throw off the subsequent indexes.
#https://stackoverflow.com/questions/11303225/how-to-remove-multiple-indexes-from-a-list-at-the-same-time

def delete_indexes(results,trimmed_titles_indexes):
  copied_results=copy.deepcopy(results)
  for index in sorted(trimmed_titles_indexes, reverse=True):
      del copied_results[index]
  return copied_results

trimmed_results=delete_indexes(res,trimmed_titles_indexes)
print_list(trimmed_results[0:200])

# using list comprehension + enumerate()
# removing multiple spaces and keeping just one
def clean_spacing(results):
  test_list=copy.deepcopy(results)
  res = [val for idx, val in enumerate(test_list)
  if val or (not val and test_list[idx - 1])]
  return test_list
cleaned_trimmed_results=clean_spacing(trimmed_results)
print_list(cleaned_trimmed_results[0:500])

def isempty(line):
  return len(line.strip()) == 0


#clean spacing before and after title
def find_spacing_before_after(results):
  long_text=copy.deepcopy(results)
  empty_lines_to_del=[]
  length=len(long_text)
  for i in range(length):
    line=long_text[i]
    if isheading(line):
      #check positions i+1,i-1 for blanks
      if(isempty(long_text[i+1])):
        empty_lines_to_del.append(i+1)
      if(isempty(long_text[i-1])):
        empty_lines_to_del.append(i-1)
  return empty_lines_to_del

del_indices=find_spacing_before_after(cleaned_trimmed_results)
final_results=delete_indexes(cleaned_trimmed_results,del_indices)
print_list(final_results)

def delete_indexes(results,trimmed_titles_indexes):
  copied_results=copy.deepcopy(results)
  for index in sorted(trimmed_titles_indexes, reverse=True):
      del copied_results[index]
  return copied_results

def isempty(line):
  return len(line.strip()) == 0
def isheading(line):
  return re.search("==",line)
def iscontent(line):
  return (not (isheading(line))) and (not (isempty(line)))


def get_single_spacing(text):
  contents=copy.deepcopy(results)
  lines_to_del=[]
  length=len(contents)
  for i in range(length):
    line=contents[i]
    #if isheading(line):
      #do nothing
  return empty_lines_to_del

def isempty(line):
  return len(line.strip()) == 0
def isheading(line):
  return re.search("==",line)
def iscontent(line):
  return (not (isheading(line))) and (not (isempty(line)))

def replace_titles(text):
  contents=copy.deepcopy(text)
  length=len(contents)
  for i in range(length):
    line=contents[i]
    if isheading(line):
      contents[i]="===="
  return contents
sample=replace_titles(final_results)
#print_list(sample)

import itertools
def my_separator(lst):
  #https://stackoverflow.com/questions/6164313/make-python-sublists-from-a-list-using-a-separator
  sample_list = ['|', u'MOM', u'DAD', '|', u'GRAND', '|', u'MOM', u'MAX', u'JULES', '|']
  key = lambda sep: sep == '===='
  new_lst=[list(group) for is_key, group in itertools.groupby(lst, key) if not is_key]
  return new_lst

topics=my_separator(sample)
print_list(topics[0])

#all_paras[topic_no][para_no][line_no]
def para_separator(lst):
  #https://stackoverflow.com/questions/6164313/make-python-sublists-from-a-list-using-a-separator
  sample_list = ['|', u'MOM', u'DAD', '|', u'GRAND', '|', u'MOM', u'MAX', u'JULES', '|']
  key = lambda sep: sep == ''
  new_lst=[list(group) for is_key, group in itertools.groupby(lst, key) if not is_key]
  return new_lst

all_paras=[]
for each_topic in topics:
  paras=para_separator(each_topic)
  all_paras.append(paras)

#print(all_paras[0][0][-1])
print()
print_list(all_paras[0][0])
#NOICE :)

"""{'=== Families ===': 6, '== Biology ==': 8, '== Behavior ==': 18, '== Interactions with humans ==': 27, '== See also ==': 36, '== References ==': 37, '== Further reading ==': 38}"""

#swaps key value pairs in a dictionary
#https://www.geeksforgeeks.org/python-program-to-swap-keys-and-values-in-dictionary/

def swap_dict(old_dict):
  new_dict = {}
  for key, value in old_dict.items():
    if value in new_dict:
      new_dict[value].append(key)
    else:
      new_dict[value]=[key]
  return new_dict

# Printing new dictionary after swapping
# keys and values
def print_dict(new_dict):
  print ("Dictionary is :  ")
  print("keys: values")
  for i in new_dict:
      print(i, " :", new_dict[i])

#master_topics=merge_list_to_dict(title_names,topic)

def extract_all_titles(results):
  all_title_names=[]
  all_title_indexes=[]
  length=len(results)
  for i in range(length):
    line=results[i]
    if isheading(line):
      all_title_names.append(line)
      all_title_indexes.append(i)
  return all_title_names,all_title_indexes

all_title_names,all_title_indexes=extract_all_titles(res)
#print_list(all_title_names)




#main function that will extract results like title:text
def construct_master_lists(results):

  return empty_lines_to_del

def get_paras(text):
  #dont know what
  return 1

#more cleanup needed
#if there is a space after title but before content cleanup


for line in res[0:100]:
  #if empty line,jump to next line
  if len(line.strip()) == 0 :
    continue
  #non empty line do what??
  #two cases possible
  #case1 title
  if(re.search("^== .*==$",line)):
    #print(line)
    #get the first occurence
    title=re.findall("^== .*==$",line)[0]
    #print(title)
    actual_title=title[3:len(title)-3]
    #print(actual_title)
  #case2 normal line
  topic_content=[]

#https://stackoverflow.com/questions/7896495/python-how-to-check-if-a-line-is-an-empty-line/7896585

#get list of topics as dictionary
#format topics["Basic Intro"]="longggg text"
topics={}

for line in res[0:100]:
  #if empty line,jump to next line
  if len(line.strip()) == 0 :
    continue
  #non empty line do what??
  #two cases possible
  #case1 title
  if(re.search("^== .*==$",line)):
    #print(line)
    #get the first occurence
    title=re.findall("^== .*==$",line)[0]
    #print(title)
    actual_title=title[3:len(title)-3]
    #print(actual_title)
  #case2 normal line
  topic_content=[]




#construct text para by para
text=[]

#format should be text[paranumber][linenumber]

#paragraph


#bullets

#paraphrasing=on/off part non plagiarised text

#itworks!!
#https://github.com/getlinksc/scrape_google/blob/master/search.py
#https://hackernoon.com/how-to-scrape-google-with-python-bo7d2tal
import urllib
import requests
from bs4 import BeautifulSoup

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

query = "hackernoon How To Scrape Google With Python"
query = query.replace(' ', '+')
URL = f"https://google.com/search?q={query}"

headers = {"user-agent": USER_AGENT}
resp = requests.get(URL, headers=headers)

if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)
    print(results)
