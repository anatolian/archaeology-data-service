<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 06.04.2015
 * Time: 10:56
 */

//require "Properties.php";
//
//function get_db() {
//    $db = pg_connect(sprintf("host=%s port=%s dbname=%s user=%s password=%s", PG_HOST, PG_PORT, PG_DB, PG_USERNAME, PG_PASSWORD));
//    return $db;
//}
//
//function get_lightness($db) {
//    $result_array = array();
//
//    $result = pg_query($db, "SELECT DISTINCT chroma FROM options.munsell_colors ORDER BY chroma") or die("query faield.") ;
//
//    while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
//        array_push($result_array, $line["chroma"]);
//    }
//    return $result_array;
//}
//
//
//$my_db = get_db();
//
//$json_2 = json_encode(get_lightness($my_db));
//echo $json_2;

require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_list_of_chromas_from_DB());
SuperWrapper::close_db();
