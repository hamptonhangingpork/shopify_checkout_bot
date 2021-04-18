## Prerequisites

Script requires the following applications

```
Python3
Google Chrome
```

## Getting Started

Before running the script, please ensure that the JSON file is in the same directory as the script file. Please see below for a short guide on setting up the configuration file -

* CHROME (str) - Path to chrome executable. Please escape special characters like the backslash (ex. "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -> "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
* BASE_LINK (str) - Webstore URL
* CART_LINK (str) - Cart directory
* COLLECTION_PAGE (str) - Collection directory
* VARIANT_KW (str) - Keywords related to the item that the script will check from the product XML (ex. "obi", "pink", "splatter")
* PRODUCT_KW (list) - Keywords related to the item that the script will check from the list of URLS in Collection Page. Multiple keyword matching is supported. (ex. ["conway"], ["conway", "goat"])
* SLEEP_TIMER (int) - Wait time before script executes another check of the store.
* QUANTITY (str) - Number of copies to be checked out

## Running the script

```
python w.py
```
