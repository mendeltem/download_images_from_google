#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 17:11:46 2022

@author: temuuleu
"""

from os import listdir
from os.path import join
import os
import dicom2nifti

from nibabel import load,save

import googlesearch
from bs4 import BeautifulSoup as bs
from googlesearch import search

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

import re
import urllib.request

def create_dir(output_path):
    """creates a directory of the given path"""
    if not os.path.exists(output_path):
        os.makedirs(output_path)


result_path ="/home/temuuleu/CSB_NeuroRad/temuuleu/Projekts/Download_images_from_internet/images"
create_dir(result_path)

search_list = list(googlesearch.search("Bilder",num_results=10, lang="en"))
soup = requests.get(search_list[2]).content
soup_utf8  = soup.decode("utf-8") 

matches = re.findall('\"(.*?)\"',soup_utf8)

image_urls = []

for m in matches:
    if m.endswith("jpg"):
        print(m)
        image_urls.append(m)
        
b_name  = os.path.basename(image_urls[0])
result_image = join(result_path,b_name)
urllib.request.urlretrieve(image_urls[0], result_image)


