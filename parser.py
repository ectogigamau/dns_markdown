# /!usr/bin/env python
# -*- coding: UTF-8 -*-
import db
import report
import mysite
import defines

import codecs
import multiprocessing

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool 
from openurl import openurl



def printSeparator():
	print('-------------------------------------------------------------------------------------')


# parse all catalog of products
def parseCatalog(html):
    data = []
    
    s = BeautifulSoup(html, 'html.parser')
    t = s.find('div', class_='products products-list')

    printSeparator()
    for product in t.find_all('div', {'class': 'product'}):
    	item = product.find('div', {'class': 'item-name'})
    	price = product.find('div', {'class': 'price_g'})
    	desc = product.find('div', {'class': 'characteristic-description'})
        
        itemtext = item.text
        desctext = desc.text.strip()
        pricetext = price.text;

        #print item
        print(itemtext.ljust(80,'.') + pricetext)
    	try:
        	print('   ' + desctext)
        except:
        	print('-error-')
        printSeparator()

        pricevalue = float(pricetext.replace(" ", ""))
        data.append([itemtext, desctext, pricevalue])

    return data


def parseCategories(html):
    print('parse categories..')
    data = []
    s = BeautifulSoup(html, 'html.parser')
    filterBlock = s.find('div', {'data-id': 'category'})
    checkboxList = filterBlock.find('ul', {'class': 'checkbox-list'})
    for li in checkboxList.find_all('li'):
    	label = li.find('label')
    	tagText = label.get('for')
    	tag = tagText.split('-')[1]
        sText = label.string
        s = sText.strip()
        data.append([tag, s])

    return data


def get_request(url, category, open_url):
    #category[0] - category_id
    return [open_url.get(url), category]

if __name__ == '__main__':
    sql_conn, sql_cursor = db.open()
    open_url = openurl()

    if db.category_is_empty(sql_cursor) or defines.ALWAYS_REINIT_CATEGORY:
        print("open catalog..")
        db.clear_category(sql_cursor);
        #categories = parseCategories(open('test.html'))
        catalog = open_url.get(defines.CATALOG_HEAD_URL)
        
        with codecs.open("test.html", "w",encoding='utf8') as f:
            f.write(catalog)

        categories = parseCategories(open_url.get(defines.CATALOG_HEAD_URL))
        for category in categories:
            db.set_category(sql_cursor, category)
    else: 
        categories = db.get_categories(sql_cursor)

    if (defines.UPDATE_DATABASE):
        if not db.category_is_empty(sql_cursor) and db.check_goods_time(sql_cursor):
            db.save_goods_table(sql_cursor)
        db.clear_goods(sql_cursor)

    #
    # use multithreading for the url open 
    #

    ## Make the Pool of workers
    #threads_count = multiprocessing.cpu_count()
    #print("threads count = " + str(threads_count))
    #pool = ThreadPool( threads_count ) 
    ## Open the urls in their own threads
    ## and return the results
    ##results = pool.map(get_request, categories[0:2])
    #results = pool.map(get_request, categories)
    ##close the pool and wait for the work to finish 
    #pool.close() 
    #pool.join()

    results = []

    i = 1
    c = len(categories)
    for category in categories:
        try:
            url = defines.url_from_tag(category[0])
            print(str(i) + '/' + str(c) +
                ': open "' + category[1] + '" from ' + url)
            r = get_request(url, category, open_url)
            results.append(r)
        except:
            print('  error:(')
        i = i + 1

    open_url.close()

    for http_answer in results:
        #http_answer[1] - category
        category =  http_answer[1]
        #category[1] - name
        print('parse "' + category[1] + '"..')
        #http_answer[0] - requests.get(url).text
        html = http_answer[0] 
        products = parseCatalog(html)
        
        if (defines.UPDATE_DATABASE):
            db.set_goods_time(sql_cursor)
            for product in products:
                db.set_goods(sql_cursor, product, category[0])

    db.calc_added_goods(sql_cursor)

    added_goods = db.get_added_goods(sql_cursor)

    time = db.get_goods_time(sql_cursor)
    report.save("index.html", added_goods, time)

    all_goods = db.get_all_goods(sql_cursor)
    report.save("all_goods.html", all_goods, time)

    site_content = ['index.html', 'all_goods.html']

    mysite.update(site_content)

    db.close(sql_conn, sql_cursor)