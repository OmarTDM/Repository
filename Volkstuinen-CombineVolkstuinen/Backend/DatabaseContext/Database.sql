SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Maakt de database en selecteert het
CREATE DATABASE IF NOT EXISTS Volkstuinen;
USE Volkstuinen;

-- Maakt complexes table
CREATE TABLE IF NOT EXISTS `complexes` (
    `Id` int(11) NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Maakt alle bekende complexes aan voor de complexes Table
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Baandert I');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Baandert II');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Ophoven');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'De Moustem');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'De Gats');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Lahrhöfke');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Sanderbout');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Slachthuis');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Overhoven');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Braokerhofke');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Den Haof');
INSERT INTO `complexes` (`Id`, `Name`) VALUES (NULL, 'Wehrer Beemd');

-- Maakt users table met foreign key reference to complexes(id)
CREATE TABLE IF NOT EXISTS `users` (
    `Id` int(11) NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(30) NOT NULL,
    `Email` VARCHAR(255) NOT NULL,
    `Password` VARCHAR(255) NOT NULL,
    `PhoneNumber` varchar(20),
    `ZipCode` VARCHAR(20),
    `Address` VARCHAR(255),
    `Complex` int(11) NOT NULL,
    `UserType` int(3) default 1,
    `Membership` tinyint(1) default 0,
    `Payment` tinyint(1) default 0,
    PRIMARY KEY (`Id`),
    FOREIGN KEY (`Complex`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Maakt messages table met foreign key reference to complexes(id)
CREATE TABLE IF NOT EXISTS `messages` (
    `Id` int(11) NOT NULL AUTO_INCREMENT,
    `Receiver` VARCHAR(255) DEFAULT NULL,
    `Sender` VARCHAR(255) DEFAULT NULL,
    `Subject` VARCHAR(255) DEFAULT NULL,
    `Message` VARCHAR(255) DEFAULT NULL,
    `User` int(11) NOT NULL,
    `Complex` int(11) NOT NULL,
    PRIMARY KEY (`Id`),
    FOREIGN KEY (`User`) REFERENCES `users`(`Id`) ON DELETE CASCADE,
    FOREIGN KEY (`Complex`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Maakt requests table met foreign key reference to complexes(id)
CREATE TABLE IF NOT EXISTS `requests` (
    `Id` INT(11) NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(255) NOT NULL,
    `Email` VARCHAR(255) NOT NULL,
    `PhoneNumber` VARCHAR(20),
    `ZipCode` VARCHAR(20),
    `Address` VARCHAR(255),
    `Motive` text NOT NULL,
    `Complex1` INT(11) NOT NULL,
    `Complex2` INT(11),
    PRIMARY KEY (`Id`),
    FOREIGN KEY (`Complex1`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE,
    FOREIGN KEY (`Complex2`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Maakt parcel table met foreign key reference to complexes(id)
CREATE TABLE IF NOT EXISTS `parcel` (
    `Id` int(11) NOT NULL AUTO_INCREMENT,
    `Name` VARCHAR(255) NOT NULL,
    `Size` int(11) NOT NULL,
    `Complex` int(11) NOT NULL,
    `User` int(11) default null,
    PRIMARY KEY (`Id`),
    FOREIGN KEY (`User`) REFERENCES `users`(`Id`) ON DELETE CASCADE,
    FOREIGN KEY (`Complex`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Maakt parcel-requests table met foreign key reference to complexes(id) & users(id)
CREATE TABLE IF NOT EXISTS `parcel-request` (
    `Id` int(11) NOT NULL AUTO_INCREMENT,
    `Parcel` int(11) NOT NULL,
    `Motive` varchar(255) NOT NULL,
    `User` int(11) NOT NULL,
    `Complex` int(11) NOT NULL,
    PRIMARY KEY (`Id`),
    FOREIGN KEY (`Complex`) REFERENCES `complexes`(`Id`) ON DELETE CASCADE,
    FOREIGN KEY (`User`) REFERENCES `Users`(`Id`) ON DELETE CASCADE,
    FOREIGN KEY (`Parcel`) REFERENCES `parcel`(`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
COMMIT;