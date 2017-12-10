<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 04.06.2015
 * Time: 17:40
 */

require_once "SuperWrapper.php";

echo SuperWrapper::json_output(SuperWrapper::get_sample_subpath());

SuperWrapper::close_db();