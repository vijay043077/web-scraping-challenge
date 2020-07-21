# import dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# create app instance
app = Flask(__name__)

# connect to local mongodb
mongo = PyMongo(app, uri ="mongodb://localhost:27017/scrape_mars")

# setup default index
@app.route("/")
def index():
    mars_info = mongo.db.scrape_mars.find_one()
    return render_template("index.html", mars_info = mars_info)

# setup scrape request
@app.route("/scrape")
def scrape_mars():
    mars_info = mongo.db.scrape_mars
    mars_info.replace_one({}, mars_info, upsert = True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)