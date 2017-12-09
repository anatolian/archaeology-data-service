<?php

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::json_output(
    SuperWrapper::get_item_weight_2_from_DB(
        UrlParametersWrapper::get_area_easting_from_url(),
        UrlParametersWrapper::get_area_northing_from_url(),
        UrlParametersWrapper::get_context_number_from_url(),
        UrlParametersWrapper::get_sample_number_from_url()));

SuperWrapper::close_db();