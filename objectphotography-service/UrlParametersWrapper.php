<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 04.06.2015
 * Time: 17:53
 */

class UrlParametersWrapper {
    public static function get_item_id_from_url() {
        if(array_key_exists("itemid", $_GET)) {
            return $_GET["itemid"];
        } else {
            return 0;
        }
    }

    public static function get_site_id_from_url() {
        if(array_key_exists("siteid", $_GET)) {
            return $_GET["siteid"];
        } else {
            return 0;
        }
    }

    public static function get_hue_from_url() {
        if(array_key_exists(HUE, $_GET)) {
            return $_GET[HUE];
        } else {
            return "";
        }
    }

    public static function get_lightness_from_url() {
        if(array_key_exists(LIGHTNESS_VALUE, $_GET)) {
            return $_GET[LIGHTNESS_VALUE];
        } else {
            return "";
        }
    }

    public static function get_chroma_from_url() {
        if(array_key_exists(CHROMA, $_GET)) {
            return $_GET[CHROMA];
        } else {
            return "";
        }
    }

    public static function get_area_easting_from_url() {
        if(array_key_exists("area_easting", $_GET)) {
            return $_GET["area_easting"];
        } else {
            return "";
        }
    }

    public static function get_area_northing_from_url() {
        if(array_key_exists("area_northing", $_GET)) {
            return $_GET["area_northing"];
        } else {
            return "";
        }
    }

    public static function get_context_number_from_url() {
        if(array_key_exists("context_number", $_GET)) {
            return $_GET["context_number"];
        } else {
            return "";
        }
    }

    public static function get_sample_number_from_url() {
        if(array_key_exists("sample_number", $_GET)) {
            return $_GET["sample_number"];
        } else {
            return "";
        }
    }

    public static function get_weight_in_kg_from_url() {
        if(array_key_exists("weight_in_kg", $_GET)) {
            return $_GET["weight_in_kg"];
        } else {
            return "";
        }
    }

    public static function get_photo_url_from_url()  {
        if(array_key_exists("photo_url", $_GET)) {
            return $_GET["photo_url"];
        } else {
            return "";
        }
    }

}