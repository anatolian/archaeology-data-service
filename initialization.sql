-- CREATE TABLE finds (
--     utm_hemisphere CHARACTER(1),
--     utm_zone INTEGER,
--     context_utm_easting_meters INTEGER,
--     context_utm_northing_meters INTEGER,
--     find_number INTEGER,
--     longitude_decimal_degrees NUMERIC(6, 3),
--     latitude_decimal_degrees NUMERIC(6, 3),
--     utm_easting_meters NUMERIC(6, 3),
--     utm_northing_meters NUMERIC(6, 3),
--     material_general VARCHAR,
--     material_specific VARCHAR,
--     category_general VARCHAR,
--     category_specific VARCHAR,
--     weight_kilograms NUMERIC(6, 3),
--     PRIMARY KEY(utm_hemisphere, utm_zone, context_utm_easting_meters, context_utm_northing_meters, find_number)
-- );
INSERT INTO finds VALUES ('N', 35, 123456, 567890, 1, 38.963, 35.243, 100.3, 27.6, 'ceramic', 'painted', 'pottery', 'bowl', 27.3);
INSERT INTO finds VALUES ('N', 35, 123456, 567890, 2, 38.963, 35.243, 100.3, 27.6, 'metal', 'copper', 'jewelry', 'bracelet', 27.3);
INSERT INTO finds VALUES ('N', 35, 123456, 098765, 1, 38.963, 35.243, 100.3, 27.6, 'ceramic', 'painted', 'pottery', 'bowl', 27.3);
INSERT INTO finds VALUES ('N', 35, 654321, 098765, 1, 38.963, 35.243, 100.3, 27.6, 'ceramic', 'painted', 'pottery', 'bowl', 27.3);
INSERT INTO finds VALUES ('N', 35, 654321, 567890, 1, 38.963, 35.243, 100.3, 27.6, 'metal', 'silver', 'jewelry', 'necklace', 27.3);
INSERT INTO finds VALUES ('N', 35, 654321, 567890, 2, 38.963, 35.243, 100.3, 27.6, 'ceramic', 'painted', 'pottery', 'bowl', 27.3);
-- CREATE TABLE finds_colors (
-- 	   utm_hemisphere CHARACTER(1),
--     utm_zone INTEGER,
--     context_utm_easting_meters INTEGER,
--     context_utm_northing_meters INTEGER,
--     find_number INTEGER,
--     color_location VARCHAR,
--     munsell_hue_number NUMERIC(6, 3),
--     munsell_hue_letter CHARACTER(1),
--     munsell_lightness_value NUMERIC(6, 3),
--     munsell_chroma NUMERIC(6, 3),
--     rgb_red_256_bit INTEGER,
--     rgb_green_256_bit INTEGER,
--     rgb_blue_256_bit INTEGER,
-- 	PRIMARY KEY(utm_hemisphere, utm_zone, context_utm_easting_meters, context_utm_northing_meters, find_number, color_location)
-- );
INSERT INTO finds_colors VALUES ('N', 35, 123456, 567890, 1, 'interior', 10.2, 'R', 20.4, 12.0, 255, 0, 0);
INSERT INTO finds_colors VALUES ('N', 35, 123456, 567890, 1, 'exterior', 20.4, 'G', 10.2, 13.0, 0, 255, 0);
INSERT INTO finds_colors VALUES ('N', 35, 123456, 567890, 2, 'interior', 10.2, 'B', 20, 1, 0, 0, 255);
INSERT INTO finds_colors VALUES ('N', 35, 123456, 567890, 2, 'exterior', 20.4, 'B', 3, 2, 0, 0, 255);
INSERT INTO finds_colors VALUES ('N', 35, 123456, 098765, 1, 'interior', 10.2, 'R', 20.4, 14.0, 0, 0, 255);
INSERT INTO finds_colors VALUES ('N', 35, 123456, 098765, 1, 'exterior', 10.2, 'R', 20.4, 14.0, 0, 0, 255);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 098765, 1, 'interior', 10.2, 'R', 20.4, 15.0, 255, 0, 255);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 098765, 1, 'exterior', 10.2, 'R', 3, 4, 255, 255, 255);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 567890, 1, 'interior', 20.4, 'B', 10.2, 16.0, 255, 255, 0);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 567890, 1, 'exterior', 20.4, 'G', 10.2, 16.0, 255, 255, 255);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 567890, 2, 'interior', 10.2, 'R', 20.4, 17.0, 0, 255, 255);
INSERT INTO finds_colors VALUES ('N', 35, 654321, 567890, 2, 'exterior', 10.2, 'R', 20.3, 110, 0, 0, 0);
DROP TABLE IF EXISTS Properties;
CREATE TABLE Properties (
    label VARCHAR,
    value VARCHAR,
    PRIMARY KEY(label)
);