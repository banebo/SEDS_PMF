-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema dw
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dw
-- -----------------------------------------------------
USE `dw` ;

-- -----------------------------------------------------
-- Table `dw`.`dw_time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_time` (
  `id_time` INT NOT NULL AUTO_INCREMENT,
  `minute` INT NOT NULL,
  `hour` INT NOT NULL,
  `day` INT NOT NULL,
  `month` INT NOT NULL,
  `year` INT NOT NULL,
  PRIMARY KEY (`id_time`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_aircraft`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_aircraft` (
  `id_aircraft` INT NOT NULL,
  `aircraft_name` VARCHAR(120) NOT NULL,
  PRIMARY KEY (`id_aircraft`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_airline`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_airline` (
  `id_airline` INT NOT NULL,
  `airline_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_airline`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_continent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_continent` (
  `id_continent` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_continent`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_country` (
  `id_country` INT NOT NULL,
  `country_name` VARCHAR(60) NOT NULL,
  `id_continent` INT NULL,
  PRIMARY KEY (`id_country`),
  INDEX `fk_dw_country_dw_continent1_idx` (`id_continent` ASC) ,
  CONSTRAINT `fk_dw_country_dw_continent1`
    FOREIGN KEY (`id_continent`)
    REFERENCES `dw`.`dw_continent` (`id_continent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_city`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_city` (
  `id_city` INT NOT NULL,
  `id_country` INT NOT NULL,
  `city_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_city`),
  INDEX `fk_dw_city_dw_country1_idx` (`id_country` ASC) ,
  CONSTRAINT `fk_dw_city_dw_country1`
    FOREIGN KEY (`id_country`)
    REFERENCES `dw`.`dw_country` (`id_country`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_airport`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_airport` (
  `id_airport` INT NOT NULL,
  `airport_name` VARCHAR(100) NOT NULL,
  `id_city` INT NOT NULL,
  PRIMARY KEY (`id_airport`),
  INDEX `fk_dw_airport_dw_city1_idx` (`id_city` ASC) ,
  CONSTRAINT `fk_dw_airport_dw_city1`
    FOREIGN KEY (`id_city`)
    REFERENCES `dw`.`dw_city` (`id_city`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`dw_facts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dw`.`dw_facts` (
  `departure_time` INT NOT NULL,
  `arrival_time` INT NOT NULL,
  `aircraft` INT NOT NULL,
  `airline` INT NOT NULL,
  `id_src_airport` INT NOT NULL,
  `id_dst_airport` INT NOT NULL,
  `tickets` INT NOT NULL,
  INDEX `fk_dw_facts_dw_time_idx` (`departure_time` ASC) ,
  PRIMARY KEY (`departure_time`, `arrival_time`, `aircraft`, `airline`, `id_src_airport`, `id_dst_airport`),
  INDEX `fk_dw_facts_dw_time1_idx` (`arrival_time` ASC) ,
  INDEX `fk_dw_facts_dw_aircraft1_idx` (`aircraft` ASC) ,
  INDEX `fk_dw_facts_dw_airline1_idx` (`airline` ASC) ,
  INDEX `fk_dw_facts_dw_airport1_idx` (`id_src_airport` ASC) ,
  INDEX `fk_dw_facts_dw_airport2_idx` (`id_dst_airport` ASC) ,
  CONSTRAINT `fk_dw_facts_dw_time`
    FOREIGN KEY (`departure_time`)
    REFERENCES `dw`.`dw_time` (`id_time`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dw_facts_dw_time1`
    FOREIGN KEY (`arrival_time`)
    REFERENCES `dw`.`dw_time` (`id_time`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dw_facts_dw_aircraft1`
    FOREIGN KEY (`aircraft`)
    REFERENCES `dw`.`dw_aircraft` (`id_aircraft`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dw_facts_dw_airline1`
    FOREIGN KEY (`airline`)
    REFERENCES `dw`.`dw_airline` (`id_airline`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dw_facts_dw_airport1`
    FOREIGN KEY (`id_src_airport`)
    REFERENCES `dw`.`dw_airport` (`id_airport`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dw_facts_dw_airport2`
    FOREIGN KEY (`id_dst_airport`)
    REFERENCES `dw`.`dw_airport` (`id_airport`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
