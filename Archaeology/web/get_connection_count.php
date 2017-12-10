<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 14.04.2015
 * Time: 14:46
 */

require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_connection_count());
SuperWrapper::close_db();