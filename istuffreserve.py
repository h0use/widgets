import json, requests, urlparse, urllib, webbrowser, time

''' Dr House's Crappy iThingymajig Stock Finder '''

# Seconds to wait between checking
waitTime = 10

# The URL to pull availability JSON from
# availabilityURL = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability.json'
availabilityURL = 'https://reserve-prime.apple.com/GB/en_GB/reserve/iPhoneX/availability.json'
# The URL to send the browser to if it finds stock
# reserveURL = 'https://reserve.cdn-apple.com/GB/en_GB/reserve/iPhone/availability?channel=1&iPP=E'
reserveURL = 'https://reserve-prime.apple.com/GB/en_GB/reserve/iPhoneX/availability?channel=1&iPP=E'

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
  'R163': 'London, Brent Cross',
  'R226': 'London, White City',
  'R659': 'London, Apple Watch at Selfridges',
  'R227': 'Kingston upon Thames, Bentall Centre',
  'R527': 'Watford, Watford',
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
def getData():
    resp = requests.get(url=availabilityURL) #, proxies=proxyDict)
    return json.loads(resp.content)

# Now for the fun bit
foundStock = False
while foundStock == False:
    data = getData()

    # Check if the availability file is up yet
    siteUp = False
    while siteUp == False:
        if len(data.keys()) == 0:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()) + ' - No data found, waiting 1 seconds before trying again'
            time.sleep(1)
            data = getData()
        else:
            siteUp = True

    # Do the needful
    for chosenStore in chosenStores:
        for store in data['stores']:
            if store == chosenStore:
                print 'Checking ' + chosenStores[chosenStore]
                for chosenSKU in chosenSKUs:
                    for SKU in data['stores'][store]:
                        if SKU == chosenSKU:
                            print '    ' + 'Checking ' + chosenSKUs[chosenSKU]
                            if data['stores'][store][SKU]['availability']['contract'] == False:
                                # Awesome, we found one
                                print '        Found ' + str( data['stores'][store][SKU]['availability'] )
                                # Generate a URL to take you straight to it
                                url = reserveURL + '&store=' + chosenStore + '&partNumber=' + urllib.quote_plus(chosenSKU)
                                print url
                                # Open that in your default browser
                                webbrowser.open(url)
                                # foundStock = True

    print time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()) + ' - None found, waiting ' + str(waitTime) + ' seconds before trying again'
    time.sleep(waitTime)
