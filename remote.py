#!/usr/bin/env python
import time, subprocess, redis, os, commands

# Lets get connected to Redis
Redis = redis.Redis("localhost");



# This will get the current command from Redis and if it's a volume key then run the volume function
# Otherwise run the commandKeys, these two could be combined but it works now so I will leave it alone
def getCommand():   
    
    # Get the actual values from Redis
    command = Redis.get("command");
    value = Redis.get("value");
    timestamp = Redis.get("timestamp");

    # Run the command       
    if command == 'key':        
        commandKeys(value)
    
    # We need to set read to true so we do not loop through the same action all the time     
    Redis.set("read", 1)
 
# This function will be used to confirm whether an application is running   
def appRunning(appName):
    getStatus = commands.getoutput('ps -C ' + appName)
    if appName in getStatus:
        return True
    else:
        return False
 
# This will perform the actions   
def commandKeys(pressed):
    
    # To check which applications are running. This will be used for application specific short-cuts.
    # applications = ['xbmc', 'rhythmbox', 'vlc']
    applications = {"vlc"       :   {   'play':['xdotool', 'key', "space"],
                                        'next':['xdotool', 'key', "n"],
                                        'prev':['xdotool', 'key', "b"],
                                        'vol-up':['xdotool', 'key', "ctrl+Up"],
                                        'vol-down':['xdotool', 'key', "ctrl+Down"], 
                                    },
                        
                    "totem"     :   {   'play':['xdotool', 'key', "space"],
                                        'next':['xdotool', 'key', "n"],
                                        'prev':['xdotool', 'key', "b"],
                                        'vol-up':['xdotool', 'key', "XF86AudioRaiseVolume"],
                                        'vol-down':['xdotool', 'key', "XF86AudioLowerVolume"],                                     
                                    },
                    
    }
    
    # The dictionary with the commands and switches to be run
    defaults = {'up':['xdotool', 'key', "Up"],
            'down':['xdotool', 'key', "Down"],
            'left':['xdotool', 'key', "Left"],
            'right':['xdotool', 'key', "Right"],
            'ok':['xdotool', 'key', "KP_Enter"],
            'play':['xdotool', 'key', "XF86AudioPlay"],
            'info':['xdotool', 'key', 'Menu'],
            'back':['xdotool', 'key', "Escape"],
            'next':['xdotool', 'key', "XF86AudioNext"],
            'prev':['xdotool', 'key', "XF86AudioPrev"],
            'xbmc':['xbmc'],
            'stop':['xdotool', 'key', "XF86AudioStop"],
            'music': ['xdotool', 'key', "XF86Go"],
            'vol-up':['xdotool', 'key', "XF86AudioRaiseVolume"],
            'vol-down':['xdotool', 'key', "XF86AudioLowerVolume"],    
            }
    
    for app in applications:
        if appRunning(app):
            if pressed in applications[app]:
                xdotool(applications[app][pressed])
    
    # Was the keypress valid? If so, run the relevant command
    if pressed in defaults:        
        xdotool(defaults[pressed])
    else:
        print pressed, "command not found, Eish"
 
# This little baby is what sends the command from the dictionary to the kernel to be processed.
def xdotool(action):
    ps = subprocess.Popen(action);
    print action #Comment this out, if you do not want to see which action was taken. Usefull for debugging
    
    
# This is the main loop with a small time delay so we do not chow the CPU to bits
while 1:
    
    # Check if a remote key was pressed by quering Redis
    if int(Redis.get("read")) == 0:
        
        # Lets get the command
        getCommand()  
        
    time.sleep(0.1) # Little sleep required (Don't we all)
