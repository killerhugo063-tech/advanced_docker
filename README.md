# Advanced Docker Deployment

Aplikasi demonstrasi multi-container menggunakan Flask, MySQL, Redis, dan Nginx.

## Teknologi dan service

| Service | Fungsi | Port |
|---|---|---|
| `web` | Backend aplikasi Flask + Gunicorn | 5000 (internal) |
| `db` | Database MySQL 8 | 3306 (internal) |
| `redis` | Cache Redis 7 dengan AOF | 6379 (internal) |
| `nginx` | Reverse proxy | 8080 pada host menuju 80 |

Hanya Nginx yang memublikasikan port ke host. Flask, MySQL, dan Redis berkomunikasi melalui network Docker.

## Struktur folder

```text
advanced-docker/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   └── init.sql
├── nginx/
│   └── default.conf
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Persiapan

- Docker Desktop sudah terpasang dan berjalan.
- Git (opsional, jika akan mengunggah ke GitHub).
- PowerShell pada Windows.

Salin `.env.example` menjadi `.env`, lalu isi password lokal sendiri. Jangan unggah `.env` ke repository publik.

```powershell
Copy-Item .env.example .env
notepad .env
```

## Menjalankan aplikasi

Jalankan perintah dari folder project:

```powershell
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Buka dashboard:

- http://localhost:8080
- Live check: http://localhost:8080/health/live
- Readiness check: http://localhost:8080/health/ready
- Nginx check: http://localhost:8080/nginx-health

## Log dan pemeliharaan

```powershell
docker compose logs --tail=100 web
docker compose logs --tail=100 db
docker compose logs --tail=100 redis
docker compose logs --tail=100 nginx
docker compose ps
```

Build ulang Flask setelah perubahan kode:

```powershell
docker compose up -d --build web
```

## Network dan volume

- `frontend`: menghubungkan Nginx dan Flask.
- `backend`: network internal untuk Flask, MySQL, dan Redis.
- `mysql_data`: menyimpan data MySQL.
- `redis_data`: menyimpan data Redis (AOF).

Periksa resource:

```powershell
docker network ls
docker volume ls
```

## Skenario pengujian praktikum

### 1. Koneksi database
Tambahkan data mahasiswa melalui dashboard dan pastikan data tampil pada tabel.

### 2. Persistence MySQL
Catat satu data uji, lalu hapus dan buat ulang container database tanpa menghapus volume:

```powershell
docker compose rm -sf db
docker compose up -d db
docker compose ps
```

Pastikan data uji masih ada setelah database sehat.

**Jangan gunakan `docker compose down -v` saat menguji persistence**, karena opsi `-v` menghapus volume.

### 3. Redis outage
```powershell
docker compose stop redis
docker compose ps
curl.exe -i http://localhost:8080/health/ready
docker compose start redis
docker compose ps
```

Readiness mengembalikan HTTP 503 saat Redis tidak tersedia, karena endpoint readiness memeriksa MySQL dan Redis.

### 4. Nginx upstream troubleshooting
Buat salinan cadangan `nginx/default.conf`. Ubah sementara upstream `server web:5000;` menjadi hostname tidak valid, restart Nginx, dan amati log serta respons browser. Kembalikan konfigurasi ke `server web:5000;`, lalu restart Nginx.

### 5. Port security
Periksa `docker compose ps`. Hanya port Nginx `8080:80` yang dipublikasikan ke host. MySQL dan Redis hanya memakai port internal network Docker.

### 6. Healthcheck dan rebuild
Periksa status dengan `docker compose ps`, lalu ubah source code Flask dan jalankan perintah rebuild di atas.

## Catatan database

`database/init.sql` dijalankan oleh image MySQL hanya ketika data directory pertama kali diinisialisasi (volume database masih kosong). Mengubah file SQL tersebut tidak otomatis mengubah database volume yang sudah ada.

## Catatan keamanan

- `.env` tidak disertakan dalam repository.
- Gunakan password yang berbeda dan kuat untuk lingkungan masing-masing.
- Password contoh pada `.env.example` harus diganti sebelum menjalankan aplikasi.
- Ini adalah project praktikum, bukan konfigurasi produksi.

## Catatan challenge

Project ini mendemonstrasikan koneksi database, rebuild, healthcheck, pembatasan port, dan Nginx upstream. Pastikan kode tantangan individual yang diwajibkan dosen cocok dengan daftar/pembagian resmi tugas.
