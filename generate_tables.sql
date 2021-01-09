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
CREATE SCHEMA IF NOT EXISTS `dw` ;
USE `dw` ;

-- -----------------------------------------------------
-- Table `dw`.`Continent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Continent` ;

CREATE TABLE IF NOT EXISTS `dw`.`Continent` (
  `idContinent` INT NOT NULL,
  `continent_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idContinent`),
  UNIQUE INDEX `name_UNIQUE` (`continent_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Region`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Region` ;

CREATE TABLE IF NOT EXISTS `dw`.`Region` (
  `idRegion` INT NOT NULL,
  `region_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idRegion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Country`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Country` ;

CREATE TABLE IF NOT EXISTS `dw`.`Country` (
  `idCountry` INT NOT NULL,
  `country_name` VARCHAR(60) NOT NULL,
  `alpha_2` VARCHAR(2) NOT NULL,
  `alpha_3` VARCHAR(3) NOT NULL,
  `code` INT NOT NULL,
  `idRegion` INT NULL,
  `idContinent` INT NULL,
  PRIMARY KEY (`idCountry`),
  UNIQUE INDEX `name_UNIQUE` (`country_name` ASC) ,
  INDEX `fk_Country_Continent_idx` (`idContinent` ASC) ,
  UNIQUE INDEX `alpha_2_UNIQUE` (`alpha_2` ASC) ,
  UNIQUE INDEX `alpha_3_UNIQUE` (`alpha_3` ASC) ,
  INDEX `fk_Country_Region1_idx` (`idRegion` ASC) ,
  UNIQUE INDEX `code_UNIQUE` (`code` ASC) ,
  CONSTRAINT `fk_Country_Continent`
    FOREIGN KEY (`idContinent`)
    REFERENCES `dw`.`Continent` (`idContinent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Country_Region1`
    FOREIGN KEY (`idRegion`)
    REFERENCES `dw`.`Region` (`idRegion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`City`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`City` ;

CREATE TABLE IF NOT EXISTS `dw`.`City` (
  `idCity` INT NOT NULL,
  `city_name` VARCHAR(45) NOT NULL,
  `time_zone` DOUBLE NULL,
  `idCountry` INT NOT NULL,
  PRIMARY KEY (`idCity`),
  INDEX `fk_City_Country1_idx` (`idCountry` ASC) ,
  UNIQUE INDEX `city_name_UNIQUE` (`city_name` ASC) ,
  CONSTRAINT `fk_City_Country1`
    FOREIGN KEY (`idCountry`)
    REFERENCES `dw`.`Country` (`idCountry`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Airport`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Airport` ;

CREATE TABLE IF NOT EXISTS `dw`.`Airport` (
  `idAirport` INT NOT NULL,
  `airport_name` VARCHAR(100) NOT NULL,
  `airport_IATA` VARCHAR(3) NULL,
  `airport_ICAO` VARCHAR(4) NULL,
  `idCity` INT NOT NULL,
  PRIMARY KEY (`idAirport`),
  INDEX `fk_Airport_City1_idx` (`idCity` ASC) ,
  CONSTRAINT `fk_Airport_City1`
    FOREIGN KEY (`idCity`)
    REFERENCES `dw`.`City` (`idCity`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Aircraft`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Aircraft` ;

CREATE TABLE IF NOT EXISTS `dw`.`Aircraft` (
  `idAircraft` INT NOT NULL,
  `aircraft_name` VARCHAR(120) NOT NULL,
  `aircraft_IATA` VARCHAR(2) NULL,
  `aircraft_ICAO` VARCHAR(3) NULL,
  PRIMARY KEY (`idAircraft`),
  UNIQUE INDEX `name_UNIQUE` (`aircraft_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Airline`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Airline` ;

CREATE TABLE IF NOT EXISTS `dw`.`Airline` (
  `idAirline` INT NOT NULL,
  `airline_name` VARCHAR(45) NOT NULL,
  `country_of_origin` INT NULL,
  `airline_IATA` VARCHAR(2) NULL,
  `airline_ICAO` VARCHAR(3) NULL,
  `callsign` VARCHAR(45) NULL,
  PRIMARY KEY (`idAirline`),
  INDEX `fk_Company_Country1_idx` (`country_of_origin` ASC) ,
  UNIQUE INDEX `name_UNIQUE` (`airline_name` ASC) ,
  CONSTRAINT `fk_Company_Country1`
    FOREIGN KEY (`country_of_origin`)
    REFERENCES `dw`.`Country` (`idCountry`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Person` ;

CREATE TABLE IF NOT EXISTS `dw`.`Person` (
  `idPerson` INT NOT NULL,
  `person_name` VARCHAR(45) NOT NULL,
  `person_surname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idPerson`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Route`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Route` ;

CREATE TABLE IF NOT EXISTS `dw`.`Route` (
  `idRoute` INT NOT NULL,
  `idAirline` INT NOT NULL,
  `id_src_airport` INT NOT NULL,
  `id_dst_airport` INT NOT NULL,
  PRIMARY KEY (`idRoute`),
  INDEX `fk_Route_Airline1_idx` (`idAirline` ASC) ,
  INDEX `fk_srcAirport_idx` (`id_src_airport` ASC) ,
  INDEX `fk_dstAirport_idx` (`id_dst_airport` ASC) ,
  CONSTRAINT `fk_Route_Airline1`
    FOREIGN KEY (`idAirline`)
    REFERENCES `dw`.`Airline` (`idAirline`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_srcAirport`
    FOREIGN KEY (`id_src_airport`)
    REFERENCES `dw`.`Airport` (`idAirport`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dstAirport`
    FOREIGN KEY (`id_dst_airport`)
    REFERENCES `dw`.`Airport` (`idAirport`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Flight`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Flight` ;

CREATE TABLE IF NOT EXISTS `dw`.`Flight` (
  `idFlight` INT NOT NULL,
  `dt_of_departure` DATETIME NOT NULL,
  `dt_of_arrival` DATETIME NOT NULL,
  `flight_number` VARCHAR(12) NOT NULL,
  `idRoute` INT NOT NULL,
  PRIMARY KEY (`idFlight`),
  INDEX `fk_Flight_Route1_idx` (`idRoute` ASC) ,
  CONSTRAINT `fk_Flight_Route1`
    FOREIGN KEY (`idRoute`)
    REFERENCES `dw`.`Route` (`idRoute`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Ticket`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Ticket` ;

CREATE TABLE IF NOT EXISTS `dw`.`Ticket` (
  `idTicket` INT NOT NULL AUTO_INCREMENT,
  `date_of_purchase` DATE NOT NULL,
  `price` INT NOT NULL,
  `idPerson` INT NOT NULL,
  `idFlight` INT NOT NULL,
  PRIMARY KEY (`idTicket`),
  INDEX `fk_Ticket_Person1_idx` (`idPerson` ASC) ,
  INDEX `fk_idFlight_idx` (`idFlight` ASC) ,
  CONSTRAINT `fk_Ticket_Person1`
    FOREIGN KEY (`idPerson`)
    REFERENCES `dw`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_idFlight`
    FOREIGN KEY (`idFlight`)
    REFERENCES `dw`.`Flight` (`idFlight`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dw`.`Route_has_Aircraft`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dw`.`Route_has_Aircraft` ;

CREATE TABLE IF NOT EXISTS `dw`.`Route_has_Aircraft` (
  `idRoute` INT NOT NULL,
  `idAircraft` INT NOT NULL,
  PRIMARY KEY (`idRoute`, `idAircraft`),
  INDEX `fk_Route_has_Aircraft_Aircraft1_idx` (`idAircraft` ASC) ,
  INDEX `fk_Route_has_Aircraft_Route1_idx` (`idRoute` ASC) ,
  CONSTRAINT `fk_Route_has_Aircraft_Route1`
    FOREIGN KEY (`idRoute`)
    REFERENCES `dw`.`Route` (`idRoute`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Route_has_Aircraft_Aircraft1`
    FOREIGN KEY (`idAircraft`)
    REFERENCES `dw`.`Aircraft` (`idAircraft`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
