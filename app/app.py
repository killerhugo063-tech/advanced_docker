
import os
import mysql.connector
import redis

from flask import Flask, request, redirect, url_for, render_template_string, jsonify

app = Flask(__name__)

# =====================================
# DATABASE CONFIGURATION
# =====================================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "advanced_db"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "appsecret"),
    "connection_timeout": 3
}

# =====================================
# REDIS CONFIGURATION
# =====================================

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=3
)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# =====================================
# DASHBOARD DESIGN
# =====================================

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Docker Dashboard</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #f8fafc;
            min-height: 100vh;
        }

        header {
            padding: 25px 7%;
            background: #111c32;
            border-bottom: 1px solid #29364d;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        header h1 {
            font-size: 23px;
            color: #60a5fa;
        }

        header span {
            color: #94a3b8;
            font-size: 13px;
        }

        main {
            width: 86%;
            max-width: 1200px;
            margin: 35px auto;
        }

        .welcome {
            margin-bottom: 28px;
        }

        .welcome h2 {
            font-size: 27px;
            margin-bottom: 9px;
        }

        .welcome p {
            color: #94a3b8;
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-bottom: 30px;
        }

        .card {
            background: #1e293b;
            padding: 24px;
            border-radius: 14px;
            border: 1px solid #334155;
        }

        .card h3 {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .status {
            font-size: 23px;
            font-weight: bold;
        }

        .online {
            color: #4ade80;
        }

        .offline {
            color: #f87171;
        }

        .content-grid {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 20px;
        }

        input {
            width: 100%;
            padding: 13px;
            margin-top: 13px;
            border-radius: 8px;
            border: 1px solid #475569;
            background: #0f172a;
            color: white;
            outline: none;
        }

        input:focus {
            border-color: #3b82f6;
        }

        button {
            width: 100%;
            padding: 13px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            margin-top: 15px;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background: #1d4ed8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 13px 10px;
            text-align: left;
            border-bottom: 1px solid #334155;
            font-size: 13px;
        }

        th {
            color: #60a5fa;
        }

        .delete {
            width: auto;
            margin: 0;
            padding: 7px 12px;
            background: #dc2626;
        }

        .message {
            background: #164e63;
            padding: 13px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .cache {
            color: #fbbf24;
            font-size: 13px;
            margin-top: 12px;
        }

        footer {
            text-align: center;
            padding: 30px;
            color: #64748b;
            font-size: 13px;
        }

        @media(max-width: 800px) {
            .status-grid {
                grid-template-columns: 1fr;
            }

            .content-grid {
                grid-template-columns: 1fr;
            }

            main {
                width: 92%;
            }

            .table-wrapper {
                overflow-x: auto;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>🐳 Advanced Docker</h1>
    <span>Multi-Container Application Dashboard</span>
</header>

<main>

    <section class="welcome">
        <h2>System Overview</h2>
        <p>Monitoring Flask, MySQL, Redis, and Docker services.</p>
    </section>

    {% if message %}
    <div class="message">{{ message }}</div>
    {% endif %}

    <section class="status-grid">

        <div class="card">
            <h3>WEB APPLICATION</h3>
            <div class="status online">● ONLINE</div>
            <p>Flask Application</p>
        </div>

        <div class="card">
            <h3>MYSQL DATABASE</h3>
            <div class="status {{ 'online' if db_status else 'offline' }}">
                {{ '● ONLINE' if db_status else '● OFFLINE' }}
            </div>
            <p>Database Connection</p>
        </div>

        <div class="card">
            <h3>REDIS CACHE</h3>
            <div class="status {{ 'online' if redis_status else 'offline' }}">
                {{ '● ONLINE' if redis_status else '● OFFLINE' }}
            </div>
            <p>In-Memory Storage</p>
        </div>

    </section>

    <section class="content-grid">

        <div class="card">
            <h3>ADD NEW STUDENT</h3>

            <form method="POST" action="{{ url_for('add_student') }}">

                <input
                    type="text"
                    name="nama"
                    placeholder="Nama mahasiswa"
                    required
                >

                <input
                    type="text"
                    name="npm"
                    placeholder="NPM mahasiswa"
                    required
                >

                <input
                    type="text"
                    name="prodi"
                    placeholder="Program studi"
                    required
                >

                <button type="submit">+ Add Student</button>

            </form>

            <div class="cache">
                Redis Cache: {{ cache_status }}
            </div>

            <div class="cache">
                Total Mahasiswa: {{ total }}
            </div>
        </div>

        <div class="card">
            <h3>STUDENT DATABASE</h3>

            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nama</th>
                            <th>NPM</th>
                            <th>Prodi</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>

                    <tbody>
                    {% for student in students %}
                        <tr>
                            <td>{{ student.id }}</td>
                            <td>{{ student.nama }}</td>
                            <td>{{ student.npm }}</td>
                            <td>{{ student.prodi }}</td>
                            <td>
                                <form method="POST"
                                      action="{{ url_for('delete_student', student_id=student.id) }}">
                                    <button class="delete" type="submit">
                                        Delete
                                    </button>
                                </form>
                            </td>
                        </tr>
                    {% else %}
                        <tr>
                            <td colspan="5">Belum ada data mahasiswa.</td>
                        </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

    </section>

</main>

<footer>
    Advanced Docker Deployment | Flask + MySQL + Redis + Nginx
</footer>

</body>
</html>
"""


# =====================================
# MAIN DASHBOARD
# =====================================

@app.route("/")
def index():

    db_status = False
    redis_status = False
    students = []
    total = 0
    cache_status = "Unavailable"

    # Check MySQL
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nama, npm, prodi
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        cursor.close()
        conn.close()

        db_status = True

    except mysql.connector.Error as error:
        print("MySQL Error:", error)

    # Check Redis and cache student count
    try:
        redis_client.ping()
        redis_status = True

        cached_total = redis_client.get("student_count")

        if cached_total is not None:
            total = int(cached_total)
            cache_status = "HIT - Data dari Redis"
        elif db_status:
            total = len(students)
            redis_client.setex("student_count", 60, total)
            cache_status = "MISS - Data disimpan ke Redis"

    except redis.RedisError as error:
        print("Redis Error:", error)

    message = request.args.get("message", "")

    return render_template_string(
        HTML,
        db_status=db_status,
        redis_status=redis_status,
        students=students,
        total=total,
        cache_status=cache_status,
        message=message
    )


# =====================================
# ADD STUDENT
# =====================================

@app.route("/add", methods=["POST"])
def add_student():

    nama = request.form.get("nama", "").strip()
    npm = request.form.get("npm", "").strip()
    prodi = request.form.get("prodi", "").strip()

    if not nama or not npm or not prodi:
        return redirect(url_for(
            "index",
            message="Semua data wajib diisi."
        ))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO students (nama, npm, prodi)
            VALUES (%s, %s, %s)
            """,
            (nama, npm, prodi)
        )

        conn.commit()

        # Hapus cache agar jumlah mahasiswa diperbarui pada kunjungan berikutnya.
        try:
            redis_client.delete("student_count")
        except redis.RedisError as redis_error:
            app.logger.warning("Cache Redis tidak dapat dihapus: %s", redis_error)

        return redirect(url_for(
            "index",
            message="Data mahasiswa berhasil ditambahkan!"
        ))

    except mysql.connector.IntegrityError as error:
        if conn and conn.is_connected():
            conn.rollback()

        app.logger.warning("Data mahasiswa melanggar aturan database: %s", error)

        if getattr(error, "errno", None) == 1062:
            message = "NPM sudah terdaftar. Gunakan NPM yang berbeda."
        else:
            message = "Data tidak dapat disimpan karena melanggar aturan database."

        return redirect(url_for("index", message=message))

    except mysql.connector.Error as error:
        if conn and conn.is_connected():
            conn.rollback()

        app.logger.exception("Kesalahan MySQL saat menambahkan mahasiswa")
        return redirect(url_for(
            "index",
            message="Gagal menyimpan data ke database. Periksa log aplikasi."
        ))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# =====================================
# DELETE STUDENT
# =====================================

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        conn.commit()
        cursor.close()

        try:
            redis_client.delete("student_count")
        except redis.RedisError:
            pass

        return redirect(url_for(
            "index",
            message="Data mahasiswa berhasil dihapus."
        ))

    except mysql.connector.Error as error:
        print("Delete Error:", error)

        return redirect(url_for(
            "index",
            message="Gagal menghapus data."
        ))

    finally:
        if conn and conn.is_connected():
            conn.close()


# =====================================
# HEALTHCHECK
# =====================================

@app.route("/health/live")
def live():

    return jsonify({
        "status": "alive",
        "service": "flask-web"
    }), 200


@app.route("/health/ready")
@app.route("/health")
def health():

    db_ok = False
    redis_ok = False

    try:
        conn = get_db_connection()
        conn.close()
        db_ok = True
    except mysql.connector.Error:
        pass

    try:
        redis_client.ping()
        redis_ok = True
    except redis.RedisError:
        pass

    healthy = db_ok and redis_ok

    return jsonify({
        "status": "healthy" if healthy else "unhealthy",
        "mysql": "connected" if db_ok else "disconnected",
        "redis": "connected" if redis_ok else "disconnected"
    }), 200 if healthy else 503


# =====================================
# APPLICATION ENTRY POINT
# =====================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
