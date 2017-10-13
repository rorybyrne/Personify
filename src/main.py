from ronald_brain import generator
from ronald_mouth import bot
from sys import exit
import csv
import io

filename = "donald_tweets.csv"


n = 3
gen = generator.Generator(filename, n)

send_to_twitter = ''
tweet = ''

while send_to_twitter != "y":
    if send_to_twitter == "q":
        exit(0)

    tweet = gen.generate(20)

    print(tweet)
    send_to_twitter = input("Post to Twitter? y/n\nTo quit, type q\n")

bot.send_tweet(tweet)
print("Sent!")



