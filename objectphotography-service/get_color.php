<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.04.2015
 * Time: 16:33
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_color_info_from_DB(UrlParametersWrapper::get_item_id_from_url()));
SuperWrapper::close_db();