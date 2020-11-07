# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 23:20:49 2020

@author: Beau
"""


#%% import modules

import csv
import requests
from os import path
import tkinter as tk
from tkinter import filedialog
import xlrd

from imdb import IMDb
import wget

tk.Tk().withdraw() #prevents annoying tkinter window


#%% define user functions

def GetMovieNames():

    workbook_name = filedialog.askopenfilename(title='Select Movie List', initialdir='./input')

    workbook = xlrd.open_workbook(workbook_name, on_demand=True)

    # sheet = workbook.sheet_by_name("Sheet1")
    sheet = workbook.sheet_by_index(0)

    # includes headers, so read columns from second row
    return sheet.col_values(0, 1)


def ScrapeIMDb(movie_name):
    query = f'imdb+movie+{movie_name.replace(" ", "+")}'
    print(movie_name)

    var = requests.get(rf'http://www.google.com/search?q={query}&btnI', allow_redirects='false')

    url = var.url
    print(url)
    
    if 'https://www.imdb.com/title/' in url:
        # example_url = r'http://www.google.com/url?q=https://www.imdb.com/title/tt0405296/'

        imdb_id = url.split('/')[-2][2:]

        movie = ia.get_movie(imdb_id)

        return movie

    else:

        raise RuntimeError


def ShowProperties(movie):
    print('Title:', movie.get('title'))
    print('Year:', movie.get('year'))
    print('Runtime:', movie.get('runtimes')[0], 'min')
    print('Genre:', '; '.join(movie.get('genre')))
    print('IMDb ID:', movie.get('imdbID'))
    # print('Cover URL:', movie.get('cover url'))
    print()


def GetProperties(movie):
    properties = []

    properties.append(movie.get('title'))
    properties.append(str(movie.get('year')))
    properties.append(movie.get('runtimes')[0] + ' min')
    properties.append('; '.join(movie.get('genre')))
    properties.append('tt' + movie.get('imdbID'))
    # properties.append(movie.get('cover url'))

    return properties


#%% main

ia = IMDb()

movie_names = GetMovieNames()

# movie.infoset2keys

columns = ['Title', 'Year', 'Runtime', 'Genre', 'IMDb ID']

if path.exists('./output.csv'):
    skip_header = True
    write_mode = 'a'
else:
    skip_header = False
    write_mode = 'wt'

with open('./output.csv', write_mode, newline='\n', encoding='utf-8') as output_file:
    wr = csv.writer(output_file, dialect='excel')

    if not skip_header: wr.writerow(columns)

    for movie_name in movie_names:

        if movie_name != '':

            try:
                movie = ScrapeIMDb(movie_name)
            except(RuntimeError):
                print(f"Check spelling: {movie_name}\n")
                continue

            ShowProperties(movie)

            wr.writerow(GetProperties(movie))
            
            cover_url = movie.get('cover url')
            cover_url = '.'.join(cover_url.split('.')[0:3]) + '._V1_SY1280_CR0,0,864,1280_.jpg'
            
            wget.download(cover_url, out=('./dvd_covers/tt'+movie.get('imdbID')+'.jpg'))   

        else:

            print('uh oh blank line...\n')

