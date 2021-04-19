# Prerequisites

Script requires the following applications

```
Python3
Google Chrome (Account must already be logged in DRW)
Chromedriver (Latest version)
```

# Getting Started

Before running the script, please ensure that the JSON file is in the same directory as the script file. 

Please see below for a short guide on setting up the configuration file -

MAIN
* CHROME (str) - Path to chrome executable. Please escape special characters like the backslash (ex. "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -> "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
* CHROMEDRIVER - Path to chromedriver executable. Please escape special characters like the backslash 
* BASE_LINK (str) - Webstore URL
* CART_LINK (str) - Cart directory
* COLLECTION_PAGE (str) - Collection directory
* VARIANT_KW (str) - Keywords related to the item that the script will check from the product XML (ex. "obi", "pink", "splatter")
* PRODUCT_KW (list) - Keywords related to the item that the script will check from the list of URLS in Collection Page. Multiple keyword matching is supported. (ex. ["conway"], ["conway", "goat"])
* SLEEP_TIMER (int) - Wait time before script executes another check of the store.
* QUANTITY (str) - Number of copies to be checked out
* CHECKOUT (bool) - Set to true to enable checkout function. 
* AUTOPAY (bool) - Set to true to enable auto checkout of order. 

CHECKOUT
* EMAIL (str) - Email address
* FIRSTNAME (str) - Customer First Name
* LASTNAME (str) - Customer Last Name
* ADDRESS1 (str) - Address Line 1
* ADDRESS2 (str) - Address Line 2
* ZIP (str) - Zip/Postal Number
* CITY (str) - City
* COUNTRY (str) - Value to be picked from County dropdown button
* STATE (str) - Value to be picked from State/Province dropdown button. Leave as empty if this is not required for your selected Country.
* PHONE (str) - Phone Number

CARD
* NUMBER (list) - Card number. Format used is XXXX XXXX XXXX XXXX (ex. ["1234", "5678", "9012", "3456"])
* NAME - Name of card holder
* EXP (list) - Expiry Date. Date format is MM/YY (ex. ["01","21"]]
* SEC (str) - Security code 


# Running the script

```
python run.py
```
