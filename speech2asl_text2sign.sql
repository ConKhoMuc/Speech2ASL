-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: speech2asl
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `text2sign`
--

DROP TABLE IF EXISTS `text2sign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `text2sign` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(1000) DEFAULT NULL,
  `video` varchar(1000) DEFAULT NULL,
  `images` varchar(1000) DEFAULT NULL,
  `source` varchar(1000) DEFAULT NULL,
  `nlpword` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `text2sign`
--

LOCK TABLES `text2sign` WRITE;
/*!40000 ALTER TABLE `text2sign` DISABLE KEYS */;
INSERT INTO `text2sign` VALUES (1,'0','','uploads/image/0.jpg','uploads/image/0.jpg',''),(2,'1','','uploads/image/1.jpg','uploads/image/1.jpg',''),(3,'2','','uploads/image/2.jpg','uploads/image/2.jpg',''),(4,'3','','uploads/image/3.jpg','uploads/image/3.jpg',''),(5,'4','','uploads/image/4.jpg','uploads/image/4.jpg',''),(6,'5','','uploads/image/5.jpg','uploads/image/5.jpg',''),(7,'6','','uploads/image/6.jpg','uploads/image/6.jpg',''),(8,'7','','uploads/image/7.jpg','uploads/image/7.jpg',''),(9,'8','','uploads/image/8.jpg','uploads/image/8.jpg',''),(10,'9','','uploads/image/9.jpg','uploads/image/9.jpg',''),(11,'a','','uploads/image/a.jpg','uploads/image/a.jpg',''),(12,'b','','uploads/image/b.jpg','uploads/image/b.jpg',''),(13,'c','','uploads/image/c.jpg','uploads/image/c.jpg',''),(14,'d','','uploads/image/d.jpg','uploads/image/d.jpg',''),(15,'e','','uploads/image/e.jpg','uploads/image/e.jpg',''),(16,'f','','uploads/image/f.jpg','uploads/image/f.jpg',''),(17,'g','','uploads/image/g.jpg','uploads/image/g.jpg',''),(18,'h','','uploads/image/h.jpg','uploads/image/h.jpg',''),(19,'i','','uploads/image/i.jpg','uploads/image/i.jpg',''),(20,'j','','uploads/image/j.jpg','uploads/image/j.jpg',''),(21,'k','','uploads/image/k.jpg','uploads/image/k.jpg',''),(22,'l','','uploads/image/l.jpg','uploads/image/l.jpg',''),(23,'m','','uploads/image/m.jpg','uploads/image/m.jpg',''),(24,'n','','uploads/image/n.jpg','uploads/image/n.jpg',''),(25,'o','','uploads/image/o.jpg','uploads/image/o.jpg',''),(26,'p','','uploads/image/p.jpg','uploads/image/p.jpg',''),(27,'q','','uploads/image/q.jpg','uploads/image/q.jpg',''),(28,'r','','uploads/image/r.jpg','uploads/image/r.jpg',''),(29,'s','','uploads/image/s.jpg','uploads/image/s.jpg',''),(30,'t','','uploads/image/t.jpg','uploads/image/t.jpg',''),(31,'u','','uploads/image/u.jpg','uploads/image/u.jpg',''),(32,'v','','uploads/image/v.jpg','uploads/image/v.jpg',''),(33,'w','','uploads/image/w.jpg','uploads/image/w.jpg',''),(34,'x','','uploads/image/x.jpg','uploads/image/x.jpg',''),(35,'y','','uploads/image/y.jpg','uploads/image/y.jpg',''),(36,'z','','uploads/image/z.jpg','uploads/image/z.jpg',''),(37,'wrong','uploads/wrong.mp4','','uploads/wrong.mp4','[\'wrong\']'),(38,'yes','uploads/yes.mp4','','uploads/yes.mp4','[\'yes\']'),(39,'you','uploads/you.mp4','','uploads/you.mp4','[\'you\']'),(40,'your','uploads/your.mp4','','uploads/your.mp4','[\'your\']'),(41,'thank you','uploads/thankyou.mp4','','uploads/thankyou.mp4','[\'thank you\']'),(42,'they','uploads/they.mp4','','uploads/they.mp4','[\'they\']'),(43,'time','uploads/time.mp4','','uploads/time.mp4','[\'time\']'),(44,'want','uploads/want.mp4','','uploads/want.mp4','[\'want\']'),(45,'we','uploads/we.mp4','','uploads/we.mp4','[\'we\']'),(46,'what','uploads/what.mp4','','uploads/what.mp4','[\'what\']'),(47,'when','uploads/when.mp4','','uploads/when.mp4','[\'when\']'),(48,'where','uploads/where.mp4','','uploads/where.mp4','[\'where\']'),(49,'why','uploads/why.mp4','','uploads/why.mp4','[\'why\']'),(50,'write','uploads/write.mp4','','uploads/write.mp4','[\'write\']'),(51,'school','uploads/school.mp4','','uploads/school.mp4','[\'school\']'),(52,'she','uploads/she.mp4','','uploads/she.mp4','[\'she\']'),(53,'sign language','uploads/sign_language.mp4','','uploads/sign_language.mp4','[\'sign\', \'language\']'),(54,'sleep','uploads/sleep.mp4','','uploads/sleep.mp4','[\'sleep\']'),(55,'small','uploads/small.mp4','','uploads/small.mp4','[\'small\']'),(56,'sorry','uploads/sorry.mp4','','uploads/sorry.mp4','[\'sorry\']'),(57,'start','uploads/start.mp4','','uploads/start.mp4','[\'start\']'),(58,'stop','uploads/stop.mp4','','uploads/stop.mp4','[\'stop\']'),(59,'take','uploads/take.mp4','','uploads/take.mp4','[\'take\']'),(60,'night','uploads/night.mp4','','uploads/night.mp4','[\'night\']'),(61,'no','uploads/no.mp4','','uploads/no.mp4','[\'no\']'),(62,'now','uploads/now.mp4','','uploads/now.mp4','[\'now\']'),(63,'phone','uploads/phone.mp4','','uploads/phone.mp4','[\'phone\']'),(64,'play','uploads/play.mp4','','uploads/play.mp4','[\'play\']'),(65,'please','uploads/please.mp4','','uploads/please.mp4','[\'please\']'),(66,'read','uploads/read.mp4','','uploads/read.mp4','[\'read\']'),(67,'right','uploads/right.mp4','','uploads/right.mp4','[\'right\']'),(68,'sad','uploads/sad.mp4','','uploads/sad.mp4','[\'sad\']'),(69,'know','uploads/know.mp4','','uploads/know.mp4','[\'know\']'),(70,'learn','uploads/learn.mp4','','uploads/learn.mp4','[\'learn\']'),(71,'like','uploads/like.mp4','','uploads/like.mp4','[\'like\']'),(72,'love','uploads/love.mp4','','uploads/love.mp4','[\'love\']'),(73,'me','uploads/me.mp4','','uploads/me.mp4','[\'me\']'),(74,'meet','uploads/meet.mp4','','uploads/meet.mp4','[\'meet\']'),(75,'money','uploads/money.mp4','','uploads/money.mp4','[\'money\']'),(76,'my','uploads/my.mp4','','uploads/my.mp4','[\'my\']'),(77,'name','uploads/name.mp4','','uploads/name.mp4','[\'name\']'),(78,'go','uploads/go.mp4','','uploads/go.mp4','[\'go\']'),(79,'good','uploads/good.mp4','','uploads/good.mp4','[\'good\']'),(80,'happy','uploads/happy.mp4','','uploads/happy.mp4','[\'happy\']'),(81,'have','uploads/have.mp4','','uploads/have.mp4','[\'have\']'),(82,'he','uploads/he.mp4','','uploads/he.mp4','[\'he\']'),(83,'help','uploads/help.mp4','','uploads/help.mp4','[\'help\']'),(84,'house','uploads/house.mp4','','uploads/house.mp4','[\'house\']'),(85,'how','uploads/how.mp4','','uploads/how.mp4','[\'how\']'),(86,'it','uploads/it.mp4','','uploads/it.mp4','[\'it\']'),(87,'can','uploads/can.mp4','','uploads/can.mp4','[\'can\']'),(88,'car','uploads/car.mp4','','uploads/car.mp4','[\'car\']'),(89,'come','uploads/come.mp4','','uploads/come.mp4','[\'come\']'),(90,'day','uploads/day.mp4','','uploads/day.mp4','[\'day\']'),(91,'feel','uploads/feel.mp4','','uploads/feel.mp4','[\'feel\']'),(92,'food','uploads/food.mp4','','uploads/food.mp4','[\'food\']'),(93,'friend','uploads/friend.mp4','','uploads/friend.mp4','[\'friend\']'),(94,'give','uploads/give.mp4','','uploads/give.mp4','[\'give\']'),(95,'again','uploads/again.mp4','','uploads/again.mp4','[\'again\']'),(96,'answer','uploads/answer.mp4','','uploads/answer.mp4','[\'answer\']'),(97,'bad','uploads/bad.mp4','','uploads/bad.mp4','[\'bad\']'),(98,'book','uploads/book.mp4','','uploads/book.mp4','[\'book\']'),(99,'I am wrong','uploads/i_am_wrong.mp4','','uploads/i_am_wrong.mp4','[\'I\', \'wrong\']');
/*!40000 ALTER TABLE `text2sign` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 22:41:11
