import datetime
from playwright.async_api import Playwright, async_playwright
import pandas as pd
import random
import asyncio
import os

delay = random.uniform(1, 3)

async def scrape_data(page, level):
	table = [['timestamp', 'link', 'title', 'company', 'description', 'error']]
	i = 0
	page_num = 1

	while True:
		try:
			await asyncio.sleep(delay)
			try:
				await page.wait_for_selector('a[data-testid="pagination-page-next"]')
				next_page_link = await page.query_selector('a[data-testid="pagination-page-next"]')
			except:
				next_page_link = None

			await page.wait_for_selector('.job_seen_beacon')
			jobs = await page.query_selector_all('.job_seen_beacon')
			for job in jobs:
				try:
					timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
					error = None
					await job.wait_for_selector('[data-testid="company-name"]')
					element_handle = await job.query_selector('[data-testid="company-name"]')
					if element_handle:
						company = await element_handle.inner_text()
					else:
						company = "Not found"
					await job.wait_for_selector('a.jcs-JobTitle')
					url_id = await job.query_selector('a.jcs-JobTitle')
					url_id = await url_id.get_attribute('href')
					link = f'https://www.indeed.com{url_id}'
					await job.click()
					await asyncio.sleep(delay)
					title = await page.inner_text('h2[data-testid="jobsearch-JobInfoHeader-title"]')
					title = title.split('\n')[0]
					description = await page.inner_text('#jobDescriptionText')
					description = description[:99999] + (description[99999:] and '...')

					# append to the table
					table.append([timestamp, link, title, company, description, error])
					i += 1
					print(f'{i}: {title} - {link} | DONE')

					await asyncio.sleep(delay)
				
				except Exception as ex:
					error = str(ex)
					table.append([None, None, None, None, None, error])
					i += 1
					print(f'{i}: ERROR: {str(ex)}')
			
		except Exception as ex:
			print(f'{page_num}. page: ERROR: {str(ex)}')
				

		# Save data on every 3rd page
		if page_num % 2 == 0:
			clean_save_data(table, level)
			print(f'data saved at page: {page_num}')
			table = [['timestamp', 'link', 'title', 'company', 'description', 'error']]

		# Move to the next page
		next_page_link = await page.query_selector('a[data-testid="pagination-page-next"]')
		if next_page_link is None:
			print("Next page button not found, ending loop.")
			clean_save_data(table, level)
			print(f'data saved at page: {page_num}')
			break
		else:
			await next_page_link.click()
			await asyncio.sleep(delay)

		page_num += 1


def clean_save_data(data, level):
	# Create a dataframe
	df = pd.DataFrame(data)
	df = df.rename(columns=df.iloc[0]).drop(df.index[0])

	# Clean title
	df['title'] = df['title'].str.lower()
	df['title'] = df['title'].str.strip()
	df['title'] = df['title'].str.replace(r'[^\w\s]', ' ', regex=True)
	
	# Filter based on title
	# filter_words = '|'.join(filter_words)
	# df = df[df['title'].str.contains(filter_words, na=False)]

	# Clean filtered data
	df = df.drop_duplicates(subset='link')
	df['description'] = df['description'].str.lower()
	df['description'] = df['description'].str.replace(r'[^\w\s]', ' ', regex=True)
	df['description'] = df['description'].str.replace('Â', '', regex=True)
	df['description'] = df['description'].str.strip()
	df = df.replace('\n',' ', regex=True).replace(',',' ', regex=True).replace(';',' ', regex=True)

	# Save to CSV
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
	df['source'] = 'Indeed'
	csv_name = f'./indeed_csv/indeed_{level}_{timestamp}.csv'

	if os.path.isfile(csv_name):
		df.to_csv(csv_name, mode='a', header=False, index=False, sep=';')
	else:
		df.to_csv(csv_name, mode='w', header=True, index=False, sep=';')
	print(f'{csv_name} | saved data')

async def run(job: str): 
	async with async_playwright() as playwright:
		browser = await playwright.chromium.launch(headless=False) 

		# Creates a new browser context and opens a new page
		context = await browser.new_context() 
		page = await context.new_page() 

		level = ['Junior', 'Medior', 'Senior']
		search_url = [
			'https://www.indeed.com/jobs?q=application+integration+%2450%2C000&sc=0kf%3Aexplvl%28ENTRY_LEVEL%29jt%28fulltime%29%3B&vjk=3e1b7379394a7595', 		# junior, full-time
			'https://www.indeed.com/jobs?q=application+integration&sc=0kf%3Aexplvl%28MID_LEVEL%29jt%28fulltime%29%3B&vjk=d099ea4c77ab8816', 					# medior, full-time
			'https://www.indeed.com/jobs?q=application+integration&sc=0kf%3Aexplvl%28SENIOR_LEVEL%29jt%28fulltime%29%3B&vjk=6ee481b5c4831166'					# senior, full-time
		]
		search_url_short = [
			'https://www.indeed.com/jobs?q=application+integration+%2460%2C000&sc=0kf%3Aexplvl%28ENTRY_LEVEL%29jt%28fulltime%29%3B&fromage=1&vjk=a48a755ca3cb4b76', 		# junior, full-time, last 24 hours, remote, 50k+
			'https://www.indeed.com/jobs?q=application+integration&sc=0kf%3Aexplvl%28MID_LEVEL%29jt%28fulltime%29%3B&fromage=1&vjk=32e83d820e08ca81', 						# medior, full-time, last 24 hours, remote
			'https://www.indeed.com/jobs?q=application+integration&sc=0kf%3Aexplvl%28SENIOR_LEVEL%29jt%28fulltime%29%3B&fromage=1&vjk=f8390fe380cf5d9b'						# senior, full-time, last 24 hours, remote
		]

		# Search job on Indeed
		for i in range(3):
			print(f'/////////////////////////////////////{level[i]}/////////////////////////////////////')
			await page.goto(search_url_short[i])
			await scrape_data(page, level[i])                         # Scrapes the data from the website

		# Turns off the browser 
		await context.close() 
		await browser.close() 