
function publish() {
   
    pubnub = new PubNub({
        publishKey : 'pub-c-33b63dec-dfe5-4b83-a2e6-bfdf4fdaabe3',
        subscribeKey : 'sub-c-4f687960-0529-11e9-989c-8ee1f208b3b7'
    })
       
    function publishSampleMessage() {
        console.log("Since we're publishing on subscribe connectEvent, we're sure we'll receive the following publish.");
        var publishConfig = {
            channel : "submit_channel",
            message: { 
                title: "greeting",
                description: "hello world!"
            }
        }
        pubnub.publish(publishConfig, function(status, response) {
            console.log(status, response);
        })
    }
       
    pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
                publishSampleMessage();
            }
        },
        message: function(msg) {
            console.log(msg.message.title);
            console.log(msg.message.description);
        },
        presence: function(presenceEvent) {
            // handle presence
        }
    })      
    console.log("Subscribing..");
    pubnub.subscribe({
        channels: ['hello_world'] 
    });
};


// function change(element, value) {
//     elems = document.getElementsByClassName("waitingSolution")
//     for el in elems:
//         if el.id == element:
//             el.attribute = value
// }