import requests, webbrowser, time, re, json, os
from bs4 import BeautifulSoup as Soup
from urllib.parse import urljoin

def checkSite():
	loopFlag = True		
	while loopFlag:
		try:
			print(f"Checking frontpage...")
			baseResponse = requests.get(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['COLLECTION_PAGE']))
			if baseResponse.status_code != 404:
				productLXML = Soup(baseResponse.text,'lxml')
				productLinks = []
				for link in productLXML.findAll('a'):
					productLinks.append(link.get('href'))
				if productLinks:
					linkOpened = False
					for link in productLinks:
						if linkOpened:
								break
						if all(kw in link for kw in configJson['MAIN']['PRODUCT_KW']):
							print(f"Checking {link}...")
							productResponse = requests.get(urljoin(configJson['MAIN']['BASE_LINK'], link) + ".xml")
							if productResponse.status_code != 404:
								productXml = Soup(productResponse.text,'xml')
								tagList = productXml.find_all('variant')
								for tag in tagList:
									productTitle = tag.find("title").text
									if configJson['MAIN']['VARIANT_KW']:
										variantFlag = re.search(f".*{configJson['MAIN']['VARIANT_KW']}.*", productTitle, re.IGNORECASE)
										if variantFlag:
											name = tag.find("id").text
											print(f"Check·out {variantFlag[0]} with product id {name}")
											webbrowser.get('chrome').open(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
											loopFlag = False
											linkOpened = True
											break
									else:
										name = tag.find("id").text
										print(f"Check·out {productTitle} with product id {name}")
										webbrowser.get('chrome').open(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
										loopFlag = False
										linkOpened = True
										break
		except Exception as e:
			print(e)
		print(f"Sleep for {configJson['MAIN']['SLEEP_TIMER']} seconds")
		time.sleep(configJson['MAIN']['SLEEP_TIMER'])
	
if __name__ == "__main__":
	with open(os.path.join(os.getcwd(), "config.json")) as jsonHandle:
		configJson = json.load(jsonHandle)

	webbrowser.register('chrome',
		None,
		webbrowser.BackgroundBrowser(configJson['MAIN']['CHROME']))
	
	checkSite()
