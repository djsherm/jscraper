# -*- coding: utf-8 -*-
"""
jeopardy selenium
Created on Fri Mar  3 11:52:45 2023

@author: Daniel
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

def jscraper(game_url, jeopardy_game):
    '''
    
    Parameters
    ----------
    game_url : str
        Link to the Jeopardy game on j-archive.com.
    jeopardy_game : Pandas DataFrame
        DataFrame that stores the clue_id, round, category, value, clue, and answer
        for the clues that the code scrapes.

    Returns
    -------
    jeopardy_game : Pandas DataFrame
        function takes DataFrame and appends the clues that it scraped from j-archive.com.

    '''
    
    #set chromedriver.exe path
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=PATH)
    driver.implicitly_wait(0.5)
    
    #launch URL
    driver.get(game_url)
    
    #get all categories
    categories = driver.find_elements(By.CLASS_NAME, 'category_name')
    single_jeopardy_categories = []
    double_jeopardy_categories = []
    final_jeopardy_category = []
    
    for i in range(len(categories)):
        if i <= 5:
            single_jeopardy_categories.append(categories[i].text)
        elif i > 5 and i <=11:
            double_jeopardy_categories.append(categories[i].text)
        elif i == 12:
            final_jeopardy_category.append(categories[i].text)
    
    
    #construct the clue IDs
    single_jeopardy_ids = []
    double_jeopardy_ids = []
    final_jeopardy_ids = ['clue_FJ']        
    for value_id in range(1,6):
        for category_id in range(1,7):
            single_jeopardy_ids.append('clue_J_{}_{}'.format(category_id, value_id))
            double_jeopardy_ids.append('clue_DJ_{}_{}'.format(category_id, value_id))
            
    #SINGLE JEOPARDY: loop through round clue ids to collect clue information
    for clue_id in single_jeopardy_ids:
        current_clue = []
        #append clue_id to current_clue vector
        current_clue.append(clue_id)
        #append round to current_clue vector
        current_clue.append('Single Jeopardy')
        
        #append category to current_clue vector (can get category id by final digit in the clue_id)
        category_num = int(clue_id[-3])
        #print('category_num: {}'.format(str(category_num)))
        if category_num == 1:
            current_clue.append(single_jeopardy_categories[0])
        elif category_num == 2:
            current_clue.append(single_jeopardy_categories[1])
        elif category_num == 3:
            current_clue.append(single_jeopardy_categories[2])
        elif category_num == 4:
            current_clue.append(single_jeopardy_categories[3])
        elif category_num == 5:
            current_clue.append(single_jeopardy_categories[4])
        elif category_num == 6:
            current_clue.append(single_jeopardy_categories[5])
            
        #append value to current_clue vector (by looking at -3 spot in clue_id)
        value_num = int(clue_id[-1])
        #print('value_num: {}'.format(str(value_num)))
        if value_num == 1:
            current_clue.append('$200')
        elif value_num == 2:
            current_clue.append('$400')
        elif value_num == 3:
            current_clue.append('$600')
        elif value_num == 4:
            current_clue.append('$800')
        elif value_num == 5:
            current_clue.append('$1000')
            
        #use selenium to scrape the clue
        try:
            clue_text = driver.find_elements(By.ID, clue_id)[0].text
            current_clue.append(clue_text)
        except IndexError:
            print(clue_id + ' not revealed')
            pass
        
        #use selenium to reveal the answer and store it
        a = ActionChains(driver)
    
        xpath = '//*[@id="jeopardy_round"]/table[1]/tbody/tr[{}]/td[{}]/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]'
        tr = int(value_num) + 1
        td = int(category_num)
        #print('tr:', tr)
        #print('td:', td)
        
        formatted_xpath = xpath.format(str(tr), str(td))
        
        try:
            answer_html_element = driver.find_element(By.XPATH, formatted_xpath)
            a.move_to_element(answer_html_element).click().perform()
            answer = driver.find_elements(By.CLASS_NAME, 'correct_response')
            #print(answer[-1].text) #the newest answer that we found
            current_clue.append(answer[-1].text)
            
        except NoSuchElementException:
            #print('Clue not revealed')
            pass
        
        if len(current_clue) == 6:
            jeopardy_game.loc[len(jeopardy_game)] = current_clue
        
    #DOUBLE JEOPARDY: loop through round clue ids to collect clue information
    for clue_id in double_jeopardy_ids:
        current_clue = []
        #append clue_id to current_clue vector
        current_clue.append(clue_id)
        #append round to current_clue vector
        current_clue.append('Double Jeopardy')
        
        #append category to current_clue vector (can get category id by final digit in the clue_id)
        category_num = int(clue_id[-3])
        #print('category_num: {}'.format(str(category_num)))
        if category_num == 1:
            current_clue.append(double_jeopardy_categories[0])
        elif category_num == 2:
            current_clue.append(double_jeopardy_categories[1])
        elif category_num == 3:
            current_clue.append(double_jeopardy_categories[2])
        elif category_num == 4:
            current_clue.append(double_jeopardy_categories[3])
        elif category_num == 5:
            current_clue.append(double_jeopardy_categories[4])
        elif category_num == 6:
            current_clue.append(double_jeopardy_categories[5])
            
        #append value to current_clue vector (by looking at -3 spot in clue_id)
        value_num = int(clue_id[-1])
        #print('value_num: {}'.format(str(value_num)))
        if value_num == 1:
            current_clue.append('$400')
        elif value_num == 2:
            current_clue.append('$800')
        elif value_num == 3:
            current_clue.append('$1200')
        elif value_num == 4:
            current_clue.append('$1600')
        elif value_num == 5:
            current_clue.append('$2000')
            
        #use selenium to scrape the clue
        try:
            clue_text = driver.find_elements(By.ID, clue_id)[0].text
            current_clue.append(clue_text)
        except IndexError:
            print(clue_id + ' not revealed')
        
        #use selenium to reveal the answer and store it
        a = ActionChains(driver)
    
        xpath = '//*[@id="double_jeopardy_round"]/table[1]/tbody/tr[{}]/td[{}]/table/tbody/tr[1]/td/div/table/tbody/tr/td[2]'
        tr = int(value_num) + 1
        td = int(category_num)
        #print('tr:', tr)
        #print('td:', td)
        
        formatted_xpath = xpath.format(str(tr), str(td))
        
        try:
            answer_html_element = driver.find_element(By.XPATH, formatted_xpath)
            a.move_to_element(answer_html_element).click().perform()
            answer = driver.find_elements(By.CLASS_NAME, 'correct_response')
            #print(answer[-1].text) #the newest answer that we found
            current_clue.append(answer[-1].text)
        except NoSuchElementException:
            pass
        
        if len(current_clue) == 6:
            jeopardy_game.loc[len(jeopardy_game)] = current_clue    
        
    # FINAL JEOPARDY
    current_clue = []
    
    current_clue.append(final_jeopardy_ids[0])
    current_clue.append("Final Jeopardy")
    current_clue.append(final_jeopardy_category[0])
    current_clue.append('FINAL JEOPARDY') #placeholder integer because there is no value for final jeopardy
    
    clue_text = driver.find_elements(By.ID, final_jeopardy_ids[0])
    current_clue.append(clue_text[0].text)
    
    final_xpath = '//*[@id="final_jeopardy_round"]/table[1]/tbody/tr[1]/td/div/table/tbody/tr[1]/td'
    answer_html_element = driver.find_element(By.XPATH, final_xpath)
    a.move_to_element(answer_html_element).click().perform()
    answer = driver.find_elements(By.CLASS_NAME, 'correct_response')
    #print(answer[-1].text)
    current_clue.append(answer[-1].text)
    
    jeopardy_game.loc[len(jeopardy_game)] = current_clue
    
    
    driver.close()
    
    return jeopardy_game

def get_games(game_id, jeopardy_game, num_pages_to_extract=3):
    '''

    Parameters
    ----------
    game_id : INT
        Starting game id at the end of the j-archive.com url.
    jeopardy_game : Pandas DataFrame
        DataFrame containing the scraped clues.
    num_pages_to_extract : INT, optional
        Number of pages to scrape from j-archive.com. 
        Function will decrement game_id num_pages_to_extract times. 
        The default is 3.

    Returns
    -------
    jeopardy_game : Pandas DataFrame
        DataFrame containing the scraped clues, 
        updated with the newly scraped game from this function call.

    '''
    #initialize variables
    index = 0
    
    archive_link = "http://www.j-archive.com/showgame.php?game_id="
    
    while index < num_pages_to_extract:
        
        current_game_id = game_id - index # subtract index to scrape older games
        jeopardy_archive_link = archive_link + str(current_game_id)
        print(jeopardy_archive_link)
        
        # scrape jeopardy game with jscraper()
        jeopardy_game = jscraper(jeopardy_archive_link, jeopardy_game)
        
        #update iterator
        index += 1
    
    return jeopardy_game

if __name__ == '__main__':
    gamesheet = pd.DataFrame(columns=['clue_id','round', 'category', 'value', 'clue', 'answer'])
    game_index = 7744 # game aired March 3, 2020
    
    gamesheet = get_games(game_index, gamesheet)
    gamesheet = gamesheet.replace('\n', ' ', regex=True)
    
    # save gamesheet to csv file
    gamesheet.to_csv('jeopardy_games.csv', sep='|')