from generate import markov_generator
from util import bot

user = 'realdonaldtrump'
gen = markov_generator.MarkovGenerator(user, 3, 2)

tweet = gen.generate(140)
bot.send_tweet(tweet, user)
