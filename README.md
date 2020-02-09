# Sentiment Solutions

A proof-of-concept web application developed by Josh Zhou, Anchey Peng, Saif Ali, and Akshana Dassanaike for the Hack the Ram hackathon.

Sentiment Solutions was designed to give companies/people insight into how their employees/friends may be doing by analyzing the sentiment of their tweets. Through the use of a Naive Bayes algorithm, we trained a classification model that could classify text as either 1 (positive) or 0 (negative) with roughly 80% accuracy. From there, we developed a Flask app that would allow users to login to their twitter accounts and see the average sentiment score of all their friends' (follows them and they follow) last 15 tweets. It also allows the user to send a direct message from the site to friends that may be at risk. You can check out a demo here: [https://sentiment-solutions.herokuapp.com/](https://sentiment-solutions.herokuapp.com/)

By no means is this project complete or fully functional, and it should not be used in anyways to diagnose mental health disorders or spread hate.

<img width="960" alt="Capture" src="https://user-images.githubusercontent.com/32548076/74111832-754d4600-4b65-11ea-84ae-31cb63376075.PNG">
What the application looks like after you login *Changed friend information for privacy purposes*

## Getting Started

Clone or download the repository

```
git clone https://github.com/joshjzhou/sentiment-solutions.git
```

### Installing

Install dependencies
```
pip install -r requirements.txt
```
## Twitter Keys

Go to [https://developer.twitter.com/](https://developer.twitter.com/) and register an app to get the consumer key and consumer secret key. You will also need to set the callback url for the application (if you are using flask, it should be http://127.0.0.1:5000/callback). Once you have the keys, go to app.py and change the values of consumer_key and consumer_secret_key (lines 38-39).

## Run the application

Navigate to folder and run
```
python app.py
```
in your terminal

## Demo Usage and Possible Errors

When using the demo, [https://sentiment-solutions.herokuapp.com/](https://sentiment-solutions.herokuapp.com/), please note that the Twitter API only allows a certain number of calls to be made in a certain time frame (read more about it [here](https://blog.twitter.com/en_us/a/2008/what-does-rate-limit-exceeded-mean-updated.html)). Because of this, accounts with large number of folllowers/people following will exceed the rate limit and crash the application. Also, repeated requests and refreshes will crash the application as well. Additionally, any firewalls or restrictions set up on your internet may also crash the application (hinders the OAuth process), so it is recommended that when you use the demo to use a VPN.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Twitter API](https://developer.twitter.com/en/docs) - Get user data
* [Bootstrap](https://getbootstrap.com/) - Front-end library used to design website

