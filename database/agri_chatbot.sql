-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 01, 2023 at 07:16 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `agri_chatbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ag_data`
--

CREATE TABLE `ag_data` (
  `id` int(11) NOT NULL,
  `query` varchar(200) NOT NULL,
  `answer` text NOT NULL,
  `voice_note` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ag_data`
--

INSERT INTO `ag_data` (`id`, `query`, `answer`, `voice_note`) VALUES
(1, 'How to grow Rice?', ' A monthly rainfall of 100-200 mm. The sowing time of Madhu rice are Kharif (April – September), Rabi (October – December), Summer/Zaid (January – March).', 'A1a1.mp3'),
(2, 'How much water to add for Wheat?', 'The amount of rainfall required for wheat cultivation varies between 30 cm and 100 cm. A crop requires 450-650 mm of available water per year.', ''),
(3, 'Yield of wheat?', 'Yield potential of approximately 1.5 bushels per acre. When applying a starter fertilizer for wheat, application methods and rates are much more flexible with phosphorus than nitrogen.', ''),
(4, 'Average yield of rice', ' It requires 800 mm to 1,200 mm of water with extremes between 520 mm and 2,550 mm during the growing season.', ''),
(5, 'Sugarcane', 'Rainfall: 100 cm to 175 cm rainfall is ideal for sugarcane production.  It grows well in deep, well-drained soils of medium fertility of sandy loam soil textures with a pH range from 6.0 to 7.7.', '');

-- --------------------------------------------------------

--
-- Table structure for table `ag_user`
--

CREATE TABLE `ag_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ag_user`
--

INSERT INTO `ag_user` (`id`, `name`, `mobile`, `email`, `address`, `uname`, `pass`, `create_date`) VALUES
(1, 'Ganesh', 8956214752, 'ganesh@gmail.com', '45, GD Nagar, Thanjavur', 'ganesh', '123456', '28-02-2023');
