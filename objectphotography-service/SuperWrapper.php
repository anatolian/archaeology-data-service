<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 08.04.2015
 * Time: 12:17
 */

require_once "Properties.php";
require_once "PgDB.php";


class SuperWrapper {

    static $db;

    public static function get_db() {
        self::$db = new PgDB();
        return self::$db->getDB();
    }

    public static function close_db() {
        $db = null;
    }


    public static function get_service_status() {

        $sql = "select * from options.procedure_properties";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        if(count($result) == 0) {
            $stm = null;
            return array("status" => false);
        } else {
            $stm = null;
            return array("status" => true);
        }

    }

    public static function is_item_exist_in_DB($item_id) {

        if($item_id == 0) {
            return array("status" => false);
        }

        $sql = "select items.itemid from items.items items where items.itemid=:itemid";
        $stm = self::get_db()->prepare($sql);
        $stm->execute(array(
            ":itemid" => $item_id,
        ));
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        if(count($result) == 1) {
            $stm = null;
            return array("status" => true);
        } else {
            $stm = null;
            return array("status" => false);
        }
    }

    public static function get_color_description_from_DB($hue, $lightness, $chroma) {

        if($hue == "" or $lightness == "" or $chroma == "") {
            return "error";
        } else {
            $sql = "SELECT description FROM options.munsell_colors WHERE hue=:hue AND lightness_value=:lightness_value AND chroma=:chroma";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                ":hue" => $hue,
                ":lightness_value" => $lightness,
                ":chroma" => $chroma
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            if(count($result) == 0) {
                return "";
            } else {
                $stm = null;
                return $result[0][DESCRIPTION];
            }
        }
    }

    public static function get_color_info_from_DB($item_id) {
        if($item_id == 0) {
            return array();
        } else {
            $result_array = array();
            $sql = "SELECT * FROM items.items_attributes_munsell WHERE itemid=:itemid";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                ":itemid" => $item_id,
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            foreach($result as $row) {
                array_push($result_array, array(
                    TYPE => $row[TYPE],
                    HUE => $row[HUE],
                    LIGHTNESS_VALUE => $row[LIGHTNESS_VALUE],
                    CHROMA => $row[CHROMA],
                    DESCRIPTION => self::get_color_description_from_DB($row[HUE], $row[LIGHTNESS_VALUE], $row[CHROMA]),
                ));
            }
            $stm = null;
            return $result_array;
        }
    }

