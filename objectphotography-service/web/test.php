<?php
error_reporting( E_ALL );
ini_set('display_errors', 1);

echo "test";

$dbopts = parse_url(getenv('DATABASE_URL'));


$dbconn = pg_connect('host='.$dbopts["host"].' dbname='.ltrim($dbopts["path"],'/').' port='.$dbopts["port"].' user='.$dbopts["user"].' password='.$dbopts["pass"])    or die('Could not connect: ' . pg_last_error());

echo pg_last_error();
        $sql = "SELECT * FROM public.areas";
echo $sql;

$result = pg_query($dbconn,$sql) or die('Query prob: ' . pg_last_error());
echo '2:'.pg_last_error();

echo "<table>\n";
while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
    echo "\t<tr>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";
?>