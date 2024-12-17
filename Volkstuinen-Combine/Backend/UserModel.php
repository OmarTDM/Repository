<?php
require_once __DIR__ . "/DatabaseContext/Database.php";
class UserModel
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

    public function findAllUsers(): array
    {
        $sql = "SELECT * FROM " . static::$table_name;
        return static::executeQuery($sql);
    }

    public function findByIdUser($id): array
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . static::$primary_key . " = :id LIMIT 1";
        return static::executeQuery($sql, [':id' => $id]);
    }

    public function SearchUser($secondary_key, $secondary_SearchTerm): array
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . $secondary_key . " = :secondary_SearchTerm";
        return static::executeQuery($sql, [':secondary_SearchTerm' => $secondary_SearchTerm]);
    }
    public function SearchConstraintUsers( $secondary_key, $tertiary_key, $tertiary_SearchTerm , $secondary_SearchTerm): array
    {
        $sql = "SELECT * FROM " . static::$table_name . " WHERE " . $tertiary_key . " = :tertiary_SearchTerm AND " . $secondary_key . " = :secondary_SearchTerm";
        return static::executeQuery($sql, [':secondary_SearchTerm' => $secondary_SearchTerm,':tertiary_SearchTerm' => $tertiary_SearchTerm]);

    }

    public function CreateUser(): bool
    {
        if (!isset($this->properties['Password']) || empty($this->properties['Password']))
        {
            throw new Exception('Password is required');
        }
        $hashedPassword = password_hash($this->properties['Password'], PASSWORD_BCRYPT);
        $columns = array_keys($this->properties);
        $placeholders = array_map(function ($col)
        {
            return ":$col";
        }, $columns);
        $sql = "INSERT INTO " . static::$table_name . " (" . implode(", ", $columns) . ") 
            VALUES (" . implode(", ", $placeholders) . ")";

        $stmt = $this->conn->prepare($sql);
        foreach ($this->properties as $key => $value)
        {
            if ($key === 'Password')
            {
                $stmt->bindValue(":$key", $hashedPassword);
            }
            else
            {
                $stmt->bindValue(":$key", $value);
            }
        }
        return $stmt->execute();
    }

    public function LoginUser($Identifier, $Password): bool
    {
        $hashedPassword = password_hash($this->$Password, PASSWORD_BCRYPT);
        $sql = "SELECT * FROM " . static::$table_name . " WHERE Email = :identifier1 OR Name = :identifier2 LIMIT 1";
        $stmt = $this->conn->prepare($sql);
        $stmt->bindValue(":identifier1", $Identifier);
        $stmt->bindValue(":identifier2", $Identifier);
        $stmt->execute();
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$user)
        {
            return false;
        }
        if (password_verify($hashedPassword, $user['Password']))
        {
            $_SESSION['user_id'] = $user['Id'];
            $_SESSION['user_name'] = $user['Name'];
            $_SESSION['user_email'] = $user['Email'];
            $_SESSION['user_complex'] = $user['Complex'];
            $_SESSION['user_type'] = $user['UserType'];
            return true;
        }
        return false;
    }

    public function UpdateUser($id): bool
    {
        $hashedPassword = password_hash($this->properties['Password'], PASSWORD_BCRYPT);
        $columns = array_keys($this->properties);
        $setClause = implode(', ', array_map(fn($col) => "$col = :$col", $columns));
        $sql = "UPDATE " . static::$table_name . " SET $setClause WHERE " . static::$primary_key . " = :id";
        $stmt = $this->conn->prepare($sql);

        foreach ($this->properties as $key => $value)
        {
            if ($key === 'Password')
            {
                $stmt->bindValue(":$key", $hashedPassword);
            }
            else
            {
                $stmt->bindValue(":$key", $value);
            }
        }
        $stmt->bindValue(":id", $id);
        return $stmt->execute();
    }

    public function DeleteUser($id): bool
    {
        $sql = "DELETE FROM " . static::$table_name . " WHERE " . static::$primary_key . " = :id";
        $stmt = $this->conn->prepare($sql);
        $stmt->bindValue(":id", $id);
        return $stmt->execute();
    }
}