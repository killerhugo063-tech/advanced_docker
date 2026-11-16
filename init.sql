
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    npm VARCHAR(30) NOT NULL UNIQUE,
    prodi VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO students (nama, npm, prodi)
VALUES
('Andi Pratama', '2301001', 'Sistem Informasi'),
('Budi Santoso', '2301002', 'Informatika'),
('Citra Lestari', '2301003', 'Sistem Informasi');
