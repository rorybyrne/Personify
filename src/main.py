from generate import generator
from util import bot

user = 'realdonaldtrump'
gen = generator.Generator(user, 3, 2)

tweet = gen.generate(140)
bot.send_tweet(tweet, user)
