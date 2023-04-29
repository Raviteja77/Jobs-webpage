# Jobs-webpage



Create Database:

```
CREATE DATABASE jobapp;

CREATE TABLE users(
    -> id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    -> first_name VARCHAR(20) NOT NULL,
    -> last_name VARCHAR(20) NOT NULL,
    -> username VARCHAR(20) NOT NULL,
    -> email VARCHAR(64) NOT NULL,
    -> password VARCHAR(100) NOT NULL,
    -> role VARCHAR(20) NOT NULL,
    -> PRIMARY KEY(id)
    -> );
```

