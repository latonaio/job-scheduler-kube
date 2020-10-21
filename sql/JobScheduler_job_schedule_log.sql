-- MySQL dump 10.13  Distrib 5.7.29, for Linux (aarch64)
--
-- Host: 127.0.0.1    Database: JobScheduler
-- ------------------------------------------------------
-- Server version	5.5.5-10.2.32-MariaDB-1:10.2.32+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `job_schedule_log`
--

DROP TABLE IF EXISTS `job_schedule_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_schedule_log` (
  `log_id` int(11) NOT NULL,
  `log_date` datetime NOT NULL,
  `job_id` int(11) DEFAULT NULL,
  `schedule_id` int(11) DEFAULT NULL,
  `repeat_type` int(11) DEFAULT NULL COMMENT '1: every month, 2: every week, 3: every day, 4: once',
  `repeat_date` int(11) DEFAULT NULL COMMENT '1-28',
  `repeat_week_day` int(11) DEFAULT NULL COMMENT '1-7',
  `repeat_hour` int(11) DEFAULT NULL COMMENT '0-23',
  `repeat_minute` int(11) DEFAULT NULL COMMENT '0-59',
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_schedule_log`
--

LOCK TABLES `job_schedule_log` WRITE;
/*!40000 ALTER TABLE `job_schedule_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_schedule_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-25 11:34:19
