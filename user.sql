SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `name` char(64) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phoneNo` int(8) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `user` (`name`, `email`, `password`, `phoneNo`) VALUES
('Amy Chan', 'amychan@gmail.com', 'iloveamy1', '91237789'),
('Ben Lim', 'benlim@gmail.com', 'weatherhot8', '87734672'),
('Chan Jun Jie', 'chanjunjie@gmail.com', 'iamcjj00', '90013008'),
('Daphne Tan', 'daphnetan@gmail.com', 'nyc88brooklyn', '97653303'),
('Evan Teo', 'evanteo@gmail.com', 'evanoet90', '81919089'),
('jerms','jerms@gmail.com','jerms123','82023613');
COMMIT;
