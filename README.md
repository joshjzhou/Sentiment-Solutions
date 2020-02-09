# Sentiment Solutions

A proof-of-concept web application developed by Josh Zhou, Anchey Peng, Saif Ali, and Akshana Dassanaike for the Hack the Ram competition.

Sentiment Solutions was designed to give companies/people insight into how their employees/friends may be doing by analyzing the sentiment of their tweets. Through the use of a Naive Bayes algorithm, we trained a classification model that could classify text as either 1 (positive) or 0 (negative) with roughly 80% accuracy. From there, we developed a Flask app that would allow users to login to their twitter accounts and see the average sentiment score of all their friends' (follows them and they follow) last 15 tweets. It also allows the user to send a direct message from the site to friends that may be at risk. You can check out a demo here: [https://sentiment-solutions.herokuapp.com/](https://sentiment-solutions.herokuapp.com/)

## Getting Started

Download the repository

```
git clone
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
