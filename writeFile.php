<?php
	if(isset($_POST['resp']))
	{
	    $conf = $_POST['resp'];
	    $ip = 0;
	    $c = 0;
	    while ($ip == 0) {
	    	if(substr($conf[$c], 0, 17) == "static ip_address") {
	    		$ip = substr($conf[$c], 18, 36);
	    	}
	    	$c++;
	    }

	    // write to file
	    file_put_contents("../../../etc/dhcpcd.conf", implode(PHP_EOL, $conf));

	    echo ("IP Address changed to ".$ip.". Rebooting now...");
	}
?>