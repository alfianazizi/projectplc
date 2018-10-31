<?php

$dir = "../log/";
$arr = [];
$i = 0;
// Open a directory, and read its contents
if (is_dir($dir)){
	if ($dh = opendir($dir)){
		while (($file = readdir($dh)) != false){
			if ($file == '.' or $file == '..' or $file == '...') continue;
		  	$arr[$i] = $file;
		  	$i++;
		}
		closedir($dh);
	}
	echo json_encode($arr);
}
?>