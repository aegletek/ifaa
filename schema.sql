CREATE TABLE customers(

customer_id VARCHAR(50) PRIMARY KEY,

customer_name VARCHAR(100),

policy_number VARCHAR(50),

join_date DATE

);


CREATE TABLE claims(

claim_id VARCHAR(50) PRIMARY KEY,

customer_id VARCHAR(50),

vehicle_number VARCHAR(50),

claim_date DATE,

claim_amount NUMERIC,

claim_description TEXT
);