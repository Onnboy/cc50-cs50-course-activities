-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports
WHERE street = 'Humphrey Street';

-- Bakery witnesses
SELECT * FROM interviews
WHERE transcript LIKE '%bakery%';

-- Check the flights that left the city on the day of the crime
SELECT * FROM flights
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute;

-- Discover the destination of the suspicious flight
SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM flights
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute LIMIT 1);

-- Check the flight passengers to identify the thief
SELECT * FROM passengers
WHERE flight_id = (SELECT id FROM flights
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute LIMIT 1);

-- Match passports to names to identify the thief
SELECT name FROM people
WHERE passport_number IN (SELECT passport_number FROM passengers
WHERE flight_id = (SELECT id FROM flights
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute LIMIT 1));

-- Check the phone calls made by the thief on the day of the crime
SELECT * FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28;

-- Find out who received the thief's call (accomplice)
SELECT name FROM people
WHERE phone_number IN (SELECT receiver FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28
AND caller = (SELECT phone_number FROM people
WHERE name = 'Bruce'));
