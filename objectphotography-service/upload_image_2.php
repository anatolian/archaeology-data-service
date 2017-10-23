<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 03.06.2015
 * Time: 18:16
 */

require_once "SuperWrapper.php";
require_once "UrlParametersWrapper.php";
require_once "add_label.php";

function get_picture_number($dir_path,$samp_num) {
    //1_pic_1.jpg, 1_pic_2.jpg, 1_pic_4.jpg, 1_pic_5a.jpg

    if ($handle = opendir($dir_path)) {

        $biggest_pic_number = 0;

        /* This is the correct way to loop over the directory. */
        while (false !== ($entry = readdir($handle))) {
            if(preg_match("/^".$samp_num."_pic_(?<pic_number>[0-9]+)\.jpg$/", $entry, $matches)) {

                $tmp_pic_number = $matches["pic_number"];
                if($tmp_pic_number > $biggest_pic_number) {
                    $biggest_pic_number = $tmp_pic_number;
                }

            }
        }


        closedir($handle);
        return $biggest_pic_number + 1;
    }
    return 1;
}


function generate_image_path_for_returning($image_base_path) {
    $area_easting = UrlParametersWrapper::get_area_easting_from_url();
    $area_northing = UrlParametersWrapper::get_area_northing_from_url();
    $context_number = UrlParametersWrapper::get_context_number_from_url();
    $sample_subpath = SuperWrapper::get_sample_subpath()["sample_subpath"];

//    return $sample_subpath . $area_easting . DIRECTORY_SEPARATOR . $area_northing . DIRECTORY_SEPARATOR . $context_number . DIRECTORY_SEPARATOR . $sample_number . "_pic_" . get_picture_number($image_base_path) . ".jpg";
    return $sample_subpath . $area_easting . DIRECTORY_SEPARATOR . $area_northing . DIRECTORY_SEPARATOR . $context_number . DIRECTORY_SEPARATOR;
}

function generate_image_file_name($image_upload_dir_path) {
    $sample_number = UrlParametersWrapper::get_sample_number_from_url();
    return $sample_number . "_pic_" . get_picture_number($image_upload_dir_path,$sample_number) . ".jpg";
}



//    $image_base_path = SuperWrapper::get_image_base_path()["base_image_path"];
$image_base_path = BASE_IMAGE_PATH;
$image_path_for_response_json = generate_image_path_for_returning($image_base_path);
$image_upload_dir_path_for_saving_file = $image_base_path . $image_path_for_response_json;


if( ! is_dir($image_upload_dir_path_for_saving_file)) {
    mkdir($image_upload_dir_path_for_saving_file, 0777, true);
}

$tmp_name = $_FILES["upload_picture"]["tmp_name"];
    $area_easting = UrlParametersWrapper::get_area_easting_from_url();
    $area_northing = UrlParametersWrapper::get_area_northing_from_url();
    $context_number = UrlParametersWrapper::get_context_number_from_url();
 $sample_number = UrlParametersWrapper::get_sample_number_from_url();

 $water_mark_text_2="$area_easting.$area_northing.$context_number.$sample_number ";
 
 watermark_text($tmp_name, $water_mark_text_2);
 
if(move_uploaded_file($tmp_name, $image_upload_dir_path_for_saving_file . generate_image_file_name($image_upload_dir_path_for_saving_file))) {
    echo SuperWrapper::json_output(array("image_url" => $image_path_for_response_json));
}

