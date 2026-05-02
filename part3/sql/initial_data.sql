-- Admin user (password: admin1234, bcrypt hash)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Admin', 'User', 'admin@hbnb.io',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    1,
    datetime('now'), datetime('now')
);

-- Amenities
INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at) VALUES
    ('00000000-0000-0000-0000-000000000010', 'WiFi',            datetime('now'), datetime('now')),
    ('00000000-0000-0000-0000-000000000011', 'Swimming Pool',   datetime('now'), datetime('now')),
    ('00000000-0000-0000-0000-000000000012', 'Air Conditioning',datetime('now'), datetime('now'));
