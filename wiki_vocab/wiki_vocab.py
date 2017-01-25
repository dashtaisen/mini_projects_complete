"""
WikiVocab: get vocabulary in other languages by checking Wikipedia titles
"""

import re
import urllib
from urllib import request
from bs4 import BeautifulSoup

#all wiki pages begin like this
wiki_url = 'http://www.wikipedia.org/wiki/'

#use this to look for disambiguation pages
disamb_suffix = '_(disambiguation)'

#ask user which word they want to find
def get_keyword():
    keyword = input("What word should I look for? ")
    return keyword

#find disambiguation pages for the vocabulary word
def find_disamb_pages(keyword):
    #https:///en.wikipedia.org/keyword_(disambiguation)
    disamb_url = wiki_url + keyword + disamb_suffix
    try:
        #see if there's a disambiguation page for the vocabulary word
        disamb_soup = BeautifulSoup(request.urlopen(disamb_url))
    except:
        """The print statement is just for debugging"""
        #print("Couldn't open {0}".format(disamb_url))
        pass
    else:
        #Return a BeautifulSoup object of the disambiguation page
        return disamb_soup

def choose_disamb_page(disamb_soup):
    """Choose a page from the disambiguation pages"""
    print("Which page do you want to check?")

    #Get a list of all tags with links to wiki pages in the HTML
    disamb_links = disamb_soup.html.find_all(href=re.compile(r"^/wiki/"))

    #From the list above, get a list of the URLs
    hrefs = [link['href'] for link in disamb_links if not ':' in link['href']]

    #Print the list of links
    for i in range(len(hrefs)):
        print("{0}: {1}".format(i, hrefs[i]))

    #Ask the user to choose one of the links
    choice = int(input("Choose a number: "))

    #In case user chooses weird number
    if choice not in range(len(hrefs)):
        print("Sorry, that's not in the range.")
    else:
        print("You chose {0}. Loading page...".format(hrefs[choice]))

        #Each link is a relative path starting with /wiki/, so start from index 6
        return BeautifulSoup(request.urlopen(wiki_url + hrefs[choice][6:]))

def find_single_page(keyword):
    """Open the wikipedia page with the exact keyword as title
         Used if there is no disambiguation page
    """

    single_page_title = wiki_url + keyword
    try:
        #try to open the page
        single_page_soup = BeautifulSoup(request.urlopen(single_page_title))
    except:
        """The print statement is just for debugging"""
        #print("Couldn't open {0}".format(single_page_title))
        pass
    else:
        return single_page_soup

def choose_lang_page(soup):
    """Get a list of possible languages, and get the title in the language chosen by the user"""

    #Get all links with the "hreflang" attribute
    langs = soup.html.find_all(lambda tag: tag.has_attr('hreflang'))

    #From the list above, get a (title, link) tuple. The title includes the language name
    lang_titles = [(lang['title'], lang['href']) for lang in langs if lang.has_attr('title')]

    #List the possible titles
    print("Found the following languages: ")
    for i in range(len(lang_titles)):
        print("{0}: {1}".format(i, lang_titles[i][0]))

    #Ask the user to choose a language
    choice = int(input("Which language do you want? "))
    if choice not in range(len(lang_titles)):
        print("Sorry, that's not in the range.")
    else:
        print("You chose {0}. Loading page...".format(lang_titles[choice][1]))
        #Get the first h1 in the page, which is the title in the target language
        return BeautifulSoup(request.urlopen(lang_titles[choice][1])).h1.string

def  find_specific_lang(soup, lang):
    vocab = []
    result = soup.html.find_all(hreflang=lang)
    if len(result) == 1:
        #return BeautifulSoup(request.urlopen(result[0]['href'])).h1.string
        vocab.append(BeautifulSoup(request.urlopen(result[0]['href'])).h1.string)
        synonyms = BeautifulSoup(request.urlopen(result[0]['href'])).find('p').find_all('b')
        synonym_strings = [synonym.string for synonym in synonyms]
        for synonym in synonym_strings:
            vocab.append(synonym)
    elif len(result) > 1:
        print("Found the following pages: ")
        for i in range(len(lang_result)):
            print("{0}: {1}".format(i, result[i]['href']))
        choice = int(input("Which page do you want? "))
        if choice not in range(len(result)):
            print("Sorry, that's not in the range.")
        else:
            print("You chose {0}. Loading page...".format(result[choice]['href']))
            #return BeautifulSoup(request.urlopen(result[0]['href'])).h1.string
            synonyms = BeautifulSoup(request.urlopen(result[0]['href'])).find('p').find_all('b')
            synonym_strings = [synonym.string for synonym in synonyms]
            for synonym in synonym_strings:
                vocab.append(synonym)
    else:
        print("Language not found.")
    return vocab

def batch_find(wordlist, lang_choice):
    vocablist = []
    for word in wordlist:
        disamb = find_disamb_pages(word)
        page = find_single_page(word)
        if disamb:
            print("Found a disambiguation page for {0}".format(word))
            choice = choose_disamb_page(disamb)
            result = find_specific_lang(choice, lang_choice)
            vocablist.append((word, result))
        elif page:
            print("Found a regular page for {0}".format(word))
            result = find_specific_lang(page, lang_choice)
            vocablist.append((word, result))
        else:
            #handle page not found at all
            print("Sorry, couldn't find any pages for {0}".format(keyword))
    return vocablist

def find_vocab():
    lang_choice = input("Which language (two-char abbreviation)?: ")
    keyword = get_keyword()
    disamb = find_disamb_pages(keyword)
    page = find_single_page(keyword)
    #handle disambiguation
    if disamb:
        print("Found a disambiguation page for {0}".format(keyword))
        choice = choose_disamb_page(disamb)
        #result = find_lang(choice)
        result = find_specific_lang(choice, lang_choice)
        print(result)
    #handle no disambiguation
    elif page:
    #handle page not found at all
        print("Found a regular page for {0}".format(keyword))
        result = find_specific_lang(page, lang_choice)
        print(result)
    else:
        print("Sorry, couldn't find any pages for {0}".format(keyword))
