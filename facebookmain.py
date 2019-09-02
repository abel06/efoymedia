from selenium import webdriver
import sys
print (sys.path)
browser = webdriver.Firefox()
browser.get('http://seleniumhq.org/')