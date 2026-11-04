-- =======================================================
-- KrishiMitra – Smart Farmer Assistance Platform
-- Database Schema: database.sql
-- Compatible with MySQL 5.7+ / MySQL 8.0+ / MariaDB
-- =======================================================

CREATE DATABASE IF NOT EXISTS `krishimitra` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `krishimitra`;

-- -------------------------------------------------------
-- Table: farmers
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `farmers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `full_name` VARCHAR(100) NOT NULL,
    `mobile` VARCHAR(15) NOT NULL UNIQUE,
    `email` VARCHAR(100) NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `state` VARCHAR(60) NOT NULL DEFAULT 'Telangana',
    `district` VARCHAR(60) NOT NULL DEFAULT 'Nirmal',
    `village` VARCHAR(100) NULL,
    `land_size_acres` DECIMAL(5, 2) NOT NULL DEFAULT 2.50,
    `soil_type` VARCHAR(50) NOT NULL DEFAULT 'Black Soil',
    `preferred_language` VARCHAR(20) NOT NULL DEFAULT 'en',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------
-- Table: crops (Crop Tracking)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `crops` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `farmer_id` INT NOT NULL,
    `crop_name` VARCHAR(60) NOT NULL,
    `variety` VARCHAR(60) NULL,
    `sowing_date` DATE NOT NULL,
    `area_acres` DECIMAL(5, 2) NOT NULL DEFAULT 1.00,
    `soil_type` VARCHAR(50) NOT NULL DEFAULT 'Black Soil',
    `stage` ENUM('Sowing', 'Germination', 'Vegetative', 'Flowering', 'Yield Formation', 'Ripening', 'Harvested') NOT NULL DEFAULT 'Vegetative',
    `health_status` ENUM('Healthy', 'At Risk', 'Diseased') NOT NULL DEFAULT 'Healthy',
    `expected_harvest_date` DATE NULL,
    `notes` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_crops_farmer` FOREIGN KEY (`farmer_id`) REFERENCES `farmers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------
-- Table: crop_activities (Irrigation, Fertilizer, Spray logs)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `crop_activities` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `crop_id` INT NOT NULL,
    `activity_type` ENUM('Irrigation', 'Fertilizer', 'Pesticide Spray', 'Weeding', 'Harvesting', 'Inspection') NOT NULL,
    `activity_date` DATE NOT NULL,
    `notes` VARCHAR(255) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_activity_crop` FOREIGN KEY (`crop_id`) REFERENCES `crops` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------
-- Table: emergency_sos (Farmer emergency requests)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `emergency_sos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `farmer_id` INT NULL,
    `farmer_name` VARCHAR(100) NOT NULL,
    `contact_number` VARCHAR(15) NOT NULL,
    `district` VARCHAR(60) NOT NULL,
    `village` VARCHAR(100) NOT NULL,
    `issue_type` VARCHAR(60) NOT NULL,
    `severity` ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL DEFAULT 'High',
    `description` TEXT NOT NULL,
    `status` ENUM('Pending', 'In Progress', 'Resolved') NOT NULL DEFAULT 'Pending',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------
-- Table: chat_logs (Farmer chatbot queries)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `farmer_id` INT NULL,
    `user_message` TEXT NOT NULL,
    `bot_response` TEXT NOT NULL,
    `language` VARCHAR(10) NOT NULL DEFAULT 'en',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------
-- Sample Seed Data for Demonstration
-- -------------------------------------------------------

-- Default Demo Farmer (Password: 'farmer123', hashed with werkzeug scrypt/pbkdf2)
-- Password hash generated for 'farmer123':
INSERT INTO `farmers` (`id`, `full_name`, `mobile`, `email`, `password_hash`, `state`, `district`, `village`, `land_size_acres`, `soil_type`, `preferred_language`)
VALUES (
    1,
    'Ramesh Patel',
    '9876543210',
    'ramesh@krishimitra.org',
    'scrypt:32768:8:1$8bKYtsDsc6HDziWj$c110e0abd981cf92ac223a6ecb31e7af6a233a389963a79c951911868b0cf64eed15ad7fcbb9912c88135c703a51714a811fc58284ee8f7cf5dd639fb85cdb78',
    'Telangana',
    'Nirmal',
    'Basar',
    4.50,
    'Black Soil',
    'en'
) ON DUPLICATE KEY UPDATE `full_name` = VALUES(`full_name`);

-- Sample Tracked Crops for Demo Farmer
INSERT INTO `crops` (`id`, `farmer_id`, `crop_name`, `variety`, `sowing_date`, `area_acres`, `soil_type`, `stage`, `health_status`, `expected_harvest_date`, `notes`)
VALUES 
(1, 1, 'Paddy (Rice)', 'BPT-5204 (Samba Mahsuri)', DATE_SUB(CURDATE(), INTERVAL 65 DAY), 2.50, 'Clay Loam', 'Flowering', 'Healthy', DATE_ADD(CURDATE(), INTERVAL 55 DAY), 'Second top-dressing of Urea applied. Panicle initiation healthy with good water level.'),
(2, 1, 'Cotton', 'Bt Cotton RCH-659', DATE_SUB(CURDATE(), INTERVAL 95 DAY), 1.50, 'Black Soil', 'Yield Formation', 'At Risk', DATE_ADD(CURDATE(), INTERVAL 45 DAY), 'Minor sucking pest symptoms observed on lower leaves. Neem oil spray scheduled.'),
(3, 1, 'Chilli', 'Teja / G4', DATE_SUB(CURDATE(), INTERVAL 35 DAY), 0.50, 'Red Sandy Loam', 'Vegetative', 'Healthy', DATE_ADD(CURDATE(), INTERVAL 80 DAY), 'Intercultured and weeded. Strong vegetative growth with drip fertigation.')
ON DUPLICATE KEY UPDATE `crop_name` = VALUES(`crop_name`);

-- Sample Activities
INSERT INTO `crop_activities` (`crop_id`, `activity_type`, `activity_date`, `notes`)
VALUES
(1, 'Irrigation', DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Maintained 3-5 cm standing water during panicle formation stage'),
(1, 'Fertilizer', DATE_SUB(CURDATE(), INTERVAL 10 DAY), 'Applied MOP (Potash) and Urea split dose'),
(2, 'Pesticide Spray', DATE_SUB(CURDATE(), INTERVAL 5 DAY), '5% Neem Seed Kernel Extract (NSKE) sprayed for whitefly control'),
(3, 'Irrigation', DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Drip irrigation for 2 hours with 19-19-19 water-soluble fertilizer');

-- Sample Emergency SOS Request
INSERT INTO `emergency_sos` (`farmer_id`, `farmer_name`, `contact_number`, `district`, `village`, `issue_type`, `severity`, `description`, `status`)
VALUES 
(1, 'Ramesh Patel', '9876543210', 'Nirmal', 'Basar', 'Pest Attack Alert', 'High', 'Sudden yellow mosaic patches and whitefly clusters observed on adjacent soybean crop plots.', 'In Progress');
