import requests
from wsse.client.requests.auth import WSSEAuth

from bs4 import BeautifulSoup

import os, os.path, sys
import glob

from xml.etree import ElementTree
import xml.etree.ElementTree as ET

import uuid
import datetime
import base64
import hashlib
import os


###########################################
def request_xml(url): # This function will get the url and will return the xml response
    Username = 'username'
    Password = 'pass'
    PasswordMD = 'b1d2128cee734a257c5e0d5c73bbdd1b'
    Nonce = 'd36e316282959a9ed4c89851497a717f'
    Date = datetime.datetime.now().replace(microsecond=0)
    Created = Date.isoformat()
    ApiCode = '123456789'


    Combination = ApiCode + Nonce + Created + PasswordMD

    PasswordDigest = base64.b64encode(hashlib.sha1(Combination.encode('utf8')).digest())
    #PasswordDigest = str(Baseto64, "utf-8")

    payload = {'Authorization': 'WSSE profile = "UsernameToken"', 'X-WSSE': 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}",ApiCode="{}"'.format(Username, PasswordDigest, Nonce, Created, ApiCode)}
    response = requests.get(url, headers=payload) 

    return response

###########################################
def get_final_xml_file(url):
    final_xml_file_response = request_xml(url) #request xml data of products
    return final_xml_file_response # get all product ids from final xml file
    
###########################################
    
def get_product_ids(xml): #This function gets product ids for further get request from first file
    ids_list = [] # holds all the ids in final xml file
    
    try:
        x = BeautifulSoup(xml.text,'xml')
        ids = x.findAll('id')
        
        for i in ids: # append all the product ids in this list
            ids_list.append(i.text) 
        
        return ids_list 
    except:
        pass

###########################################

def get_single_product_xml(ids_list): # Get each data of each product separately 
    xml_list = [] # contains all the xmls of all products
    primary_url = "http://api.polycomp.bg/service/data/v1/extproduct/"
    for i in ids_list:
        final_url_product = primary_url+str(i) # Combined url with product id 
        response = request_xml(final_url_product) #request xml of single product
        
        xml_list.append(response)
    
    return xml_list # returns the list containing xml of each product separately

###########################################

def generate_all_product_xml(xml_list): # This function take xml of single product and merge it into the final one.
    
    root = ET.Element("All products") # Root element in which all productdata will be enclosed
    
    for response_xml in xml_list:
        response_xml.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>','') # Remove unwanted first line from each file
        ET.SubElement(root,response_xml.text) # append each product xml to under the root
        
    tree = ET.ElementTree(root) # Form an xml tree and then write it to the file
    
    
    #Save this file to another location or rename it to avoid overwriting of next final file
    tree.write("final_file.xml") 
    
    
###########################################
    
if __name__ == "__main__":
    ### Enter the data 
    vendor_id = str(input("Enter the vendor id: "))
    group_id = str(input("Enter the group id: "))
    SubGroup_id = str(input("Enter the sub_group id: "))
    
    
    ### AFTER ENTRING THE WILL BE YOUR FINAL URL
    final_url = "http://api.polycomp.bg/service/data/v1/products/test/"+vendor_id+"/"+group_id+"/"+SubGroup_id
    
    #Request Data of products in one file from where we gonna get product ids for furhter use
    products_total_xml = get_final_xml_file(final_url)
    
    #Send the final_
    ids_list = get_product_ids(products_total_xml) # This will save the product ids in global variable ids_list
    
    #get each product xml in a list 
    xml_list = get_single_product_xml(ids_list)
    
    #Generate final file containing all products
    generate_all_product_xml(xml_list)
    
    
    