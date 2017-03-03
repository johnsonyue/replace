<?php
	$config = parse_ini_file("config.ini");
	$code_path = $config["code_path"];

	$node_id = $_POST["id"];
	$node_key = $_POST["key"];
	$type = $_POST["type"];
	$task = $_POST["task"];
	
	$source = $_POST["source"];
	
	if (exec("python $code_path/run.py $source auth $node_id $node_key") == "True"){
		if ($type != "finished"){
			echo exec("python $code_path/run.py $source on_notify $type $node_id $task");
		}
		else{
			$time_used = $_POST["time_used"];
			echo exec("python $code_path/run.py $source on_notify $type $node_id $task $time_used");
		}
	}
	else{
		echo "auth failed";
	}
?>
