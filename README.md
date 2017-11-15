# plugin.video.arconaitv
A way to watch arconaitv content from Kodi.

ArconaiTV is a website with various 24/7 show, movie and cable channel streams. As of November 14 2017 it is hosted at https://www.arconaitv.us/. The rationale for writing this plugin was so that the 
content could be accessed using the Kodi media center in situations where the given platform lacks the necessary browser functionality or where navigation among other issues makes using a browser too 
cumbersome. This plugin *should* work on any platform that can run Kodi but it has only been tested on arch linux and amazon firestick.

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

## Some Things You Should Know

### This plugin is a work in progress!!!

First of all, there is currently no artwork for the shows, movies and cable channels. Some of the descriptions are there but one, I got them from wikipedia and two a lot of the descriptions are missing. 
This does not, however, affect functionality. You can still watch the shows, movies or channels. 

Second, sometimes a channel, show or movie will not load. Check to make sure it is not down at the website before blaming the plugin. 

Third, ArconaiTV uses a type of javascript obfuscation that obscates obscated code. Yup. I wrote my own deobscation code (may be useful) that results in Dean Edwards packer obscuated code. This code was 
then deobscated using jsbeautify. Keep in mind that arconaitv is liable to and probably will change their code. In the event that it does, *this plugin will break*. I will try to fix it but no guarantees. 

Finally, the three scraper files aren't really necessary as they don't do anything. The show descriptions are stored locally in a json formatted file in resources. The three aforementioned files were used 
to create the json files. After that, you no longer need them. I don't have an api key for TVDB or TMDB and I don't intend to get one. ArconaiTV does not really have a practical way of getting their 
artwork and summaries for all the shows so far as I can tell. Thus, the problem of show summaries and artwork remains open. Suggestions are welcome. Actually, I do have an api key for fanart.tv so the 
artwork shouldn't be a problem, but the summaries are still problematic for me barring an api key or really annoying scraping. 

If you like this project consider making a donation by contacting me here on github. 
