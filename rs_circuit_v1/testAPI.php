<?php
session_start();
    $host = "localhost"; //localhost
    $user = "smartshopping";
    $pass = -;
    $bdd = -;

    @mysql_connect($host, $user, $pass) or saveLog("Impossible de se connecter à la base de données 3 : " . mysql_error());
	@mysql_select_db($bdd) or saveLog("Impossible de se connecter à la base de données 4");
    @mysql_query("SET NAMES 'utf8'");  //--Test

	if(isset($_SESSION["connected"]) && $_SESSION["connected"] === true)
	{    		
    	$session_array['connected'] = $_SESSION["connected"];
		$session_array['email']  = $_SESSION["email"];
		
		$query_user = "SELECT * FROM users WHERE email= '" . $_SESSION["email"] . "'";
		$res = mysql_query($query_user);
		if ($res)
		{   
			while($row = mysql_fetch_assoc($res)) 
			{
	       		$id_user = $row["id"];
	    	}
	    }
		if (isset($_POST['taffyy']))
		{
			echo $_POST['taffyy'];
			$taffy = $_POST['taffyy'];
			//$taffy = addslashes($taff)
			$check_taffy = "SELECT * FROM taffy_list WHERE id_utilisateur = '".$id_user."'";
			mysql_query($check_taffy);
			if (mysql_num_rows(mysql_query($check_taffy)) == 0)
			{
				echo "je trouve rien";
				$add_taffy = "INSERT INTO taffy_list (`id_utilisateur`,`taffy`) VALUES ('".$id_user."','".$taffy."')";
				mysql_query($add_taffy);
			}
			else 
			{
				$modifie_taffy = "UPDATE taffy_list SET `taffy` = '".$taffy."' WHERE id_utilisateur = '".$id_user."'";
				$ress =  mysql_query($modifie_taffy);
				if ($ress)
				{echo "Taffy was updated.";}
				else 
				{echo "Something went wrong when updating Taffy.";} 	
			}
		}
	 	else if (isset($_POST['giveme']))
	 	{
	 		$qry = "SELECT * FROM taffy_list WHERE id_utilisateur = '".$id_user."'";
	 		$res = mysql_query($qry);
	 		if (mysql_num_rows($res) == 0)
	 			echo "[]";
	 		else 
	 		{
	 			while ($roow = mysql_fetch_assoc($res))
	 			{
	 				echo $roow['taffy'];
	 			}

	 		} 
	 	}
	 	else if (isset($_POST['panID']))
	 	{
	 		$pan = "SELECT * FROM panier WHERE id_utilisateur = '".$id_user."'"; 
	 		$panier = mysql_query($pan);
	 		if (mysql_num_rows($panier) ==0)
	 		{
	 			echo "empty"; 
	 		}
	 		else 
	 		{
	 			while($line = mysql_fetch_assoc($panier)){
	 				$paniercourant = $line['id_panier'];
	 			}
				echo $paniercourant;
	 		}
	 	
	 	}
	 	else if (isset($_POST['pantodrop']))
	 	{
	 		$asupprimer = $_POST['pantodrop']; 
	 		$supr = "DELETE FROM panier WHERE id_utilisateur = '".$id_user."' AND id_panier = '".$asupprimer."'";
	 		mysql_query($supr);
	 	}
	 	else if (isset($_POST['current']))
	 	{
	 		$pantoadd = $_POST['current'];
			$check_panier = "SELECT * FROM panier WHERE id_utilisateur = '".$id_user."'"; 
			$check = mysql_query($check_panier);
			if (mysql_num_rows($check) == 0){	 		
	 		$addpan = "INSERT INTO panier (`id_panier`,`id_utilisateur`) VALUES ('".$pantoadd."','".$id_user."')";
	 		mysql_query($addpan);
	 		
	 		echo $pantoadd;
	 		}
	 	}
	 	else if (isset($_POST['enseignes']))
	 	{	
	 		$enseignes = $_POST['enseignes'];
	 		echo $enseignes;

	 		$ensUsr = "UPDATE taffy_list SET `enseignes` ='".$enseignes."' WHERE id_utilisateur = '".$id_user."'";
	 		mysql_query($ensUsr);
	 	}
		else if (isset($_POST['taffy_tmp_str'])){
			$taffy_tmp_str = $_POST['taffy_tmp_str'];
			$province = $_POST['province'];
			$prov = str_replace('"', '', $province);
			if(!is_dir('users/'.$id_user)) mkdir('users/'.$id_user);
			file_put_contents('users/'.$id_user.'/taffy.json', $taffy_tmp_str);
			$get_taffy = "SELECT taffy FROM taffy_list WHERE id_utilisateur = '".$id_user."'";
			$taffy_query = mysql_query($get_taffy);
			$taffy = mysql_fetch_array($taffy_query);
			file_put_contents('users/'.$id_user.'/full_taffy.json', $taffy[0]);
			if(!file_exists('users/'.$id_user.'/training_set.csv')){
				exec('/usr/local/bin/python3.7 /var/www/html/run_from_site.py ' . $id_user . ' ' . $prov);
				$taffy_rec = file_get_contents('users/'.$id_user.'/taffy_to_site.json'); 
				$recommendation= json_encode($taffy_rec); 
				$update_taffy = "UPDATE taffy_list SET `taffy` ='".$taffy_rec."' WHERE id_utilisateur = '".$id_user."'";
				mysql_query($update_taffy);
				echo $recommendation;
			}
			else{
				
				exec('/usr/local/bin/python3.7 /var/www/html/recommend_selected_from_site.py ' . $id_user . ' ' . $prov);
				$taffy_rec = file_get_contents('users/'.$id_user.'/taffy_to_site.json'); 
				$recommendation= json_encode($taffy_rec); 
				$update_taffy = "UPDATE taffy_list SET `taffy` ='".$taffy_rec."' WHERE id_utilisateur = '".$id_user."'";
				mysql_query($update_taffy);
				echo $recommendation;
			}
		}
	}
?>
