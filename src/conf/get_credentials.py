import conf.twitter_credentials_hark as hark
import conf.twitter_credentials_ronald as ronald

def get_credentials(user):
    if(user == "realdonaldtrump"):
        return {"c_key": ronald.CONSUMER_KEY,
                "c_secret": ronald.CONSUMER_SECRET,
                "a_key": ronald.ACCESS_KEY,
                "a_secret": ronald.ACCESS_SECRET}
    elif(user == "markhumphrys"):
        return {"c_key": hark.CONSUMER_KEY,
                "c_secret": hark.CONSUMER_SECRET,
                "a_key": hark.ACCESS_KEY,
                "a_secret": hark.ACCESS_SECRET}