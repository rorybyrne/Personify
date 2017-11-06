from ronald_brain import generator

g = generator.Generator("markhumphrys", 3, 2)

send_to_twitter = ''
tweet = ''

while send_to_twitter != "n":
    if send_to_twitter == "q":
        exit(0)

    tweet = g.generate(140)

    print("\n%s" % tweet)
    send_to_twitter = input("Another? y/n\nTo quit, type q\n")

