#!/usr/bin/env python
print "Content-type: text/html\n"
import json
import os, sys, stat
from splinter import Browser

sessionpath = "/home/guni/.mozilla/firefox/72wc3h5t.default/sessionstore-backups/recovery.js"
f = open(sessionpath, "r")
data = json.loads(f.read())
f.close()
urls = []

for win in data.get("windows"):
    for tab in win.get("tabs"):
        i = tab.get("index") - 1
        urls.append(tab.get("entries")[i].get("url"))
print urls[-1]  
browser = Browser('firefox') 
browser.visit(urls[-1])
browser.driver.save_screenshot('1.png')
if browser is not None:
    browser.quit()
