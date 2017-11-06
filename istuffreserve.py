import json, requests, urlparse, urllib, webbrowser, datetime, time, sys
from lxml import html
from pushbullet import Pushbullet


''' Dr House's Crappy iThingymajig Stock Finder '''

# Seconds to wait between checking
waitTime = 10

# Whether to open the page anyway
forceOpen = False

# Whether to keep running indefinitely
runForever = False

# Whether to ping you
pushBullet = True
pbAPIKey = ''

# Whether to open a local browser or not
openBrowser = True

# The URL to pull availability JSON from
# availabilityURL = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability.json'
availabilityURL = 'https://reserve-prime.apple.com/GB/en_GB/reserve/iPhoneX/availability.json'
# The URL to send the browser to if it finds stock
# reserveURL = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability?channel=1&iPP=E'
reserveURL = 'https://reserve-prime.apple.com/GB/en_GB/reserve/iPhoneX/availability?channel=1&iPP=E&store={}&partNumber={}'

# Check if the JSON has actually changed
updated = ''

# If you're behind a proxy, set it here
proxyDict = {
    'http'  : '',
    'https' : '',
    }

# Set which stores you're willing to go to
chosenStores = {
  'R410': 'London, Stratford City',
  'R245': 'London, Covent Garden',
  'R092': 'London, Regent Street',
  # 'R163': 'London, Brent Cross',
  'R226': 'London, White City',
  # 'R659': 'London, Apple Watch at Selfridges',
  # 'R227': 'Kingston upon Thames, Bentall Centre',
  # 'R527': 'Watford, Watford',
  # 'R242': 'Grays, Lakeside',
  # 'R113': 'Greenhithe, Bluewater',
  # 'R269': 'Milton Keynes, Milton Keynes',
  # 'R176': 'Reading, The Oracle',
  # 'R270': 'Cambridge, Grand Arcade',
  # 'R482': 'Basingstoke, Festival Place',
  }

# Set which SKUs you want
chosenSKUs = {
    'MQAF2B/A': 'iPhone X 256GB Space Grey',
    }

# Pulls the JSON from the server
def getAvailData():
    try:
        resp = requests.get(url=availabilityURL) #, proxies=proxyDict)
        return json.loads(resp.content)
    except Exception:
        time.sleep( waitTime )
        return getAvailData()

def pushMessage( title, url ):
    pb = Pushbullet( pbAPIKey ) #, proxy=proxyDict)
    push = pb.push_link( title, url )

# Now for the fun bit
foundStock = False
while not foundStock or runForever:
    availData = getAvailData()

    if not availData['updated'] == updated:
        updated = availData['updated']
        dt = datetime.datetime.fromtimestamp( float( updated )/1000 )
        print "Last updated at: {}".format( dt.strftime('%Y-%m-%d %H:%M:%S') )

        # Do the needful
        for chosenStore in chosenStores:
            for store in availData['stores']:
                if store == chosenStore:
                    for chosenSKU in chosenSKUs:
                        for SKU in availData['stores'][store]:
                            if SKU == chosenSKU:
                                if ( availData['stores'][store][SKU]['availability']['contract'] == True ) or ( availData['stores'][store][SKU]['availability']['unlocked'] == True ) or forceOpen:
                                    # Awesome, we found one
                                    notification = 'Found {} at {}'.format( chosenSKUs[chosenSKU], chosenStores[chosenStore]  )
                                    # Generate a URL to take you straight to it
                                    url = reserveURL.format( chosenStore, urllib.quote_plus(chosenSKU) )
                                    # Notifications
                                    print notification
                                    if pushBullet:
                                        pushMessage( notification, url )
                                    if openBrowser:
                                        webbrowser.open(url)

                                    foundStock = True

        if not foundStock:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()) + ' - None found, waiting ' + str(waitTime) + ' seconds before trying again'
            time.sleep(waitTime)

    else:
        print 'Availability hasn\'t changed since last run'
        time.sleep(waitTime)
