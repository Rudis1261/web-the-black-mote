#!/usr/bin/env python
import time, subprocess, redis

# Lets get connected to Redis
Redis = redis.Redis("localhost");

# This will get the current command from Redis and if it's a volume key then run the volume function
# Otherwise run the commandKeys, these two could be combined but it works now so I will leave it alone
def getCommand():   
    
    # Get the actual values from Redis
    command = Redis.get("command");
    value = Redis.get("value");
    timestamp = Redis.get("timestamp");
    
    # Run the command in question
    if command == 'volume':
        volume(value)
        
    if command == 'key':        
        commandKeys(value)
    
    # We need to set read to true so we do not loop through the same action all the time     
    Redis.set("read", 1)
 
# This will perform the actions   
def commandKeys(pressed):
    
    # The dictionary with the commands and switches to be run
    keyDict = {'up':['xdotool', 'key', "Up"],
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
            }
    
    # Was the keypress valid? If so, run the relevant command
    if pressed in keyDict:        
        xdotool(keyDict[pressed])
    else:
        print pressed, "command not found, Eish"

# Same as commandKeys, but for volumes
def volume(upDown):
    
    # Direction to move the volume
    directions = {'up':['xdotool', 'key', "XF86AudioRaiseVolume"],
                  'down':['xdotool', 'key', "XF86AudioLowerVolume"] }
    
    # Is the command value in the dictionary above? Then run the relevant command
    if upDown in directions:        
        xdotool(directions[upDown])
    else:
        print pressed, "you want the volume to go where?"
 
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
