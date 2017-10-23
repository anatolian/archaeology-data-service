<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 23.04.2015
 * Time: 17:02
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_area_northing(UrlParametersWrapper::get_area_easting_from_url()));

SuperWrapper::close_db();