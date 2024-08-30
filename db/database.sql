create database ai;
use db;

CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `nick_name` varchar(128) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `system_content` varchar(1024) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `lang` varchar(4) DEFAULT NULL,
  `gpt` tinyint DEFAULT 0,
  `voice` tinyint DEFAULT 0,
  `pic` tinyint DEFAULT 0,
  `sub` tinyint DEFAULT 0,
  `ref_link` varchar(128) DEFAULT NULL,
  `ref_count` tinyint DEFAULT 0,
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

CREATE TABLE `group_chats` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `group_id` varchar(31) DEFAULT NULL,
  `members` tinyint DEFAULT NULL,
  `cnt` tinyint DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2048 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `payments` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint DEFAULT NULL,
  `plan` tinyint DEFAULT NULL,
  `price` tinyint DEFAULT 0,
  `txn_id` varchar(63) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1024 DEFAULT CHARSET=utf8mb4;