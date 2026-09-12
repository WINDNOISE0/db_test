INSERT INTO users (email) VALUES ('alice@test.com'), ('bob@test.com'), ('carol@test.com'), ('dave@test.com');

INSERT INTO accounts (user_id, balance, currency) VALUES (1, 1000.00, 'USD'), (2, 500.00, 'EUR'), (3, 0.00, 'USD'), (4, 0.00, 'USD');

INSERT INTO transactions (account_id, type, amount, status) VALUES
(1, 'deposit', 200.00, 'success'),
(1, 'withdrawal', 50.00, 'success'),
(2, 'deposit', 100.00, 'pending'),
(2, 'deposit', 300.00, 'success'),
(3, 'deposit', 20.00, 'failed');
