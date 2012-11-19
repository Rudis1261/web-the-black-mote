<?php
require 'classes/class.redis.php';
require 'classes/class.remotecontrol.php';
$r = new RemoteControl(); // Start the class which does the grunt work
    
// This API will look for get variables pushed through from the page and then adds it in redis.
// it looks for something like remote.php?command=key&value=up and stores it
if (  (isset($_GET['command']))
&& (isset($_GET['value']))  )
{
    echo (int)$r->add($_GET['command'], $_GET['value']);    // Returns 1 or 0 for the jQuery Ajax
    // $r->add adds the following to redis
    /*   $this->redis->set('command', $command);
         $this->redis->set('value', $value);
         $this->redis->set('timestamp', time());
         $last = $this->redis->set('read', 0);  */
    die(); // We need nothing else from this call, so lets stop execution here
}


// Simple as that, now all that's lets is to create the page to display the remote.
// For this we use a mixture or jQuery and Bootstrap from twitter
// http://twitter.github.com/bootstrap/index.html
// http://jquery.com/
?>
<!DOCTYPE html>
<html>
    
    <head>
        <title>Remote control</title>
        <!-- Bootstrap -->
        <link href="assets/css/bootstrap.min.css" rel="stylesheet" media="screen">
    </head>
    
    <body>
        <!-- Main Container, to center the remote -->
        <div align="center">
            <br />
            
            <!-- We need to set width limits in order to center spans -->
            <!-- Main remote container -->
            <div style="width: 375px;">
                
                <!-- Direction arrows and ok button -->
                <div class="pull-left well well-small">
                    <div>
                        <!--
                            You may notice I have some data-{variable} html attributes. These are used by my script later
                            The data-keycode is the keycode value for the button pressed, this makes it a bit easier to use
                            Don't know how to pick this up, check my remote.js file
                            
                            The id is the action to be performed. And the click is picked up with the "remoteKeys" and "volume" classes
                        -->
                        <a href="#" data-keycode="119" id="up" class="remoteKeys btn btn-large btn-inverse">
                            <i class="icon icon-white icon-arrow-up"></i>
                        </a>
                    </div>
                    
                    <br />
            
                    <div>
                        <a href="#" data-keycode="97" id="left" class="remoteKeys btn btn-large btn-inverse">
                            <i class="icon icon-white icon-arrow-left"></i>
                        </a>
                            &nbsp;&nbsp;&nbsp;            
                        <a href="#" data-keycode="13" id="ok" class="remoteKeys btn btn-large btn-primary">OK</a>
                            &nbsp;&nbsp;&nbsp;
                        <a href="#" data-keycode="100" id="right" class="remoteKeys btn btn-large btn-inverse">
                            <i class="icon icon-white icon-arrow-right"></i>
                        </a>        
                    </div>
                    
                    <br />
            
                    <div>
                        <a href="#" data-keycode="115" id="down" class="remoteKeys btn btn-large btn-inverse">
                            <i class="icon icon-white icon-arrow-down"></i>
                        </a>                 
                    </div>        
                </div>
                
                <!-- Play, stop, next and prev as well as XBMC and Music icons -->
                <div class="pull-left span">
                    <div>
                        <div class="btn-group">
                            <a href="#" id="prev" class="remoteKeys btn btn-large">
                                <i data-keycode="98" class="icon icon-backward"></i>
                            </a>
                            <a href="#" id="play" class="remoteKeys btn btn-large">
                                <i data-keycode="32" class="icon icon-play"></i>
                            </a>
                            <a href="#" id="next" class="remoteKeys btn btn-large">
                                <i data-keycode="110" class="icon icon-forward"></i>
                            </a>
                        </div>
                        
                        <br />
                        
                        <div>
                            <a data-keycode="27" href="#" id="back" class="remoteKeys btn btn-large">
                                <i class="icon icon-repeat"></i>
                            </a>
                                &nbsp;&nbsp;&nbsp;
                            <a href="#" data-keycode="105" id="info" class="remoteKeys btn btn-large">
                                <i class="icon icon-info-sign"></i>
                            </a>
                        </div>
                        
                        <br />
                        
                        <div>                     
                        <a href="#" data-keycode="120" id="xbmc" class="remoteKeys">
                            <img src='assets/img/xbmc2.png' width="60" />                    
                        </a>
                        <a href="#" data-keycode="114" id="music" class="remoteKeys">
                            <img src='assets/img/music.jpg' width="64" />                    
                        </a>
                        </div>
                        
                    </div>
                    
                </div> 
            </div><!-- Done with the main remote component -->
            
            <div class="clearfix"></div>
            
            <!-- Time for the volume controls -->
            <div class="row">
                <div class="btn-group">       
                    <button class="btn btn-large remoteKeys" data-keycode="113" id="vol-down">Volume Down <i class="icon icon-volume-down"></i></button>                
                    <button class="btn btn-large activity"><i class="activity-icon icon icon-heart"></i></button>           
                    <button class="btn btn-large remoteKeys" data-keycode="101" id="vol-up">Volume Up <i class="icon icon-volume-up"></i></button>
                </div>
            </div>
    
        </div><!-- </main div> -->
        
        <!-- Lastly the javascript needed -->        
        <script src="assets/js/jquery.js"></script>
        <script src="assets/js/remote.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>      
    </body>
</html>