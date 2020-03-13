import praw
import os
import requests
import time
from xml.etree import ElementTree

previousOperatingStatus = None
previousDateStatusPosted = None

def make_post(r, root):
    print("Making post...")
    appliesTo = root.find("AppliesTo").text
    shortStatusMessage = root.find("ShortStatusMessage").text
    longStatusMessage = root.find("LongStatusMessage").text
    extendedInformation = root.find("ExtendedInformation").text
    dateStatusPosted = root.find("DateStatusPosted").text
    disclaimer = "Disclaimer: I am a bot. This may not be the most accurate or up-to-date information! See for yourself here: https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/"
    title = "OPM Status for " + appliesTo + " | " + shortStatusMessage
    text = longStatusMessage + "\n\n" + extendedInformation + "\n\n" + dateStatusPosted + "\n\n" + disclaimer
    print("Post title: ", title)
    print("Post text: ", text)
    subreddit = r.subreddit('washingtondc')
    r.submit(subreddit, title, text)

def posting_logic(xmlfile):
    #print("Checking post logic...")
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()
    operatingStatus = root.find("OperatingStatus").text
    dateStatusPosted = root.find("DateStatusPosted").text
    #print("operatingStatus: ", operatingStatus)
    #print("dateStatusPosted: ", dateStatusPosted)
    global previousOperatingStatus
    global previousDateStatusPosted
    #print("previousOperatingStatus: ", previousOperatingStatus)
    #print("previousDateStatusPosted: ", previousDateStatusPosted)
    if (operatingStatus != "Open") and ((dateStatusPosted != previousDateStatusPosted) or (operatingStatus != previousOperatingStatus)):
        print("Make a post!")
        previousOperatingStatus = operatingStatus
        previousDateStatusPosted = dateStatusPosted
        return root, True
    else:
        #print("Don't make a post!")
        previousOperatingStatus = operatingStatus
        previousDateStatusPosted = dateStatusPosted
        return root, False

def run_bot():
    print ("Running bot...")
    while True:
        try:
            url = "https://www.opm.gov/xml/operatingstatus.xml"
            request = requests.get(url)
            #print("Making OPM status request...")
            if (request.status_code == 200):
                #print("Good request! Status code 200.")
                with open('status.xml', 'wb') as f: 
                	f.write(request.content)
                root, flag = posting_logic('status.xml')
                if (flag):
                    r = bot_login()
                    print(r.user.me())
                    print ("Logged in!")
                    make_post(r, root)
            else:
                print("Bad request!")
            time.sleep(60)
        except Exception as e:
                print (str(e.__class__.__name__) + ": " + str(e))
                time.sleep(60)

def bot_login():
    print ("Logging in...")
    from credentials import username, password, client_id, client_secret, user_agent
    r = praw.Reddit(username = username,
		password = password,
		client_id = client_id,
		client_secret = client_secret,
		user_agent = "test")
    return r

if __name__ == "__main__":
    while True:
        try:
            run_bot()

        except Exception as e:
            print (str(e.__class__.__name__) + ": " + str(e))
            time.sleep(60)