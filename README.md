# We_Eat
The Restaurant Recommender for Couples and Friends.  

How much time have you wasted trying to figure out where to eat with your partner or a group of friends?

  "Where should we eat? 
      "I'm cool with anywhere."
        "Me, too.  I'll leave it up to you."

Enough with that.  Use WeEat to save time and eat good.

WeEat learns your tastes, and your partners' tastes, sets up a restaurant profile for the two of you, and offers tailored recommendations, optimized to leave everyone happy!

How does WeEat ensure everyone is happy?  Instead of just taking the restaurant with the highest average score between users, WeEat operates on a principle of minimizing dissatisfaction.  

Imagine the following scenario:

Users | Restaurant A | Restaurant B 
--- | --- | ---
You | 10 | 7 | 
Your friend | 4 | 7

Pretty obvious when it's laid out like this.  Restaurant B optimizes happiness for *both* parties.  But in reality we don't know each other's ratings for every restaurant and you will likely recommend your favorite restaurants first, not knowing how your friend feels about them, and vice versa.  It may take 10 ideas before you land on that 7 and 7.  Or, your friend might just be the nonconfrontational Seattle type who will just go with what you say but end up not enjoying the meal. 

When you add more people, the decisions just get harder and harder.

Users | Restaurant A | Restaurant B | Restaurant C | Restaurant D | Restaurant E
--- | --- | --- | --- | --- | ---
You | 9 | 5 | 1 | 2 | 8 | 6
Friend | 5 | 7 | 10 | 4 | 7 | 3
Friend2 | 2 | 6 | 10 | 9 | 5 | 4
Friend3 | 4 | 8 | 6 | 3 | 9 | 7

Eesh.  Looks like a thirty minute conversation going nowhere.

A restaurant choice can make or break a date night or a brunch gathering with friends.  Don't leave it up to chance, WeEat's got your back.

---
**Data**


Data was compiled from a combination of requests to the Yelp API and scraping reviews online using BeautifulSoup. All data was saved in a MongoDB.
- 621 restaurants (within 1 mile radius of Galvanize)
- 1524 unique users (who had reviewed >1 restaurant in the dataset)
- 5216 reviews


**Methods**


|  Data Collection | Collaborative Filtering Model  |   |   |   | Recommendations  |   |
|---|---|---|---|---|---|---|
| Store restaurant info from Yelp API and scraped reviews in MongoDB  |  Train a collaborative filtering model using Spark ALS | Matrix factorization to get latent restaurant features |  Users take survey to address cold start problem ==> np.linalg.lstsq to get latent user features | Matrix multiplication of latent user features and latent restaurant features to find a user's rating score for every restaurant in the dataset  |  Store user rating matrices in MongoDB |  Sort using principle of minimum dissatisfaction to provide recommendations | Deploy to website using Flask Bootstrap  |


**Evaluation**


One of the most important questions to ask about recommender systems is: how do you know it works?  The model is still in development so it hasn't been officially deployed yet, but I plan to evaluate the quality of the recommendations through a rating system.  Users will be able to provide ratings on restaurants that they actually eat at.  This will not only allow me to evaluate the performance of the model, but the recommendations for users will also improve the more they use the app.

**Next Steps**


Add filters: Vegan/Vegetarian/Gluten-Free/Kids/Dogs/etc
Add features: Cool stats. Weights on walking distance. Brunch/Lunch/Dinner settings. 
Make it mobile and add review capability for users after they actually eat at restaurants.
Connect with social media: FB, dating apps, etc.

---
**Tools and Packages Used**


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





