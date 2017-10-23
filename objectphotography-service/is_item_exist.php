<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.04.2015
 * Time: 12:19
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::is_item_exist_in_DB(UrlParametersWrapper::get_item_id_from_url()));

SuperWrapper::close_db();