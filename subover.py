#
# subover.py : A Subdomain Takeover Tool
# Written By : @Ice3man
# Twitter : @ice3man543
# Github : www.github.com/ice3man543
#
# Some Ideas By : 0x94 (thanks buddy)               
#
# (C) Ice3man, 2018-19 All Rights Reserved
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#! /usr/bin/python

import argparse
import time
import json
import Queue
import threading
import sys
import urllib3

queue = Queue.Queue()

try:
    import dns.resolver
except:
    print("error: You need to install dnspython")
    sys.exit(1)

try:
    import colorama
except:
    print("error: You need to install colorama")
    sys.exit(1)

# Set various colors requried throughout the script
g = colorama.Fore.GREEN
y = colorama.Fore.YELLOW
c = colorama.Fore.CYAN
b = colorama.Fore.BLUE
r = colorama.Fore.RED
rs = colorama.Fore.RESET

# Contains the Providers data in json format
providers_data = ""

# global verbosity flag
global_verbosity = False

# Global Output Storage Buffer
output_buffer = ""

# Main DNS Scanning Thread
class ThreadDns(threading.Thread):
    def __init__(self, queue,lock):
        threading.Thread.__init__(self)
        self.queue      = queue
        self.lock       = lock
           
    def run(self):    	
        while not self.queue.empty(): 
            try:
        	   subdomain = self.queue.get()
        	   answer = dns.resolver.query(subdomain, 'CNAME')
        	   for rdata in answer:
                    self.lock.acquire()
                    if global_verbosity==True:
                    	print "[-] Subdomain: " , subdomain  , " CNAME: " , rdata.target
                    self.check_domain_resolve(rdata.target.to_text())
                    self.detect_takeover(rdata.target.to_text(), subdomain)
                    self.lock.release()
            except:
        	   	error="error"

			self.queue.task_done() 

    def check_domain_resolve(self, cname):
        try:
        	dns.resolver.query(cname)
        	return True
        except:
        	return False

    def detect_takeover(self, domain, subdomain):
    	''' Here, we start loading the json providers data and
    		use that data to check for all potential takeovers '''
    	global providers_data
        for provider in providers_data["providers"]:
        	if provider["cname"] in domain:
        		print b, "[",domain,"] Company:", provider["name"], " CNAME:", provider["cname"], " Found On:", subdomain, rs
        		try:
        			urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        			http = urllib3.PoolManager(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'})
        			web_response = http.request('GET', "http://"+subdomain).data.decode('utf-8')
        			for response in provider["response"]:
        				if response in web_response:
        					with self.lock:
        						print g, "[+] Subdomain Takeover Detected : ", subdomain, rs
        						output_buffer = output_buffer + "\n[+] Subdomain Takeover On : " + subdomain
        		except Exception as e:
        			print e

def scan_takeovers(domainlist, threads):
	lock = threading.Lock()

	# Read all targets available in the file
	domainfile = open(domainlist)
	for target in domainfile:
		queue.put(target.strip())

	#spawn a pool of threads, and pass them queue instance 
	for i in range(threads):
		t = ThreadDns(queue, lock)
		t.setDaemon(True)
		t.start()

	#wait on the queue until everything has been processed     
	queue.join()

def main():
	# Argument Parsing
	parser = argparse.ArgumentParser(version='1.0', description="The Best Subdomain Takeover Tool", epilog="Usage : subover.py -l <subdomain_list>.txt -t <num_threads> -o <output_file>.txt")

	parser.add_argument('-l', action='store', dest='targets_list',
                    help='A text file containing list of targets')

	parser.add_argument('-V', action='store_true', default=False,
                    dest='boolean_switch',
                    help='Display Verbose Information')

	parser.add_argument('-t', action='store', dest='num_threads',
                    help='Number of Threads To Use (Default=20)', type=int)

	parser.add_argument('-o', action='store', dest='output_name',
                    help='Name of the output file')

	results = parser.parse_args()

	# Get the target list file and
	# other informations
	target_list_file = results.targets_list
	verbose_settings = results.boolean_switch
	num_threads = results.num_threads
	output_name = results.output_name

	if (target_list_file == None):
		print "\nerror : no valid inputs provided"
		print "for help, try with option -h"
		sys.exit(0)

	# set the global verbosity level 
	global global_verbosity 
	global_verbosity = verbose_settings

	# Output file
	if (output_name == None):
		output_name = None

	# default threads
	if (num_threads == None):
		num_threads = 20

	# Load the providers data 
	f = open("providers.json", "r")
	global providers_data
	providers_data = json.loads(f.read())
	f.close()

	print r + """
             ____        _      ___                 
            / ___| _   _| |__  / _ \__   _____ _ __ 
            \___ \| | | | '_ \| | | \ \ / / _ \ '__|
             ___) | |_| | |_) | |_| |\ V /  __/ |   
            |____/ \__,_|_.__/ \___/  \_/ \___|_|   

            					Take Over Everything :-)""" + rs

	print c + "\n[x] subover : Powerful Subdomain Takeover Tool" + rs
	print c + "[x] Author : @Ice3man (Twitter : @ice3man543)" + rs
	print c + "[x] Github : www.github.com/ice3man543" + rs
	print c + "[x] Version : 1.0" + rs

	print y + "\n[-] Using Target List : " + target_list_file  + rs
	print y + "[-] No of Threads : " + str(num_threads) + "\n" + rs
	
	scan_takeovers(target_list_file, num_threads) 
    
	if (output_name != None):
		with open(output_name, "a+") as outfile:
			outfile.write(output_buffer)

if __name__ == '__main__':
	main()
