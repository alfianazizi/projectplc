<?php

// phpinfo();
session_start();

$server = "localhost"; //ganti sesuai server Anda
$username = "root"; //ganti sesuai username Anda
$password = ""; //ganti sesuai password Anda
$db_name = "projectplc"; //ganti sesuatu nama database Anda
$conn = mysqli_connect($server,$username,$password);

mysqli_select_db($conn, $db_name) or DIE("Database not found.");
$query = "select id_user from tb_user where (username = '" . $_POST['username'] . "') and (password = '" . md5($_POST['password']) . "')";
$result = $conn->query($query);

if ($result->num_rows == 1) {
	$res = $result->fetch_assoc();
	$_SESSION['userid'] = $res['id_user'];
	echo "<script>console.log('".json_encode($_SESSION['userid'])."')</script>";
	$conn->close();
	header("Location: ../home.html");
}
else {
	header("Location: ../index.html");
}

?>