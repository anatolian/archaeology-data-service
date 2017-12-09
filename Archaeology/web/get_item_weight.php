<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.04.2015
 * Time: 15:22
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_item_weight_from_DB(UrlParametersWrapper::get_item_id_from_url()));
SuperWrapper::close_db();