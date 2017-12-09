<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 10.04.2015
 * Time: 15:39
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_images(UrlParametersWrapper::get_item_id_from_url()));

SuperWrapper::close_db();