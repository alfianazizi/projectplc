<?php
	if(isset($_POST['resp']))
	{
	    $conf = $_POST['resp'];
	    // echo "<script>console.log('".json_encode($conf)."')</script>";

	    // write to file
	    file_put_contents("../../../etc/dhcpcd.conf", implode(PHP_EOL, $conf));

	    // restart device
	    exec('sudo reboot');

	}
?>