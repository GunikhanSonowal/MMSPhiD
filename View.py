from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from firstproject.forms import LoginForm
import socket
import os
import urllib2
import time
import sys
from tld import get_tld
import json
import fileinput
from glob import glob
import math
from metaphone import doublemetaphone
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
import subprocess
import csv
from ipwhois import IPWhois
from pprint import pprint
from django.contrib.sites.shortcuts import get_current_site
from ipwhois.utils import get_countries
import subprocess
def current_url(request):

		try:
		        temp = 1
		    	rank = 0
		    	time.sleep(10)
		    	sessionpath = "/home/guni/.mozilla/firefox/9i3lgk6r.default/sessionstore-backups/recovery.js"
		        f = open(sessionpath, "r")
		        data = json.loads(f.read())
		        f.close()
		        urls = []
		        url = ""
		        for win in data.get("windows"):
		                for tab in win.get("tabs"):
		                        i = tab.get("index") - 1
		                        urls.append(tab.get("entries")[i].get("url"))
		        print urls[-1]
		        url = urls[-1]
		        
		        domain =  get_tld(urls[-1]) 
		        
		        print "Top Level domain ", domain +"\n"
		        localtime = time.asctime( time.localtime(time.time()) )
		        print "Local current time :", localtime
		        creatfile = open("/home/guni/projectname/secondproject/list_checking_url.txt","a")
		        creatfile.write(urls[-1]+": Access time"+localtime+"\n") 
		        hand = open('/home/guni/projectname/secondproject/shopping_Metaphone.txt',"r")
		        for line in hand:
		                row = line.split(',')
		                if domain in row[1]:
		                        urls = urls[-1]
		                        rank = rank + 1
		                        temp = 0
		        hand.close()
	        	if temp == 0:
	            		return render(request, "/home/guni/projectname/firstproject/templates/viewurl.html", {"url" : url, "domain" : domain })  
	     
	        
	    
	    		return render(request, "/home/guni/projectname/firstproject/templates/phoneme.html", {"domain" : domain , "url" :  url})       
		except Exception,e: 
				str1 = str(e)
				return render(request, "/home/guni/projectname/firstproject/templates/sorry.html", {"wrong" : str1})

def moreinformation(request):

		temp = 1       
		domain = ""
		try:
				if request.POST:
						urls = request.POST['url']
						domain = get_tld(urls)
						ipadress = socket.gethostbyname(domain)
						obj = IPWhois(ipadress)
						results = obj.lookup_rdap(depth=1)
						verify = ""
						asn1 = str(results['asn'])
						print asn1
						file1 = open("/home/guni/projectname/secondproject/GeoIPASNum2.txt" , "r")
						for line1 in file1:
								line = line1.split(",")
								print asn1
								if asn1 in line[2]:
										verify = "TRUE"
										break
								else:
										#print line[2]
										verify = "FALSH"

						countries = get_countries()
						country1 = countries[results['asn_country_code']]
						
						return render(request, "/home/guni/projectname/firstproject/templates/moreinformation.html", { "url" :urls ,"ip" : ipadress, "asn" : results['asn'] , "verify" : verify, "code" : results['asn_country_code'] , "Registration":  results['asn_date'],  "country" : country1, "register1": results['asn_registry'] })
		except Exception,e: 
				str1 = str(e)
				return render(request, "/home/guni/projectname/firstproject/templates/sorry.html", {"wrong" : str1})	

