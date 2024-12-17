<?php
const DB_HOST = 'localhost';
const DB_USER = 'root';
const DB_PASS = '';
const DB_NAME = 'Volkstuinen';

class Database
{
    private static $connection = null;

    private function __construct() {} // Prevent direct instantiation

    public static function GetConnection()
    {
        if (self::$connection === null)
        {
            $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ];
            try
            {
                self::$connection = new PDO($dsn, DB_USER, DB_PASS, $options);
            }
            catch (PDOException $e)
            {
                error_log('Database connection error: ' . $e->getMessage());
                throw new Exception('Could not connect to the database. Please try again later.');
            }
        }
        return self::$connection;
    }

    public static function InitializeDatabase()
    {
        $connection = self::GetConnection();
        $sqlFilePath = __DIR__ . "/Database.sql";
        if (!file_exists($sqlFilePath))
        {
            error_log("SQL file not found: " . $sqlFilePath);
            echo "Initialization failed: SQL file missing.";
            return;
        }

        try
        {
            $connection->beginTransaction();
            $sql = file_get_contents($sqlFilePath);
            $connection->exec($sql);
            $connection->commit();
            echo "Database initialized successfully.";
        }
        catch (PDOException $e)
        {
            $connection->rollBack();
            error_log('Database initialization error: ' . $e->getMessage());
            echo 'Database initialization failed. Check the error log for details.';
        }
    }
}