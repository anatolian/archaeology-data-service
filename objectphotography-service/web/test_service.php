<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 31.03.2015
 * Time: 15:13
 */
require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_service_status());
SuperWrapper::close_db();