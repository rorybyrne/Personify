from generate import generator

g = generator.Generator("realdonaldtrump", 2, 2)
print('')

send_to_twitter = ''
tweet = ''

while send_to_twitter != "n":
    if send_to_twitter == "q":
        exit(0)

    tweet = g.generate(140)

    print("%s" % tweet)
    send_to_twitter = input("Another? y/n\nTo quit, type q\n")

