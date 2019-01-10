
function listen() {
   
    pubnub = new PubNub({
        publishKey : 'pub-c-33b63dec-dfe5-4b83-a2e6-bfdf4fdaabe3',
        subscribeKey : 'sub-c-4f687960-0529-11e9-989c-8ee1f208b3b7'
    })
       
    // function publishSampleMessage() {
    //     console.log("Since we're publishing on subscribe connectEvent, we're sure we'll receive the following publish.");
    //     var publishConfig = {
    //         channel : "submit_channel",
    //         message: { 
    //             title: "greeting",
    //             description: "hello world!"
    //         }
    //     }
    //     pubnub.publish(publishConfig, function(status, response) {
    //         console.log(status, response);
    //     })
    // }

    console.log('Start listening') 
    pubnub.addListener({
        message: function(m) {
            // handle message
            console.log('I have received message: ')
            console.log(m)
            var channelName = m.channel; // The channel for which the message belongs
            var channelGroup = m.subscription; // The channel group or wildcard subscription match (if exists)
            var pubTT = m.timetoken; // Publish timetoken
            var msg = m.message[0]; // The Payload
            var sol_id = m.message[1]
            var publisher = m.publisher; //The Publisher
            console.log(msg)
            var s = '#' + sol_id
            console.log($(s))
            console.log(sol_id)
            $(s).html(msg)
        },
        presence: function(p) {
            
        },
        status: function(s) {
            
        }
    });

    console.log("Subscribing...");
    pubnub.subscribe({
        channels: ['submit_channel'] 
    });
    // publishSampleMessage();
};

listen();
console.log(pubnub)
