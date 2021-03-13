<?php	

// Connect to databse
$host = "localhost"; //localhost
$user = "smartshopping";
$pass = -;
$bdd = -;

@mysql_connect($host, $user, $pass) or saveLog("Impossible de se connecter à la base de données 3 : " . mysql_error());
@mysql_select_db($bdd) or saveLog("Impossible de se connecter à la base de données 4");
@mysql_query("SET NAMES 'utf8'");  //--Test

//make recommendation for users
$files = scandir('/var/www/html/users/');
$files = array_slice($files, 2);
$prov = 1; //province : trouver un moyen de rendre dynamique
foreach($files as $file){
	try{
		$id_user = $file;	
		$get_taffy = "SELECT taffy FROM taffy_list WHERE id_utilisateur = '".$id_user."'";
		$taffy_query = mysql_query($get_taffy);
		//if(mysql_num_rows($taffy_query)==0) continue;
		$taffy = mysql_fetch_array($taffy_query);
		file_put_contents('/var/www/html/users/'.$id_user.'/taffy.json', $taffy[0]);
		file_put_contents('/var/www/html/users/'.$id_user.'/full_taffy.json', $taffy[0]);
		echo("\n\n".$id_user."\n\n\n\n\n\n\n\n");
		exec('/usr/local/bin/python3.7 /var/www/html/run_from_site.py ' . $id_user . ' ' . $prov);
		$new_taffy = file_get_contents('/var/www/html/users/'.$id_user.'/taffy_to_site.json');
		$update_taffy = "UPDATE taffy_list SET `taffy` ='".$new_taffy."' WHERE id_utilisateur = '".$id_user."'";
		mysql_query($update_taffy);
		}
	catch(exception $e){
		echo('There was an error for the user with id'.$file."\n");
		echo($e."\n");
		}
	}
?>