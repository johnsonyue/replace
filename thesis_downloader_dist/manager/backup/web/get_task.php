<?php
	$config = parse_ini_file("config.ini");
	$code_path = $config["code_path"];

	$node_id = $_POST["id"];
	$node_key = $_POST["key"];
	
	$source = $_POST["source"];
	
	if (exec("python $code_path/run.py $source auth ".$node_id." ".$node_key) == "True"){
		echo exec("python $code_path/run.py $source get_task");
	}
	else{
		echo "auth failed";
	}
?>
