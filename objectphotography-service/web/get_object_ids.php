<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.04.2015
 * Time: 10:25
 */
require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_item_ids_from_DB(UrlParametersWrapper::get_site_id_from_url()));

SuperWrapper::close_db();