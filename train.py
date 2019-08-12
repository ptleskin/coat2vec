#!/usr/bin/env python
# coding: utf-8
'''
Created on 27 December 2018
@author: petrileskinen, petri.leskinen@icloud.com

Example of usage:
python3 train.py --infolder commons/ --model xception --outcsv commons_xc.csv --depth 4 --outimage commons4xc.png
'''

import argparse
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import pandas as pd

#    source: https://github.com/datarobot/pic2vec
from pic2vec import ImageFeaturizer

from sklearn import svm
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infolder',
                        default='../../original/Suomi/Kunta/', 
                        help='folder containing the source images')
    parser.add_argument('--coatfolder',
                        default=None, 
                        help='folder containing the output images')
    parser.add_argument('--outimage', 
                        default='embedding.png', 
                        help='Name of the output image')
    parser.add_argument('--outcsv', 
                        default='vectors.csv', 
                        help='Name of the csv output')
    parser.add_argument('--dpi', 
                        default=300, type=int,
                        help='Resolution of the output image')
    
    parser.add_argument('--zoom', 
                        default=0.1, type=float,
                        help='size of a coat in output image')
    
    parser.add_argument('--depth', 
                        default=1, type=int,
                        help='Network depth')
    
    parser.add_argument('--model', 
                        default='squeezenet',
                        help='Network type')
    
    args = parser.parse_args()
    
    
    image_path = args.infolder
    outimage = args.outimage
    if args.coatfolder is None:
        coatfolder = image_path
    else:
        coatfolder = args.coatfolder
    
    #    Extract vectors
    featurizer = ImageFeaturizer(depth=args.depth, autosample = False, model=args.model)
    featurizer.load_data('images', image_path=image_path)
    featurize_preloaded_df = featurizer.featurize_preloaded_data(save_features=True)
    
    #    Output to csv file
    featurize_preloaded_df.to_csv(path_or_buf = args.outcsv, sep = '\t')
    print('Vector data saved to {}'.format(args.outcsv))
    
    images = featurize_preloaded_df.values[:,0]
    
    paths = [coatfolder+x for x in images]
    
    #    extract vectors:
    X = featurize_preloaded_df.values[:,2:]
    
    #    First dimensionality reduction to 32 dimensions using truncated singular value decomposition 
    Y = TruncatedSVD(32).fit_transform(X)
    
    #    For plotting dimensionality reduction to 2D with TSNE
    Y = TSNE(n_components=2, perplexity=30.0).fit_transform(Y)
    
    #    Plot the output image
    plt.tight_layout()
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.scatter(Y[:,0], Y[:,1])

    arr = []
    for x0, y0, path in zip(Y[:,0], Y[:,1], paths):
        try:
            ab = AnnotationBbox(getImage(path, zoom=args.zoom), (x0, y0), frameon=False)
            arr.append(ax.add_artist(ab))
        except FileNotFoundError:
            pass
    
    fig.savefig(outimage, dpi=args.dpi, bbox_inches='tight')
    print("{} saved.".format(outimage))


def getImage(path,zoom=0.1):
    return OffsetImage(plt.imread(path),zoom=zoom)


if __name__ == "__main__":
    main()
