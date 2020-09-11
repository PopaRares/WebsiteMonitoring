import requests # to download page
from bs4 import BeautifulSoup # to parse the contents
import time # to wait until requests
import smtplib # email capabilities
import os # to import ENV variables
import hashlib as hash # to hash website contents

#url = os.environ['URL']
wait_time = int(os.environ['WAIT'])

url = 'https://ac.utcluj.ro/cazare.html'

#to trick website that we are a real person
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

prev_hash = 0
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
while True:
    response = requests.get(url, headers=header, verify=False)
    soup = BeautifulSoup(response.text, "lxml")
    soup_hash = hash.md5(str(soup).encode())
    if prev_hash == 0:
        prev_hash = soup_hash
    if soup_hash != prev_hash:
        print('They be different!')
        #send email
        prev_hash = soup_hash
        break
    else:
        print('They be the same')
        time.sleep(wait_time)
        continue


