<?php
/**
 * Created by PhpStorm.
 * User: msenol
 * Date: 08.04.2015
 * Time: 11:56
 */

class PgDB {

    private $dbConnection;


    function __construct() {
        $this->dbConnection = new PDO('pgsql:dbname=' . PG_DB .';host=' . PG_HOST . ';user=' . PG_USERNAME . ';password=' . PG_PASSWORD);

        $this->dbConnection->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        $this->dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }

    function getDB() {
        return $this->dbConnection;

    }
} 