from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from django.shortcuts import redirect


pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-4f687960-0529-11e9-989c-8ee1f208b3b7"
pnconfig.publish_key = "pub-c-33b63dec-dfe5-4b83-a2e6-bfdf4fdaabe3"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)


def publish(msg): 
    pubnub.publish().channel('submit_channel').message(msg).sync()
    print(msg)
    print('published')
