import requests # to download page
from bs4 import BeautifulSoup # to parse the contents
import time # to wait until requests
import smtplib, ssl # email capabilities
import os # to import ENV variables

url = os.environ['URL']
wait_time = int(os.environ['WAIT'])
keep_alive = os.environ['KEEP_ALIVE']
destination_email = os.environ['DESTINATION'].split(" ")

#to trick website that we are a real person
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#to trick SINU into giving handsahke
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

sender_email = "atom.automated@gmail.com"
password = "atomPi123456"
port = 465
smtp_server = "smtp.gmail.com"

def sendEmail():
    message = 'The website {} has been recently modified.'.format(url)
    content = 'Subject: {}\n\n{}'.format('Website Activity', message)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, destination_email, content)


def main():
    while True:
        response = requests.get(url, headers=header, verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        soup_hash = hash(soup)
    
        #check if previous hash has been set, init otherwise 
        try:
            prev_hash
        except NameError:
            prev_hash = soup_hash
    
        if soup_hash != prev_hash:
            print('Change detected. Sending email.')
            sendEmail()
            prev_hash = soup_hash
            if keep_alive != 'True':
                break
        else:
            print('No changes detected. Sleeping.')
            time.sleep(wait_time)
            continue

if __name__ == "__main__":
    main()
