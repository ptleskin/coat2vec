#!/usr/bin/env python
# coding: utf-8
'''
Created on 27 December 2018
@author: petrileskinen, petri.leskinen@icloud.com
'''

import argparse
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

import pandas as pd

from scipy.spatial import KDTree


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imagename',
                        default='001.png', 
                        help='image to be located')
    parser.add_argument('--csvfile', 
                        default='vectors.csv', 
                        help='Name of the csv file')
    parser.add_argument('--imagefolder',
                        default='../../original/Suomi/Kunta/', 
                        help='folder containing the images')
    parser.add_argument('--dpi', 
                        default=300, type=int,
                        help='Resolution of the output image')
    parser.add_argument('--outimage',
                        default=None, 
                        help='image to be written')
    
    
    args = parser.parse_args()
    
    C = pd.read_csv(args.csvfile, sep="\t")
    filenames = list(C.values[:,1])
    
    imgname = args.imagename
    if not imgname in filenames:
        print("Image not found in csv")
        return
    imgindex = filenames.index(imgname)
    
    X = C.values[:,3:]
    tree = KDTree(X)
    _,res = tree.query(X[imgindex], k=6)
    
    paths = [args.imagefolder + filenames[x] for x in res]
    print([filenames[x] for x in res])
    
    if args.outimage is not None:
        drawTable(paths, args)


def drawTable(paths, args):
    
    fig, axarr = plt.subplots(1, len(paths))
    
    for i,path in enumerate(paths):
        
        axarr[i].set_axis_off()
        img = mpimg.imread(path)
        axarr[i].imshow(img)
    
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    
    fig.savefig(args.outimage, dpi=args.dpi, bbox_inches='tight')
    print("{} saved.".format(args.outimage))
    

if __name__ == "__main__":
    main()