def phonemCheck(request):
        temp = 1
        domain = ""
        result = 0
     
        print "gunikhan"
        try:
		        outfile = open("/home/guni/projectname/firstproject/templates/suggetion.html","w")
		        outfile.write("<html><body><center><marquee>We will suggest you following url which is geniune </marquee><br>Click info for more formation<hr><fieldset style='width:570px'>"+"\n")
		        if request.POST:
		            domain = request.POST['url']
		            #domain =  get_tld(domain) 

		            print "domain sent", domain, "\n"
		        
		            
		            
		            domain_phonetic = doublemetaphone(domain)
		            print "Metaphone code generation is :",domain_phonetic[0],"\n"
		            infile = open("/home/guni/projectname/secondproject/shopping_Metaphone.txt","r")
		            
		            for line in infile:
		                row = line.split(',')
		                result = normalized_damerau_levenshtein_distance(domain_phonetic[0], row[0]) 
		                result = (1-result) * 100
		                if result >= 76:
		                        
		                        #ipadress = socket.gethostbyname(row[1].strip())
		                        #print ipadress
		                        #obj = IPWhois(ipadress)
		                        #results = obj.lookup_rdap(depth=1)
		                        #countries = get_countries()
		                        #country1 = countries[results['asn_country_code']]
		                        #details = " <br> Contry code : "  + results['asn_country_code'] + ";&nbsp " +"Registration date :&nbsp" + results['asn_date'] +"&nbsp"+ country1
		                        #outfile.write("<a href ="+'"http://www.'+row[1] +'"'+ ">"+row[1]+"</a>"+details+"<br><br>"+"\n")
		                        outfile.write("<a href ="+'"http://www.'+row[1] +'"'+ ">"+row[1]+"</a><br><br>"+"\n")
		                        print "your are search this Url :"+row[1] +'#'+ row[0]
		                        print "\nSimilarity percentage : ",result 
		                        
		                        temp = 0

		        outfile.write("<br></fieldset>")
		        print "khan sonowal" 
		        outfile.close() 

		        
		        if temp == 0:
		                print "suggestion_page open"
		                return render(request, "/home/guni/projectname/firstproject/templates/suggetion.html") 
        		return render(request, "/home/guni/projectname/firstproject/templates/phonemeMatch.html",{"domain" : domain})
        except Exception,e: 
				str1 = str(e)
				print "not open"
				return render(request, "/home/guni/projectname/firstproject/templates/sorry.html", {"wrong" : str1})                      
def typo(request):
		temp = 1

		try:
				if request.POST:

						domain = request.POST['url']

						subprocess.call(['/home/guni/projectname/secondproject/dnstwist.py', domain]) 
						print "gunikhan  sonowal", domain
		######################## Extract the register file ###################
		  
						infile = open("/home/guni/projectname/secondproject/Total_domain.csv", "r")
						reader = csv.reader(infile)
						header = reader.next
						next(infile)
						outfile = open("/home/guni/projectname/secondproject/ip_exist.csv","w")
						writer= csv.writer(outfile)


						for row in reader: 
		        				if 'fuzzer' not in row: 
		        						if row[2] != '':
		        								writer.writerow(row) 
		                        
						outfile.close()

		######################## Extract the domain only  ###################

						f1 = open ("/home/guni/projectname/secondproject/ip_exist.csv","rU") 
						outfile1 = open("/home/guni/projectname/secondproject/out.txt",'w')
						for line in f1:
		    					cells = line.split( "," )
		    
		    					outfile1.write(cells[1]+ '\n')
		    
						outfile1.close()


						my_list = open("/home/guni/projectname/secondproject/out.txt").readlines()
						phonetic = open('/home/guni/projectname/secondproject/phonectic.txt','w')

						for n in my_list:
		    					code = doublemetaphone(n)
		    					if code[1] != None:
		        						n1 = code[0]+code[1]+',' +n
		    					else:
		        						n1 = code[0]+','+n    
		    					phonetic.write(n1)
		    
						phonetic.close()    
						f1.close()   

		#######################Typosqutting domain matching with whitelist#########################

						phoneticfile = open('/home/guni/projectname/secondproject/phonectic.txt','r')
						alexafile = open("/home/guni/projectname/secondproject/shopping_Metaphone.txt","r")
						outfile = open("/home/guni/projectname/firstproject/templates/suggetion1.html","w")
						outfile.write("<html><body><center><marquee>We will suggest you following url which is geniune </marquee><br>Click info for more formation<hr><fieldset style='width:570px'>"+"\n")

						for rowpho in phoneticfile:
		        				rowpho1 = rowpho.split(",")
		        				for rowalex in alexafile:
		                				rowalex1 = rowalex.split(",")
		                				result = normalized_damerau_levenshtein_distance(rowpho1[0], rowalex1[0]) 
		                				result = (1-result) * 100
		                				if result >= 75:
												
		                        				print "hi"
		                        				print result
		                        				print rowalex1[1] 
		                        				outfile.write("<a href ="+'"http://www.'+rowalex1[1] +'"'+ ">"+rowalex1[1]+"</a><br><br>"+"\n")  
		                        				
		                        				temp = 0
		                outfile.close()
		                if temp == 0:
		                		return render(request, "/home/guni/projectname/firstproject/templates/suggetion1.html") 
						        		
		except Exception, e: 
				str1 = str(e)
				return render(request, "/home/guni/projectname/firstproject/templates/sorry.html", {"wrong" : str1}) 
		return render(request, "/home/guni/projectname/firstproject/templates/phishing.html")			
def index(request):
    
        return HttpResponse("<html><body><center>Hello, world. You're at the fristproject index.")

