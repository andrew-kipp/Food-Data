# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:19:42 2018

@author: IOLAP-USER
"""

# Menu and Tags
# Reviews, rating

import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup 
import time

recipes_list_full = pd.read_csv(r'C:\Users\IOLAP-USER\Documents\GitHub\Food-Data\Data\recipes_links.csv')

recipe_data = recipes_list_full[['link']]
recipe_data.drop_duplicates(inplace = True)
recipe_data['title'], recipe_data['author'] = ['', '']
recipe_data['publisher'], recipe_data['published_date'] = ['', '']
recipe_data['overall_rating'], recipe_data['best_rating'] = ['', '']
recipe_data['worst_rating'], recipe_data['num_reviews'] = ['', '']
recipe_data['make_it_again_pct'], recipe_data['description'] = ['', '']
recipe_data['yield'], recipe_data['active_time'] = ['', '']
recipe_data['total_time'] = ''
recipe_data['ingredients'] = ''
recipe_data['preparation'] = ''
recipe_data['servings'], recipe_data['calories'] = ['', '']
recipe_data['carbohydrates'], recipe_data['fat'] = ['', '']
recipe_data['protein'], recipe_data['saturated_fat'] = ['', '']
recipe_data['sodium'], recipe_data['fiber'] = ['', '']
recipe_data['cholesterol'], recipe_data['polyunsaturated_fat'] = ['', '']
recipe_data['monounsaturated_fat'] = ''
recipe_data['cuisine_tags'], recipe_data['category_tags'] = ['', '']

# for i in range(len(recipe_link_data)):
for recipe_pos in range(len(recipe_data)):
    if recipe_pos % 400 == 0:
        print('5 Min Nap')
        time.sleep(300)
    # Recipe Link
    # search_link = 'http://www.epicurious.com' + recipe_data['link'].iloc[recipe_pos]
    search_link = 'https://www.epicurious.com/recipes/food/views/strawberry-and-watercress-salad'
    # https://www.epicurious.com/recipes/food/views/bittersweet-chocolate-marquise-with-cherry-sauce-108254
    # https://www.epicurious.com/recipes/food/views/strawberry-and-watercress-salad
    # Request link page data
    url_response = requests.get(search_link)
    # Soupify
    recipe_page = BeautifulSoup(url_response.text, 'lxml')
    
    
    # Extract Title
    recipe_title = recipe_page.find('h1', {'itemprop': 'name'}).text
    recipe_data['title'].iloc[recipe_pos] = recipe_page.find('h1', {'itemprop': 'name'}).text
    # Extract Author
    try: 
        recipe_data['author'].iloc[recipe_pos] = recipe_page.find('a', {'class': 'contributor', 'itemprop': 'author'}).text
    except: 
        print('Author N/A')
    # Extract Publisher
    try: 
        recipe_data['publisher'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'source', 'itemprop': 'publisher'}).text
    except:
        print('Publisher N/A')
    # Extract Publication Date
    try: 
        recipe_data['published_date'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'pub-date'}).text
    except:
        print('Published Date N/A')
    
    
    # Extract Overall Rating, Best Rating, Worst Rating
    try:
        recipe_data['overall_rating'].iloc[recipe_pos] = recipe_page.find('meta', {'itemprop': 'ratingValue'})['content']
    except:
        print('Overall Rating N/A')
    try:
        recipe_data['best_rating'].iloc[recipe_pos] = recipe_page.find('meta', {'itemprop': 'bestRating'})['content']
    except:
        print('Best Rating N/A')
    try:
        recipe_data['worst_rating'].iloc[recipe_pos] = recipe_page.find('meta', {'itemprop': 'worstRating'})['content']
    except:
        print('Worst Rating N/A')
    # Extract Num Reviews
    try:
        recipe_data['num_reviews'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'reviews-count', 'itemprop': 'reviewCount'}).text
    except:
        print('Number of Reviews N/A')
    # Extract Make-It-Again Percentage
    try:
        recipe_data['make_it_again_pct'].iloc[recipe_pos] = recipe_page.find('div', {'class': 'prepare-again-rating'}).find('span').text
    except:
        print('Make It Again Percent N/A')
    # Extract Recipe Description
    try:
        recipe_data['description'].iloc[recipe_pos] = recipe_page.find('div', {'class': 'dek', 'itemprop': 'description', 'data-reactid': '18'}).find('p').text
    except:
        print('Description N/A')


    # Extract Recipe Yield
    try:
        recipe_data['yield'].iloc[recipe_pos] = recipe_page.find('dd', {'class': 'yield', 'itemprop': 'recipeYield'}).text
    except:
        print('Yield N/A')
    # Extract Active Time
    try:
        recipe_data['active_time'].iloc[recipe_pos] = recipe_page.find('dd', {'class': 'active-time'}).text
    except:
        print('Active Time N/A')
    # Extract Total Time
    try:
        recipe_data['total_time'].iloc[recipe_pos] = recipe_page.find('dd', {'class': 'total-time'}).text
    except:
        print('Total Time N/A')
        
    
    # Extract Ingredients
    try:
        recipe_ingredients_packed = recipe_page.find('ol', {'class': 'ingredient-groups'}).findAll('li', {'class': 'ingredient-group'})
        recipe_ingredients_unpacked = []
        current_key = recipe_title
            
        for i in range(len(recipe_ingredients_packed)):
            try:
                # If there is a Strong item, then this is used as a new key in the dictionary
                # Otherwise items are appended to the most recent key
                current_key = recipe_ingredients_packed[i].find('strong').text
            except:
                print('Part of previous section')
            
            ingredients = recipe_ingredients_packed[i].findAll('li', {'class': 'ingredient'})
            for ingredient in ingredients:
                current_ingredient = current_key + ' - ' + ingredient.text
                recipe_ingredients_unpacked.append(current_ingredient)
                
        recipe_data['ingredients'].iloc[recipe_pos] = ", ".join(recipe_ingredients_unpacked)
        del i, current_key, ingredients, recipe_ingredients_packed
        del recipe_ingredients_unpacked
    except:
        print('Ingredients N/A')
        
        
    # Extract Directions
    try:
        recipe_preparation_packed = recipe_page.find('ol', {'class': 'preparation-groups'}).findAll('li', {'class': 'preparation-group'})
        recipe_preparation_unpacked = []
        current_key = recipe_title
        
        for i in range(len(recipe_preparation_packed)):
            try:
                # If there is a Strong item, then this is used as a new key in the dictionary
                # Otherwise items are appended to the most recent key
                current_key = recipe_preparation_packed[i].find('strong').text
            except:
                print('Part of previous section')
            
            preparation = recipe_preparation_packed[i].findAll('li', {'class': 'preparation-step'})
            for pred_step in preparation:
                current_step = current_key + ' - ' + pred_step.text
                recipe_preparation_unpacked.append(current_step)
                
        recipe_data['preparation'].iloc[recipe_pos] = ", ".join(recipe_preparation_unpacked)
        del i, current_key, preparation, recipe_preparation_packed
        del recipe_preparation_unpacked
    except:
        print('Preparation N/A')
            
            
    # Extract Nutrition
    try:
        recipe_data['servings'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'per-serving'}).text
    except:
        print('Servings N/A')
    try:
        recipe_data['calories'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'calories'}).text
    except:
        print('Calories N/A')
    try:
        recipe_data['carbohydrates'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'carbohydrateContent'}).text
    except:
        print('Carbohydrates N/A')
    try:
        recipe_data['fat'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'fatContent'}).text
    except:
        print('Fat N/A')
    try:
        recipe_data['protein'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'proteinContent'}).text
    except:
        print('Protein N/A')
    try:
        recipe_data['saturated_fat'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'saturatedFatContent'}).text
    except:
        print('Saturated Fat N/A')
    try:
        recipe_data['sodium'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'sodiumContent'}).text
    except:
        print('Sodium N/A')
    try:
        recipe_data['fiber'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'fiberContent'}).text
    except:
        print('Fiber N/A')
    try:
        recipe_data['cholesterol'].iloc[recipe_pos] = recipe_page.find('span', {'class': 'nutri-data', 'itemprop': 'cholesterolContent'}).text
    except:
        print('Cholesterol N/A')
    
    try:
        nutrition_content = recipe_page.find('div', {'class': 'nutrition content'}).findAll('li')
        for li_val in nutrition_content:
            if li_val.find('span', {'class': 'nutri-label'}).text == 'Polyunsaturated Fat':
                recipe_data['polyunsaturated_fat'].iloc[recipe_pos] = li_val.find('span', {'class': 'nutri-data'}).text
            elif li_val.find('span', {'class': 'nutri-label'}).text == 'Monounsaturated Fat':
                recipe_data['monounsaturated_fat'].iloc[recipe_pos] = li_val.find('span', {'class': 'nutri-data'}).text  
        
        del li_val, nutrition_content
    except:
        print('Nutrition N/A')
       
    
    # Extract Tags
    try:
        recipe_tags = recipe_page.find('div', {'class': 'menus-tags content'})
        # Cuisine Tags
        try: 
            recipe_cuisine_tags_packed = recipe_tags.findAll('dt', {'itemprop': 'recipeCuisine'})
            recipe_data['cuisine_tags'].iloc[recipe_pos] = ",".join([x.text for x in recipe_cuisine_tags_packed])
        except:
            print('Cuisine Tags N/A')
        # Category Tags
        try:
            recipe_category_tags_packed = recipe_tags.findAll('dt', {'itemprop': 'recipeCategory'})
            recipe_data['category_tags'].iloc[recipe_pos] = ", ".join([x.text for x in recipe_category_tags_packed])
        except:
            print('Category Tags N/A')
    except:
        print('Tags N/A')

    
recipe_data.to_csv(r'C:\Users\IOLAP-USER\Documents\GitHub\Food-Data\Data\recipes_data.csv')