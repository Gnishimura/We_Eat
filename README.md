# We_Eat
### The Restaurant Recommender for Couples and Friends.  

How much time have you wasted trying to figure out where to eat with your partner or a group of friends?

>   "Where should we eat?" 

>       "I'm good with anything."

>             "Me, too.  I'll leave it up to you."

Enough with that. WeEat learns your tastes, sets up a restaurant profile you, and offers tailored recommendations that will leave everyone happy!

View the live website here: http://www.we-eat.xyz/

Table of Contents
=================
   * [How It Works](#how-it-works)
   * [Data](#data)
   * [Methods](#methods)
   * [Evaluation](#evaluation)
   * [Next Steps](#next-steps)
   * [Tools and Packages Used](#tools-and-packages-used)


---
### How it works
When you take the survey, WeEat applies your results to its collaborative filtering model and produces your predicted ratings for every restaurant in the database. 

This is accomplished by learning the "latent features" of restaurant and users.  Essentially, latent features reduce the dimensionality of our problem.  Instead of needing to know how each user feels about every one of the 621 restaurants in my dataset (impossible), I was able to reduce the restaurant dataset down to just 10 key features, by which every single restaurant can be described. Then, taking user survey results and Numpy's linalg.lstsq algorithm, I am able to learn the user's latent features.  When I multiply these two matrices together, I am able to get that particular user's predicted ratings for every single restaurant.  This dataframe can be sorted and manipulated to provide all types of recommendations.

During the sorting process, WeEat operates on a principle of minimizing dissatisfaction. Imagine the following scenario:

Users | Restaurant A | Restaurant B 
--- | --- | ---
You | 10 | 7 | 
Your friend | 4 | 7

It seems pretty straightforward when it's laid out like this.  Restaurant B optimizes happiness for *both* parties.  But in reality we don't know each other's ratings for every restaurant and you will likely recommend your favorite restaurants first, not knowing how your friend feels about them, and vice versa.  It may take 10 ideas before you land on that 7 and 7.  Or, your friend might just be the nonconfrontational Seattle type who will just go with what you say but end up not enjoying the meal. 

A restaurant choice can make or break a date night or a brunch gathering with friends.  Don't leave it up to chance, WeEat's got your back.

---
### Data
Data was compiled from a combination of requests to the Yelp API and scraping reviews online using BeautifulSoup. All data was saved in a MongoDB.
- 621 restaurants (within 1 mile radius of Galvanize)
- 1524 unique users (who had reviewed >1 restaurant in the dataset)
- 5216 reviews

---
### Methods

|  Data Collection | Collaborative Filtering Model|   |   |   | Recommend|   |
|---|---|---|---|---|---|---|
| Store restaurant info from Yelp API and scraped reviews in MongoDB  |  Train a collaborative filtering model using Spark ALS | Matrix factorization to get latent restaurant features |  Users take survey to address cold start problem ==> np.linalg.lstsq to get latent user features | Matrix multiplication of latent user features and latent restaurant features to find a user's rating score for every restaurant in the dataset  |  Store user rating matrices in MongoDB |  Sort using principle of minimum dissatisfaction to provide recommendations | Deploy to website using Flask Bootstrap  |

---
### Evaluation
One of the most important questions to ask about recommender systems is: how do you know it works?  The model is still in development so it hasn't been officially deployed yet, but I plan to evaluate the quality of the recommendations through a rating system.  Users will be able to provide ratings on restaurants that they actually eat at.  This will not only allow me to evaluate the performance of the model, but the recommendations for users will also improve the more they use the app.

### Next Steps
* Add filters: Vegan/Vegetarian/Gluten-Free/Kids/Dogs/etc
* Add features: Cool stats. Weights on walking distance. Brunch/Lunch/Dinner settings. 
* Make it mobile and add review capability for users after they actually eat at restaurants.
* Connect with social media: FB, dating apps, etc.
* Explore meaning of latent features in order to improve initial survey
* Make the website pretty


---
### Tools and Packages Used

Stack:
* python
* git
* markdown

Web Scraping:
* requests
* Beautifulsoup
* json

Data Storage:
* MongoDB
* AWS EC2, S3
* pickle

Modeling/Machine Learning
* Spark ALS
* Numpy
* Pandas

Web App:
* Flask
* Bootstrap
* HTML
* CSS





