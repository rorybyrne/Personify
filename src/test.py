from sys import exit

from generate import markov_generator
from util import bot

user = 'realdonaldtrump'
gen = markov_generator.MarkovGenerator(user, 3, 2)

send_to_twitter = ''
tweet = ''

while send_to_twitter != "y":
    if send_to_twitter == "q":
        exit(0)

    tweet = "%s" % (gen.generate(126))

    print(tweet)
    send_to_twitter = input("Post to Twitter? y/n\nTo quit, type q\n")

tag = input("Tag %s? y/n\n" % user) == "y"

if(tag):
    bot.send_tweet("@" + tweet, user)
else:
    bot.send_tweet(tweet, user)


print("Sent!")
