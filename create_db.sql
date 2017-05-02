CREATE TABLE `klimov`.`user` ( 
	`login` VARCHAR(16) NOT NULL , 
	`fio` VARCHAR(128) NOT NULL , 
	`group` VARCHAR(6) NULL DEFAULT NULL , 
	`role` SET('student','admin','blocked') NOT NULL DEFAULT 
	'student' , `passw` VARCHAR(40) NOT NULL , PRIMARY KEY (`login`)
	) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE `klimov`.`token` ( 
	`uid` VARCHAR(64) NOT NULL , 
	`login` VARCHAR(16) NOT NULL , 
	PRIMARY KEY (`uid`),
	FOREIGN KEY (`login`)
		REFERENCES `klimov`.`user`(`login`)
    	ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

CREATE TABLE `klimov`.`result` ( 
	`uid` BIGINT NOT NULL AUTO_INCREMENT , 
	`login` VARCHAR(16) NOT NULL ,
	`date_passing` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
	`log_answ` VARCHAR(20) NOT NULL , 
	`syst_huma` TINYINT NOT NULL , 
	`syst_sign` TINYINT NOT NULL , 
	`syst_arti` TINYINT NOT NULL , 
	`syst_tech` TINYINT NOT NULL , 
	`syst_natu` TINYINT NOT NULL ,
    PRIMARY KEY (`uid`),
	FOREIGN KEY (`login`)
		REFERENCES `klimov`.`user`(`login`)
    	ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_general_ci;

INSERT INTO `klimov`.`user` VALUES (
	'admin', 'Койшинов Тимур Саматулы', NULL, 'admin', SHA1('mysecretpass'));