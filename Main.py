import credentials
import settings
import re
import tweepy
import mysql.connector as mysql
import pandas as pd
from textblob import TextBlob

class MyStreamListener(tweepy.StreamListener):

    def deEmojify(self,text):
        if text:
            return text.encode('ascii', 'ignore').decode('ascii')
        else:
            return None

    def mycheck(self):
        print("--------10000----------")

    def on_status(self, status):
        if status.retweeted:
            return True
        
        id_str = status.id_str
        created_at = status.created_at
        text = self.deEmojify(status.text)    # Pre-processing the text  
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        
        user_created_at = status.user.created_at
        user_location = self.deEmojify(status.user.location)
        #user_description = status.user.description
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None

        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))
        
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "billy7bones",
        database = "demo",
        charset = 'utf8'
        )

        if db.is_connected():
            mycursor = db.cursor()
            mycursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_name = '{0}'
                """.format("Facebook"))
            if mycursor.fetchone()[0] != 1:
                mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
                db.commit()
            mycursor.close()

    
        if db.is_connected():
                mycursor = db.cursor()
                sql = "INSERT INTO {} (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_followers_count, longitude, latitude, retweet_count, favorite_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
                val = (id_str, created_at, text, polarity, subjectivity, user_created_at, user_location, user_followers_count, longitude, latitude, retweet_count, favorite_count)
                mycursor.execute(sql, val)
                db.commit()
                mycursor.close()



    def on_error(self, status_code):
        if status_code==420:
            return False



if __name__ == "__main__":
    auth=tweepy.OAuthHandler(credentials.API_KEY,credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)
    api=tweepy.API(auth)

    myStreamListener=MyStreamListener()
    myStream=tweepy.Stream(auth=api.auth,listener=MyStreamListener())
    myStream.filter(languages=["en"],track=["facebook"])



