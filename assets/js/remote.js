// Lets make it easy to change the filename
var myScript = "index.php";

// When the key is pressed, set it in the DB by running the AJAX
$(".remoteKeys").click(function(event) {
        event.preventDefault();        
        var keyPressed = $(this).attr('id');
	$.get(myScript, { command: "key", value: keyPressed },
	function(data){
		if (data == 1)
		{
			$(".activity").addClass("btn-primary");
			$(".activity-icon").addClass("icon-white");
		} else {
			$(".activity").addClass("btn-danger");
			$(".activity-icon").addClass("icon-white");
		}
		setTimeout(clear, 200);
	});
});

// Clear the activity display 
function clear() {	
	$(".activity").removeClass("btn-primary btn-danger");
	$(".activity-icon").removeClass("icon-white");
};

// Lets get some shortcuts going
$(document).keypress(function(event) {
	event.preventDefault();
	//alert(event.which); // Keep this to check the keys, just uncomment the first section
	$('[data-keycode="' + event.which + '"]').click();	
});