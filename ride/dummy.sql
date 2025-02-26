
INSERT INTO user (username, email, password, role) VALUES
('john_doe', 'john@example.com', 'securepass123', 'driver'),
('jane_doe', 'jane@example.com', 'mypassword456', 'customer'),
('mike_smith', 'mike@example.com', 'driverpass789', 'driver'),
('sarah_connor', 'sarah@example.com', 'custpass321', 'customer');

-- Insert new drivers
INSERT INTO user (username, email, password, role) VALUES
('driver_1', 'driver1@example.com', 'pass1123', 'driver'),
('driver_2', 'driver2@example.com', 'pass2123', 'driver'),
('driver_3', 'driver3@example.com', 'pass3123', 'driver'),
('driver_4', 'driver4@example.com', 'pass4123', 'driver'),
('driver_5', 'driver5@example.com', 'pass5123', 'driver'),
('driver_6', 'driver6@example.com', 'pass6123', 'driver'),
('driver_7', 'driver7@example.com', 'pass7123', 'driver'),
('driver_8', 'driver8@example.com', 'pass8123', 'driver'),
('driver_9', 'driver9@example.com', 'pass9123', 'driver'),
('driver_10', 'driver10@example.com', 'pass10123', 'driver');

-- Insert vehicles for each driver
INSERT INTO vehicle (driver_id, vehicle_type, license_plate, model, color) VALUES
((SELECT id FROM user WHERE username='driver_1'), 'car', 'XYZ-1234', 'Toyota Camry', 'Red'),
((SELECT id FROM user WHERE username='driver_2'), 'bike', 'XYZ-5678', 'Yamaha R15', 'Blue'),
((SELECT id FROM user WHERE username='driver_3'), 'scooter', 'XYZ-9101', 'Suzuki Access', 'Black'),
((SELECT id FROM user WHERE username='driver_4'), 'car', 'XYZ-2345', 'Honda Civic', 'White'),
((SELECT id FROM user WHERE username='driver_5'), 'bike', 'XYZ-6789', 'Tesla Model 3', 'Green'),
((SELECT id FROM user WHERE username='driver_6'), 'scooter', 'XYZ-3456', 'BMW X5', 'Silver'),
((SELECT id FROM user WHERE username='driver_7'), 'car', 'XYZ-7890', 'Toyota Camry', 'Red'),
((SELECT id FROM user WHERE username='driver_8'), 'bike', 'XYZ-4567', 'Yamaha R15', 'Blue'),
((SELECT id FROM user WHERE username='driver_9'), 'scooter', 'XYZ-8901', 'Suzuki Access', 'Black'),
((SELECT id FROM user WHERE username='driver_10'), 'car', 'XYZ-5678', 'Honda Civic', 'White');
