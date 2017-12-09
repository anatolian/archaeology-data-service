<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 02.04.2015
 * Time: 11:56
 */
require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_sitename_and_siteids_from_DB());
SuperWrapper::close_db();