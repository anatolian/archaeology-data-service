<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 06.04.2015
 * Time: 10:54
 */
require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_list_of_lightness_from_DB());
SuperWrapper::close_db();