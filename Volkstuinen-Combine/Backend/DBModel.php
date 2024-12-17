<?php
require_once __DIR__ . "/DatabaseContext/Database.php";

class DBModel
{
    protected static string $table_name;
    protected static string $primary_key;
    protected static array $errors = [];
    protected array $properties = [];
    protected PDO $conn;

    public function __construct()
    {
        $this->conn = Database::GetConnection();
    }

    public function __set($property, $value)
    {
        $this->properties[$property] = $value;
    }

    public function __get($property)
    {
        return $this->properties[$property] ?? null;
    }

    protected static function executeQuery(string $sql, array $params = [])
    {
        $stmt = Database::GetConnection()->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function findAll(): array
    {
        $sql = "SELECT * FROM " . static::$table_name;
        return static::executeQuery($sql);
    }

    public function findById($id): array|bool
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . static::$primary_key . " = :id LIMIT 1";
        $result = static::executeQuery($sql, [':id' => $id]);
        return !empty($result) ? $result[0] : false;
    }

    public function Search( $secondary_key, $secondary_SearchTerm): array
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . $secondary_key . " = :secondary_SearchTerm";
        return static::executeQuery($sql, [':secondary_SearchTerm' => $secondary_SearchTerm]);
    }
    public function SearchWithConstraints( $secondary_key, $tertiary_key, $tertiary_SearchTerm , $secondary_SearchTerm): array|bool
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . $tertiary_key . " = :tertiary_SearchTerm AND " . $secondary_key . " = :secondary_SearchTerm";
        return static::executeQuery($sql, [':secondary_SearchTerm' => $secondary_SearchTerm,':tertiary_SearchTerm' => $tertiary_SearchTerm]);
    }

    public function Create(): bool
    {
        $columns = array_keys($this->properties);
        $placeholders = array_map(fn($col) => ":$col", $columns);
        $sql = "INSERT INTO " . static::$table_name . " (" . implode(', ', $columns) . ") VALUES (" . implode(', ', $placeholders) . ")";
        $stmt = $this->conn->prepare($sql);

        foreach ($this->properties as $key => $value)
        {
            $stmt->bindValue(":$key", $value);
        }

        return $stmt->execute();
    }

    public function Update($id): bool
    {
        $columns = array_keys($this->properties);
        $setClause = implode(', ', array_map(fn($col) => "$col = :$col", $columns));
        $sql = "UPDATE " . static::$table_name . " SET $setClause WHERE " . static::$primary_key . " = :id";
        $stmt = $this->conn->prepare($sql);

            foreach ($this->properties as $key => $value)
            {
            $stmt->bindValue(":$key", $value);
        }

        $stmt->bindValue(":id", $id);
        return $stmt->execute();
    }
    public function Delete($id): bool
    {
        $sql = "DELETE FROM " . static::$table_name . " WHERE " . static::$primary_key . " = :id";
        $stmt = $this->conn->prepare($sql);
        $stmt->bindValue(":id", $id);
        return $stmt->execute();
    }
}
