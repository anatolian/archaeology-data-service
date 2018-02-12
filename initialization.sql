DROP TABLE IF EXISTS Samples;
CREATE TABLE Samples (
    area_easting INTEGER,
    area_northing INTEGER,
    context_number INTEGER,
    sample_number INTEGER,
    material VARCHAR(10),
    exterior_color_hue VARCHAR(10),
    exterior_color_lightness_value VARCHAR(10),
    exterior_color_chroma VARCHAR(10),
    interior_color_hue VARCHAR(10),
    interior_color_lightness_value VARCHAR(10),
    interior_color_chroma VARCHAR(10),
    weight_kilograms NUMERIC(6, 3),
    status VARCHAR(8),
    PRIMARY KEY(area_easting, area_northing, context_number, sample_number)
);
INSERT INTO Samples VALUES (30, 40, 3, 4, 'clay', '10R', '5', '3', '5YR', '6', '4', 0, 'active');
INSERT INTO Samples VALUES (50, 60, 4, 5, 'ceramic', '8YR', '3', '2', '6R', '1', '1', 88, 'active');
INSERT INTO Samples VALUES (11, 21, 1, 5, 'metal', '10R', '5', '3', '5YR', '6', '4', 123.0, 'active');
INSERT INTO Samples VALUES (10, 20, 1, 1, 'stone', 'brown', 'light_br', 'brownish', 'red', 'light_red', 'reddish', 0.163, 'active');
DROP TABLE IF EXISTS Areas;
CREATE TABLE Areas (
	area_easting INTEGER,
	area_northing INTEGER,
	area_key VARCHAR(10),
	status VARCHAR(8),
	PRIMARY KEY(area_easting, area_northing)
);
INSERT INTO Areas VALUES (10, 20, '10.20', 'active');
INSERT INTO Areas VALUES (11, 21, '11.21', 'active');
INSERT INTO Areas VALUES (30, 40, '30.40', 'active');
INSERT INTO Areas VALUES (50, 60, '50.60', 'active');
DROP TABLE IF EXISTS Properties;
CREATE TABLE Properties (
    label VARCHAR(40),
    value VARCHAR(100),
    PRIMARY KEY(label)
);