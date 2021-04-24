import requests, webbrowser, time, json, os
from bs4 import BeautifulSoup as Soup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def checkOut(url):
	driver = webdriver.Chrome(configJson['MAIN']['CHROMEDRIVER'])
	driver.get(url)
	
	Select(driver.find_element_by_id("checkout_shipping_address_country")).select_by_value(configJson['CHECKOUT']['SHIPPING']['COUNTRY'])
	
	#Ignore countries with no state field
	try:
		Select(driver.find_element_by_id("checkout_shipping_address_province")).select_by_visible_text(configJson['CHECKOUT']['SHIPPING']['STATE'])
	except:
		pass
		
	driver.find_element_by_id("checkout_email_or_phone").send_keys(configJson['CHECKOUT']['SHIPPING']['EMAIL'])
	driver.find_element_by_id("checkout_shipping_address_first_name").send_keys(configJson['CHECKOUT']['SHIPPING']['FIRSTNAME'])
	driver.find_element_by_id("checkout_shipping_address_last_name").send_keys(configJson['CHECKOUT']['SHIPPING']['LASTNAME'])
	driver.find_element_by_id("checkout_shipping_address_address1").send_keys(configJson['CHECKOUT']['SHIPPING']['ADDRESS1'])
	if configJson['CHECKOUT']['SHIPPING']['ADDRESS2']:
		driver.find_element_by_id("checkout_shipping_address_address2").send_keys(configJson['CHECKOUT']['SHIPPING']['ADDRESS2'])
	driver.find_element_by_id("checkout_shipping_address_city").send_keys(configJson['CHECKOUT']['SHIPPING']['CITY'])
	driver.find_element_by_id("checkout_shipping_address_zip").send_keys(configJson['CHECKOUT']['SHIPPING']['ZIP'])
	
	#Ignore platforms without phone
	try:
		driver.find_element_by_id("checkout_shipping_address_phone").send_keys(configJson['CHECKOUT']['SHIPPING']['PHONE'])
	except:
		pass
	
	#Proceed to shipping options
	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'continue_button'))).click()
	
	#Proceed to billing
	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'continue_button'))).click()
	
	driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-number-')]"))
	for number in configJson['CARD']['NUMBER']:
		driver.find_element_by_id("number").send_keys(number);
	driver.switch_to.parent_frame();

	driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-name-')]"))
	driver.find_element_by_id("name").send_keys(configJson['CARD']['NAME']);
	driver.switch_to.parent_frame();

	driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-expiry-')]"))
	for number in configJson['CARD']['EXP']:
		driver.find_element_by_id("expiry").send_keys(number);
	driver.switch_to.parent_frame();

	driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-verification_value-')]"))
	driver.find_element_by_id("verification_value").send_keys(configJson['CARD']['SEC']);
	driver.switch_to.parent_frame();
	
	driver.find_element_by_id("checkout_different_billing_address_true").click()
	Select(driver.find_element_by_id("checkout_billing_address_country")).select_by_visible_text(configJson['CHECKOUT']['BILLING']['COUNTRY'])
	
	#Ignore countries with no state field
	try:
		Select(driver.find_element_by_id("checkout_billing_address_province")).select_by_visible_text(configJson['CHECKOUT']['BILLING']['STATE'])
	except:
		pass
		
	driver.find_element_by_id("checkout_billing_address_first_name").send_keys(configJson['CHECKOUT']['BILLING']['FIRSTNAME'])
	driver.find_element_by_id("checkout_billing_address_last_name").send_keys(configJson['CHECKOUT']['BILLING']['LASTNAME'])
	driver.find_element_by_id("checkout_billing_address_address1").send_keys(configJson['CHECKOUT']['BILLING']['ADDRESS1'])
	if configJson['CHECKOUT']['BILLING']['ADDRESS2']:
		driver.find_element_by_id("checkout_billing_address_address2").send_keys(configJson['CHECKOUT']['BILLING']['ADDRESS2'])
	driver.find_element_by_id("checkout_billing_address_city").send_keys(configJson['CHECKOUT']['BILLING']['CITY'])
	driver.find_element_by_id("checkout_billing_address_zip").send_keys(configJson['CHECKOUT']['BILLING']['ZIP'])
	
	#Ignore platforms without phone
	try:
		driver.find_element_by_id("checkout_billing_address_phone").send_keys(configJson['CHECKOUT']['BILLING']['PHONE'])
	except:
		pass
	
	#Pay now or proceed to order review page
	if configJson['MAIN']['AUTOPAY']:
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'continue_button'))).click()
	
	#Pay now if platform has a order review page
	try:
		if configJson['MAIN']['AUTOPAY']:
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'continue_button'))).click()
	except:
		pass
	
	#Selenium closes the browser once script execution is finished so I added 5 min sleep timer so you can check order details 
	time.sleep(300)
	
