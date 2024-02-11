CREATE DATABASE  IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `mydb`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` int NOT NULL,
  `admin_pass` varchar(255) NOT NULL,
  `admin_name` varchar(255) NOT NULL,
  `phone_number` int DEFAULT NULL,
  `admin_email` varchar(255) DEFAULT NULL,
  `admin_picture_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_email` (`admin_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (3001,'admin1','Ahmad',7785452,'admin1@gmail.com','Pictures/Admin/Ahmad.jpg'),(3002,'admin2','Hassan',7865452,'admin2@gmail.com','Pictures/Admin/Hassan.jpg'),(3003,'admin3','Mohammed',7945213,'admin3@gmail.com','Pictures/Admin/Mohammed.jpg');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `availability`
--

DROP TABLE IF EXISTS `availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `availability` (
  `book_id` int NOT NULL,
  `no_of_copies` int NOT NULL,
  PRIMARY KEY (`book_id`),
  CONSTRAINT `availability_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `availability`
--

LOCK TABLES `availability` WRITE;
/*!40000 ALTER TABLE `availability` DISABLE KEYS */;
INSERT INTO `availability` VALUES (2001,2),(2002,4),(2003,6),(2004,7),(2005,2),(2006,1),(2007,5),(2008,8),(2009,7),(2010,3),(2011,6),(2012,5),(2013,4),(2014,8),(2015,9),(2016,6),(2017,2),(2018,10);
/*!40000 ALTER TABLE `availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `book_id` int NOT NULL,
  `book_title` varchar(255) DEFAULT NULL,
  `book_author` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL,
  `specialty` varchar(255) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `book_picture_path` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (2001,'Java for absolute beginners','Luliana cosmina','Code',1,'Java',0,'Pictures/Book/2001.jpg','Shelf A, First Row (From the top)'),(2002,'Effective Java','Joshua Bloch','Code',1,'Java',1,'Pictures/Book/2002.jpg','Shelf A, Second Row (From the top)'),(2003,'Java Concurrency in Practice','Brain Goetz','Code',1,'Java',2,'Pictures/Book/2003.jpg','Shelf A, Third Row (From the top)'),(2004,'Python Crash Course','Eric Matthes','Code',1,'Python',0,'Pictures/Book/2004.jpg','Shelf B, First Row (From the top)'),(2005,'Fluent Python','Luciano Ramalho','Code',1,'Python',1,'Pictures/Book/2005.jpg','Shelf B, Second Row (From the top)'),(2006,'Flask Web Development','Miguel Grinberg ','Web',1,'Python',2,'Pictures/Book/2006.jpg','Shelf B, Third Row (From the top)'),(2007,'HTML and CSS: Design and Build Websites','Jon Duckett','Web',1,'HTML/CSS',0,'Pictures/Book/2007.jpg','Shelf C, First Row (From the top)'),(2008,'JavaScript for Kids','Nick Morgan','Web',1,'JavaScript',0,'Pictures/Book/2008.jpg','Shelf D, First Row (From the top)'),(2009,'C Programming Absolute Beginner\'s Guide','Perry, Miller, and Haner','Code',1,'C',0,'Pictures/Book/2009.jpg','Shelf F, Third Row (From the top)'),(2010,'Eloquent JavaScript','Marijn Haverbeke','Web',1,'JavaScript',1,'Pictures/Book/2010.jpg','Shelf D, Second Row (From the top)'),(2011,'Head First Java','Kathy Sierra','Code',1,'Java',1,'Pictures/Book/2011.jpg','Shelf A, Fourth Row (From the top)'),(2012,'JavaScript: The Good Parts','Douglas Crockford','Web',1,'JavaScript',2,'Pictures/Book/2012.jpg','Shelf D, Third Row (From the top)'),(2013,'C++ Primer','Stanley B. Lippman','Code',1,'C++',0,'Pictures/Book/2013.jpg','Shelf E, First Row (From the top)'),(2014,'Accelerated C++: Practical Programming','Andrew Koeing','Code',1,'C++',0,'Pictures/Book/2014.jpg','Shelf E, Second Row (From the top)'),(2015,'Effective Modern C++','Scott Meyers','Code',1,'C++',1,'Pictures/Book/2015.jpg','Shelf E, Third Row (From the top)'),(2016,'Modern C++ Design: Generic Programming and Design Patterns Applied','Andrei Alexandrescu','Code',1,'C++',2,'Pictures/Book/2016.jpg','Shelf E, Fourth Row (From the top)'),(2017,'CSS Secrets: Better Solutions to Everyday Web Design Problems','Lea Verou','Web',1,'HTML/CSS',1,'Pictures/Book/2017.jpg','Shelf C, Second Row (From the top)'),(2018,'Responsive Web Design with HTML5 and CSS3','Ben Frain','Web',1,'HTML/CSS',2,'Pictures/Book/2018.jpg','Shelf C, Third Row (From the top)');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` int NOT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `book_id` int DEFAULT NULL,
  `specialty` varchar(255) DEFAULT NULL,
  `difficulty` int DEFAULT NULL,
  `prerequisite_course` int DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (4001,'Introduction to IT','Code',2001,'Java',0,NULL),(4002,'Object-oriented Programming','Code',2002,'Java',1,4001),(4003,'Data Structures','Code',2003,'Java',2,4002),(4004,'C++ for Beginners','Code',2013,'C++',0,NULL),(4005,'Intermediate C++','Code',2015,'C++',1,4004),(4006,'C++ Advanced','Code',2016,'C++',2,4005),(4007,'Web Application development','Web',2007,'HTML/CSS',0,NULL),(4008,'Web Application development 2','Web',2017,'HTML/CSS',1,4007),(4009,'Web Application development 3','Web',2018,'HTML/CSS',2,4008),(4010,'Introduction to JavaScript','Web',2008,'JavaScript',0,NULL),(4011,'JavaScript for web development','Web',2010,'JavaScript',1,4010),(4012,'Advanced JavaScript','Web',2012,'JavaScript',2,4011),(4013,'Visual Programming','Code',2009,'C',0,NULL),(4014,'Python','Code',2004,'Python',0,NULL),(4015,'Intermediate Python','Code',2005,'Python',1,4014),(4016,'Advanced Python','Code',2006,'Python',2,4015);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `st_id` int NOT NULL,
  `course_id` int NOT NULL,
  `grade` int NOT NULL,
  `pass` tinyint(1) NOT NULL,
  PRIMARY KEY (`st_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`st_id`) REFERENCES `student` (`st_id`),
  CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1001,4001,80,1),(1001,4002,40,0),(1001,4004,20,0),(1001,4007,100,1),(1001,4010,60,1),(1002,4001,60,1),(1002,4002,10,0),(1002,4010,100,1),(1002,4011,100,1),(1003,4013,10,0),(1003,4014,70,1),(1003,4015,50,1),(1004,4001,100,1),(1004,4004,100,1),(1005,4007,100,1),(1005,4008,80,1),(1005,4009,65,1),(1006,4010,65,1),(1006,4011,15,0);
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `st_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`st_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`st_id`) REFERENCES `student` (`st_id`),
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
INSERT INTO `history` VALUES (1001,2001),(1002,2002),(1003,2004),(1004,2004),(1005,2006),(1002,2010),(1001,2013);
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preference`
--

DROP TABLE IF EXISTS `preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preference` (
  `st_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`st_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `preference_ibfk_1` FOREIGN KEY (`st_id`) REFERENCES `student` (`st_id`),
  CONSTRAINT `preference_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preference`
--

LOCK TABLES `preference` WRITE;
/*!40000 ALTER TABLE `preference` DISABLE KEYS */;
INSERT INTO `preference` VALUES (1001,2001),(1004,2004),(1005,2006),(1002,2010);
/*!40000 ALTER TABLE `preference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `st_id` int NOT NULL,
  `st_pass` varchar(255) NOT NULL,
  `st_email` varchar(255) DEFAULT NULL,
  `st_name` varchar(255) NOT NULL,
  `penalized` tinyint(1) NOT NULL,
  `st_picture_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`st_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1001,'password','michael@gmail.com','Michael',0,'Pictures/Students/Michael.jpg'),(1002,'password','noor@gmail.com','Noor',0,'Pictures/Students/Noor.jpg'),(1003,'password','osama@gmail.com','Osama',1,'Pictures/Students/Osama.jpg'),(1004,'password','khalil@gmail.com','Khalil',0,'Pictures/Students/Khalil.jpg'),(1005,'password','ahmad@gmail.com','Ahmad',0,'Pictures/Students/Ahmad.jpg'),(1006,'password','abdullah@gmail.com','Abdullah',1,'Pictures/Students/Abdullah.jpg');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-25 11:48:03
