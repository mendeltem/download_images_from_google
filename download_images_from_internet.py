#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 17:11:46 2022

@author: temuuleu
"""

import pip
from os import listdir
from os.path import join
import os


def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        
        pip.main(['install', package])       
        
import_or_install("googlesearch")
import_or_install("bs4")

import random
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
        
        
def download_images_from_url_list(list_of_images,result_path):
        
    for image_url in list_of_images:
        
                
        try:
            b_name  = os.path.basename(image_url)
            
            pure_name  = b_name.split(".")[0]
            ending     = b_name.split(".")[1]
            pure_name = pure_name + str(random.randint(1,1000))
            
            b_name     = pure_name+"."+ending
            result_image = join(result_path,b_name)
            print(f"downloading {image_url}")

            urllib.request.urlretrieve(image_url, result_image)
        except:
            print("failed")
            
            
def get_sub_url_images(url):

    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    scheme  = urlparse(url).scheme
    domain_link = scheme + "://"+ domain_name
    soup = bs(requests.get(url).content, "html.parser")
    
    soup_content = requests.get(url).content
    
    list_urls = []
    list_of_images = []
    extern_links  = []

    try:
        soup_utf8  = soup_content.decode("utf-8") 
        matches = re.findall('\"(.*?)\"',soup_utf8)
        matches += re.findall('\'(.*?)\'',soup_utf8)

        for match in matches:
            if ".jpg" in match:
                print(match)
                list_of_images+=[match]
    except:
        print("utfailed")
      
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        
        if href:
            if href[0]=="/":
                link = domain_link+href
                if href.endswith(".jpg") or href.endswith(".png"): 
                    list_of_images.append(link)
                else:  
                    list_urls.append(link)
                    
            elif not "@" in href or not "mail" in href:
                extern_links.append(href)
                    
    return list(set(list_urls)),list(set(list_of_images)),list(set(extern_links))


result_path ="/home/temuuleu/CSB_NeuroRad/temuuleu/Projekts/Download_images_from_internet/images"
create_dir(result_path)


search_list = list(search("whale images",num_results=10, lang="en"))
url  = search_list[1]


all_list_of_images = []
all_extern_links_level_2 = []
all_extern_links_level_3 = []

list_urls,list_of_images,extern_links  = get_sub_url_images(url)
#download_images_from_url_list(list_of_images,result_path)
all_list_of_images += list_of_images

for url_s in list_urls:
    list_urls,list_of_images,extern_links_level_2  = get_sub_url_images(url_s)
    print(list_of_images)
    all_list_of_images += list_of_images
    all_extern_links_level_2 += extern_links_level_2
   
    
for extern_link in extern_links:
    print("extern links :", extern_link)
    list_urls,list_of_images,extern_links_level_2  = get_sub_url_images(extern_link)
    all_list_of_images += list_of_images
    all_extern_links_level_2 += extern_links_level_2
    
    for url_s in list_urls:
        list_urls,list_of_images,matches  = get_sub_url_images(url_s)
        print(list_of_images)
        all_list_of_images += list_of_images
        
        
all_extern_links_level_2 = list(set(all_extern_links_level_2))   
    
for extern_link in all_extern_links_level_2:
    print("extern links :", extern_link)
    list_urls,list_of_images,extern_links_level_3  = get_sub_url_images(extern_link)
    all_list_of_images += list_of_images
    all_extern_links_level_3 += extern_links_level_3
    
    for url_s in list_urls:
        list_urls,list_of_images,extern_links_level_3  = get_sub_url_images(url_s)
        print(list_of_images)
        all_list_of_images += list_of_images
        
        
#get unique links    
for i,image_link in enumerate(all_list_of_images):
    regex_find_html = "(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    
    r = re.findall(regex_find_html,image_link)
    
    if r:
        tupl = r[0]
        image_link_joined = tupl[0]+"://"+ tupl[1] + tupl[2]
        all_list_of_images[i] = image_link_joined
        
    
    
all_list_of_images = list(set(all_list_of_images))   
len(all_list_of_images)
#download all images
download_images_from_url_list(all_list_of_images,result_path)

