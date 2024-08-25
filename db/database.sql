create database ai;
use db;

CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `nick_name` varchar(128) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `system_content` varchar(1024) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  'lang', varchar DEFAULT NULL,
  'gpt', smallint DEFAULT 0,
  'voice', smallint DEFAULT 0,
  'pic', smallint DEFAULT 0,
  'sub', smallint DEFAULT 0,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `records` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `content` text NOT NULL,
  `tokens` int DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `reset_at` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1974 DEFAULT CHARSET=utf8mb4;