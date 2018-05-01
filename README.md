# plugin.video.arconaitv
A way to watch arconaitv content from Kodi.

ArconaiTV is a website with various 24/7 show, movie and cable channel streams. The rationale for writing this plugin was so that the content could be accessed using the Kodi media center in situations where the given platform lacks the necessary browser functionality or where navigation among other issues makes using a browser too cumbersome. This plugin *should* work on any platform that can run Kodi but it has only been tested on arch linux and amazon firestick. 

Also, this plug in is intended for educational purposes only. It is not intended for use. 

## Installation

Installation is easy. On Linux you would do the following:

    git clone https://github.com/a-posadas/plugin.video.arconaitv
    zip -r plugin.video.arconaitv.zip plugin.video.arconaitv/ -x *.git*

At this point you should have a zip file you can sideload into your device. On a firestick (or possibly android):

    adb connect <ip address of your device>
    adb push plugin.video.arconaitv.zip /sdcard/plugin.video.arconaitv.zip

On a raspberry pi you would use scp but if you have one of those I'm guessing you already know how to do most of this. 

Ok, so you have your zip file on your device, time to install it onto kodi.
1. Add-ons
2. Box icon (top left)
3. Install from zip file 

And that should be it. 

## Dependencies

Please note that this plugin requires Muckys Common Libraries, specifically, jsbeautifier, to deobfuscate javascript, beautifulsoup, to parse HTML, and requests to make web requests. Most likely, your 
Kodi installation will automatically download and install the libraries once you install this plugin (or you probably already have them). If not, you can find the zip here 
(https://github.com/mucky-duck/mdrepo/tree/master/script.module.muckys.common).

## A very disorganized mess
This addon is not organized, there is no real version and I update it sporadically. There is also the problem of the content the addon scrapes. For this reason, I do not condone the use of this addon. I am using my freespeech rights to explain something in detail with no intention of its being used in the manner described. 

01/26/2018 made the deobfuscator a class that can be used in different projects. It takes in a unicode string. Make sure it's unicode. 

Check out my site!
http://technicology.dx.am/
