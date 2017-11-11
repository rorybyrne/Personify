from ronald_brain import generator
from ronald_mouth import bot
from sys import exit

user = 'realdonaldtrump'
gen = generator.Generator(user, 3, 2)

tweet = gen.generate(140)
bot.send_tweet(tweet, user)
