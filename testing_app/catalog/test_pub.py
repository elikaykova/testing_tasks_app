# from pubnub.callbacks import SubscribeCallback
# from pubnub.enums import PNStatusCategory
# from pubnub.pnconfiguration import PNConfiguration
# from pubnub.pubnub import PubNub
 
# pnconfig = PNConfiguration()
 
# pnconfig.subscribe_key = "sub-c-4f687960-0529-11e9-989c-8ee1f208b3b7"
# pnconfig.publish_key = "pub-c-33b63dec-dfe5-4b83-a2e6-bfdf4fdaabe3"
 
# pubnub = PubNub(pnconfig)
 
 
# def my_publish_callback(envelope, status):
#     # Check whether request successfully completed or not
#     if not status.is_error():
#         pass  # Message successfully published to specified channel.
#     else:
#         pass  # Handle message publish error. Check 'category' property to find out possible issue
#         # because of which request did fail.
#         # Request can be resent using: [status retry];
 
 
# class MySubscribeCallback(SubscribeCallback):
#     def presence(self, pubnub, presence):
#         pass  # handle incoming presence data
 
#     def status(self, pubnub, status):
#         if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
#             pass  # This event happens when radio / connectivity is lost
 
#         elif status.category == PNStatusCategory.PNConnectedCategory:
#             # Connect event. You can do stuff like publish, and know you'll get it.
#             # Or just use the connected event to confirm you are subscribed for
#             # UI / internal notifications, etc
#             pubnub.publish().channel("submit_channel").message("hello!!").pn_async(my_publish_callback)
#         elif status.category == PNStatusCategory.PNReconnectedCategory:
#             pass
#             # Happens as part of our regular operation. This event happens when
#             # radio / connectivity is lost, then regained.
#         elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
#             pass
#             # Handle message decryption error. Probably client configured to
#             # encrypt messages and on live data feed it received plain text.
 
#     def message(self, pubnub, message):
#         msg = message.message
#         print("Got: {}".format(msg))
 
 
# pubnub.add_listener(MySubscribeCallback())
# pubnub.subscribe().channels('submit_channel').execute()

# pubnub.publish().channel("submit_channel").message(["helloooooo!!"]).pn_async(my_publish_callback)