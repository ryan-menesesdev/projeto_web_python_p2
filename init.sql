CREATE DATABASE livraria_bd;
USE livraria_bd;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
);

INSERT INTO products (title, price, stock) VALUES 
('Dom Quixote', 45.90, 10),
('1984', 35.50, 5),
('O Senhor dos Aneis', 120.00, 8),
('A Menina que Roubava Livros', 40.00, 15),
('O Pequeno Principe', 25.00, 20),
('Harry Potter e a Pedra Filosofal', 55.00, 12),
('O Alquimista', 30.00, 7),
('A Culpa e das Estrelas', 35.00, 10),
('O Codigo Da Vinci', 45.00, 4),
('Sapiens: Uma Breve Historia da Humanidade', 60.00, 6);
