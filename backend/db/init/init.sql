-- Créer la base (si elle n'existe pas)
-- Note: Avec PostgreSQL, la DB principale est créée via env POSTGRES_DB, donc souvent inutile ici

-- Table des produits
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    promo_price NUMERIC(10,2) DEFAULT 0,
    promo TEXT DEFAULT 'Non',
    description TEXT,
    images TEXT,
    product TEXT,
    stock INT DEFAULT 0
);


CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number TEXT ,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT,
    product TEXT,
    price NUMERIC(10,2),
    quantity INT DEFAULT 1,
    livré TEXT DEFAULT 'Non',
    date_livré TIMESTAMP,
    retourné TEXT DEFAULT 'Non',
    date_retour TIMESTAMP,
    fermé TEXT DEFAULT 'Non'
);

-- --------------------------
-- Table products
-- --------------------------
INSERT INTO products (name , product, price, promo_price, promo, description, images, stock) VALUES
('Chaussures','Chaussures', 100, 80, 'yes', 'Chaussures confortables', 'chaussures.jpg', 10),
('Sac à main','Sac à main', 150, 150, 'no', 'Sac en cuir élégant', 'sac.jpg', 5),
('Collier','Collier', 50, 45, 'yes', 'Collier en or', 'collier.jpg', 12),
('Montre connectée','Montre connectée', 250, 220, 'yes', 'Montre intelligente', 'smartwatch.jpg', 6);

-- --------------------------
-- Table orders
-- --------------------------
-- INSERT INTO orders (date, name, email, phone, address, product, price, quantity, livré, date_livré, retourné, date_retour, fermé) VALUES
-- ('2025-12-28 12:00', 'Alice Dupont', 'alice@example.com', '0601020304', '10 rue de Paris', 'Chaussures', 100, 2, 'Non', 'pas encore', 'Non', 'pas encore', 'Non'),
-- ('2025-12-28 13:30', 'Bob Martin', 'bob@example.com', '0612345678', '20 avenue Lyon', 'Montre', 200, 1, 'Oui', '2025-12-29 10:00', 'Non', 'pas encore', 'Non'),
-- ('2025-12-28 14:00', 'Claire Leroy', 'claire@example.com', '0678901234', '5 boulevard Nice', 'Sac à main', 150, 1, 'Non', 'pas encore', 'Non', 'pas encore', 'Non');

