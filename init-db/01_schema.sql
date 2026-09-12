CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    balance NUMERIC(12,2) DEFAULT 0,
    currency TEXT NOT NULL
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(id),
    type TEXT NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
