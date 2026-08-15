-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: employee_system
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can view user',1,'view_user'),(5,'Can add log entry',2,'add_logentry'),(6,'Can change log entry',2,'change_logentry'),(7,'Can delete log entry',2,'delete_logentry'),(8,'Can view log entry',2,'view_logentry'),(9,'Can add permission',4,'add_permission'),(10,'Can change permission',4,'change_permission'),(11,'Can delete permission',4,'delete_permission'),(12,'Can view permission',4,'view_permission'),(13,'Can add group',3,'add_group'),(14,'Can change group',3,'change_group'),(15,'Can delete group',3,'delete_group'),(16,'Can view group',3,'view_group'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add branch',7,'add_branch'),(26,'Can change branch',7,'change_branch'),(27,'Can delete branch',7,'delete_branch'),(28,'Can view branch',7,'view_branch'),(29,'Can add company setting',12,'add_companysetting'),(30,'Can change company setting',12,'change_companysetting'),(31,'Can delete company setting',12,'delete_companysetting'),(32,'Can view company setting',12,'view_companysetting'),(33,'Can add product',16,'add_product'),(34,'Can change product',16,'change_product'),(35,'Can delete product',16,'delete_product'),(36,'Can view product',16,'view_product'),(37,'Can add activity log',8,'add_activitylog'),(38,'Can change activity log',8,'change_activitylog'),(39,'Can delete activity log',8,'delete_activitylog'),(40,'Can view activity log',8,'view_activitylog'),(41,'Can add attendance',9,'add_attendance'),(42,'Can change attendance',9,'change_attendance'),(43,'Can delete attendance',9,'delete_attendance'),(44,'Can view attendance',9,'view_attendance'),(45,'Can add backup',10,'add_backup'),(46,'Can change backup',10,'change_backup'),(47,'Can delete backup',10,'delete_backup'),(48,'Can view backup',10,'view_backup'),(49,'Can add branch evaluation',11,'add_branchevaluation'),(50,'Can change branch evaluation',11,'change_branchevaluation'),(51,'Can delete branch evaluation',11,'delete_branchevaluation'),(52,'Can view branch evaluation',11,'view_branchevaluation'),(53,'Can add message',14,'add_message'),(54,'Can change message',14,'change_message'),(55,'Can delete message',14,'delete_message'),(56,'Can view message',14,'view_message'),(57,'Can add notification',15,'add_notification'),(58,'Can change notification',15,'change_notification'),(59,'Can delete notification',15,'delete_notification'),(60,'Can view notification',15,'view_notification'),(61,'Can add reward',17,'add_reward'),(62,'Can change reward',17,'change_reward'),(63,'Can delete reward',17,'delete_reward'),(64,'Can view reward',17,'view_reward'),(65,'Can add weekly ranking',18,'add_weeklyranking'),(66,'Can change weekly ranking',18,'change_weeklyranking'),(67,'Can delete weekly ranking',18,'delete_weeklyranking'),(68,'Can view weekly ranking',18,'view_weeklyranking'),(69,'Can add evaluation',13,'add_evaluation'),(70,'Can change evaluation',13,'change_evaluation'),(71,'Can delete evaluation',13,'delete_evaluation'),(72,'Can view evaluation',13,'view_evaluation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_activitylog`
--

DROP TABLE IF EXISTS `core_activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_activitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_activitylog_user_id_8705e516_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_activitylog_user_id_8705e516_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_activitylog`
--

LOCK TABLES `core_activitylog` WRITE;
/*!40000 ALTER TABLE `core_activitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_activitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_attendance`
--

DROP TABLE IF EXISTS `core_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `check_in_time` time(6) DEFAULT NULL,
  `check_out_time` time(6) DEFAULT NULL,
  `check_in_ip` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `check_out_ip` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `late_minutes` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_attendance_user_id_fdad1ea2_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_attendance_user_id_fdad1ea2_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_attendance`
--

LOCK TABLES `core_attendance` WRITE;
/*!40000 ALTER TABLE `core_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_backup`
--

DROP TABLE IF EXISTS `core_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_backup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_size` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_backup_created_by_id_961e3b8d_fk_core_user_id` (`created_by_id`),
  CONSTRAINT `core_backup_created_by_id_961e3b8d_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_backup`
--

LOCK TABLES `core_backup` WRITE;
/*!40000 ALTER TABLE `core_backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_branch`
--

DROP TABLE IF EXISTS `core_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_branch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_branch`
--

LOCK TABLES `core_branch` WRITE;
/*!40000 ALTER TABLE `core_branch` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_branchevaluation`
--

DROP TABLE IF EXISTS `core_branchevaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_branchevaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employees_score` decimal(5,2) NOT NULL,
  `admin_score` decimal(5,2) NOT NULL,
  `total_branch_score` decimal(5,2) NOT NULL,
  `week_number` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `branch_id` bigint NOT NULL,
  `evaluator_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_branchevaluation_branch_id_5687f270_fk_core_branch_id` (`branch_id`),
  KEY `core_branchevaluation_evaluator_id_efd3fa25_fk_core_user_id` (`evaluator_id`),
  CONSTRAINT `core_branchevaluation_branch_id_5687f270_fk_core_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `core_branch` (`id`),
  CONSTRAINT `core_branchevaluation_evaluator_id_efd3fa25_fk_core_user_id` FOREIGN KEY (`evaluator_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_branchevaluation`
--

LOCK TABLES `core_branchevaluation` WRITE;
/*!40000 ALTER TABLE `core_branchevaluation` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_branchevaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_companysetting`
--

DROP TABLE IF EXISTS `core_companysetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_companysetting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attendance_time` time(6) NOT NULL,
  `backup_enabled` tinyint(1) NOT NULL,
  `backup_days` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_companysetting`
--

LOCK TABLES `core_companysetting` WRITE;
/*!40000 ALTER TABLE `core_companysetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_companysetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_evaluation`
--

DROP TABLE IF EXISTS `core_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_evaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `criteria_dealing` decimal(5,2) NOT NULL,
  `criteria_accuracy` decimal(5,2) NOT NULL,
  `criteria_honesty` decimal(5,2) NOT NULL,
  `criteria_work_quality` decimal(5,2) NOT NULL,
  `total_score` decimal(5,2) NOT NULL,
  `evaluation_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `week_number` int NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `evaluated_employee_id` bigint NOT NULL,
  `evaluator_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_evaluation_evaluator_id_evaluated_e_2a16da10_uniq` (`evaluator_id`,`evaluated_employee_id`,`week_number`),
  KEY `core_evaluation_evaluated_employee_id_420772c7_fk_core_user_id` (`evaluated_employee_id`),
  CONSTRAINT `core_evaluation_evaluated_employee_id_420772c7_fk_core_user_id` FOREIGN KEY (`evaluated_employee_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_evaluation_evaluator_id_e5ed403a_fk_core_user_id` FOREIGN KEY (`evaluator_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_evaluation`
--

LOCK TABLES `core_evaluation` WRITE;
/*!40000 ALTER TABLE `core_evaluation` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_message`
--

DROP TABLE IF EXISTS `core_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `receiver_group` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `receiver_id` bigint DEFAULT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_message_receiver_id_62f2e4a8_fk_core_user_id` (`receiver_id`),
  KEY `core_message_sender_id_0ecf4560_fk_core_user_id` (`sender_id`),
  CONSTRAINT `core_message_receiver_id_62f2e4a8_fk_core_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `core_message_sender_id_0ecf4560_fk_core_user_id` FOREIGN KEY (`sender_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_message`
--

LOCK TABLES `core_message` WRITE;
/*!40000 ALTER TABLE `core_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `read_at` datetime(6) DEFAULT NULL,
  `link` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_notification_user_id_6e341aac_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_notification_user_id_6e341aac_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_product`
--

DROP TABLE IF EXISTS `core_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `offer_price` decimal(10,2) DEFAULT NULL,
  `offer_description` longtext COLLATE utf8mb4_unicode_ci,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_offer_active` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_product`
--

LOCK TABLES `core_product` WRITE;
/*!40000 ALTER TABLE `core_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_reward`
--

DROP TABLE IF EXISTS `core_reward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_reward` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `week_number` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_reward_user_id_9e21aaa9_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_reward_user_id_9e21aaa9_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_reward`
--

LOCK TABLES `core_reward` WRITE;
/*!40000 ALTER TABLE `core_reward` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_reward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `branch_id` bigint DEFAULT NULL,
  `points` decimal(7,2) NOT NULL,
  `profile_pic` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dark_mode` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `employee_code` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  `last_login_ip` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `employee_code` (`employee_code`),
  KEY `core_user_branch_id_90a0c1d9` (`branch_id`),
  CONSTRAINT `core_user_branch_id_90a0c1d9_fk_core_branch_id` FOREIGN KEY (`branch_id`) REFERENCES `core_branch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'pbkdf2_sha256$1200000$2ohtKKzlJp4xokd6CLIhta$8Ro4VEe1f4KkeOWrSi8BrRnqnlPQi24zl7MyznDo87A=','2026-07-31 20:29:25.928128',1,'w','','','w@gmail.com',1,1,'2026-07-31 20:27:25.321385','CASHIER',NULL,0.00,'',0,'2026-07-31 20:27:30.705331',NULL,NULL,'2026-07-31 20:27:30.705432',NULL),(2,'!Ywk0y0tjXE6dAx7kokCv7A8eIhP9vw08gjOmzPYc',NULL,0,'اخمد','','','',0,1,'2026-07-31 21:52:08.542324','CASHIER',NULL,0.00,'',0,'2026-07-31 21:52:08.554160',NULL,NULL,'2026-07-31 21:52:08.554208',NULL);
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_weeklyranking`
--

DROP TABLE IF EXISTS `core_weeklyranking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_weeklyranking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `week_number` int NOT NULL,
  `rank_position` int NOT NULL,
  `reward_amount` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_weeklyranking_user_id_aec5e150_fk_core_user_id` (`user_id`),
  CONSTRAINT `core_weeklyranking_user_id_aec5e150_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_weeklyranking`
--

LOCK TABLES `core_weeklyranking` WRITE;
/*!40000 ALTER TABLE `core_weeklyranking` DISABLE KEYS */;
INSERT INTO `core_weeklyranking` VALUES (1,1,30,100.00,'2026-07-31 21:52:35.639355',2);
/*!40000 ALTER TABLE `core_weeklyranking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-07-31 21:52:08.584457','2','اخمد',1,'[{\"added\": {}}]',1,1),(2,'2026-07-31 21:52:35.644053','1','اخمد - الأسبوع 1',1,'[{\"added\": {}}]',18,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'admin','logentry'),(3,'auth','group'),(4,'auth','permission'),(5,'contenttypes','contenttype'),(8,'core','activitylog'),(9,'core','attendance'),(10,'core','backup'),(7,'core','branch'),(11,'core','branchevaluation'),(12,'core','companysetting'),(13,'core','evaluation'),(14,'core','message'),(15,'core','notification'),(16,'core','product'),(17,'core','reward'),(1,'core','user'),(18,'core','weeklyranking'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-07-31 20:12:20.401121'),(2,'contenttypes','0002_remove_content_type_name','2026-07-31 20:12:22.698518'),(3,'auth','0001_initial','2026-07-31 20:12:30.060965'),(4,'auth','0002_alter_permission_name_max_length','2026-07-31 20:12:32.217334'),(5,'auth','0003_alter_user_email_max_length','2026-07-31 20:12:32.380538'),(6,'auth','0004_alter_user_username_opts','2026-07-31 20:12:32.563339'),(7,'auth','0005_alter_user_last_login_null','2026-07-31 20:12:32.711834'),(8,'auth','0006_require_contenttypes_0002','2026-07-31 20:12:32.856325'),(9,'auth','0007_alter_validators_add_error_messages','2026-07-31 20:12:33.038320'),(10,'auth','0008_alter_user_username_max_length','2026-07-31 20:12:33.143627'),(11,'auth','0009_alter_user_last_name_max_length','2026-07-31 20:12:33.283201'),(12,'auth','0010_alter_group_name_max_length','2026-07-31 20:12:33.663208'),(13,'auth','0011_update_proxy_permissions','2026-07-31 20:12:33.776957'),(14,'auth','0012_alter_user_first_name_max_length','2026-07-31 20:12:33.862435'),(15,'core','0001_initial','2026-07-31 20:12:46.973988'),(16,'admin','0001_initial','2026-07-31 20:12:54.859967'),(17,'admin','0002_logentry_remove_auto_add','2026-07-31 20:12:55.172130'),(18,'admin','0003_logentry_add_action_flag_choices','2026-07-31 20:12:55.897697'),(19,'sessions','0001_initial','2026-07-31 20:12:59.449746'),(20,'core','0002_branch_user_employee_code_user_phone_user_updated_at_and_more','2026-07-31 20:26:17.658437'),(21,'core','0003_companysetting_product_user_last_login_ip_and_more','2026-07-31 21:15:51.690002'),(22,'core','0004_alter_activitylog_options_alter_attendance_options_and_more','2026-07-31 21:47:16.449274');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('lw4kerad5qn3bidmwz2sjft5i154rc0x','.eJxVjMsOwiAQRf-FtSEDw6O4dN9vIDOAUjU0Ke3K-O_apAvd3nPOfYlI21rj1ssSpyzOQonT78aUHqXtIN-p3WaZ5rYuE8tdkQftcpxzeV4O9--gUq_fGgGTBgye8mDCkLVWhhwasgWUT6CZ6eqBGKy3iAqC08jFc1IYgjPi_QG0FTaU:1wptrC:XBYN1Qb_ivSGWw6LgQ0KEVdp2V9Xp76dWDpZTV7pU4U','2026-08-14 20:29:26.080098');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-01  1:07:05
