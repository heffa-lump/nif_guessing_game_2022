# -*- coding: utf-8 -*-

import nif_exchange_2022 as nif_exchange
from nif_exchange_2022 import HTML_DIR 
import urllib3
import os
from bs4 import BeautifulSoup
import io
import time

AO3_DELAY = 6 	# seconds

def WriteWorkToFile(outdir, work_data, raw = False):
	# Get work title
	work_soup = BeautifulSoup(work_data, 'html.parser')
	title_soup = work_soup.find(lambda x: x.name == 'h2' and x['class'][0] == 'title' and x['class'][1] == 'heading')
	if not title_soup:
		raise BaseException('Could not find title!')
	title = title_soup.text.strip()

	# Strip non-ascii characters from title
	ascii_title = title + '.txt'

	# Clear outfile
	out_filename = '%s/%s' % (outdir, ascii_title)
	outfile = open(out_filename, 'w')
	outfile.close()

	# Write work body to file
	if raw:
		content = str(work_soup)
		outfile = io.open(out_filename, 'a', encoding='utf-8')
		outfile.write(content)
		outfile.close()		
	else:
		chapters = work_soup.find_all(lambda x: x.name == 'div' and x.has_attr('class') and len(x['class']) > 0 and x['class'][0] == 'userstuff')
		for chapter in chapters:
			for node in chapter.children:
				if node.name == 'h3' and node.has_attr('class') and node['class'][0] == 'landmark' and node['class'][1] == 'heading':
					continue
				content = str(node)
				outfile = io.open(out_filename, 'a', encoding='utf-8')
				outfile.write(content)
				outfile.close()


def FindWorks(soup):
	ols = soup.find_all(lambda x: x.name == 'ol' and x['class'][0] == 'work' and x['class'][1] == 'index' and x['class'][2] == 'group')
	if not ols:
		raise 'Count not find works in soup!'
		print(soup)
		return
	if len(ols) > 1:
		raise 'More than 1 work index group!'
	work_index_group = ols[0]
	works = work_index_group.find_all(lambda x: x.name == 'li' and x.has_attr('id'))
	return works


def DownloadExchangeWorks(work_ids, raw=False):
	http = urllib3.PoolManager()
	outdir = nif_exchange.TEST_DIR
	if raw:
		outdir = nif_exchange.TEST_DIR + '_raw'
	for work_id in work_ids:
		work_url = "https://archiveofourown.org/works/%s?view_full_work=true&view_adult=true" % work_id
		print(work_url)

		time.sleep(5)
		work_response = http.request('GET', work_url)
		if work_response.status != 200:
			raise BaseException('Something went wrong in fetching work!')
		
		WriteWorkToFile(outdir, work_response.data, raw=raw)


def DownloadRevealedWorks(creators):
	http = urllib3.PoolManager()
	for creator, url in creators.items():
		print(url)
		outdir = "%s/%s" % (HTML_DIR, creator)
		if os.path.exists(outdir):
			continue
		os.mkdir(outdir)

		# Fetch creator works page
		time.sleep(AO3_DELAY)
		response = http.request('GET', url)
		if response.status != 200:
			raise BaseException('Something went wrong in fetching creator page!')

		soup = BeautifulSoup(response.data, 'html.parser')

		works = FindWorks(soup)

		# Fetch each work
		for work in works:
			rel_url = work.a['href']
			work_url = "https://archiveofourown.org/%s?view_full_work=true&view_adult=true"	% rel_url
			print(work_url)

			time.sleep(AO3_DELAY)
			work_response = http.request('GET', work_url)
			if work_response.status != 200:
				raise BaseException('Something went wrong in fetching work!')
			
			WriteWorkToFile(outdir, work_response.data)


if __name__ == '__main__':
#	DownloadRevealedWorks(nif_exchange.creator_urls)
	DownloadExchangeWorks(nif_exchange.work_ids, raw=True)






