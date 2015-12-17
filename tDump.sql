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
-- Table structure for table `active_effects`
--

DROP TABLE IF EXISTS `active_effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `active_effects` (
  `Name` varchar(40) DEFAULT NULL,
  `EffectID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Scope` varchar(40) DEFAULT NULL,
  `Type` varchar(40) DEFAULT NULL,
  `Details` varchar(255) DEFAULT NULL,
  `Cooldown` int(10) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`EffectID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `active_effects`
--

LOCK TABLES `active_effects` WRITE;
/*!40000 ALTER TABLE `active_effects` DISABLE KEYS */;
/*!40000 ALTER TABLE `active_effects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `armour_definitions`
--

DROP TABLE IF EXISTS `armour_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `armour_definitions` (
  `ItemID` int(10) unsigned NOT NULL,
  `Slot` varchar(40) DEFAULT NULL,
  `Part1` int(10) unsigned DEFAULT NULL,
  `Part2` int(10) unsigned DEFAULT NULL,
  `Part3` int(10) unsigned DEFAULT NULL,
  KEY `ItemID` (`ItemID`),
  KEY `Part1` (`Part1`),
  KEY `Part2` (`Part2`),
  KEY `Part3` (`Part3`),
  CONSTRAINT `armour_definitions_ibfk_5` FOREIGN KEY (`Part3`) REFERENCES `armour_parts` (`PartID`),
  CONSTRAINT `armour_definitions_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `armour_definitions_ibfk_2` FOREIGN KEY (`Part1`) REFERENCES `armour_parts` (`PartID`),
  CONSTRAINT `armour_definitions_ibfk_3` FOREIGN KEY (`Part2`) REFERENCES `armour_parts` (`PartID`),
  CONSTRAINT `armour_definitions_ibfk_4` FOREIGN KEY (`Part2`) REFERENCES `armour_parts` (`PartID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `armour_definitions`
--

LOCK TABLES `armour_definitions` WRITE;
/*!40000 ALTER TABLE `armour_definitions` DISABLE KEYS */;
INSERT INTO `armour_definitions` VALUES (2,'head',1,2,3);
/*!40000 ALTER TABLE `armour_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `armour_parts`
--

DROP TABLE IF EXISTS `armour_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `armour_parts` (
  `PartID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `PassiveEffect` int(10) unsigned DEFAULT NULL,
  `ActiveEffect` int(10) unsigned DEFAULT NULL,
  `Word` varchar(40) DEFAULT NULL,
  `PartType` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`PartID`),
  KEY `PassiveEffect` (`PassiveEffect`),
  KEY `ActiveEffect` (`ActiveEffect`),
  CONSTRAINT `armour_parts_ibfk_2` FOREIGN KEY (`ActiveEffect`) REFERENCES `active_effects` (`EffectID`),
  CONSTRAINT `armour_parts_ibfk_1` FOREIGN KEY (`PassiveEffect`) REFERENCES `passive_effects` (`EffectID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `armour_parts`
--

LOCK TABLES `armour_parts` WRITE;
/*!40000 ALTER TABLE `armour_parts` DISABLE KEYS */;
INSERT INTO `armour_parts` VALUES (1,2,NULL,'Sluggish','Comb'),(2,2,NULL,'Sluggish','Visor'),(3,2,NULL,'Slugs','Helm');
/*!40000 ALTER TABLE `armour_parts` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `ID` int(10) unsigned NOT NULL,
  `Head` int(10) unsigned DEFAULT NULL,
  `Shoulders` int(10) unsigned DEFAULT NULL,
  `Hands` int(10) unsigned DEFAULT NULL,
  `Legs` int(10) unsigned DEFAULT NULL,
  `Feet` int(10) unsigned DEFAULT NULL,
  `Back` int(10) unsigned DEFAULT NULL,
  `MainHand` int(10) unsigned DEFAULT NULL,
  `OffHand` int(10) unsigned DEFAULT NULL,
  `Inventory` text,
  KEY `ID` (`ID`),
  KEY `Head` (`Head`),
  KEY `Shoulders` (`Shoulders`),
  KEY `Hands` (`Hands`),
  KEY `Legs` (`Legs`),
  KEY `Feet` (`Feet`),
  KEY `Back` (`Back`),
  KEY `MainHand` (`MainHand`),
  KEY `OffHand` (`OffHand`),
  CONSTRAINT `inventory_ibfk_9` FOREIGN KEY (`OffHand`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `players` (`id`),
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`Head`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_3` FOREIGN KEY (`Shoulders`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_4` FOREIGN KEY (`Hands`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_5` FOREIGN KEY (`Legs`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_6` FOREIGN KEY (`Feet`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_7` FOREIGN KEY (`Back`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `inventory_ibfk_8` FOREIGN KEY (`MainHand`) REFERENCES `item_definitions` (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3 6'),(2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'4');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_definitions`
--

DROP TABLE IF EXISTS `item_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item_definitions` (
  `ItemID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Type` varchar(40) DEFAULT NULL,
  `Weight` int(11) DEFAULT NULL,
  `Value` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_definitions`
--

LOCK TABLES `item_definitions` WRITE;
/*!40000 ALTER TABLE `item_definitions` DISABLE KEYS */;
INSERT INTO `item_definitions` VALUES (1,'Firm Shield of Firm Firmness','weapon',1,5),(2,'Sluggish Helm of Sluggish Slugs','armour',1,0);
/*!40000 ALTER TABLE `item_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ItemID` int(10) unsigned NOT NULL,
  `Owner` int(10) unsigned DEFAULT '0',
  `Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ItemID` (`ItemID`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item_definitions` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (3,1,1,'new'),(4,1,2,'new'),(6,2,1,'new');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passive_effects`
--

DROP TABLE IF EXISTS `passive_effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passive_effects` (
  `Name` varchar(40) DEFAULT NULL,
  `EffectID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Scope` varchar(40) DEFAULT NULL,
  `Stat` varchar(20) DEFAULT NULL,
  `Modifier` int(11) DEFAULT NULL,
  `IsSpecial` tinyint(1) DEFAULT '0',
  `SpecialRules` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`EffectID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passive_effects`
--

LOCK TABLES `passive_effects` WRITE;
/*!40000 ALTER TABLE `passive_effects` DISABLE KEYS */;
INSERT INTO `passive_effects` VALUES ('small def up',1,'self','def',2,0,NULL),('small dex up',2,'self','dex',-2,0,NULL);
/*!40000 ALTER TABLE `passive_effects` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,0,'jabird',3,4,5,11,2,2,0,0,0,0,NULL,'healthy'),(2,0,'chris',15,4,2,8,3,3,0,0,0,0,NULL,'healthy');
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
  `HPBoostModifier` int(11) DEFAULT '1',
  `RiposteDice` int(11) DEFAULT '6'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variableprofiles`
--

LOCK TABLES `variableprofiles` WRITE;
/*!40000 ALTER TABLE `variableprofiles` DISABLE KEYS */;
INSERT INTO `variableprofiles` VALUES ('demo',1,1,1,1,1,20,20,20,20,20,10,10,10,10,10,7,7,7,7,7,1,1,0,1,1,10,10,10,10,10,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,2,0,1,6),('riposte damage',1,1,1,1,1,20,20,20,20,20,10,10,10,10,10,7,7,7,7,7,1,1,0,1,0,10,10,10,10,10,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,1,2,0,1,6);
/*!40000 ALTER TABLE `variableprofiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weapon_definitions`
--

DROP TABLE IF EXISTS `weapon_definitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weapon_definitions` (
  `ItemID` int(10) unsigned NOT NULL,
  `WeaponType` varchar(40) DEFAULT NULL,
  `Hand` varchar(40) DEFAULT NULL,
  `Part1` int(10) unsigned DEFAULT NULL,
  `Part2` int(10) unsigned DEFAULT NULL,
  `Part3` int(10) unsigned DEFAULT NULL,
  KEY `ItemID` (`ItemID`),
  KEY `Part1` (`Part1`),
  KEY `Part2` (`Part2`),
  KEY `Part3` (`Part3`),
  CONSTRAINT `weapon_definitions_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item_definitions` (`ItemID`),
  CONSTRAINT `weapon_definitions_ibfk_2` FOREIGN KEY (`Part1`) REFERENCES `weapon_parts` (`PartID`),
  CONSTRAINT `weapon_definitions_ibfk_3` FOREIGN KEY (`Part2`) REFERENCES `weapon_parts` (`PartID`),
  CONSTRAINT `weapon_definitions_ibfk_4` FOREIGN KEY (`Part3`) REFERENCES `weapon_parts` (`PartID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weapon_definitions`
--

LOCK TABLES `weapon_definitions` WRITE;
/*!40000 ALTER TABLE `weapon_definitions` DISABLE KEYS */;
INSERT INTO `weapon_definitions` VALUES (1,'Shield','off',1,2,3);
/*!40000 ALTER TABLE `weapon_definitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weapon_parts`
--

DROP TABLE IF EXISTS `weapon_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weapon_parts` (
  `PartID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `PassiveEffect` int(10) unsigned DEFAULT NULL,
  `ActiveEffect` int(10) unsigned DEFAULT NULL,
  `Word` varchar(40) DEFAULT NULL,
  `PartType` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`PartID`),
  KEY `PassiveEffect` (`PassiveEffect`),
  KEY `ActiveEffect` (`ActiveEffect`),
  CONSTRAINT `weapon_parts_ibfk_2` FOREIGN KEY (`ActiveEffect`) REFERENCES `active_effects` (`EffectID`),
  CONSTRAINT `weapon_parts_ibfk_1` FOREIGN KEY (`PassiveEffect`) REFERENCES `passive_effects` (`EffectID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weapon_parts`
--

LOCK TABLES `weapon_parts` WRITE;
/*!40000 ALTER TABLE `weapon_parts` DISABLE KEYS */;
INSERT INTO `weapon_parts` VALUES (1,1,NULL,'Firmness','boss'),(2,1,NULL,'Firm','enarmes'),(3,1,NULL,'Firm','bouche');
/*!40000 ALTER TABLE `weapon_parts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-17 20:18:25
