-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 12 déc. 2024 à 13:19
-- Version du serveur : 8.0.31
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `security_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `id_employee` int NOT NULL AUTO_INCREMENT,
  `last_name` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `photo_url` varchar(255) DEFAULT NULL,
  `date_birth` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `date_hire` date NOT NULL,
  `id_role` int NOT NULL,
  PRIMARY KEY (`id_employee`),
  KEY `id_role` (`id_role`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `employee`
--

INSERT INTO `employee` (`id_employee`, `last_name`, `first_name`, `photo_url`, `date_birth`, `phone_number`, `email`, `address`, `date_hire`, `id_role`) VALUES
(1, 'ren', 'nat', 'faces/1.jpg', '0000-00-00', '0613548658', 'nfugsduf@gmail.com', '7 rue mgl du biz', '0000-00-00', 1);

-- --------------------------------------------------------

--
-- Structure de la table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
CREATE TABLE IF NOT EXISTS `equipment` (
  `id_equipment` int NOT NULL AUTO_INCREMENT,
  `equipment_name` varchar(50) DEFAULT NULL,
  `quantity_equipment` int NOT NULL,
  PRIMARY KEY (`id_equipment`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `equipment`
--

INSERT INTO `equipment` (`id_equipment`, `equipment_name`, `quantity_equipment`) VALUES
(1, 'Mousquetons', 15),
(2, 'Gants d’intervention', 10),
(3, 'Ceintures de sécurité tactique', 20),
(4, 'Détecteurs de métaux', 25),
(5, 'Brassards de sécurité', 30),
(6, 'Lampes torches', 5),
(7, 'Bandeaux « Agents cynophiles »', 5),
(8, 'Gilets pare-balles', 12),
(9, 'Chemises manches courtes', 30),
(10, 'Blousons', 30),
(11, 'Coupe-vents', 30),
(12, 'Talkies walkies', 20),
(13, 'Kits oreillettes', 10),
(14, 'Tasers', 5);

-- --------------------------------------------------------

--
-- Structure de la table `have`
--

DROP TABLE IF EXISTS `have`;
CREATE TABLE IF NOT EXISTS `have` (
  `id_equipment` int NOT NULL,
  `id_employee` int NOT NULL,
  PRIMARY KEY (`id_equipment`,`id_employee`),
  KEY `id_employee` (`id_employee`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `id_role` int NOT NULL AUTO_INCREMENT,
  `type_role` varchar(50) NOT NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `role`
--

INSERT INTO `role` (`id_role`, `type_role`) VALUES
(1, 'administrator'),
(2, 'security_agent');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
