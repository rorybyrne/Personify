from ronald_brain import generator
from ronald_mouth import bot
from sys import exit

filename = "/home/rory/projects/ronald/data/trump-tweets.csv"
gen = generator.Generator(filename, 3, 2)

tweet = gen.generate(140)
bot.send_tweet(tweet)
