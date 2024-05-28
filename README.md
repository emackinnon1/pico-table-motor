# pico-table-motor
A raspberry pi pico that powers a couple of linear actuators attached to a table hinge using an MQTT server to send and receive messages.


![20240528_084158-ezgif com-optimize](https://github.com/emackinnon1/pico-table-motor/assets/49004020/ae06bcd8-f7e9-4cbe-8672-15942d747368)

[video](https://photos.google.com/share/AF1QipOxRTt1fZprU7FDNkr2YeoZxs5IqVx5rKe-qXA9ltJ0vuCPGBfnsxae41Ng3UkEgA?key=bEtFODZ1ZkVuVEs3YWlqcHM2YlJTelRWT1RiMEpR)


## Explanation of project
I will go ahead and tell you right now: This is a totally unnecessary project.  
This project is built using a coffee table that has a hinged that works _just fine_ when opened manually, as the manufacturer intended. When I wired everything up, put the final pieces together, and ran it successfully for the first time to show my girlfriend, the first words out of my mouth upon it completing the opening and closing movements were: "Pretty pointless, huh?"  
That being said, this was fun to build and it does actually make for a cool party trick when people are over. I used this in conjunction with Home Assistant and running a Mosquitto server, but you could still make this work if you have an alternative MQTT set up.

The list of supplies you will need are:
One of these coffee tables with a similar hinge type:
[Amazon has many of them](https://www.amazon.com/WLIVE-Compartment-Adjustable-Storage-Tabletop/dp/B084ZH1LYN/ref=sr_1_5?crid=5P9PBM8AS2RC&dib=eyJ2IjoiMSJ9.QP0Wr3yhdWK-O9EmXHmrSCHlWGZXnfk5IVOXPG5sAc-JEvmLHho3q2Cc-nKfStqA-UZ4J2xyNIWStKfbYQ3T_G-ighAq5isxhPtRcMUBQPCuSdKSkuoHHQfmFMzrPkRhSS1Ftrx0k4zJGXwNIzit7JsBY3apqz7Y7LDI-PZmnh4wciaZVCy9tOh4KIXbiTXtE1fPlNKU8DdVmpa2tzSTu2i-O1Fct7mhBWQs3M_BcDrY-cRMZP7d2Kox8XPwuIxLwyuMPctrc4_FpTBjXFs5LByFAd7zul3tfbWFhxg8SH0.z8FR5_8iPUGp_aSoKt8MAozwXIaweSCMwF5p_9Yw_7Y&dib_tag=se&keywords=coffee+table+with+lifting+top&qid=1716911642&sprefix=coffee+table+with+%2Caps%2C159&sr=8-5)

Linear actuators:
I used the [4 inch version](https://www.amazon.com/gp/product/B00NM8H6VS/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1), which I think will fit most of these tables

A couple of diodes:
Also available on [Amazon](https://www.amazon.com/gp/product/B07BTKVRG8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

Adafruit DRV8871 DC Motor Driver Breakout Board:
[Amazon link](https://www.amazon.com/gp/product/B06Y4VRXN4/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

Raspberry pi pico:
[Amazon link](https://www.amazon.com/waveshare-Pico-Microcontroller-Development-High-Performance/dp/B08TVF499B/ref=sr_1_2_sspa?crid=2GTA0EB54NWS5&dib=eyJ2IjoiMSJ9.aV3crTctFWgEgyr786MZFsERvsvm9gN0kfVFjMQJ2w4Oy7-KyZ6eJ6Txnx_2uvRYGMq4LSl_rTz_VjXYyHuJ5MI8mITybLGsDreL2kXhIl2zjd_8V3_3tnVhgWsz1BdlT9Rx-rSgnKtNBOrpaJl4a6TB15Aciunp96GrHxGJA091Xwnu3E8inrM22j22YZWH1xNhz0XKscyVfvobA6eyQTe5BC5P_bhRSmWlKavomQ6qNTQpYH2MxW1JcxtntM1vbz1epW-WV0EzbesW_OQBrW6bg-vFGC5H-hoKqmRodyU.WFFwS5RM-73vJEs37lQcGHrs44jUIbJ03hyZ8YQ9JM8&dib_tag=se&keywords=raspberry+pi+pico&qid=1716912038&s=electronics&sprefix=raspberry+pi+pico%2Celectronics%2C165&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)

Limit switches:
[Amazon link](https://www.amazon.com/HiLetgo-KW12-3-Roller-Switch-Normally/dp/B07X142VGC/ref=sr_1_3?dib=eyJ2IjoiMSJ9.FPAndwd916JYq_epoDDZGt1UkKnKuCz2JwJC7vKB9bfr7XFP5tuGhxiMFKyzOBHkM84pkE7EJTQwqpN_WdhKAvNC5UOXbREGlXfUAHBeSoA12h1_qXVwjs2mc7c9I0u6iu8cGsmybnKx1op-O3UetE3Y0xmni6kPxp2PV5nYx31uilhjYzA65zcc10zDP7rOp6689DvpZ_vjbNauazt7g-SYnqhOf6M-7W7-pK3N0o0.lBSatlHIkgBmWPLdE_Z5e1MQiCVrEfvln3GQhbWAy7Y&dib_tag=se&keywords=limit+switches&qid=1716912102&sr=8-3)
You'll also need some small bolts to attach these to the table. I went to my local hardware store for these.

Power supply:
I used a [12v 5a supply](https://www.amazon.com/gp/product/B07L4LNSJV/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).

You will also need something to attach the linear actuators to the hinge. This was the hardest part to figure out for me. I ended up getting a few supplies to drill a hole in the arm of the table hinge in order to run a bolt through the whole of the actuator. To reduce the wiggle that you get when you do this, I used some plastic spacers. Hopefully this is clearer in the pictures when you see them. There may be better ways to do this, it was the best idea that I came up with, though.

Plastic spacers:
[Amazon link](https://www.amazon.com/gp/product/B0BYPHB7D5/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&th=1)

Countersink bolts (the countersunk nut fit the linear actuator through hole perfectly; also used to attache the bottom brackets of the actuator to the table):
[Amazon link](https://www.amazon.com/gp/product/B08NBXVW98/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&th=1)

1/4 to 1-3/8 Inches HSS Step Drill Bit for drilling holes in metal, among other materials:
[Amazon link](https://www.amazon.com/gp/product/B0995NNB7F/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1)


## Methods of the Madness
### Attaching the actuator
I unfortunately did not remember to take many photos during the building process, but the finished product photos will hopefully suffice. The other thing that I wish I had done is to build this at the same time as I was putting the table together. It is not the end of the world if you build the table and then later come back and put the motors on, but it sure would have been easier if I could have done it all at once.
The hardest part of this project was figuring out just how to attach the linear actuators. For quite some time, I tested the actuators without actually drilling any holes or attaching the brackets that come with them to any part of the table; I wanted to see if the stroke length would match up well enough to the arms on the hinge to just attach them to one spot and not have to do anything extra. There are little hydraulic pistons that attach to posts on the hinge that I thought I could co-opt, but unfortunately that didn't work.  
![Screenshot 2024-05-28 at 10 22 17](https://github.com/emackinnon1/pico-table-motor/assets/49004020/f0a8af54-10cc-4e1e-be6b-d5beed25bfca)  
However, I knew that if I could attach the end of the actuator to the right spot and then have some way of shutting off power to the actuator once the table reached the right position, this was a doable project!


It is a good idea to power the linear actuator all the way out to the end of its length and use that to figure out where to attach the bottom bracket table's bottom floor in the inner compartment, along with where on the hinge arm you need to attach the end of the actuator  
![20240528_101628](https://github.com/emackinnon1/pico-table-motor/assets/49004020/5e989384-09be-4670-a2e2-0e5b6cd3976e)  
In the picture above, the actuator is a little less than fully extended (just enough to give myself a couple of centimeters of extra room, but the distance doesn't matter all that much). At this point, the other thing that you will want to do is to be absolutely _sure_ that once you retract the actuator, the hinge will be fully closed. The bottom bracket (which comes with the actuator usually) was easy to mark the outline of using chalk. You will want to be sure that you don't put it too close to the compartment wall. I also marked off where the top of the actuator should attach via the through hole with a white paint marker on the actual hinge. Another thing I did (because I did all of this _after_ the table was built) was to take the top table part off of the hinges to make things easier to measure and work with. Otherwise you cannot measure where the retracted actuator should be positioned with the hinge all the way closed. I cannot stress enough that you should measure, test, remeasure, and test again as many times as possible until you are absolutely certain you have both the bottom bracket and the top through hole measured to the right spots on the bottom of the table compartment and the hinge arm respectively; it'll make your life way easier if you aren't doing this on the fly later.  

Once you figure out where the actuator needs to be positioned, it's time to start drilling the holes. There isn't too much that is special about the bottom bracket. The countersink screws worked pretty well for attaching this as well. For the hinge arm, I took the hole thing off the table and drilled through it, being extra careful to make the hole as centered as possible. I went slow and constantly checked to be sure the hole didn't get too big for the screw. These tables aren't crazy expensive, but I wanted to not have to start over if I ruined it.  

Since the end of the linear actuator needs to physically be a little apart from the hinge arm, you will have to get the correctly-sized spacer. I had to cut mine to the right size.  
![20240528_101635](https://github.com/emackinnon1/pico-table-motor/assets/49004020/4e61e9e1-263e-49a2-a783-98a19c92163e)

You will want to pick out the right spacer or cut it to size as needed.

After everything is attached, we can move on to getting the limit switches, drivers, power, etc all wired up and the code uploaded to the pico!

### Wiring
![motor-controller drawio](https://github.com/emackinnon1/pico-table-motor/assets/49004020/e0951f14-086b-410d-ae31-89a1590b5368)
![20240528_084543](https://github.com/emackinnon1/pico-table-motor/assets/49004020/405705ab-569e-403e-9d91-0cd942631011)

All in all, this isn't that complicated of a wiring job. You need to connect the correct pins on the pico to the motor drivers, split the power from the power supply and run it to the power inputs of the motor driver, then run the motor outputs from the drivers to the limit switches and subsequently to the actuators. The diodes should be wired to the correct poles of the limit switches as well. For the experts who read this, you will already know this, but for others: I recommend _NOT_ soldering anything until you are sure you have it all in working order. Start with one actuator, wiring everything up (using electrical tape to maintain connections before permanently soldering later) and get it working before moving onto the second actuator. Be sure you can disconnect power to the motor quickly in case the limit switches aren't working properly at first. You can also take the pin out of the bottom brackets that hold the actuator to it, if needed, but be aware that it can be a little tricky to get back on.

The limit switches need to be attached in place so the hinge triggers them when the table is fully open. I took some long skinny screws that I got from the hardware store and a plastic spacer cut to size that would hold the switch far enough awa from the sidewall of the table to engage when the hinge was all the way open. For the size, you will probably have to tailor this to the table that you buy. I bought a size that fit snugly through the limit switch bolt holes (just bring the switch to the store with you) and I bought a series of lengths of them starting from something like 25mm on up to 40mm (I think, it was about 6 months ago) and took used the first one that fit well, which was 35mm I believe.  

![20240528_101722](https://github.com/emackinnon1/pico-table-motor/assets/49004020/750a0f8a-2482-4684-a106-2c6d48dd197a)


![20240528_101705](https://github.com/emackinnon1/pico-table-motor/assets/49004020/b0ecdb1a-0963-49bb-a288-178684e0aae3)


![20240528_101649](https://github.com/emackinnon1/pico-table-motor/assets/49004020/823dde5d-70ae-4b36-8f6e-813b8c553b38)

I used electrical tape to wrap the exposed metal parts of the diode and the poles of the limit switches. As you are wiring / soldering, TEST AND TEST AGAIN to be sure that everything is still working as expected. I left the motor drivers until last so I could use the power outputs to be sure that the limit switches and actuators were working.

### Coding
If you haven't already flashed micropython to a raspberry pi pico before, google it. There are plenty of tutorials on that and on getting Thonny running to do some coding. After you have done that grab the code from this repo and upload it via Thonny. You'll need to have an MQTT server and a way of sending messages to the pico, or you can set up Home Assistant to do all of this. I have also included my yaml set up if anyone wants to go that route.

The code is pretty straightforward. You will need to put in your network id and password and your MQTT server. The quick and dirty explanation of the code is:
After the pico is connected to the MQTT server, it will then be ready to receive messages on the `cmd_topic` which will match to the string of `"OPEN"` or `"CLOSED"`. Depending on which one is received, it will change the output pins which switches the polarity to the motors. The `state_topic` sends the updated state of `"OPEN"` or `"CLOSED"` to the MQTT server. The server also gets pinged periodically to maintain the connection, although occasionally (at least for my set up) I have to unplug and replug the pico back in because the connection gets dropped.

### Final thoughts
I listed as many things to watch out for as I could so you don't have as much trouble as I did, but I may have missed some things. Feel free to comment with whatever thoughts or questions you may have. I am sure someone somewhere has some ideas on improving it.
