<?php

/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

	function watermark_text($oldimage_name, $water_mark_text_2){
	//echo $oldimage_name;
	//echo "<br>";
	//echo $new_image_name;
            echo $oldimage_name;
    $label_placement = "right-top";
    $text_height=1;
    $text_width=1;  
    $main_height=1;
    $main_width=1;
    $posx_text=1;
    $posy_text=1;
    $posx_image=1;
    $posy_image=1;
    $image_main=1;
    		
  $font_path = "times.ttf";
  $font_size = "200";
  
  echo "watermark  $water_mark_text_2";
  $type_space = imagettfbbox($font_size, 0, $font_path, $water_mark_text_2);
			
		$image_width = abs($type_space[4] - $type_space[0]);
		$image_height = abs($type_space[5] - $type_space[1]);
    echo "imw $image_width imh $image_height";
   list($owidth,$oheight) = getimagesize($oldimage_name);
  
    $width = $owidth;
	$height = $oheight; 
        
        echo "width $width and h $height";
	//$font_size=25; 
	//$label_placement="right-bottom";
	if($label_placement=="top-left")
	{
	$text_width=$width;
	$text_height=$image_height+10;	
	$posx=10; 
	$posy=$image_height+5;
	$angel=0;
	$posx_text=0;
	$posy_text=0;
	$posx_image=0;
	$posy_image=$text_height;
	$image_main = imagecreatetruecolor($width,$text_height+$height);
	
	
	}
	elseif($label_placement=="top-center")
	{
		$text_width=$width;
	    $text_height=$image_height+10;
		$posx=($width/2)-abs($image_width/2); 
		$posy=$image_height+5;
		$angel=0;
		$posx_text=0;
		$posy_text=0;
		$posx_image=0;
		$posy_image=$text_height;
		//$image_main = imagecreate($width,$text_height+$height);
		$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	elseif($label_placement=="top-right")
	{
		$text_width=$width;
	    $text_height=$image_height+10;
		$posx=$width-$image_width-10; 
		$posy=$image_height+5;
		$angel=0;
		$posx_text=0;
		$posy_text=0;
		$posx_image=0;
		$posy_image=$text_height;
		$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	elseif($label_placement=="bottom-left")
	{
		$text_width=$width;
	    $text_height=$image_height+10;
		$posx=10; 
		$posy=$image_height+5;
		$angel=0;
		$posx_text=0;
		$posy_text=$height;
		$posx_image=0;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	elseif($label_placement=="bottom-center")
	{
		$text_width=$width;
	    $text_height=$image_height+10;
		$posx=($width/2)-abs($image_width/2);
		$posy=$image_height+5;
		$angel=0;
		$posx_text=0;
		$posy_text=$height;
		$posx_image=0;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	elseif($label_placement=="bottom-right")
	{
		$text_width=$width;
	    $text_height=$image_height+10;
		$posx=$width-$image_width-10; 
		$posy=$image_height+5;
		$angel=0;
		$posx_text=0;
		$posy_text=$height;
		$posx_image=0;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	elseif($label_placement=="left-top")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=$image_width+10;
		$angel=90;
		$posx_text=0;
		$posy_text=0;
		$posx_image=$text_width;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	elseif($label_placement=="left-center")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=($height/2)+abs($image_width/2);
		$angel=90;
		$posx_text=0;
		$posy_text=0;
		$posx_image=$text_width;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	elseif($label_placement=="left-bottom")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=$height-10;
		$angel=90;
		$posx_text=0;
		$posy_text=0;
		$posx_image=$text_width;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	elseif($label_placement=="right-top")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=$image_width+10;
		$angel=90;
		$posx_text=$width;
		$posy_text=0;
		$posx_image=0;
		$posy_image=0;
                echo "in right -top $width+$text_width posx $posx";
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	elseif($label_placement=="right-center")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=($height/2)+abs($image_width/2);
		$angel=90;
		$posx_text=$width;
		$posy_text=0;
		$posx_image=0;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	elseif($label_placement=="right-bottom")
	{
		$text_width=$image_height+10;
	    $text_height=$height;
		$posx=$image_height+5; 
		$posy=$height-10;
		$angel=90;
		$posx_text=$width;
		$posy_text=0;
		$posx_image=0;
		$posy_image=0;
		$image_main = imagecreatetruecolor($width+$text_width,$height);
	}
	else
	{
	$text_width=$width;
	$text_height=$image_height+10;	
	$posx=10; 
	$posy=$image_height+5;
	$angel=0;
	$posx_text=0;
	$posy_text=0;
	$posx_image=0;
	$posy_image=$text_height;
	$image_main = imagecreatetruecolor($width,$text_height+$height);
	}
	
    $image = imagecreatetruecolor($width, $height);
	$info   = getimagesize($oldimage_name);
	$type   = $info['mime'];
	
	if($type=='image/png')
	{
		$image_src = imagecreatefrompng($oldimage_name);
	}
	else
	{
    $image_src = imagecreatefromjpeg($oldimage_name);
	}
	$image1 = imagecreate($text_width,$text_height);
	$black1 = imagecolorallocate($image1, 255, 255, 255);
    $oranage1 = imagecolorallocate($image1, 0, 0, 0);
	 imagettftext($image1, $font_size, $angel, $posx,$posy, $oranage1, $font_path, $water_mark_text_2);
	
	//imagejpeg($image1, 'aaa1.jpg', 100);
    //imagedestroy($image1);
	
	//$image_src = imagecreatefromjpeg($oldimage_name);
   // imagecopyresampled($image, $image_src, 0, 0, 0, 0, $width, $height, $owidth, $oheight);
	imagecopymerge($image_main, $image1, $posx_text, $posy_text, 0, 0,$text_width,$text_height, 100);
	imagecopymerge($image_main, $image_src, $posx_image, $posy_image, 0, 0, $width, $height, 100);
	// imagejpeg($image_main, 'aaa11.jpg', 100);
	 
	//imagedestroy($image_main);
   	//$black = imagecolorallocate($image, 0, 0, 0);
    //$oranage = imagecolorallocate($image, 255, 102, 0);
	//echo $water_mark_text_2;
   // imagettftext($image, $font_size, 0, 30, 190, $black, $font_path, $water_mark_text_1);
   //imagettftext($image, $font_size, $angel, $posx , $posy, $oranage, $font_path, $water_mark_text_2);
    imagejpeg($image_main, $oldimage_name, 100);
	
	//imagejpeg($image_main, 'aaa1.jpg', 100);
	imagedestroy($image_src);
	imagedestroy($image1);
    imagedestroy($image_main);
    return true;
}