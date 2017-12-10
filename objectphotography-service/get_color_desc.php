<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 06.04.2015
 * Time: 11:59
 */
require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

echo SuperWrapper::get_color_description_from_DB(
        UrlParametersWrapper::get_hue_from_url(),
        UrlParametersWrapper::get_lightness_from_url(),
        UrlParametersWrapper::get_chroma_from_url());
SuperWrapper::close_db();