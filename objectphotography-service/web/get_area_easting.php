<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 23.04.2015
 * Time: 16:53
 */

require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_area_easting());

SuperWrapper::close_db();