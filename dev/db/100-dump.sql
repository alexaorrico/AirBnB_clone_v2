-- MySQL dump 10.13  Distrib 5.7.8-rc, for Linux (x86_64)
--
-- Host: localhost    Database: hbnb_dev_db
-- ------------------------------------------------------
-- Server version	5.7.8-rc

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

-- Drop database
DROP DATABASE IF EXISTS hbnb_dev_db;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost';
SET PASSWORD FOR 'hbnb_dev'@'localhost' = 'hbnb_dev_pwd';
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;

USE hbnb_dev_db;

--
-- Table structure for table `amenities`
--

DROP TABLE IF EXISTS `amenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `amenities` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenities`
--

LOCK TABLES `amenities` WRITE;
/*!40000 ALTER TABLE `amenities` DISABLE KEYS */;
INSERT INTO `amenities` VALUES ('017ec502-e84a-4a0f-92d6-d97e27bb6bdf','2017-03-25 02:17:06','2017-03-25 02:17:06','Cable TV'),('0d375b05-5ef9-4d43-aaca-436762bb25bf','2017-03-25 02:17:06','2017-03-25 02:17:06','Lockbox'),('12e9ccb4-03e4-4f82-ac3d-4fc7e3ebfbfe','2017-03-25 02:17:06','2017-03-25 02:17:06','Internet'),('1e0f976d-beef-497b-b29c-b4a25d1c071a','2017-03-25 02:17:06','2017-03-25 02:17:06','Other pet(s)'),('20f281b1-2cd1-4e36-a7c7-d1062ff16bcd','2017-03-25 02:17:06','2017-03-25 02:17:06','Smartlock'),('28ff856a-2cfb-44df-91b8-1285914553c8','2017-03-25 02:17:06','2017-03-25 02:17:06','Private living room'),('2a98b8af-1cd7-4236-a99e-7200c992fad7','2017-03-25 02:17:06','2017-03-25 02:17:06','Pets live on this property'),('2c620702-d41c-4732-a1cf-6e40f7877dc3','2017-03-25 02:17:06','2017-03-25 02:17:06','Self Check-In'),('2f055228-5fd3-4b1d-a021-7e4b9b7d70a6','2017-03-25 02:17:06','2017-03-25 02:17:06','TV'),('3e73edf2-c3d6-409f-9202-213df4a7a25a','2017-03-25 02:17:06','2017-03-25 02:17:06','Cat(s)'),('3fccec93-2842-49a0-8fdb-4008af2ef041','2017-03-25 02:17:06','2017-03-25 02:17:06','Hot tub'),('416cddd7-746e-4715-821c-3ad30b9bc3c3','2017-03-25 02:17:06','2017-03-25 02:17:06','Gym'),('43d414fb-0fff-4ea9-8c44-3819ec041c9b','2017-03-25 02:17:06','2017-03-25 02:17:06','Essentials'),('43de9883-8b2d-44dc-81d3-8b719ea50734','2017-03-25 02:17:06','2017-03-25 02:17:06','Heating'),('47327246-6852-4c70-b3db-77077ab61a32','2017-03-25 02:17:06','2017-03-25 02:17:06','Family/kid friendly'),('49fcaedc-481a-4e05-934f-4867988c8ec5','2017-03-25 02:17:06','2017-03-25 02:17:06','Wireless Internet'),('4a0a3fa7-21a0-411a-bb0a-9b4eed1901ef','2017-03-25 02:17:06','2017-03-25 02:17:06','Pets allowed'),('4e320c4e-deb6-4ccb-b45e-b77a5df3ff40','2017-03-25 02:17:06','2017-03-25 02:17:06','Kitchen'),('5429dc8c-799d-4555-98c6-f2d714a9fe50','2017-03-25 02:17:06','2017-03-25 02:17:06','Doorman Entry'),('6b9c3987-a344-4baf-8d11-077d719688ba','2017-03-25 02:17:06','2017-03-25 02:17:06','Lock on bedroom door'),('6dd36c9f-9863-4850-a810-a7629fe07d72','2017-03-25 02:17:06','2017-03-25 02:17:06','Washer'),('6f8987f8-7354-4770-8774-4f5e25acb173','2017-03-25 02:17:06','2017-03-25 02:17:06','Wheelchair accessible'),('79f2ca91-dc2b-44cb-9e08-f43c1a9d6d54','2017-03-25 02:17:06','2017-03-25 02:17:06','Elevator in building'),('7ae79c7e-955f-474a-bbdc-f05d4229fcd2','2017-03-25 02:17:06','2017-03-25 02:17:06','Fire extinguisher'),('885a80bf-1a79-431c-a5c7-f05d87c9e159','2017-03-25 02:17:06','2017-03-25 02:17:06','Free parking on premises'),('886e4374-db3d-43dc-9615-ec1c98c15c12','2017-03-25 02:17:06','2017-03-25 02:17:06','24-hour check-in'),('8d5b1bf3-4bd2-4283-86ce-91211fbc788d','2017-03-25 02:17:06','2017-03-25 02:17:06','Keypad'),('919be9d0-5789-4b56-b785-0e4d72ecc8ba','2017-03-25 02:17:06','2017-03-25 02:17:06','Air conditioning'),('92709c8a-65d4-4fb9-811a-f25ef328822e','2017-03-25 02:17:06','2017-03-25 02:17:06','Suitable for events'),('98850f9d-0835-46df-90e3-5fef156724a0','2017-03-25 02:17:06','2017-03-25 02:17:06','Laptop friendly workspace'),('9c54e3ed-48b3-4438-bb2c-304e14a9bde4','2017-03-25 02:17:06','2017-03-25 02:17:06','Breakfast'),('a6fc4fa4-345b-4c64-aee9-791afaf10f11','2017-03-25 02:17:06','2017-03-25 02:17:06','Smoke detector'),('baf27726-2b9c-4cb4-ad97-2baec4527be6','2017-03-25 02:17:06','2017-03-25 02:17:06','Shampoo'),('c4b9d932-71f4-4f10-9e09-502c3eb67ee2','2017-03-25 02:17:06','2017-03-25 02:17:06','Safety card'),('cb0c9658-79a7-41ac-b816-4201f3e98d80','2017-03-25 02:17:06','2017-03-25 02:17:06','Iron'),('cf701d1a-3c19-4bac-bd99-15321f1140f2','2017-03-25 02:17:06','2017-03-25 02:17:06','Dog(s)'),('d087d6cd-2ded-4bf7-8f32-61612a2da417','2017-03-25 02:17:06','2017-03-25 02:17:06','Hangers'),('d3cb5b63-2f99-4c55-86a7-3127eb4a8128','2017-03-25 02:17:06','2017-03-25 02:17:06','Buzzer/wireless intercom'),('d7275f8c-70e5-4c27-bcd6-aafd5256fccd','2017-03-25 02:17:06','2017-03-25 02:17:06','Carbon monoxide detector'),('dcfb45cc-b170-4ace-97af-9957b564606a','2017-03-25 02:17:06','2017-03-25 02:17:06','Indoor fireplace'),('e7680872-7b76-4565-aa8b-6
/*!40000 ALTER TABLE `amenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cities` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  `state_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `state_id` (`state_id`),
  CONSTRAINT `cities_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES ('05b0b99c-f10e-4e3a-88d1-b3187d6998ee','2017-03-25 02:17:06','2017-03-25 02:17:06','San Francisco','9799648d-88dc-4e63-b858-32e6531bec5c'),('14e2f358-f8fb-419c-8e8f-0017f971d82d','2017-03-25 02:17:06','2017-03-25 02:17:06','Tempe','459e021a-e794-447d-9dd2-e03b7963f7d2'),('14e49d0b-7363-40e3-8854-a89e96481f67','2017-03-25 02:17:06','2017-03-25 02:17:06','Joliet','d2398800-dd87-482b-be21-50a3063858ad'),('1721b75c-e0b2-46ae-8dd2-f86b62fb46e6','2017-03-25 02:17:06','2017-03-25 02:17:06','Douglas','459e021a-e794-447d-9dd2-e03b7963f7d2'),('1aef765c-3c91-47aa-a716-ffd3b8d748df','2017-03-25 02:17:06','2017-03-25 02:17:06','Kearny','459e021a-e794-447d-9dd2-e03b7963f7d2'),('1da255c0-f023-4779-8134-2b1b40f87683','2017-03-25 02:17:06','2017-03-25 02:17:06','New Orleans','2b9a4627-8a9e-4f32-a752-9a84fa7f4efd'),('3308ceb8-8e99-4abb-9c2a-a6446eaf01f7','2017-03-25 02:17:06','2017-03-25 02:17:06','Fremont','9799648d-88dc-4e63-b858-32e6531bec5c'),('33c525b5-f087-421c-946d-ba8c7a1c2efe','2017-03-25 02:17:06','2017-03-25 02:17:06','San Jose','9799648d-88dc-4e63-b858-32e6531bec5c'),('36bff3a3-e3b3-41b9-a6b5-ab2185a8cdf0','2017-03-25 02:17:06','2017-03-25 02:17:06','Saint Paul','b5fc9076-6c20-44a7-ac9b-97de17112329'),('3ffd4ed8-b645-46bc-8bc3-40c0e51f2b44','2017-03-25 02:17:06','2017-03-25 02:17:06','Jackson','bbee73a7-2f71-47e6-938a-2d9e932d4ff9'),('44e7a911-2c16-4dc0-ad68-9ae0412afc21','2017-03-25 02:17:06','2017-03-25 02:17:06','Pearl city','541bba6e-9543-4b33-8062-77ef26cd9778'),('45903748-fa39-4cd0-8a0b-c62bfe471702','2017-03-25 02:17:06','2017-03-25 02:17:06','Lafayette','2b9a4627-8a9e-4f32-a752-9a84fa7f4efd'),('492cc20d-21b4-474b-a727-e1981cfc49d5','2017-03-25 02:17:06','2017-03-25 02:17:06','Urbana','d2398800-dd87-482b-be21-50a3063858ad'),('4a0c57bb-60da-450c-afcf-c59be4c05e67','2017-03-25 02:17:06','2017-03-25 02:17:06','Chicago','d2398800-dd87-482b-be21-50a3063858ad'),('5481bd82-04ab-4a58-ae01-d67443aec20c','2017-03-25 02:17:06','2017-03-25 02:17:06','Denver','f8d21261-3e79-4f5c-829a-99d7452cd73c'),('5e061866-d4ad-4aa7-befe-2bf5f8698e29','2017-03-25 02:17:06','2017-03-25 02:17:06','Kailua','541bba6e-9543-4b33-8062-77ef26cd9778'),('660c9bbd-76c4-454f-b9a4-87efab0e948f','2017-03-25 02:17:06','2017-03-25 02:17:06','Calera','0e391e25-dd3a-45f4-bce3-4d1dea83f3c7'),('6a1ea750-b16f-4814-ad7e-9f25e3843f53','2017-03-25 02:17:06','2017-03-25 02:17:06','Sonoma','9799648d-88dc-4e63-b858-32e6531bec5c'),('712ffb97-b0eb-42f9-8cb9-69548882ab5d','2017-03-25 02:17:06','2017-03-25 02:17:06','Orlando','5976f0e7-5c5f-4949-aae0-90d68fd239c0'),('79ff14a4-1888-4cd3-8a31-230fa34bfa00','2017-03-25 02:17:06','2017-03-25 02:17:06','Honolulu','541bba6e-9543-4b33-8062-77ef26cd9778'),('94f16095-5ce6-4bec-8114-d1f3fa6f2b16','2017-03-25 02:17:06','2017-03-25 02:17:06','Babbie','0e391e25-dd3a-45f4-bce3-4d1dea83f3c7'),('a5e4fa5a-2a0d-4c7c-b824-d318409e11e8','2017-03-25 02:17:06','2017-03-25 02:17:06','Eugene','10098698-bace-4bfb-8c0a-6bae0f7f5b8f'),('b11616e0-fa23-4939-bd3f-0e178de3530b','2017-03-25 02:17:06','2017-03-25 02:17:06','Portland','10098698-bace-4bfb-8c0a-6bae0f7f5b8f'),('b695fcb4-7e61-420c-aa22-d1651cde13dc','2017-03-25 02:17:06','2017-03-25 02:17:06','Peoria','d2398800-dd87-482b-be21-50a3063858ad'),('c49639ab-d287-40ec-8a31-76b493cd9a3a','2017-03-25 02:17:06','2017-03-25 02:17:06','Meridian','bbee73a7-2f71-47e6-938a-2d9e932d4ff9'),('c5bbe76a-87f0-44f8-8b4d-e805e6cd757c','2017-03-25 02:17:06','2017-03-25 02:17:06','Naperville','d2398800-dd87-482b-be21-50a3063858ad'),('d96b80e3-2c05-4fb6-922e-36643005a530','2017-03-25 02:17:06','2017-03-25 02:17:06','Napa','9799648d-88dc-4e63-b858-32e6531bec5c'),('dacec983-cec4-4f68-bd7f-af9068a305f5','2017-03-25 02:17:06','2017-03-25 02:17:06','Miami','5976f0e7-5c5f-4949-aae0-90d68fd239c0'),('e4e40a6e-59ff-4b4f-ab72-d6d100201588','2017-03-25 02:17:06','2017-03-25 02:17:06','Baton rouge','2b9a4627-8a9e-4f32-a752-9a84fa7f4efd'),('f01c88dc-9f08-4b32-a1c1-625fb1e44972','2017-03-25 02:17:06','2017-03-25 02:17:06','Akron','0e391e25-dd3a-45f4-bce3-4d1dea83f3c7'),('f14fefb3-c6e4-42f6-8a5a-ee704a101f8
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `place_amenity`
--

DROP TABLE IF EXISTS `place_amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `place_amenity` (
  `place_id` varchar(60) NOT NULL,
  `amenity_id` varchar(60) NOT NULL,
  PRIMARY KEY (`place_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `place_amenity_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `place_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place_amenity`
--

LOCK TABLES `place_amenity` WRITE;
/*!40000 ALTER TABLE `place_amenity` DISABLE KEYS */;
INSERT INTO `place_amenity` VALUES ('02d9a2b5-7dca-423f-8406-707bc76abf7e','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('073084e1-1d9d-49e6-8383-42ef6f4325b5','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('0a454f9a-eaac-488b-8443-23cf58f7ae37','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('0feb3595-1c64-4bad-816c-769446217d4f','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('10974581-bff8-4ba6-9a00-2ae42d521162','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('12ff7d06-9910-41cd-9eee-bdc21476d119','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('1ff1963c-7afa-470c-bc05-562b01549b09','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('30e56424-c0f0-4e36-9523-f5e904bb3142','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('32945f6e-5a96-4233-b8ae-048d51323d7b','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('3827c1d1-14d5-4643-a24b-3dca656192fa','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('3a60974c-0fd8-4b17-b18b-ca0fe58db88f','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('3c702a05-81f1-450e-b07f-386ae8a3b124','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('453b0b1c-6bf3-4e94-8265-082ef06ab85f','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('4703b2d8-e417-4243-a6f3-044fc06f020e','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('4ae40c33-23c9-47a9-b867-0a6d8f25fd8c','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('52d726db-2427-40ca-a5f0-d5c117625d1c','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('552b5aaf-33b7-407b-a2dc-459ab730b3a5','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('6ebec357-8589-435b-a5cb-fcd99b638fae','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('7b8ecd06-c520-4adc-b2e4-bfaa7f8bab2e','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('8835ba11-7757-45c6-9138-f7e2e4b5f80f','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('96233d68-319e-4ae0-a20f-3af55dcadb0a','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('98b1678d-d25c-476a-b6c3-c11978617e90','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('9c5a1e44-0090-464b-ac3b-89e0f65cc6e1','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('a16c7358-bf66-4802-8933-1616b5a322db','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('a302bce0-cb8e-4e54-ba2b-0822b0565303','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('aaf389be-c794-4fb4-a6cf-619ca956898f','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('acd9cdca-855e-484b-baf9-ffda99d945f2','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('ad124633-a610-483f-862a-6f54dda19c6e','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('af92250e-2f85-4fca-8c04-03029a1b1fad','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('b493f8ca-c5d2-414a-9441-6cd4dcebcd36','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('b4a927e4-9715-4cd2-9918-47491f97df3e','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('b4d6d884-e50d-41eb-9b97-6395a07a43f9','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('bc227cc3-0ad7-4b9a-b72a-6c2a45e6a88a','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('cb681375-76ad-41d4-ac03-7fe74df9aed3','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('cd9eb9ef-2237-445a-b2be-e108d999eae8','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('cff8a023-eacb-4a38-a24f-a01fe9ddde18','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('d590593b-c4ef-4a9a-b631-9f4bf7a3d6c2','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('df2548db-377d-422e-b805-4e8e0c794302','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('e2d4feeb-4cb0-4df4-a10e-5a54748621b3','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('e3f28357-a476-4032-8726-4ac7262cbc72','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('e6c33577-5de3-4481-9147-47ef4710b986','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('e990e07f-1b6f-4bc5-a553-ddddad30211b','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('f19fa153-154e-440b-9f4b-debee403b0d2','017ec502-e84a-4a0f-92d6-d97e27bb6bdf'),('12ff7d06-9910-41cd-9eee-bdc21476d119','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('19ae5055-f503-499d-a64f-2bf7d92eff5b','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('2b6e6650-5f69-426d-a084-71f7ad30d1f1','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('453b0b1c-6bf3-4e94-8265-082ef06ab85f','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('478d6061-fc78-40c3-a1b2-0e906fb86da8','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('4ae40c33-23c9-47a9-b867-0a6d8f25fd8c','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('552b5aaf-33b7-407b-a2dc-459ab730b3a5','0d375b05-5ef9-4d43-aaca-436762bb25bf'),('66fb8e5d-2ad2-44be-8890-a13a9992f257','0d375b05-5ef9-4d43-
/*!40000 ALTER TABLE `place_amenity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `places`
--

DROP TABLE IF EXISTS `places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `places` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `city_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `number_rooms` int(11) NOT NULL,
  `number_bathrooms` int(11) NOT NULL,
  `max_guest` int(11) NOT NULL,
  `price_by_night` int(11) NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `places_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`),
  CONSTRAINT `places_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `places`
--

LOCK TABLES `places` WRITE;
/*!40000 ALTER TABLE `places` DISABLE KEYS */;
INSERT INTO `places` VALUES ('02d9a2b5-7dca-423f-8406-707bc76abf7e','2017-03-25 02:17:06','2017-03-25 02:17:06','1721b75c-e0b2-46ae-8dd2-f86b62fb46e6','3ea61b06-e22a-459b-bb96-d900fb8f843a','The Lynn House','Our place is 2 blocks from Vista Park (Farmer\'s Market), Historic Warren Ballpark, and about 2 miles from Old Bisbee where there is shopping, dining, and site seeing. We offer continental breakfast. You get the quiet life with great mountain and garden views. This is a 100+ year old cozy home which has been on both the Garden and Home tours. You have access to whole house, except for 1 restricted area (She-Shack).  Hosts are on site in a casita in the back from 8pm until 7am when we are in town.<BR /><BR />Our home has two bedrooms, one king and one queen.  There are 2 bathrooms, 1  1950\'s soak tub with shower and 1 with shower only.  Guests have access to the living/dining room area, and the kitchen (except for use of stove/oven).  Each morning, coffee/tea, and muffins are ready for guests.  A small frig is available in the dining room with water/juice and an area for guest items.  1 parking space is directly across the street.  There is a large back patio with a grill for guests to u',2,2,4,82,31.4141,-109.879),('0675a2d6-f64c-4be7-9a8a-f55341f09d4b','2017-03-25 02:17:06','2017-03-25 02:17:06','4a0c57bb-60da-450c-afcf-c59be4c05e67','3fda0d5c-fea4-4920-bc91-6e6c6663d161','Cozy, Bright Studio in GOLD COAST w/Rooftop','This lovely, sunny studio is in the beautiful Gold Coast neighborhood of downtown Chicago. Bars, restaurants, parks, shopping and public transport are within walking distance. Steps away from the Loop. Prime nearby attractions include Lake Michigan, Oak Street Beach, Lincoln Park, Museum of Contemporary Art and the Lyric Opera. Rush Street, which offers great dinning, shopping and entertainment, is a short block away.<BR /><BR />Apartment has shared rooftop with beautiful views of Chicago\'s skyline.<BR /><BR />This 250 sq. ft. studio is cozy, warm, and with lots of light. The small kitchen has a stove, a microwave, a toaster, and an espresso machine loaded with good coffee. Our apartment has a queen-sized mattress, and two-person sofa: altogether they can accommodate three persons. Plenty of closet space.<BR /><BR />You will have an access to a shared rooftop, and a laundry room. Free street parking is available very close to the building on LaSalle Street (except 4PM - 6:30 PM on week',0,1,2,65,41.9009,-87.6298),('073084e1-1d9d-49e6-8383-42ef6f4325b5','2017-03-25 02:17:06','2017-03-25 02:17:06','f3923bdf-81f2-45e9-a5e1-fd128e122d45','dfed3ea3-c133-47e8-8cfa-312eecbcc56d','Fairpark. Downtown Tupelo','A private bedroom with a queen size bed and private bathroom is available in my 3 bedroom home in Tupelo\'s Downtown Fairpark. Access to Living area, laundry and kitchen included. One block from downtown shopping, restaurants, BancorpSouth Arena and the Farmer\'s Market. This is a friendly and quiet neighborhood. There are 2 bedrooms available for up to 4 guests.<BR /><BR />Parking is available at house. One block from downtown tupelo, Lots of restaurants, shopping and entertainment within 1 block of house.',1,1,2,54,34.2546,-88.7022),('09b4888f-0e06-4ab1-abbc-05e9865634d0','2017-03-25 02:17:06','2017-03-25 02:17:06','e4e40a6e-59ff-4b4f-ab72-d6d100201588','00e93fc3-53ff-4da4-8e72-faa5216f81bb','Spanish Town Historic District, Heart of Downtown','Our home is a block away from parks, art and culture, including several museums and the Capitol district,  and restaurants and bars within walking distance. Very safe, quiet, in the bustle of downtown but the privacy of a neighborhood. The location, the people, and the ambiance of our funky neighborhood, Spanish Town, make this a perfect spot when visiting. My place is perfect for couples, solo adventurers, business travelers, and pets.',1,1,2,65,30.4557,-91.1827),('0a454f9a-eaac-488b-8443-23cf58f7ae37','2017-03-25 02:17:06','2017-03-25 02:17:06','5e061866-d4ad-4aa7-befe-2bf5f8698e29','f9b11370-f316-492c-92da-014d7bce7213','Beautiful, Bungalow steps to Beach!','
/*!40000 ALTER TABLE `places` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `place_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `text` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `place_id` (`place_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES ('01a2c67a-b39d-4940-b910-a1cc3289557d','2017-03-25 02:17:07','2017-03-25 02:17:07','314b188e-990b-423e-ae63-f0199b8c2b17','150e591e-486b-48ee-be42-4aecba665020','Lovely haven on a quiet street.'),('0230dc18-a336-4ded-97ef-0fee0b4d6ea0','2017-03-25 02:17:07','2017-03-25 02:17:07','453b0b1c-6bf3-4e94-8265-082ef06ab85f','30a890e4-a62c-44f9-abc0-07e2c74021da','We loved our stay here! The cottage is gorgeous, comfortable, and has an extra touch you can tell. Our hosts were great and offered some awesome suggestions (like delicious Italian at Beppe\'s that made our night). Very relaxing and cosy, we would highly recommend!'),('0245460e-d3ed-4c21-b003-155bf74ce3d8','2017-03-25 02:17:07','2017-03-25 02:17:07','7ed82a23-cd4f-437b-be12-9c54e84281ef','61302be9-4b31-4be0-92fc-d0dda253e167','Great place! Very clean and nice...we were visiting family that lives near by and it was perfect...much better than the local motels. I have a feeling I will be fighting other members of my family to stay here again, everyone was very impressed. Thank you Lynn, Becky and Rebecca for your hospitality!'),('0278a560-6531-4a28-975f-f68bfc5fe0f9','2017-03-25 02:17:07','2017-03-25 02:17:07','ffcc9c22-759e-4418-b788-81eda89c2865','426624f6-84a9-4ec4-84f3-7655dc70e86e','I only stayed for one night but they were very accommodating with check in and check out times. I was greeted by their pups and barking, but don\'t be afraid they\'re actually really sweet. <BR />Although the idea of having your room accessed by others may be a turn off it wasn\'t that awkward hahaha<BR />In your bedroom they provide a curtain with the bed for extra privacy. It really does make your stay more comfortable and is a very nice detail that helped me sleep more comfortably at night. s a very urban and photogenic area. THANK YOU KATIE AND MATTHIJS ! '),('0363cc1f-6b48-426f-997b-e7b0b5f69195','2017-03-25 02:17:07','2017-03-25 02:17:07','cff8a023-eacb-4a38-a24f-a01fe9ddde18','5e181cc6-cac7-49e9-a7a1-3095b0f9010b','As of the first week of march 2017 there were 165 reviews...all positive!...Cara and Bryan\'s KBCG lives up to every one of them...if there was a choice for 6 stars I would have...we have been coming to oahu for the past 17 years and this was easily the BEST vacation ever...Cara and Bryan are just good people and you absolutely cannot go wrong with Kailua Beach Cottage (URL HIDDEN) Ka Oi'),('03774280-2251-4721-ac2a-ae032b4e866f','2017-03-25 02:17:07','2017-03-25 02:17:07','645127dd-38b4-4fad-9950-57b3ce0a5301','5e181cc6-cac7-49e9-a7a1-3095b0f9010b','Cameron and Sara are very friendly. They allow me to check in earlier to get a quick snap before my audition. I would be happy to be here again. You can cook, take shower and have a cozy bedroom. And their cat spent time with me. The cat is very friendly and lovely.'),('03d137bf-773f-4ae2-9fcb-fc388550636d','2017-03-25 02:17:07','2017-03-25 02:17:07','b180ad52-fe00-4040-97f9-9efdfc3d406d','dfed3ea3-c133-47e8-8cfa-312eecbcc56d','This is a private entrance and space in a small RV.  Not really big enough for more than 2 persons.  Great family and close to I5, shops and supplies.'),('053c8af0-d775-4d20-b938-0834572e28cf','2017-03-25 02:17:07','2017-03-25 02:17:07','47b9ca37-915d-405d-861d-7dbf74559441','7771bbe9-92ab-46d1-a636-864526361d7d','Very clean and worth the money'),('056a429c-61f4-4a8b-a1fa-e4e129d6697f','2017-03-25 02:17:07','2017-03-25 02:17:07','60b77ea7-04c9-4b8a-b835-dc92c6aa196b','3fda0d5c-fea4-4920-bc91-6e6c6663d161','Excellent location near one of the most iconic beaches in the world, Lanikai Beach.  The layout is very comfortable with a private space with all the amenities needed for an awesome stay, whether it\'s a day or a couple of weeks.  Josh and Josey were super-helpful and made sure I had all the info I needed to make the stay comfortable and cozy.  I gladly recommend this cottage to anyone looking for a great experience.'),('05a4063b-07b8-4ce4-b738-35217f82cfdc','2017-03-25 02:17:07','2017-03-25 02:17:07','453b0b1c-6bf3-4e94-8265-082ef06ab85f','c81d66a3-f0fe-44e9-9f31-cb3c6
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `states`
--

DROP TABLE IF EXISTS `states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `states` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
INSERT INTO `states` VALUES ('0e391e25-dd3a-45f4-bce3-4d1dea83f3c7','2017-03-25 02:17:06','2017-03-25 02:17:06','Alabama'),('10098698-bace-4bfb-8c0a-6bae0f7f5b8f','2017-03-25 02:17:06','2017-03-25 02:17:06','Oregon'),('2b9a4627-8a9e-4f32-a752-9a84fa7f4efd','2017-03-25 02:17:06','2017-03-25 02:17:06','Louisiana'),('459e021a-e794-447d-9dd2-e03b7963f7d2','2017-03-25 02:17:06','2017-03-25 02:17:06','Arizona'),('541bba6e-9543-4b33-8062-77ef26cd9778','2017-03-25 02:17:06','2017-03-25 02:17:06','Hawaii'),('5976f0e7-5c5f-4949-aae0-90d68fd239c0','2017-03-25 02:17:06','2017-03-25 02:17:06','Florida'),('9799648d-88dc-4e63-b858-32e6531bec5c','2017-03-25 02:17:06','2017-03-25 02:17:06','California'),('b5fc9076-6c20-44a7-ac9b-97de17112329','2017-03-25 02:17:06','2017-03-25 02:17:06','Minnesota'),('bbee73a7-2f71-47e6-938a-2d9e932d4ff9','2017-03-25 02:17:06','2017-03-25 02:17:06','Mississippi'),('d2398800-dd87-482b-be21-50a3063858ad','2017-03-25 02:17:06','2017-03-25 02:17:06','Illinois'),('f8d21261-3e79-4f5c-829a-99d7452cd73c','2017-03-25 02:17:06','2017-03-25 02:17:06','Colorado');
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('00a11245-12fa-436e-9ccc-967417f8c30a','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail6@gmail.com','pwd6','Todd','Seanez'),('00e93fc3-53ff-4da4-8e72-faa5216f81bb','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail28@gmail.com','pwd28','Richard','Steere'),('150e591e-486b-48ee-be42-4aecba665020','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail23@gmail.com','pwd23','Cecilia','Boes'),('30a890e4-a62c-44f9-abc0-07e2c74021da','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail2@gmail.com','pwd2','David','Meador'),('32c11d3d-99a1-4406-ab41-7b6ccb7dd760','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail18@gmail.com','pwd18','Susan','Finney'),('3ea61b06-e22a-459b-bb96-d900fb8f843a','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail8@gmail.com','pwd8','Melissa','Ward'),('3fda0d5c-fea4-4920-bc91-6e6c6663d161','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail12@gmail.com','pwd12','Robert','Graham'),('426624f6-84a9-4ec4-84f3-7655dc70e86e','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail19@gmail.com','pwd19','Gail','Mccarthy'),('5e181cc6-cac7-49e9-a7a1-3095b0f9010b','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail21@gmail.com','pwd21','Rebecca','Stapleton'),('61302be9-4b31-4be0-92fc-d0dda253e167','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail13@gmail.com','pwd13','Virginia','Lewis'),('70b18dcc-08ef-4040-91cf-4075973d320a','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail9@gmail.com','pwd9','Duane','Smiley'),('7231eaa1-400f-4cb5-a867-f5eba8adbb81','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail11@gmail.com','pwd11','Betty','Hicks'),('7771bbe9-92ab-46d1-a636-864526361d7d','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail16@gmail.com','pwd16','Lynn','Melton'),('8394fd35-8a8a-479f-a398-48f53b4a6554','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail3@gmail.com','pwd3','Emily','Dancy'),('85651506-c13c-4c2f-9c79-8fbebc048e39','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail15@gmail.com','pwd15','Fredrick','Morasca'),('887dcd8d-d5ee-48de-9626-73ff4ea732fa','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail27@gmail.com','pwd27','Walter','Olsen'),('91e27a07-1f47-43c9-b851-60c6882abcd3','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail5@gmail.com','pwd5','Olivia','Hampton'),('9e7b2291-3bff-43b9-9241-8ff685e7a6dd','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail24@gmail.com','pwd24','Carol','Hass'),('9eec6c06-5918-4867-833a-face490d4715','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail1@gmail.com','pwd1','Jacqueline','Watkins'),('aa92d1ff-f0ad-4ba3-9c20-2afef207bf70','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail10@gmail.com','pwd10','John','Hooten'),('b6160096-c503-4909-a674-7bfbddc8cc45','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail25@gmail.com','pwd25','Melida','Wright'),('c81d66a3-f0fe-44e9-9f31-cb3c6f27db4e','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail22@gmail.com','pwd22','Gina','Jauregui'),('cf1780e6-d294-4113-8749-1c728b9e3f81','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail4@gmail.com','pwd4','Hazel','Kyung'),('d622edfa-fc35-4732-b5ec-a15d794267ec','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail7@gmail.com','pwd7','Roy','Grant'),('df668e22-e344-4c89-a050-e5ad211cbaa6','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail14@gmail.com','pwd14','Leo','Minnick'),('dfc6b9a5-6673-4f1b-83cd-0dfa800c0d08','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail26@gmail.com','pwd26','James','Diaz'),('dfed3ea3-c133-47e8-8cfa-312eecbcc56d','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail0@gmail.com','pwd0','Georgia','Boshard'),('f33e2624-520b-4bc2-b6a0-190ee1d41855','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail17@gmail.com','pwd17','Tracy','Tillman'),('f9b11370-f316-492c-92da-014d7bce7213','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail29@gmail.com','pwd29','Dawn','Kitchen'),('fa44780d-ac48-41ab-9dd0-ac54a15755cf','2017-03-25 02:17:06','2017-03-25 02:17:06','noemail20@gmail.com','pwd20','Leon','Sarro');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-25 18:45:25
