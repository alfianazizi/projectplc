<?php

// phpinfo();
session_start();

$server = "localhost"; //ganti sesuai server Anda
$username = "root"; //ganti sesuai username Anda
$password = ""; //ganti sesuai password Anda
$db_name = "projectplc"; //ganti sesuatu nama database Anda
$conn = mysqli_connect($server,$username,$password);

mysqli_select_db($conn, $db_name) or DIE("Database not found.");
$login = mysqli_query($conn, "select * from tb_user where (username = '" . $_POST['username'] . "') and (password = '" . md5($_POST['password']) . "')");

$rowcount = mysqli_num_rows($login);
if ($rowcount == 1) {
	$_SESSION['username'] = $_POST['username'];
	header("Location:../home.html");
}
else {
	header("Location:../index.html");
}

?>