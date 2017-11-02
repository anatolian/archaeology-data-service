<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 23.04.2015
 * Time: 17:17
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

$area_easting = UrlParametersWrapper::get_area_easting_from_url();
$area_northing = UrlParametersWrapper::get_area_northing_from_url();
$context_number = UrlParametersWrapper::get_context_number_from_url();

echo SuperWrapper::json_output(SuperWrapper::get_sample_number($area_easting, $area_northing, $context_number));

SuperWrapper::close_db();