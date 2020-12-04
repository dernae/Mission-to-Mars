from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#set up Flask:
app = Flask(__name__)

#tell Python how to connect to Mongo using PyMongo.
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#setting up two flask routes: one for the main HTML page everyone will view when visiting the web app,
#  and one to actually scrape new data using the code we've written.

#define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#set up our scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   #add an empty JSON object 
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Now that we've gathered new data, we need to update the database using .update()
#.update(query_parameter, data, options)

#tell Flask to run
if __name__ == "__main__":
   app.run()