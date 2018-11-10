# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:19:42 2018

@author: IOLAP-USER
"""

# image
# yield
# description
# ingredients
# recipe
# Menu and Tags
# Reviews, rating

import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup 
import time

recipes_list_full = pd.read_csv(r'C:\Users\IOLAP-USER\Documents\GitHub\epicurious-recipes-with-rating-and-nutrition\recipes_links.csv')

recipe_data = recipes_list_full[['link']]
recipe_data.drop_duplicates(inplace = True)
recipe_data['title'], recipe_data['origin'], recipe_data['author'] = ['', '', ''] 
recipe_data['date'], recipe_data['overall_rating'] = ['', 0]
recipe_data['best_rating'], recipe_data['worst_data'] = [0, 0]
recipe_data['num_reviews'], recipe_data['make_it_again_pct'] = [0, '']
recipe_data['yield'] = 0
recipe_data['description'], recipe_data['ingredients'] = ['', '']
recipe_data['recipe'], recipe_data['nutrition'], recipe_data['tags'] = ['', '', '']
# recipe_data['reviews'], recipe_data['review_rating'] = [list(), list()]

# for i in range(len(recipe_link_data)):
for i in range(10):
    i = 0
    # Recipe Link
    search_link = 'http://www.epicurious.com' + recipe_data['link'].iloc[i]
    # Request link page data
    url_response = requests.get(search_link)
    # Soupify
    recipe_page = BeautifulSoup(url_response.text, 'lxml')
    
    # Extract Title
    recipe_title = recipe_page.find('h1', {'itemprop': 'name'}).text
    # Extract Author
    recipe_author = recipe_page.find('a', {'class': 'contributor', 'itemprop': 'author'}).text
    # Extract Publisher
    recipe_publisher = recipe_page.find('span', {'class': 'source', 'itemprop': 'publisher'}).text
    # Extract Publication Date
    recipe_pub_date = recipe_page.find('span', {'class': 'pub-date'}).text
    
    # Extract Overall Rating, Best Rating, Worst Rating
    recipe_overall_rating = recipe_page.find('meta', {'itemprop': 'ratingValue'})['content']
    recipe_best_rating = recipe_page.find('meta', {'itemprop': 'bestRating'})['content']
    recipe_worst_rating = recipe_page.find('meta', {'itemprop': 'worstRating'})['content']
    # Extract Num Reviews
    recipe_num_reviews = recipe_page.find('span', {'class': 'reviews-count', 'itemprop': 'reviewCount'}).text
    # Extract Make-It-Again Percentage
    recipe_make_it_again_pct = recipe_page.find('div', {'class': 'prepare-again-rating'}).find('span').text


