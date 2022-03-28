# ThreeAmigoTest  

This web application takes in websites and tests them against various penetration testing algorithms, then outputs the results. Simply insert the link in the textbox and hit submit and after scanning a full report of all potential vulnerabilities to appear. This web application tests the website based on the Top OWSAP vulnerabilties.  

Steps to use the the application:
  1. Insert link into text box
  2. Hit 'Submit'
  3. Wait for scanning to finish
  4. Read the results




NOTE: To run this application the ZAP API key is needed. Follow these steps to install:
     1. First go to https://www.zaproxy.org/download/ and download the appropriate exe file
     2. run the exe file and open the application
     3. goto Tools > Options > API
     4. copy the API KEY.
     5. In the app.py file replace the api key with your own in Line 23
     
Dependencies:
  - Flask
  - json
  - zapv2
  - time
  - pprint
