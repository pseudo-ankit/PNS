<p align="center">
  <a href="https://cdn.jim-nielsen.com/ios/512/opera-news-personalized-news-2019-07-23.png">
    <img src="NewsApp/static/personalized-news.jpg" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">Personalized-News-System</h3>

  <p align="center">
    A personalized news system powered by hybrid recommender system.
    <br />
  </p>
</p>


## Table of Contents

* [About the Project](#about-the-project)
  - [Built With](#built-with)
  - [Domain Study](#domain-study)
* [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Setup](#setup)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This is a web based [hybrid recommender system](https://en.wikipedia.org/wiki/Recommender_system#Hybrid_recommender_systems) for recommending news articles. It recommends news articles to user according to user's interest(using [content-based filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering)) and also incorporates popularity of the article(using [popularity-based filtering](https://medium.com/@madasamy/introduction-to-recommendation-systems-and-how-to-design-recommendation-system-that-resembling-the-9ac167e30e95)).

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Bootstrap](https://getbootstrap.com)
* [Twitter API](https://developer.twitter.com/en/docs)
* [News API](newsapi.org/)

### Domain Study
* In domain of recommender systems a commonly faced problem is the [Cold Start Problem](https://en.wikipedia.org/wiki/Cold_start_(recommender_systems)).
* In case of news recommendation it is even more persistent.
* Also in case of news recommendation **novelty of data** is very important.
* And we need to incorporate the **user interest** as well.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

What things you need to install the software and how to install them
```bash
# Clone this repository
$ git clone https://github.com/pseudo-ankit/PNS.git

# Go into the repository
$ cd PNS

# Install dependencies
$ pip install -r requirements.txt

# Downloading nltk stopwords and punctuations
$ nltk.download('punkt')

$ nltk.download('stopwords')

$ nltk.download('wordnet')
```
After cloning the repo the file structure should be like below.
```bash
$ ls
```
```
PNS
│   README.md
│   requirements.txt
|   setting.py
│
└───DataCollection
│   │   NewsCategories.py
|   |   Top_Headlines.py
│   │   TwitterHandles.py
|   |   TwitterPublicTimeline.py
|   |   collect_data.py
|   |   get_article_pop_score.py
|   |   get_article_profile.py
|   |   handles.json
|   |   init_handles_json.py
|   |   setting.py
│   │
│   └───Data
│       |
|       |
|
└───NewsApp
    │   __init__.py
    │   app.py
    |   config.py
    |   forms.py
    |   init_last_used_csv.py
    |   last_used_csv.json
    |   models.py
    |   setting.py
    |   stream_to_db.py
    |   views.py
    |   .flaskenv
    └───static
    └───tamplates
```

### Setup

* Get your API keys for [Twitter API](https://developer.twitter.com/en/docs) and [News API](newsapi.org/).
* Put them in **credentials.py**(inside DataCollection).
```bash
$ PSN/DataCollection/credentials.py
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret  = 'YOUR_TWITTER_SECRET_KEY'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SCERET'
news_api_key =  'YOUR_NEWS_API'
```

* Also place your [DataBase URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) key in **config.py**(inside NewsApp).

Now follow below steps to setup on your local machine.

Inside the DataCollection directory run below scripts.
```bash
$ cd PSN/NewsApp/

# Initialising handles.json file
$ python init_handles_json.py

# Collecting the data
$ python collect_data.py
```

Now inside the NewsApp directory run below scripts

```bash
$ flask run
```
After running the above command your flask server should be up and running. Now navigate to [http://127.0.0.1:5000/](#) in your browser. You will be redirected to login/signup page.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: NewsApp/static/screenshot.png
