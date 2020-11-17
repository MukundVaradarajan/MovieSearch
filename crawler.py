import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os
import pandas as pd
import time

domain_base = 'https://en.wikipedia.org/'
url_base = 'https://en.wikipedia.org/wiki/List_of_American_films_of_'
base_year = 2015
final_year = 2020
folder = '/home/mukund/Documents/College/Sem-IX/IR/Films'
folder_created = False
movie_db = {'url': [], 'name': [], 'location': []}

def open_html_file(location='/home/mukund/Documents/College/Sem-IX/IR/MovieSearch/2015A.html'):
	import codecs
	# print(1)
	f = codecs.open(location, 'r')
	value = f.read()
	f.close()
	return value


def save_to_file(data, file_name):
	try:
		os.mkdir(folder)
		folder_created = True
	except:
		pass
	location = os.path.join(folder, file_name+'.txt')
	
	try:
		f = open(location, 'w')
		f.write(data)
		f.close()
	except:
		movie_db['url'] = movie_db['url'][:-1]
		movie_db['name'] = movie_db['name'][:-1]
		return

	movie_db['location'].append(location)



def parse_soup_to_file(soup, name):
	final_str = ''
	for elt in soup.body:
		if elt.name == 'div' and 'id' in elt.attrs \
		and elt.attrs['id'] == 'content':
			content_soup = elt
			contents = content_soup.find_all('p')
			# cast = content_soup.find_all('li')
			for content in contents:
				final_str += (content.text+'\n')
			# print(final_str)
			divs = content_soup.find_all('div')
			cast_names = ''
			for div in divs:
				if 'class' in div.attrs and \
				div.attrs['class'] == ['div-col', 'columns', 'column-width']:
					cast = div.find_all('li')
					for actor in cast:
						cast_names += (actor.text+'\n')
			# print(cast_names)
			final_str += cast_names

	# print(final_str)
	save_to_file(final_str, name)

	return

def crawl_film_list(soup_table):
	movies = soup_table.find_all('i')
	# print(movies[:1])
	for movie in movies:
		movie_name = movie.text
		# print(movie_name)
		if movie.a == None:
			continue
		movie_url = domain_base + movie.a.attrs['href']
		if 'redlink=1' in movie_url:
			print("Movie data doesn't exist")
			continue
		movie_name = movie.a.attrs['title']
		print('++++++MOVIE++++++')
		print(movie_url)
		movie_html = urlopen(movie_url)
		time.sleep(5)
		movie_db['url'].append(movie_url)
		movie_db['name'].append(movie_name)
		movie_soup = bs(movie_html, 'html.parser')
		parse_soup_to_file(movie_soup, movie_name)
	return

def get_all_lists(url):
	folder_created = False
	print('Started crawling...')
	for year in range(base_year, final_year+1):
		year_url = url_base + str(year)
		# Crawl the page for a particular year
		print(year, time.time())
		year_html = urlopen(year_url)
		time.sleep(5)
		year_soup = bs(year_html, 'html.parser')
		all_tables = year_soup.find_all('table')
		film_tables = []
		# Of all tables, find the ones required (class: wikitable sortable)
		for table in all_tables:
			if 'class' in table.attrs and table.attrs['class'] == ['wikitable', 'sortable']:
				# Send them to crawl_film_list to be parsed into 
				# individual films
				crawl_film_list(table)
		print(year, 'finished')

	df = pd.DataFrame.from_dict(movie_db)
	df.to_csv(folder+'/movies.csv', index=False)
	
if __name__ == '__main__':
	get_all_lists(url_base)
# print(2)
# open_html_file()