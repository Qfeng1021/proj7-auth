<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>

    <body>
<?php
	$username = "phptest";
	$password = "1234567890";
	$data = array("username" => $username, "password" => $password);
	$url = "http://laptop-service/api/register";
	$postdata = http_build_query($data);  
	$opts = array('http' =>   
		array( 'method'  => 'POST','header'  => 'Content-type: application/x-www-form-urlencoded', 'content' => $postdata));  
	$context = stream_context_create($opts);  
	$result = file_get_contents($url, false, $context);

	$json = file_get_contents("http://laptop-service/api/token?username=".$username."&password=".$password);
	$obj = json_decode($json);
	$Token = $obj->token;

	echo "<h2>listAll</h2>";
	$json = file_get_contents("http://laptop-service/listAll?token=".$Token);
	$obj = json_decode($json);
	$Opens = $obj->open;
	$Closes = $obj->close;
	echo "Open Time:";
	foreach ($Opens as $o) {
		echo "<li>$o</li>";
	}
	echo "Close Time:";
	foreach ($Closes as $c) {
		echo "<li>$c</li>";
	}

	echo "<h2>listAll Top=2</h2>";
	$json = file_get_contents("http://laptop-service/listAll/json?top=2&token=".$Token);
	$obj = json_decode($json);
	$Opens = $obj->open;
	$Closes = $obj->close;
	echo "Open Time:";
	foreach ($Opens as $o) {
		echo "<li>$o</li>";
	}
	echo "Close Time:";
	foreach ($Closes as $c) {
		echo "<li>$c</li>";
	}

	echo "<h2>listAll/Csv Top=2</h2>";
	echo file_get_contents("http://laptop-service/listAll/csv?top=2&token=".$Token);

	echo "<h2>listOpenOnly</h2>";
	$json = file_get_contents("http://laptop-service/listOpenOnly?token=".$Token);
	$obj = json_decode($json);
	$Opens = $obj->open;
	echo "Open Time:";
	foreach ($Opens as $o) {
		echo "<li>$o</li>";
	}
	
	echo "<h2>listOpenOnly Top=4</h2>";
	$json = file_get_contents("http://laptop-service/listOpenOnly?top=4&token=".$Token);
	$obj = json_decode($json);
	$Opens = $obj->open;
	echo "Open Time:";
	foreach ($Opens as $o) {
		echo "<li>$o</li>";
	}

	echo "<h2>listOpenOnly/Csv Top=4</h2>";
	echo file_get_contents("http://laptop-service/listOpenOnly/csv?top=4&token=".$Token);

	echo "<h2>listCloseOnly</h2>";
	$json = file_get_contents("http://laptop-service/listCloseOnly?token=".$Token);
	$obj = json_decode($json);
	$Closes = $obj->close;
	echo "Close Time:";
	foreach ($Closes as $c) {
		echo "<li>$c</li>";
	}

	echo "<h2>listCloseOnly Top=3</h2>";
	$json = file_get_contents("http://laptop-service/listCloseOnly?top=3&token=".$Token);
	$obj = json_decode($json);
	$Closes = $obj->close;
	echo "Close Time:";
	foreach ($Closes as $c) {
		echo "<li>$c</li>";
	}

	echo "<h2>listCloseOnly/Csv Top=3</h2>";
	echo file_get_contents("http://laptop-service/listCloseOnly/csv?top=3&token=".$Token);
?>
    </body>
</html>
