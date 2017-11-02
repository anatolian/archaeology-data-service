<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.04.2015
 * Time: 15:38
 */

require "Properties.php";



function get_db() {
    $db = pg_connect(sprintf("host=%s port=%s dbname=%s user=%s password=%s", PG_HOST, PG_PORT, PG_DB, PG_USERNAME, PG_PASSWORD));
    return $db;
}


function get_item_id() {
    return intval($_GET["itemid"]);
}

function get_weight() {
    return $_GET["weight"];
}

function check_numeric_type($value, $precision_limit, $scale_limit) {

    $fraction_part = explode(".", $value)[1];
    $decimal_part = explode(".", $value)[0];

    if(strlen($decimal_part) <= $precision_limit and strlen($fraction_part) <= $scale_limit) {
        return true;
    }
    else {
        return false;
    }

}

assert(check_numeric_type("23.5141", 6, 4));

function get_status($db, $item_id) {

    $result_array = array("value" => "");

    if($item_id == 0) {
        return $result_array;
    }

    $result = pg_query($db, "SELECT value FROM items.items_attributes_numeric WHERE name='Weight Kgs' AND itemid=" . $item_id) or die("query faield.") ;

    while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
        $result_array["value"] = $line["value"];
    }
    return $result_array;
}

function set_weight($db, $item_id, $weight) {
    if(get_status($db, $item_id)["value"] == "") { //insert

    } else { // update

    }
}

$my_db = get_db();

$json_2 = json_encode(get_status($my_db, get_item_id()));
echo $json_2;