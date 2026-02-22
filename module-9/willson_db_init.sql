-- ---------------------------------------------------------------
-- Willson Financial - Milestone #2
-- File: willson_db_init.sql
--
-- Purpose:
--   1) Create a database for the group milestone project
--   2) Create tables with PK/FK + appropriate data types
--   3) Insert sample data (6+ per table + extra transactions for Milestone #3 prep)
--
-- Notes:
--   - Uses client_transaction (not "transaction") to avoid reserved keyword issues
--   - Sets up child tables first to avoid FK issues
-- ---------------------------------------------------------------

/* 1) Create and use the database */
CREATE DATABASE IF NOT EXISTS willson_financial;
USE willson_financial;


/* 2) Drop tables */
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS client_transaction;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS client;


/* 3) Create tables */
CREATE TABLE client (
  client_id INT AUTO_INCREMENT PRIMARY KEY,
  client_first_name VARCHAR(50) NOT NULL,
  client_last_name  VARCHAR(50) NOT NULL,
  client_email      VARCHAR(100) NOT NULL UNIQUE,
  client_created_date DATE NOT NULL
);

CREATE TABLE employee (
  employee_id INT AUTO_INCREMENT PRIMARY KEY,
  employee_first_name VARCHAR(50) NOT NULL,
  employee_last_name  VARCHAR(50) NOT NULL,
  employee_role       VARCHAR(50) NOT NULL
);

CREATE TABLE client_transaction (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  transaction_date DATE NOT NULL,
  transaction_amount DECIMAL(15,2) NOT NULL,
  transaction_type VARCHAR(50) NOT NULL,
  client_id INT NOT NULL,
  CONSTRAINT fk_client_transaction_client
    FOREIGN KEY (client_id)
    REFERENCES client(client_id)
    ON DELETE CASCADE
);

CREATE TABLE appointment (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  appointment_date DATETIME NOT NULL,
  client_id INT NOT NULL,
  employee_id INT NOT NULL,
  CONSTRAINT fk_appointment_client
    FOREIGN KEY (client_id)
    REFERENCES client(client_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_appointment_employee
    FOREIGN KEY (employee_id)
    REFERENCES employee(employee_id)
    ON DELETE CASCADE
);


/* 4) Insert data */

/* CLIENT (6 records) */
INSERT INTO client (client_first_name, client_last_name, client_email, client_created_date)
VALUES
  ('Ava',    'Martinez', 'ava.martinez@email.com',    '2025-10-15'),
  ('Mason',  'Reed',     'mason.reed@email.com',      '2025-11-04'),
  ('Sophia', 'Nguyen',   'sophia.nguyen@email.com',   '2025-12-12'),
  ('Ethan',  'Carter',   'ethan.carter@email.com',    '2026-01-05'),
  ('Olivia', 'Bennett',  'olivia.bennett@email.com',  '2026-01-18'),
  ('Noah',   'Parker',   'noah.parker@email.com',     '2026-02-01');

/* EMPLOYEE (6 records) */
INSERT INTO employee (employee_first_name, employee_last_name, employee_role)
VALUES
  ('Jake',    'Willson',   'Advisor'),
  ('Ned',     'Willson',   'Advisor'),
  ('Phoenix', 'Two Star',  'Office Administrator'),
  ('June',    'Santos',    'Compliance Manager'),
  ('Morgan',  'Lee',       'Advisor'),
  ('Taylor',  'Brooks',    'Client Services');

/*
CLIENT_TRANSACTION:
- Provide 6+ transactions for each client (10+ transactions in a single month for
  one client (client_id = 1) to support Milestone #3 requirement
*/
INSERT INTO client_transaction (transaction_date, transaction_amount, transaction_type, client_id)
VALUES
  -- Client 1 (Ava Martinez) - 11 transactions in January 2026
  ('2026-01-02',  5000.00, 'Deposit',    1),
  ('2026-01-05',   250.00, 'Withdrawal', 1),
  ('2026-01-06',   400.00, 'Withdrawal', 1),
  ('2026-01-07',  1200.00, 'Deposit',    1),
  ('2026-01-08',   150.00, 'Withdrawal', 1),
  ('2026-01-09',   900.00, 'Deposit',    1),
  ('2026-01-10',   100.00, 'Withdrawal', 1),
  ('2026-01-11',   300.00, 'Withdrawal', 1),
  ('2026-01-12',   700.00, 'Deposit',    1),
  ('2026-01-13',   200.00, 'Withdrawal', 1),
  ('2026-01-14',  1100.00, 'Deposit',    1),

  -- Other clients (spread across months)
  ('2026-01-15',  2500.00, 'Deposit',    2),
  ('2026-01-18',   500.00, 'Withdrawal', 3),
  ('2026-02-02',  3500.00, 'Deposit',    4),
  ('2026-02-10',   250.00, 'Withdrawal', 5),
  ('2026-02-12',   900.00, 'Deposit',    6);

/* APPOINTMENT (6 records) */
INSERT INTO appointment (appointment_date, client_id, employee_id)
VALUES
  ('2026-02-10 09:00:00', 1, 1), -- Ava with Jake
  ('2026-02-11 10:30:00', 2, 2), -- Mason with Ned
  ('2026-02-12 14:00:00', 3, 5), -- Sophia with Morgan
  ('2026-02-13 13:15:00', 4, 6), -- Ethan with Taylor
  ('2026-02-14 11:00:00', 1, 4), -- Ava with June (compliance)
  ('2026-02-15 15:30:00', 5, 3); -- Olivia with Phoenix (admin)