    public static function get_list_of_lightness_from_DB() {
        $result_array = array();
        $sql = "select distinct lightness_value from options.munsell_colors order by lightness_value";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $row) {
            array_push($result_array, $row[LIGHTNESS_VALUE]);
        }
        $stm = null;
        return $result_array;
    }
    public static function get_list_of_chromas_from_DB() {
        $result_array = array();
        $sql = "select distinct chroma from options.munsell_colors order by chroma";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $row) {
            array_push($result_array, $row[CHROMA]);
        }
        $stm = null;
        return $result_array;
    }


    public static function get_list_of_reading_locs_from_DB() {
        $result_array = array();
        $sql = "select reading_location from options.munsell_color_reading_locations order by \"order\"";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $row) {
            array_push($result_array, $row[TYPE]);
        }
        $stm = null;
        return $result_array;
    }

    public static function get_hues_from_DB() {
        $result_array = array();
        $sql = "SELECT DISTINCT hue FROM options.munsell_colors ORDER BY hue ";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $row) {
            array_push($result_array, $row["hue"]);
        }
        $stm = null;
        return $result_array;
    }

    public static function get_item_weight_from_DB($item_id) {

        $result_array = array("value" => "");

        if($item_id == 0) {
            return $result_array;
        } else {
            $sql = "SELECT value FROM items.items_attributes_numeric WHERE name='Weight Kgs' AND itemid=:itemid";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                ":itemid" => $item_id,
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            if(count($result) == 0 ){
                $stm = null;
                return $result_array;
            } else {
                $result_array["value"] = $result[0]["value"];
                $stm = null;
                return $result_array;
            }
        }
    }


    public static function get_item_ids_from_DB($site_id) {
        $result_array = array();
        if($site_id == 0) {
            return $result_array;
        } else {
            $sql = "select items.itemid from items.items items where items.siteid=:siteid";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                ":siteid" => $site_id,
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            foreach($result as $row) {
                $tmp_array =array();
                $tmp_array["itemid"] = $row["itemid"];
                array_push($result_array, $tmp_array);
            }
            $stm = null;
            return $result_array;
        }
    }

    public static function get_sitename_and_siteids_from_DB() {
        $result_array = array();
        $sql = "select * from items.view_items_per_site";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        foreach($result as $row) {
            $tmp_array = array();
            $tmp_array["site_name"] = $row["site_name"];
            $tmp_array["siteid"] = $row["siteid"];
            array_push($result_array, $tmp_array);
        }
        $stm = null;
        return $result_array;
    }

    public static function get_image_base() {
        $sql = " SELECT value FROM options.procedure_properties WHERE property='ceramics_figure_http_base1'";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        if(count($result) == 0) {
            $stm = null;
            return "";
        } else {
            $result_str = $result[0]["value"];
            $stm = null;
            return $result_str;
        }
    }

    public static function get_image_base_url_2() {
        $sql = " SELECT property_value FROM options.procedure_properties WHERE property='base_image_url'";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        if(count($result) == 0) {
            $stm = null;
            return "";
        } else {
            $result_str = $result[0]["property_value"];
            $stm = null;
            return $result_str;
        }
    }

    public static function get_images($item_id) {
        $image_base = self::get_image_base();
        $result_array = array("image_base" => $image_base);

        $sql = "SELECT citation, figureid, \"primary\" FROM items.items_figures WHERE itemid=:itemid ORDER BY \"primary\" DESC";
        $stm = self::get_db()->prepare($sql);
        $stm->execute(array(
            ":itemid" => $item_id,
        ));
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $tmp_array = array();
        foreach($result as $row) {
            array_push($tmp_array, array(
                "citation" => $row["citation"],
                "figureid" => $row["figureid"]
            ));
        }
        $result_array["images"] = $tmp_array;
        $stm = null;
        return $result_array;

    }

    public static function get_images_2($area_easting, $area_northing, $context_number, $sample_number) {



        $sample_subpath = self::get_sample_subpath();
        if(TEST_MODE) {
            $image_base_path = TEST_BASE_IMAGE_PATH;
            $image_base_url = TEST_BASE_IMAGE_URL;
        } else {
            //print_r(self::get_image_base_path());
            $x_array = $image_base_path= self::get_image_base_path();
            $image_base_path = $x_array["base_image_path"];
            $image_base_url = self::get_image_base_url_2();
        }



        $interpath=$sample_subpath["sample_subpath"].$area_easting."/".$area_northing."/".$context_number."/";

        $target_dir = $image_base_path.$interpath;
        $target_url = $image_base_url.$interpath;
        if(is_dir($target_dir)) {
            chdir($target_dir);
            $images=glob($sample_number."_pic_[0-9]*",GLOB_NOSORT);

            $imageArray=array();
            foreach($images as $image){
                $imageExplode1 = explode(".",$image);
                $imageExplode2 = explode("_",$imageExplode1[0]);
                $imageNumber = intval($imageExplode2[2]);
                if (strval($imageNumber) == $imageExplode2[2])
                {
                    $imageArray[$imageNumber]=$image;
                }
            }
            ksort($imageArray);
            $tmp_array = array();
            foreach($imageArray as $image) {
                array_push($tmp_array, $target_url.$image);
            }
            $result_array["images"] = $tmp_array;
            return $result_array;
        } else {
            return array("images" =>  array());
        }



    }
    
    public static function get_connection_count() {
        $sql = "SELECT count(*) FROM pg_stat_activity";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $stm = null;
        return $result[0]["count"];

    }

    public static function get_area_easting() {
        $sql = "SELECT DISTINCT area_easting FROM sde.excavation_areas WHERE status='active' ORDER BY area_easting";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $tmp_array = array();
        foreach($result as $row) {
            array_push($tmp_array, $row["area_easting"]);
        }
        $stm = null;
        return $tmp_array;
    }

    public static function get_area_northing($area_easting) {
        $sql = "SELECT DISTINCT area_northing FROM sde.excavation_areas WHERE area_easting=:area_easting AND status='active' ORDER BY area_northing";
        $stm = self::get_db()->prepare($sql);
        $stm->execute(array(
            ":area_easting" => $area_easting
        ));
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $tmp_array = array();
        foreach($result as $row) {
            array_push($tmp_array, $row["area_northing"]);
        }
        $stm = null;
        return $tmp_array;
    }

    public static function get_context_number($area_easting, $area_northing) {
        $sql = "SELECT context_number FROM excavation.contexts_spatial WHERE area_northing=:area_northing AND area_easting=:area_easting ORDER BY context_number";
        $stm = self::get_db()->prepare($sql);
        $stm->execute(array(
            ":area_easting" => $area_easting,
            ":area_northing" => $area_northing
        ));
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $tmp_array = array();
        foreach($result as $row) {
            array_push($tmp_array, $row["context_number"]);
        }
        $stm = null;
        return $tmp_array;
    }

    public static function get_sample_number($area_easting, $area_northing, $context_number) {
        $sql = "SELECT sample_number FROM samples.samples WHERE area_easting=:area_easting AND area_northing=:area_northing AND context_number=:context_number ORDER BY sample_number";
        $stm = self::get_db()->prepare($sql);
        $stm->execute(array(
            "area_easting" => $area_easting,
            "area_northing" => $area_northing,
            "context_number" => $context_number
        ));
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        $tmp_array = array();
        foreach($result as $row) {
            array_push($tmp_array, $row["sample_number"]);
        }
        $stm = null;
        return $tmp_array;
    }


    public static function get_item_weight_2_from_DB($area_easting, $area_northing, $context_number, $sample_number) {

        $result_array = array("weight_kilograms" => "");

        if($area_easting == "" or $area_northing == "" or $context_number == "" or $sample_number == "") {
            return $result_array;
        } else {
            $sql = "SELECT weight_kilograms FROM samples.samples WHERE area_easting=:area_easting AND area_northing=:area_northing AND context_number=:context_number AND sample_number=:sample_number";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                "area_easting" => $area_easting,
                "area_northing" => $area_northing,
                "context_number" => $context_number,
                "sample_number" => $sample_number
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            if(count($result) == 0 ){
                $stm = null;
                return $result_array;
            } else {
                $result_array["weight_kilograms"] = $result[0]["weight_kilograms"];
                $stm = null;
                return $result_array;
            }
        }

    }

    public static function set_item_weight_2_from_DB($weight_in_kg, $area_easting, $area_northing, $context_number, $sample_number) {
        $result_array_fail = array("status" => "fail");
        if($weight_in_kg == "" or $area_easting == "" or $area_northing == "" or $sample_number == "") {
            return $result_array_fail;
        } else {
            $sql = "UPDATE samples.samples SET weight_kilograms=:weight_in_kg WHERE area_easting=:area_easting AND area_northing=:area_northing AND context_number=:context_number AND sample_number=:sample_number";
            $stm = self::get_db()->prepare($sql);
            $is_success = $stm->execute(array(
                "weight_in_kg" => $weight_in_kg,
                "area_easting" => $area_easting,
                "area_northing" => $area_northing,
                "context_number" => $context_number,
                "sample_number" => $sample_number
            ));
            if($is_success) {
                $stm =null;
                return array("status" => "ok");
            } else {
                $stm = null;
                return $result_array_fail;
            }
        }
    }

    public static function get_exterior_color_2_from_DB($area_easting, $area_northing, $context_number, $sample_number) {
        $result_array = array(
            "exterior_color_hue" => "",
            "exterior_color_lightness_value" => "",
            "exterior_color_chroma" => ""
        );

        if($area_easting == "" or $area_northing == "" or $context_number == "" or $sample_number == "") {
            return $result_array;
        } else {
            $sql = "SELECT exterior_color_hue, exterior_color_lightness_value, exterior_color_chroma FROM samples.samples WHERE area_easting=:area_easting AND area_northing=:area_northing AND context_number=:context_number AND sample_number=:sample_number";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                "area_easting" => $area_easting,
                "area_northing" => $area_northing,
                "context_number" => $context_number,
                "sample_number" => $sample_number
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            if(count($result) == 0 ){
                $stm = null;
                return $result_array;
            } else {
                $result_array["exterior_color_hue"] = $result[0]["exterior_color_hue"];
                $result_array["exterior_color_lightness_value"] = $result[0]["exterior_color_lightness_value"];
                $result_array["exterior_color_chroma"] = $result[0]["exterior_color_chroma"];
                $stm = null;
                return $result_array;
            }
        }
    }

    public static function get_interior_color_2_from_DB($area_easting, $area_northing, $context_number, $sample_number) {
        $result_array = array(
            "interior_color_hue" => "",
            "interior_color_lightness_value" => "",
            "interior_color_chroma" => ""
        );

        if($area_easting == "" or $area_northing == "" or $context_number == "" or $sample_number == "") {
            return $result_array;
        } else {
            $sql = "SELECT interior_color_hue, interior_color_lightness_value, interior_color_chroma FROM samples.samples WHERE area_easting=:area_easting AND area_northing=:area_northing AND context_number=:context_number AND sample_number=:sample_number";
            $stm = self::get_db()->prepare($sql);
            $stm->execute(array(
                "area_easting" => $area_easting,
                "area_northing" => $area_northing,
                "context_number" => $context_number,
                "sample_number" => $sample_number
            ));
            $result = $stm->fetchAll(PDO::FETCH_ASSOC);
            if(count($result) == 0 ){
                $stm = null;
                return $result_array;
            } else {
                $result_array["interior_color_hue"] = $result[0]["interior_color_hue"];
                $result_array["interior_color_lightness_value"] = $result[0]["interior_color_lightness_value"];
                $result_array["interior_color_chroma"] = $result[0]["interior_color_chroma"];
                $stm = null;
                return $result_array;
            }
        }
    }

    public static function upload_image($upload_path) {
        $uploaddir = '/var/www/uploads/';
        $uploadfile = $uploaddir . basename($_FILES['userfile']['name']);

    }

    public static function get_image_base_path() {
        $sql = "SELECT  property_value FROM options.procedure_properties WHERE \"property\"='base_image_path'";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        return array("base_image_path" => $result[0]["property_value"]);
    }

    public static function get_sample_subpath() {
        $sql = "SELECT  property_value FROM options.procedure_properties WHERE \"property\"='sample_subpath'";
        $stm = self::get_db()->prepare($sql);
        $stm->execute();
        $result = $stm->fetchAll(PDO::FETCH_ASSOC);
        return array("sample_subpath" => $result[0]["property_value"]);
    }

    public static function json_output($a_string) {
        return json_encode($a_string);
    }


} 
