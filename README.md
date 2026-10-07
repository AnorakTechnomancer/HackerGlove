# **H4ck3rGl0v3 Beta**

## Concept
Soooo, I've had a fascination with wearable computers for a long time, probably since I saw my first Pip-Boy in a fallout game.
I think this glove computer thing is probably gonna come out similar in look to the Pip-Boy 3000 in terms of I remember it having a sort of attached glove with it.

There's a few things I want to accomplish with this device:
1. Mini/Portable Kali Linux Hacking terminal that I can launch preloaded attacks from, as well as interact with to conduct recon and stuff.
2. Gesture controlled via attached glove, based off a project on Hackaday.io by Zach Freedman.
3. Paired mini drone that will act as a sort of relay to give my recon and attacks better range.
4. Meshtastic integration, also using the drone as a comms relay.

I'll probably add to that list as the project grows, but those are my main initial ideas. It would be sick if I could make this glove semi rugged and off grid capable, maybe add some solar charging?

I would also maybe like to add in a heads up display, I have a little one I bought off someone a while ago. It's kinda shit, but I have it on hand. 
I kinda got a little inspired by the concept of a Gargoyle from the book Snow Crash. (Good read but Chapter 52 is actually insane like tf.)

I really just wanna make this my AIO cyberdeck. The main controls and everything will be in the unit on the wrist, and I'll probably just keep adding on stuff as I go along. 
Take up some of the capabilities of the flipper and HackRF One Portapack, etc.

So far, the hardware I plan on using is as follows:

| Purpose | Part | Reason |
|---|---|---|
| Main Compute | Rasberry Pi Zero 2W | Just what I have on hand. |
| Glove Compute | ESP32-C6 Feather | Low power, should be capable enough. Also has Stemma connectors for the ICM. |
| Glove Gesture Control | ICM-20948 | Just what I found as the best option. |
| Glove Thumbstick | PSP 3000 | Need extra controls for drone, possibly useful for other stuff. Also really small. |