def checkSite():
	loopFlag = True
	#Convert keywords to lowercase to make string matching with URL case insensitive
	kwVariant= [kw.lower() for kw in configJson['MAIN']['VARIANT_KW']]
	exclude_kwVariant= [kw.lower() for kw in configJson['MAIN']['EXCLUDE_VARIANT_KW']]
	kwProduct = [kw.lower() for kw in configJson['MAIN']['PRODUCT_KW']]
		
	while loopFlag:
		try:
			print(f"Checking frontpage...")
			baseResponse = requests.get(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['COLLECTION_PAGE']))
			if baseResponse.status_code != 404:
				productLXML = Soup(baseResponse.text,'lxml')
				productLinks = []
				#Convert URL to lowercase to make string matching with URL case insensitive
				for link in [str(ahref.get('href')).lower() for ahref in productLXML.findAll('a')]:
					if all(kw in link for kw in kwProduct) and link not in productLinks:
						productLinks.append(link)
				if productLinks:
					linkOpened = False
					for link in productLinks:
						if linkOpened:
							break
						print(f"Checking {link}...")
						productResponse = requests.get(urljoin(configJson['MAIN']['BASE_LINK'], link) + ".xml")
						if productResponse.status_code != 404:
							productXml = Soup(productResponse.text,'xml')
							tagList = productXml.find_all('variant')
							for tag in tagList:
								skipFlag = False
								productTitle = tag.find("title").text
								print(productTitle)
								if kwVariant:
									if all(kw in productTitle.lower() for kw in kwVariant):
										if exclude_kwVariant:
											if all(kw in productTitle.lower() for kw in exclude_kwVariant):
												skipFlag = True
										if not skipFlag:
											name = tag.find("id").text
											print(f"Check·out {productTitle} with product id {name}")
											if not configJson['MAIN']['CHECKOUT']:
												webbrowser.register('chrome',
												None,
												webbrowser.BackgroundBrowser(configJson['MAIN']['CHROME']))
												webbrowser.get('chrome').open(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
											else:
												checkOut(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
											loopFlag = False
											linkOpened = True
											break
								else:
									name = tag.find("id").text
									print(f"Check·out {productTitle} with product id {name}")
									if not configJson['MAIN']['CHECKOUT']:
										webbrowser.register('chrome',
											None,
											webbrowser.BackgroundBrowser(configJson['MAIN']['CHROME']))
										webbrowser.get('chrome').open(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
									else:
										checkOut(urljoin(configJson['MAIN']['BASE_LINK'], configJson['MAIN']['CART_LINK']) + f"/{name}:{configJson['MAIN']['QUANTITY']}")
									loopFlag = False
									linkOpened = True
									break
				else:
					print(f"0 matched for keyword/s - {str(configJson['MAIN']['PRODUCT_KW'])}")
		except Exception as e:
			print(e)
		print(f"Sleep for {configJson['MAIN']['SLEEP_TIMER']} seconds")
		time.sleep(configJson['MAIN']['SLEEP_TIMER'])
	
if __name__ == "__main__":
	with open(os.path.join(os.getcwd(), "config.json")) as jsonHandle:
		configJson = json.load(jsonHandle)
	checkSite()