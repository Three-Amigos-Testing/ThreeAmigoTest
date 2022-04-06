from flask import Flask, request, jsonify, render_template, abort, redirect, url_for, session
from flask_caching import Cache
import time
from pprint import pprint
from zapv2 import ZAPv2
import json
import json2table

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

config = {
    "DEBUG": False,             # some Flask specific configs
    "CACHE_TYPE": "simple",     # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1
}

app = Flask(__name__)
app.config.from_mapping(config) #set app with configurations
cache = Cache(app)              #create cache instance for app
app.secret_key = 'ThreeAmigos'

global TARGET_WEBSITE

time_ran = ""

def zap(url):
  print("starting zap")
  # A helpful reference: https://github.com/zaproxy/zaproxy/wiki/ApiPython
  
  # The value of api must match api.key when running the daemon
  apikey = "#insert the api key"

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
  # print(type(zap.core.alerts()))
  f = open("output.json", "w")
  f.write(json.dumps(zap.core.alerts()))
  f.close()
  
  
#main route to ask for input
@app.route("/", methods=['GET','POST'])
def index():
  if request.method == 'POST':
    session['target'] = request.form['text']
    ## recieve input from text box    
    return render_template('loading.html')
  return render_template('index.html')

#this route is used to run the tests on the website
@app.route("/scanning")
def scanning():
  start = time.time()
  zap(session['target'])
  done = time.time()
  session['elapsed'] = str(done - start)
  print( session['elapsed'])
  
  return 'elapsed'

#this route will parse the results and output it to the page
@app.route("/results")
def results():
  ##parse through json
  ## creates string 
  ## output string on page
  f = open('output.json')
  infoFromJson = json.load(f)
  
  above = ''' <!DOCTYPE html>
              <html lang="en">
              <script> window.alert = function() {{}};</script>
              <head>
                <meta charset="UTF-8">
                <meta content="IE=edge" http-equiv="X-UA-Compatible">
                <meta content="width=device-width,initial-scale=1" name="viewport">
                <meta content="description" name="description">
                <meta name="google" content="notranslate" />
                
                <style>
                  .body{
                    background-color: #b61924;
                  }
                  .inside {
                  position: absolute;
                  bottom: 0;
              }
                
                </style>
                <!-- Disable tap highlight on IE -->
                <meta name="msapplication-tap-highlight" content="no">
                
                <link rel="apple-touch-icon" sizes="180x180" href="./assets/apple-icon-180x180.png">
                <link href="./assets/favicon.ico" rel="icon">
                <title>Three Amigos </title>  


              <link href="/static/css/bootstrap.min.css" rel="stylesheet">


              </head>

              <body style="background-color: white;">

                  
              <!-- Add your content of header -->

              <!-- Navigation -->
              <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                  <div class="container">
                    <a class="navbar-brand" href="#">
                      <img src="/static/img/sample.png" alt="..." height="40"> Three Amigos
                    </a>
                    
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                      <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                      <ul class="navbar-nav ms-auto">                     
                      
                      </ul>
                    </div>
                  </div>
                </nav>
            '''
  code =  str(session['elapsed'])

  print(code)

  heading = '<h1 style="text-align:center; "> Results from Three Amigos Testing </h1> <br> <p style="text-align: center;"> Time it took to scan: %s seconds</p> ' % code 
  table = '<style>table, th, td {  border: 1px solid; margin:auto; width: 60%} table{border: 3px solid}</style>'

  below = ''' <!--Bootsstrap 5.1.0 -->
              <script type="text/javascript" src="/static/js/bootstrap.bundle.min.js"></script>
              <script type="text/javascript" src="/static/js/bootstrap.bundle.min.js"></script>
                  
                  
              </body>


              <footer style="margin-top: 20px;" class="bg-dark text-center text-lg-start ">
                <!-- Copyright -->
                <div class="text-center p-3" style="color: antiquewhite;">
                  Copyright © 2022 Three Amigos. All Rights Reserved.
                  
                </div>
                <!-- Copyright -->
              </footer>

              </html>
          '''
  for x in infoFromJson:
    table += "<br>"+ json2table.convert(x)

  table.replace("alert","alrt")
  return str(above+heading+table+below)


if __name__ == "__main__":
  app.run()


