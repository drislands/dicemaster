-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: dicebot
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

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
-- Table structure for table `currentprofile`
--

DROP TABLE IF EXISTS `currentprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `currentprofile` (
  `DefaultP` text,
  `CurrentP` text,
  `ph` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currentprofile`
--

LOCK TABLES `currentprofile` WRITE;
/*!40000 ALTER TABLE `currentprofile` DISABLE KEYS */;
INSERT INTO `currentprofile` VALUES ('demo','demo',1);
/*!40000 ALTER TABLE `currentprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `duels`
--

DROP TABLE IF EXISTS `duels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `duels` (
  `Challenger` int(11) NOT NULL DEFAULT '0',
  `Defender` int(11) NOT NULL DEFAULT '0',
  `Active` tinyint(1) NOT NULL DEFAULT '0',
  `Favoured` int(11) NOT NULL DEFAULT '0',
  `Winner` int(11) DEFAULT NULL,
  `Accepted` tinyint(1) NOT NULL DEFAULT '0',
  `Turn` int(11) DEFAULT NULL,
  `DuelID` varchar(40) NOT NULL DEFAULT '',
  `Stage` int(11) DEFAULT '1',
  `Dice` int(10) unsigned DEFAULT '0',
  `SpecialDice` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`DuelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `duels`
--

LOCK TABLES `duels` WRITE;
/*!40000 ALTER TABLE `duels` DISABLE KEYS */;
/*!40000 ALTER TABLE `duels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Active` tinyint(1) NOT NULL DEFAULT '0',
  `Name` varchar(255) NOT NULL,
  `Attack` int(11) DEFAULT NULL,
  `Defense` int(11) DEFAULT NULL,
  `Strength` int(11) DEFAULT NULL,
  `Dexterity` int(11) DEFAULT NULL,
  `MaxHP` int(11) DEFAULT NULL,
  `CurHP` int(11) DEFAULT NULL,
  `Boosts` int(11) NOT NULL DEFAULT '0',
  `Used_Boosts` int(11) NOT NULL DEFAULT '0',
  `Rerolls` int(11) NOT NULL DEFAULT '0',
  `Used_Rerolls` int(11) NOT NULL DEFAULT '0',
  `CurrentDuel` varchar(40) DEFAULT NULL,
  `Status` varchar(40) NOT NULL DEFAULT 'healthy',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variableprofiles`
--

DROP TABLE IF EXISTS `variableprofiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variableprofiles` (
  `Name` text,
  `MinAtt` int(11) DEFAULT '1',
  `MinDef` int(11) DEFAULT '1',
  `MinHP` int(11) DEFAULT '1',
  `MinStr` int(11) DEFAULT '1',
  `MinDex` int(11) DEFAULT '1',
  `MaxAtt` int(11) DEFAULT '20',
  `MaxDef` int(11) DEFAULT '20',
  `MaxHP` int(11) DEFAULT '20',
  `MaxStr` int(11) DEFAULT '20',
  `MaxDex` int(11) DEFAULT '20',
  `HitDie` int(11) DEFAULT '10',
  `DefDie` int(11) DEFAULT '10',
  `AttDie` int(11) DEFAULT '10',
  `StrDie` int(11) DEFAULT '10',
  `DexDie` int(11) DEFAULT '10',
  `HitThr` int(11) DEFAULT '7',
  `DefThr` int(11) DEFAULT '7',
  `AttThr` int(11) DEFAULT '7',
  `StrThr` int(11) DEFAULT '7',
  `DexThr` int(11) DEFAULT '7',
  `DubHit` tinyint(1) DEFAULT '1',
  `DubDef` tinyint(1) DEFAULT '1',
  `DubAtt` tinyint(1) DEFAULT '0',
  `DubStr` int(11) DEFAULT '1',
  `DubDex` int(11) DEFAULT '1',
  `DubHitThr` int(11) DEFAULT '10',
  `DubDefThr` int(11) DEFAULT '10',
  `DubAttThr` int(11) DEFAULT '10',
  `DubStrThr` int(11) DEFAULT '10',
  `DubDexThr` int(11) DEFAULT '10',
  `NegHit` tinyint(1) DEFAULT '0',
  `NegDef` tinyint(1) DEFAULT '0',
  `NegAtt` tinyint(1) DEFAULT '0',
  `NegStr` int(11) DEFAULT '0',
  `NegDex` int(11) DEFAULT '0',
  `NegHitThr` int(11) DEFAULT '1',
  `NegDefThr` int(11) DEFAULT '1',
  `NegAttThr` int(11) DEFAULT '1',
  `NegStrThr` int(11) DEFAULT '1',
  `NegDexThr` int(11) DEFAULT '1',
  `WinBoosts` int(11) DEFAULT '1',
  `LoseBoosts` int(11) DEFAULT '0',
  `FavourBoosts` int(11) DEFAULT '1',
  `BoostVal` int(11) DEFAULT '1',
  `WinRerolls` int(11) DEFAULT '0',
  `LoseRerolls` int(11) DEFAULT '1',
  `RollBoostRate` int(11) DEFAULT '2',
  `BoostToRoll` int(11) DEFAULT '0',
  `HPBoostModifier` int(11) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variableprofiles`
--

LOCK TABLES `variableprofiles` WRITE;
/*!40000 ALTER TABLE `variableprofiles` DISABLE KEYS */;
INSERT INTO `variableprofiles` VALUES ('demo',1,1,1,1,1,20,20,20,20,20,10,10,10,10,10,7,7,7,7,7,1,1,0,1,1,10,10,10,10,10,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,2,0,1),('riposte damage',1,1,1,1,1,20,20,20,20,20,10,10,10,10,10,7,7,7,7,7,1,1,0,1,0,10,10,10,10,10,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,2,0,1);
/*!40000 ALTER TABLE `variableprofiles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-11 14:41:03
