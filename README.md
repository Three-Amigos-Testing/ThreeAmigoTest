# ThreeAmigoTest  

This web application takes in websites and tests them against various web application penetration testing algorithms and vulnerabilities, then outputs the results. Simply insert the link in the textbox and hit submit and after scanning a full report of all potential vulnerabilities to appear with code fizes and possible solutions. This web application tests the website based on the Top 10 OWSAP vulnerabilties.  

Steps to use the the application:
  1. Insert link into text box  
     ![Step 1](/assets/step1.JPG)
  3. Hit 'Submit'  
     ![Step 2](/assets/step2.JPG)
  5. Wait for scanning to finish (NOTE: depending on the number of vulnerabilities this may take some time...)  
     ![Step 3](/assets/step3.JPG)
  7. Read the results  
     ![Step 4](/assets/step4.png)  




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

Front End: html, css, js
Backend: python, flask
