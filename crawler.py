import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

domain_base = 'https://en.wikipedia.org/'
url_base = 'https://en.wikipedia.org/wiki/List_of_American_films_of_'
base_year = 2015
final_year = 2015
folder = '/home/mukund/Documents/College/Sem-IX/IR/Films'

def open_html_file(location='/home/mukund/Documents/College/Sem-IX/IR/MovieSearch/2015A.html'):
	import codecs
	# print(1)
	f = codecs.open(location, 'r')
	value = f.read()
	f.close()
	return value


def parse_soup_to_file(soup, name):
	print()
	return

def crawl_film_list(soup_table):
	movies = soup_table.find_all('i')
	for movie in movies:
		movie_name = movie.a.text
		movie_url = domain_base + movie.a.atts['href']
		movie_html = urlopen(movie_url)
		movie_soup = bs(movie_html, 'html.parser')
		parse_soup_to_file(movie_soup, movie_name)
	return

def get_all_lists(url):
	
	for year in range(base_year, final_year+1):
		year_url = url_base + str(year)
		# Crawl the page for a particular year
		year_html = urlopen(year_url)
		year_soup = bs(year_html, 'html.parser')
		all_tables = year_soup.find_all('table')
		film_tables = []
		# Of all tables, find the ones required (class: wikitable sortable)
		for table in all_tables:
			if 'class' in table.attrs and table.attrs['class'] == ['wikitable', 'sortable']:
				# Send them to crawl_film_list to be parsed into 
				# individual films
				print(table)
				# crawl_film_list(table)
	
	# year_html = open_html_file()
	# year = 2015
	# year_url = url_base + str(year)
	# year_html = urlopen(year_url)
	# year_soup = bs(year_html, 'html.parser')
	# all_tables = year_soup.find_all('table')
	# print(all_tables)


get_all_lists(url_base)
# print(2)
# open_html_file()