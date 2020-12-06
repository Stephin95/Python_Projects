from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pickle
from tqdm import tqdm
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}



url=input('Enter the Url')
url1='https://www.amazon.in/s?bbn=1375424031&rh=n%3A976392031%2Cn%3A%21976393031%2Cn%3A1375424031%2Cp_85%3A10440599031%2Cp_36%3A7252031031%2Cp_n_condition-type%3A8609960031&dc&fst=as%3Aoff&pf_rd_i=1375424031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=da9ba959-29e3-4d10-ac01-2fe67bae76d1&pf_rd_r=3E1NZDJ3N9S7T19GM6F9&pf_rd_s=merchandised-search-13&pf_rd_t=101&qid=1551690318&rnid=8609959031&ref=s9_acss_bw_cg_Laptops_2d1_w'


def pndas(data):
	df=pd.DataFrame(data)
	mainresult = df.to_html()
	filew(mainresult,'MainResult.html')
	print(df)
	print('Total Data Scraped Saved To MainResult.html file' )
	term='re'
	while term == 're':
		term=input('Enter Search word \n')or 'invalid'
		if term == 'invalid':
			break
		rdf=df[df.Name.str.contains(term,flags=re.IGNORECASE,regex=True)]
		while True:
				if term== 're':
					break
				elif term:
					rdf=rdf[rdf.Name.str.contains(term,flags=re.IGNORECASE,regex=True)]
					print(rdf)
					term=''
					term=input('\n To refine search Add More Keywords \n To Save the Search Result press Enter\nTo Search Again Enter "re" \n ')

				else:
					break
			
#	rdf=rdf[rdf['Prices']<42000]
	print(rdf)
	result = rdf.to_html()
	filew(result,'Results.html')
	print('Search Result Saved To Results.html file' )



def html_format(soup):
	k=0
	address={}
	soupy=(soup.prettify())
	index=0
	for i in tqdm(range(0,len(soupy))):
		if soupy[i] ==' ':
			index =index+1
			if soupy[i+1]==' ':
				pass
			else:
				if index>2:
					k=k+1
					address[k]=index
					soupy=soupy[:i]+f'_{k}_-_{index}__'+soupy[i:]
				index=0
		else:
			pass
	print('Completed Extracting Html and reformating it')
	filew(soupy,'Formatted_Html.txt')
	print(soupy)
	print('Html output saved to Formatted_Html.txt file')
	return address
	



#rept variables informs the function to perform a thorough second search to confirm the result from first one which was only a partial search passing rept as 0 will trigger this action

def html_search(address,rept,start=0,end=0):
	if rept==0:
		print('\n Enter the starting and end line no. of the block you are intrested in so I will try to give the tags it will be inaccurate but still be a goodplace to start looking\n')
		start=int(input('Start :-'))
		end=int(input('End :-'))
	old=start
	for x in range((start+1),end):
		if address[start]==address[x]:
			print(f'checked {start}:{address[start]} = {x}:{address[x]} :match')
#check if following range need to be increased say to 2500 because it may solve going up 0 places error		
			for diff in range(1,2000):
				if ((address[start])-1)==address[start-diff]:
					start= start-diff
					break
				else:
					continue
		elif address[start]>address[x]:
			for diff in range(1,2000):
				if ((address[x])-1)==address[start-diff]:
					start= start-diff
					break
				else:
					continue
			
			jump=old-start
			print(f'from {old}:{address[old]} to  {start}:{address[start]} - Going up {jump} places')
			old=start
		elif (x-1)==end:
			print(f'Tag you are looking is {address[start]} finished')
			break
			
		else:
			print(f'checking {start}:{address[start]} = {x}:{address[x]} - no match')
	if rept==0:
		print('initialising second search')
		html_search(address,1,start,end)
	elif rept==1:
		print('all process completed',address[start],start)
	return address[start]









def filew(matter,fnme='read.txt'):
		with open(fnme, 'w') as file:
			file.writelines(matter)
			return('Success')
			
			
			
			
def filer(matter,fnme='read.txt'):
		with open(fnme, 'r') as file:
			return file.read()
			
			
			
def scoup(url):

	try:
		response_temp = pickle.load( open( "save.p", "rb" ) )
		new=int(input('Get latest response from site or get offline old data to work on .For the former press 1 ') or 0)
	except:
		print('cant find old data')
		new=1
	if new==0:
			response=response_temp
			print('Reading old data successful')
			soup=BeautifulSoup(response,'lxml')
	elif new==1:
			print('Loading html-')
			response=requests.get(url,headers=headers).content
			print('\nDownloaded html successfully\nSaving html file to save.p......')
			pickle.dump( response, open( "save.p", "wb" ) )
			print('completed')
	soup=BeautifulSoup(response,'lxml')
		
	return soup
	
	
def scoupy(url):
	print('Loading html-')
	response=requests.get(url,headers=headers).content
	soup=BeautifulSoup(response,'lxml')
	print('successful')
	return soup


