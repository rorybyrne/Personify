from ronald_brain import generator
from ronald_mouth import bot
from sys import exit

filename = "/home/rory/projects/ronald/data/trump-tweets.csv"
gen = generator.Generator(filename, 3, 2)

send_to_twitter = ''
tweet = ''

while send_to_twitter != "y":
    if send_to_twitter == "q":
        exit(0)

    tweet = gen.generate(140)

    print("\n%s" % tweet)
    send_to_twitter = input("Post to Twitter? y/n\nTo quit, type q\n")

bot.send_tweet(tweet)
print("Sent!")
