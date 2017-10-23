<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 04.06.2015
 * Time: 17:35
 */
require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_image_base_path());
SuperWrapper::close_db();