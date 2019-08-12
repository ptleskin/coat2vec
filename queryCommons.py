'''
Created on 8 Dec 2018
@author: petrileskinen
'''

from collections import Counter
from csv import DictReader

import glob
import json
import os
import requests
import random
import re 
import shutil
import sys
import time 

LANGS = ['en', 'fr', 'sv', 'fi', 'eo', 'eu', 'nl', 'hu', 'en', 'pt', 'la', 'es', 'sk', 'ca', 'it', 'cs', 'nn', 'gl', 'no', 'sp', 'pl', 'da', 'et', 'ru', 'de', 'br']

COATDESCRIPTIONFILE = 'Commons-vaakunat.csv'
OUTFOLDER = 'commons'
STARTNUMBER = 0
IMAGESIZE = 299

#    for downloading coats of arms from wikimedia commons
def main(args):
    

    data = readCoats(100, [])
    commands = []
    for i, ob in enumerate(data):
        
        outfolder = OUTFOLDER # +random.choice(['test','train','train','train','train','train'])
        
        res = makeCommonsQuery(ob['url'])
        try:
            pages = res['query']['pages']
            for k in pages:
                if 'imageinfo' in pages[k]:
                    commons_url = pages[k]['imageinfo'][0]['thumburl']
                    
                    fname = re.sub(r'^(.+?/)([^/]+)$', '\g<2>', commons_url)
                    fname = re.sub(r'^\d+px\-', '', fname)
                    fname = fname.replace('.svg', '').replace('.png', '').replace('.jpg', '')
                    fname = '{}/{}.jpg'.format(outfolder, fname)
                    
                    #    download, resize and save wikimedia image to local folder
                    params = ' '.join(['bash',
                           'modifyAndSaveImage.bash',
                           commons_url,
                           '{}x{}'.format(IMAGESIZE, IMAGESIZE),
                           fname
                           ])

                    os.system(params)
                    print("Written {}\t{}".format(i, fname))
                    
        except KeyError:
            continue
    
    # os.system(' & '.join(commands))
    #    for params in commands:
    #    os.system(params)
    
   
def readCoats(N=100, prove_words=[]):
    fields = ['blazon','blazon_of','description','image']
    
    res = []
    
    
    with open(COATDESCRIPTIONFILE, newline='') as csvfile:
        reader = DictReader(csvfile, fieldnames=fields, 
                            restkey=None, restval=None, delimiter=';')
        count = 0
        for id, row in enumerate(reader):
            
            if id<STARTNUMBER:
                continue 
            
            if not 'blazon' in row or row['blazon'] is None or not 'image' in row or row['image'] is None:
                continue
            
            
            #    [[commons:File:AT Herzogenburg COA.svg]]            
            m = re.match(r'\[+commons:(File:.+?)\]+', row['image'])
            if m is None:
                continue
            
            ob = {'id': id, 'url': m.group(1), 'desc': []}      
            
            res.append(ob)
            
            count += 1
            if count >= N: 
                break

    # print(S)
    # dct.save_as_text('gensim_dict.csv')
    return res


def makeCommonsQuery(fname):
    """
    WIKIMEDIA COMMONS QUERY EXAMPLE:
    https://commons.wikimedia.org/w/api.php?action=query&titles=File:AUT%20Hallein%20COA.jpg&prop=imageinfo&&iiprop=url&iiurlwidth=240
    
    action=query
    titles=File:AUT%20Hallein%20COA.jpg
    prop=imageinfo
    iiprop=url
    iiurlwidth=200
    """
    params = {'action': 'query',
              'titles': fname,
              'prop': 'imageinfo',
              'iiprop': 'url',
              'iiurlwidth': str(IMAGESIZE),
              'format': 'json'
              }
    
    ob = makeQuery(params, 'https://commons.wikimedia.org/w/api.php')
    ob['filename'] = fname
    return ob

def makeQuery(params, apiservice="https://api.flickr.com/services/rest/"):
    
    try:
        r = requests.post(apiservice,
                      data = params)
        
        if r.status_code != requests.codes.ok:
            #r.raise_for_status()
            print(r)
            print(r.url)
            return {}
        
        return json.loads(r.text)
        
    except Exception as e:
        print(e)
        # KeyError: no result
        pass
    return {}


if __name__ == '__main__':
    t0 = time.time()
    
    main(sys.argv)
    
    t1 = time.time()
    print("Time elapsed {} sec".format(t1-t0))
