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

	// foreach ($lineArr as $key => $value) {
		// if($value != "\n") {
		// echo $value;
	// }
	// echo "<script>console.log('".print_r($lineArr)."')</script>";
	// echo "<script>console.log('".print_r($arr)."')</script>";
	$whoami = exec('who am i');
	echo json_encode($whoami);
//	echo json_encode($lineArr);

?>
