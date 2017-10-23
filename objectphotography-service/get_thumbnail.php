<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 12.06.2015
 * Time: 17:54
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";

function scaleImage($imagePath) {
    $imagick = new \Imagick(realpath($imagePath));
    $image_width = $imagick->getImageWidth();
    $image_height = $imagick->getImageHeight();
    $imagick->scaleImage($image_width / 4, $image_height / 4, true);
    header("Content-Type: image/jpg");
    echo $imagick->getImageBlob();
}

$photo_path = "/Library/WebServer/Documents/upload/excavation/sample/1/1/2/3_pic_4.jpg";
scaleImage($photo_path);
