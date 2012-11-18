**The short and the long:**
-----------

######Tested on Ubuntu 12.04 LTS. 
######(Requirements)  
Apache Server (V2.2.22)      
PHP5 (V5.3.10)  
Python (V2.7.3) installed as standard  
Redis (V2.7.3)  
xdotool (V1:2)  
Python-redis (V2.7.3)  

######Installation
```terminal
sudo apt-get install apache2  
sudo apt-get install php5  
sudo apt-get install redis-server  
sudo apt-get install xdotool  
sudo apt-get install python-redis
```

*If there are any more dependencies, I apologize as this is all that springs to mind.*
  
***Once upon a time***  

I thought I would share this, should someone look for something similar and happen upon this. 

The easiest way I found to send the keystrokes through Python is by installing ***xdotool*** which is a unix based scripting tool, which is pretty awesome. It supports all the multimedia keys. Including the context menu a.k.a "Menu". 

***So what did I need it for?***  
I built a remote for my ***Ubuntu*** since my Compro Remote stopped working.

***How does it work?***  
It leverages Apache, Bootstrap, PHP, Redis, Python and finally xdotools (Boy that's a mouthful). I created a mini website which I access through my WIFI with remote buttons which when clicked sends the command in the background to the PHP  Script running on Apache.

This PHP script then saves the command and values in Redis which is polled constantly by Python. Once Python picks the command up. It checks it in the dictionary of commands and sends the appropriate command line to xdotool. Xdotool then runs the Media Keys or starts Rhythm-box or XBMC or pauses and plays. Whatever. So far it's working like a charm.


----------

## The CODE ##
***index.php***    
Generates the remote through web interface  

[Checkout the latest index.php](https://github.com/drpain/web-the-black-mote/blob/master/index.php)  

![Web-the-black-mote GUI](https://raw.github.com/drpain/web-the-black-mote/master/assets/img/webmote.jpg)

***Remote.js***  
This is what will detect key and button presses and send the command to the PHP script  
[1]: https://github.com/drpain/web-the-black-mote/blob/master/assets/js/remote.js        "Checkout the latest remote.js"  

GET /repos/:drpain/:web-the-black-remote/contents/:index.php

***class.remotecontrol.php***  
All this really does is take the action sent through from the jQuery and adds the values to Redis so Python can pick it up.   

```php
    <?php
        // Create the remote object
        class RemoteControl
        {
    	public $redis;
    	
    	// Bootstrap / Init the class by creating an instance for Redis
            public function __construct()
            {
    	    $this->redis = new Redis();
    	    $this->redis->debug=false;	   
            }
    	
    	// Add the values to Redis which Python polls for the info
    	public function add($command, $value)
    	{
    	    $this->redis->set('command', $command);
    	    $this->redis->set('value', $value);
    	    $this->redis->set('timestamp', time());
    	    $last = $this->redis->set('read', 0);	
    	    if ($last == "OK"){
    		return 1;
    	    } 
    	    return 0;
    	}
        }    
    ?>
```

***Remote.py***  
This baby goes into Redis and checks for commands and dispatches the relevant command to the Linux kernel to be action-ed. Very nice! **Remember to make this executable if you want to launch with it** *(sudo chmod +x remote.py)*  

```python2.7
    #!/usr/bin/env python
    # Import the python modules we will need
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
        print action #Comment this out, if you do not want to see which action was taken. Useful for debugging
        
        
    # This is the main loop with a small time delay so we do not chow the CPU to bits
    while 1:
        
        # Check if a remote key was pressed by querying Redis
        if int(Redis.get("read")) == 0:
            
            # Lets get the command
            getCommand()  
            
        time.sleep(0.1) # Little sleep required (Don't we all)
```