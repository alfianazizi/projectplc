<?php
	$lineArr = [];
	$counter = 0;
	if ($file = fopen("../../etc/dhcpcd.conf", "r")) {
		while (!feof($file)) {
	        // if (fgets($file) != "\r\n") {
		        $lineArr[$counter] = fgets($file);
		        $counter++;
		    // }
	    }
	    fclose($file);
	}

	// echo "<script>console.log('".print_r($lineArr)."')</script>";
	// echo "<script>console.log('".print_r($arr)."')</script>";

	echo json_encode($lineArr);

?>