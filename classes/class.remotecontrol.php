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