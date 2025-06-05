# LLM-using-google-API-s

# Introduction 

This project focuses on implementation of multimodal LLM using google APIs. The main goal is to 
leverage Google's advanced machine learning and AI capabilities to receive audio input from the 
user and transcribe it to text and provide sentiment analysis on it. By integrating the Google cloud 
platform services, the project aims to explore the features and working of Google cloud’s 
multimodal LLM APIs. The Key features include seamless real-time conversion of an input audio to 
transcribed text and provide the sentiment of the audio. This implementation showcases the 
potential for enhancing accessibility, automation, and communication in modern technology 
solutions.

# Architecture
![Archi](https://github.com/8LuLzSeC8/LLM-using-google-API-s/blob/c39eaab721ee9529b2be95012fd5974e13c87b45/archi.png)

**User Interface:** The user interface of the project application is a standard HTML landing page which 
send GET and POST requests to upload or retrieve data. This HTML page is rendered through a 
backend flask application. The users can use the recorder to input audio to be transcribed into text 
and get the sentiment of the audio analysed. The output is generated below the input block. The 
users can hit the transcription button to see the output and sentiment of their audio.

**Application Backend:** The backend of the application is a built-on Flask which is a python 
development framework. It helps handle the requests coming from the front end of the application, 
In our case the HTML page. The Flask application contains all the libraries and code required to 
implement and integrate the data flow between the APIs and the User interface. 
The backend application catches the users GET or POST requests to retrieve and upload data 
to/from the directory folders or to trigger the Google Cloud APIs to transcribe the input data.  
The authentication required to access or call the APIs from the Google Cloud Platform is 
configured in the application using the “os” library in python.

**Google Cloud Platform:** The audio input prompts the gen-ai google API to take the default prompt 
setup in the code to get the transcription and sentiment of the input. The API returns the 
transcription and sentiment in text format which is sent to the user interface. 

**Database/Storage:** The data for this application is stored as text or audio files. The input and 
generated output files are stored in the folders created in the project directory.

# Configuration 
**serv_account.json** – this file is the service account authentication key for google cloud 
services. The following code links the credentials in app.py

**Dockerfile** – This file is used to create a docker image which is used to create a container to 
deploy the application in a host service. The app working directory or the location of the app 
in the server is specified in this file.

**Requirements.txt** – This file is used to mention the dependencies for the project. It is used 
by Dockerfile to setup the container with required dependencies in the deployment phase. 

**Storage** - The data and files generated are stored in folders created inside the project directory. The following 
code is used in app.py to create the folders.

# Pros and Cons 

**Pros:** It is a simple and easy to navigate application. The is no complex interface, the outputs for the 
given input are generated right below the input forms can be easily accessed. 

**Cons:** the application is a basic implementation to call the API requests. It cannot scale flexibly 
with the increase in users or multiple requests at a time. And the storage for this project is just the 
folders in the project directory which may cause issues in case large amounts of data is generated. 

# Problems encountered and Solutions 

Some of the issues encountered while building the project is the authentication with the google 
cloud services. Though the request calls from application were working fine in the local 
environment, when deployed to the host the request was throwing a permission error from google 
cloud service. Later, this issue was solved as the authentication key was probably expired and 
needed to be generated again to successfully deploy the application.

# Lessons learned 

- How to use google cloud services and implement multi-model LLMs using the google APIs 
 and Cloud Run to deploy than application.
- How to tackle deployment issues using the build logs in the google console.
- Integrating APIs into a flask application.
- Setting up google authentication using python.
