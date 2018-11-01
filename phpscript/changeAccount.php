<?php

// get userdata from sesion
session_start();
$userdata;
if(isset($_SESSION["userid"])) {
 	$userdata = $_SESSION["userid"];
}

$server = "localhost"; //ganti sesuai server Anda
$username = "root"; //ganti sesuai username Anda
$password = "root"; //ganti sesuai password Anda
$db_name = "projectplc"; //ganti sesuatu nama database Anda
$conn = new mysqli($server,$username,$password,$db_name);

$uname = $_POST['username'];
$pass = $_POST['password'];
$cPass = $_POST['confirm_password'];

$q = "Update tb_user set username = '" . $uname . "', password = '" . md5($pass) . "' where id_user = " . $userdata;
	// mysqli_query($conn, $q);

// check confirm password
if ($pass == $cPass) {
	if ($conn->query($q) === TRUE) {
		echo "<script>
			alert('Username dan password berhasil diubah');
			window.location.href='../settings.html';
		</script>";
	}
} else {
	echo "<script>
		alert('Harap konfirmasi ulang password');
		window.location.href='../settings.html';
	</script>";
}

?>
