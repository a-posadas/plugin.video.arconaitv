# plugin.video.arconaitv
A way to watch arconaitv content from Kodi.

ArconaiTV is a website with various 24/7 show, movie and cable channel streams. As of November 14 2017 it is hosted at https://www.arconaitv.us/. The rationale for writing this plugin was so that the 
content could be accessed using the Kodi media center in situations where the given platform lacks the necessary browser functionality or where navigation among other issues makes using a browser too 
cumbersome. This plugin *should* work on any platform that can run Kodi but it has only been tested on arch linux and amazon firestick.

##Installation
Installation is easy. On Linux you would do the following:
    git clone https://github.com/a-posadas/plugin.video.arconaitv
    zip -r plugin.video.arconaitv.zip plugin.video.arconaitv/ -x *.git*
At this point you should have a zip file you can sideload into your device. On a firestick (or possibly android):
    adb connext <ip address of your device>
    adb push plugin.video.arconaitv.zip /sdcard/plugin.video.arconaitv.zip
On a raspberry pi you would use scp but if you have one of those I'm guessing you already know how to do most of this. 

Ok, so you have your zip file on your device, time to install it onto kodi.
1. Add-ons
2. Box icon (top left)
3. Install from zip file 

And that should be it. 

##Dependencies
Please note that this plugin requires Muckys Common Libraries, specifically, jsbeautifier, to deobfuscate javascript, beautifulsoup, to parse HTML, and requests to make web requests. Most likely, your 
Kodi installation will automatically download and install the libraries once you install this plugin (or you probably already have them). If not, you can find the zip here 
(https://github.com/mucky-duck/mdrepo/tree/master/script.module.muckys.common).