data=[]
old_dict=[]
def amzonecrwl(url,mode):
	global data
	global dict
	if mode==1:
		soup=scoup(url)
		address=html_format(soup)
		reqm=input('do you need to search the html for tags enter 1 else press enter')
		
		if reqm:
			o=1
			while o==1:
				html_search(address,0)
				('HTML Search Operation Completed')
				o=int(input('To Continue Searching Press Enter, Else To Continue Scraping Press 1') )
				if 0==o:
					break
	elif mode==0:
		soup=scoupy(url)
	testing2=soup.find_all('div',attrs={ 'class':'a-fixed-left-grid-col a-col-right'})
	testing=soup.find_all('div',attrs={'class':'sg-col-inner'})
	if len(testing2)>2 and len(testing)<2:
		testing=testing2
		capt=1
	else:
		capt=0
		pass
	ii=1
	linkold=''
	for test in testing:
		try:
			link=test.a.get('href')
			spon=test.find_all('div',attrs={'data-component-type':'sp-sponsored-result'})
			spon2=test.find_all('div',attrs={'class':'aok-inline-block s-sponsored-label-info-icon'})
			spon3=test.find_all('div',attrs={'class':'s-label-popover-hover'})
			if link == linkold:
				continue
			elif test.h5 or spon3 or spon2 or spon:
				continue
			else:
				pass
				
			linkold=link
			link='https://www.amazon.in'+link
			
			if capt==1:
				title=test.find('h2').get('data-attribute')
				price=test.find('span' ,class_='a-size-base a-color-price s-price a-text-bold').text
			else:
				title=test.find('span',class_='a-size-medium a-color-base a-text-normal').text
				price=test.find('span' ,class_="a-offscreen").text
			ii=ii+1
#			print(f'{ii})Price:-{price}\n')	
#			print(f'{ii}){title}\nPrice:-{price}\n')	
			print(f'\n__{ii}__\n{title}\nPrice:-{price}\n{link}\n___')
			dict={'Name':title,'Prices':price,'Link':link}
			data.append(dict)
			
		except Exception as e:
			pass
#			print("Oops!", e.__class__, "occurred.")	
	try:

		if capt==1:
			nxt=soup.find('a', class_='pagnNext').get('href')
		elif capt==0:
			nxt=soup.find('li',class_="a-last").a.get('href')
		nxt='https://www.amazon.in'+nxt
		print(f'next page link is {nxt}')
		print('Sleeping for 2 Seconds')
		time.sleep(2)
		amzonecrwl(nxt,0)
	except:
		print('COMPLETED!!!!!')
		if mode==1:
			if input('Do You Want Continue Add The Data to Pandas Dataframe If Yes Press Enter ' or 1):
				pndas(data)
		elif mode==0:
			pndas(data)
		
	

def flipcrawl(url,mode):
	error_msg='Unknown'	
	global data
	global dict
	if mode==1:
		soup=scoup(url)
		address=html_format(soup)
		reqm=input('\nDo you Need to Search the html for tags enter 1 else press Enter\n')
		
		if reqm:
			o=0
			while o==0:
				html_search(address,0)
				o=int(input('To Continue Press 1 Else For Continue Searching Press 0') or 0)
			
			
	elif mode==0:
		soup=scoupy(url)
	lst=soup.find_all('div')
	
	for x in lst:
				if x.get('data-id') is not None:
					item_name=x.img.get('alt')
					item_link='https://www.flipkart.com'+x.a.get('href')
					item_price=x.div.find_all(attrs={"class":"_30jeq3"})[0].text
					item_price=int(re.sub('₹|,','',item_price))
					try:
						item_discount=int(re.findall('(\d|\d\d)?[%]\soff?',str(x))[0])
					
					except:
						item_discount=error_msg
					try:
						temp=x.div.find_all('div',attrs={'class':'gUuXy-'})
						item_rating=int(temp[0].div.text)
					except:
						item_rating=error_msg
						
					dict={'Name':item_name,'Prices':item_price,'Link':item_link}
					data.append(dict)
					
#					dict={'Name':item_name,'Prices':item_price,'Rating':item_rating,'Discounts':item_discount,'Link':item_link}
				
						
				
	
	rsl=soup.find_all('link',attrs={"id":"next-page-link-tag"})

	if len(rsl)==0:
		print('All pages Crawled run completed')
		pndas(data)
		
		
	else:
		print('Loading Next Page')
		soupy=BeautifulSoup(str(rsl[0]),'lxml')
		nxtlk=soupy.link.get('href')
		flipcrawl(nxtlk,0)
	
	
choice=int(input('press 1 for amazon and 0 for flikart' )or 0)


mode=int(input('Advanced mode or easy mode \n Enter 1 for Advance mode\n Enter 0 for Easy Mode') or 0)

if choice==1:
	amzonecrwl(url,mode)
elif choice==0:
	flipcrawl(url,mode)