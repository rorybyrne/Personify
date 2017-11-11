from ronald_brain import generator
from ronald_mouth import bot
from sys import exit
import ronald_brain.util.constants as c

user = 'realdonaldtrump'
gen = generator.Generator(user, 3, 2)

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
