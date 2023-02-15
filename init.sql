
DROP DATABASE chatapp;
DROP USER 'testuser'@'localhost';

CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'Testuser1!';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'localhost';

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE channels (
    channel_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    channel_name VARCHAR(255) UNIQUE NOT NULL,
    abstract VARCHAR(255),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    channel_id INTEGER,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);
