from flask import Flask, request, jsonify, render_template, abort, redirect, url_for
from flask_caching import Cache
import time
from pprint import pprint
from zapv2 import ZAPv2
import json

config = {
    "DEBUG": False,             # some Flask specific configs
    "CACHE_TYPE": "simple",     # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1
}

app = Flask(__name__)
app.config.from_mapping(config) #set app with configurations
cache = Cache(app)              #create cache instance for app

def zap(url):
  print("starting zap")
  # A helpful reference: https://github.com/zaproxy/zaproxy/wiki/ApiPython
  
  # The value of api must match api.key when running the daemon
  apikey = "uhot4eld0nvar4c5grjoum9gq9"

  target = url

  zap = ZAPv2(apikey=apikey)
  # Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
  # zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

  # Proxy a request to the target so that ZAP has something to deal with
  print('Accessing target {}'.format(target))
  zap.urlopen(target)
  # Give the sites tree a chance to get updated
  time.sleep(2)

  print('Spidering target {}'.format(target))
  scanid = zap.spider.scan(target)
  # Give the Spider a chance to start
  time.sleep(2)
  
  while (int(zap.spider.status(scanid)) < 100):
      # Loop until the spider has finished
      print('Spider progress %: {}'.format(zap.spider.status(scanid)))
      time.sleep(2)

  print ('Spider completed')

  while (int(zap.pscan.records_to_scan) > 0):
        print ('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
        time.sleep(2)

  print ('Passive Scan completed')

  print ('Active Scanning target {}'.format(target))
  scanid = zap.ascan.scan(target)
  while (int(zap.ascan.status(scanid)) < 100):
      # Loop until the scanner has finished
      print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
      time.sleep(5)

  print ('Active Scan completed')

  # Report the results

  print ('Hosts: {}'.format(', '.join(zap.core.hosts)))
  print ('Alerts: ')
  pprint (zap.core.alerts())

  f = open("output.txt", "w")
  f.write(zap.core.alerts())
  f.close()
  return redirect(url_for('results'))



@app.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    ## recieve input from text box
    zap('https://google-gruyere.appspot.com/526435151700772202118564821480864815257/')
    return "<p> Scanning in Progress...<p>"
  return render_template('index.html')

@app.route("/results")
def results():
  ##parse through json
  ## creates string 
  ## output string on page
  return 'hi'

if __name__ == "__main__":
  app.run(debug=True)


