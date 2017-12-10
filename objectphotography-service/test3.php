<?php
error_reporting( E_ALL );
ini_set('display_errors', 1);

echo "test3\n";
$dbopts = parse_url(getenv('DATABASE_URL'));

$pdo = new PDO('pgsql:host='.$dbopts["host"].' dbname='.ltrim($dbopts["path"],'/').' port='.$dbopts["port"].' user='.$dbopts["user"].' password='.$dbopts["pass"]);    

 

$pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
$pdo->setAttribute(PDO::MYSQL_ATTR_INIT_COMMAND,"SET NAMES 'UTF8'");





        $sql = "SELECT * FROM public.areas";
        $stm = $pdo->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
print_r($result);

?>