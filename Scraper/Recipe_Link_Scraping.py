# You’ve been asked to write an app that, given a bunch of search terms,
# delivers a recipe (name, description, ingredients, and instructions)
# to the user. You decide that the simplest thing to do is to:
# 1. ask the user to enter their search terms
# 2. construct an epicurious url with these search terms
# 3. get a list of recipes from epicurious
# 4. pick the first recipe from this list
# 5. open the recipe page
# 6. extract the name, description, ingredients and instructions from the recipe page
# 7. print them out so that the user can see them. 

# For example: spicy cumin burritos; banana strawberry

# import urllib.request as ul
import requests
from bs4 import BeautifulSoup 
import time

term_list = ['salad', 'chicken', 'beef', 'pork', 'lamb', 'curry', 'dessert', 
             'chocolate', 'cake', 'fruit', 'risotto', 'soup', 'stew', 'chili',
             'egg', 'roast', 'vegetarian', 'french', 'maple', 'fried', 
             'grilled', 'pasta', 'itallian', 'german', 'dinner', 'lunch',
             'sausage', 'ham', 'seafood', 'fish', 'noodle', 'winter', 'summer',
             'fall', 'spring', 'bake', 'holiday', 'party', 'pizza', 'zucchini'
             'sheet-pan', 'spicy']
result_list = list()

for term in term_list:
    time.sleep(60)
    print(term)
    # term = input("Enter a search term or END to exit: ")
    # if term == 'END':
    #     break
    # term_list.append(term)
    # list2=list()
    # list2=term_list[0].split()
    
    # search_link = 'http://www.epicurious.com/tools/searchresults?search='+list2[0]    
    # for i in range(1,len(list2)):
    #     search_link +='+'+list2[i]
    
    # Check the first page
    search_link = 'http://www.epicurious.com/search/' + term
    # url_response = ul.urlopen(search_link)
    url_response = requests.get(search_link)
    epicurious_soup_initial = BeautifulSoup(url_response.text, 'lxml')
    sector_result_initial = epicurious_soup_initial.findAll(
            name = 'article', class_ = 'recipe-content-card')
    if len(sector_result_initial) == 0:
        print("no results")
    else:
        for result in sector_result_initial:
            result_list.append([term, result.find_all('a')[0].get('href')])
            
    # Check all pages beyond the first page
    j = 2
    while True:
        print('page: ' + str(j))
        search_link = 'https://www.epicurious.com/search/' + term + '?page=' + str(j)
        url_response = requests.get(search_link)
        if url_response.status_code == 200:
            epicurious_soup = BeautifulSoup(url_response.text, "lxml")
            sector_result = epicurious_soup.findAll(
                    name = 'article', class_ = 'recipe-content-card')
            if len(sector_result) == 0:
                print("no results")
            else:
                for result in sector_result:
                    result_list.append([term, result.find_all('a')[0].get('href')])
            # Iterate for next page
            j+=1
        else:
            break

import pandas as pd
term_list_full = []
result_list_full = []

for i in range(len(result_list)):
    term_list_full.append(result_list[i][0])
    result_list_full.append(result_list[i][1])

temp_df = pd.DataFrame({'term':term_list_full, 'link':result_list_full})
temp_df.to_csv(r'C:\Users\IOLAP-USER\Documents\GitHub\Unused Data\epicurious-recipes-with-rating-and-nutrition\recipes_links.csv', index = False)

# =============================================================================
#     recipe_link = 'http://www.epicurious.com'+first_recipe
#     url_recipe = ul.urlopen(recipe_link)
#     recipe_soup = BeautifulSoup(url_recipe)
#     
#     name = recipe_soup.find('div', class_='title-source').find('h1').get_text()
#     
#     if recipe_soup.find('div', class_='dek').get_text('p'):
#         description = recipe_soup.find('div', class_='dek').get_text('p')
#     else: 
#         description = "None"
#         
#     ingredients = recipe_soup.find('div', class_='ingredients-info').get_text(separator = "\n")
#     preparation = recipe_soup.find('div', class_='instructions', itemprop = 'recipeInstructions').find('li').get_text(separator = "\n")  
#     
#     print("\n"+'Name: '+ name +"\n")
#     print("Description: "+description+"\n")
#     print(ingredients)
#     print("Preparation: "+"\n"+preparation)
# 
#     term_list.clear()
# =============================================================================
