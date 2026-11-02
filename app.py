import os
import sqlite3
import secrets
import hashlib
import hmac
import csv
import io
from datetime import datetime
from functools import wraps
from flask import (
    Flask, g, request, redirect, url_for, session,
    flash, render_template, make_response, abort
)
import requests
import re
import time
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from flask import jsonify

SARAFI_URL = "https://sarafi.af/fa/exchange-rates/sarai-shahzada"

rates_cache = {
    "data": [],
    "updated_at": None,
    "last_fetch": 0
}

def get_sarai_shahzada_rates():
    now = time.time()

    # Use cached data for 60 seconds
    if rates_cache["data"] and now - rates_cache["last_fetch"] < 60:
        return rates_cache["data"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8"
    }

    response = requests.get(
        SARAFI_URL,
        headers=headers,
        timeout=15
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    found_rates = []

    for row in soup.select("table tr"):
        cells = row.find_all(["td", "th"], recursive=False)

        if len(cells) < 3:
            continue

        values = [
            cell.get_text(" ", strip=True)
            for cell in cells
        ]

        row_text = " ".join(values)
        code_match = re.search(r"\b([A-Z]{3})\b", row_text)

        if not code_match:
            continue

        code = code_match.group(1)

        # Ignore rows outside the main currency list
        allowed_codes = {
            "USD", "EUR", "GBP", "IRR", "PKR",
            "SAR", "AED", "CHF", "AUD", "CAD",
            "RUB", "DKK", "SEK", "NOK", "TRY",
            "CNY", "KWD", "QAR", "BHD", "JPY"
        }

        if code not in allowed_codes:
            continue

        numbers = []
        for value in values:
            cleaned = value.replace(",", "")
            if re.fullmatch(r"\d+(?:\.\d+)?", cleaned):
                numbers.append(float(cleaned))

        if len(numbers) < 2:
            continue

        found_rates.append({
            "code": code,
            "name": values[0],
            "buy": numbers[0],
            "sell": numbers[1],
            "unit": 1000 if code in ["IRR", "PKR", "JPY"] else 1
        })

    # Do not replace good cached data with an empty result
    if not found_rates:
        if rates_cache["data"]:
            return rates_cache["data"]
        raise ValueError("No exchange rates were found on the source page.")

    # Remove duplicate currency rows
    unique_rates = {}
    for rate in found_rates:
        unique_rates[rate["code"]] = rate

    result = list(unique_rates.values())

    rates_cache["data"] = result
    rates_cache["last_fetch"] = now
    rates_cache["updated_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    return result


def live_rates_api():
    try:
        data = get_sarai_shahzada_rates()

        return jsonify({
            "success": True,
            "source": SARAFI_URL,
            "updated_at": rates_cache["updated_at"],
            "rates": data
        })

    except Exception as error:
        if rates_cache["data"]:
            return jsonify({
                "success": True,
                "cached": True,
                "message": "Showing last available rates.",
                "updated_at": rates_cache["updated_at"],
                "rates": rates_cache["data"]
            })

        return jsonify({
            "success": False,
            "message": "Exchange rates are temporarily unavailable."
        }), 503
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get(
    "SHARIFI_DB_PATH",
    os.path.join(APP_DIR, "sharifi.db")
)

SECRET_KEY = os.environ.get("SHARIFI_SECRET_KEY")
if not SECRET_KEY:
    if os.environ.get("RENDER") or os.environ.get("FLASK_ENV") == "production":
        raise RuntimeError("SHARIFI_SECRET_KEY must be configured in production.")
    SECRET_KEY = "dev-only-change-this-secret-key-before-deployment"

app = Flask(__name__)
app.secret_key = SECRET_KEY
LANGUAGES = {
    "fa": {
        "name": "دری",
        "dir": "rtl"
    },
    "en": {
        "name": "EN",
        "dir": "ltr"
    }
}

@app.route("/language/<lang>")
def change_language(lang):
    if lang not in LANGUAGES:
        lang = "fa"

    session["language"] = lang

    return redirect(request.referrer or url_for("index"))
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("SHARIFI_HTTPS", "0") == "1",
    MAX_CONTENT_LENGTH=1_000_000,
)

BUSINESS = {
    "name": "صرافی شریفی",
    "english": "Sharifi Exchange",
    "phone": "0775179090",
    "email": "mohammadomarsharifi11279@gmail.com",
    "address": "سمنگان، شهر آیبیک، مارکیت جدید صرافی ها، کوچه بایسیکل سازی، منزل سوم، دوکان نمبر 122",
}

CURRENCIES = [
    ("AFN", "افغانی", "Afghan Afghani"),
    ("USD", "دالر امریکایی", "US Dollar"),
    ("EUR", "یورو", "Euro"),
    ("GBP", "پوند بریتانیا", "British Pound"),
    ("PKR", "کلدار پاکستانی", "Pakistani Rupee"),
    ("IRR", "ریال ایرانی", "Iranian Rial"),
    ("AED", "درهم امارات", "UAE Dirham"),
    ("SAR", "ریال سعودی", "Saudi Riyal"),
    ("TRY", "لیره ترکیه", "Turkish Lira"),
    ("INR", "روپیه هندی", "Indian Rupee"),
]


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA busy_timeout = 5000")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        260_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password, encoded):
    try:
        salt, expected = encoded.split("$", 1)
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            260_000
        ).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, AttributeError):
        return False


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")

    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE COLLATE NOCASE,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL DEFAULT 'customer',
      created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS rates (
      code TEXT PRIMARY KEY,
      name_dari TEXT NOT NULL,
      name_en TEXT NOT NULL,
      buy_rate TEXT,
      sell_rate TEXT,
      updated_at TEXT,
      updated_by INTEGER,
      source TEXT NOT NULL DEFAULT 'Not configured',
      FOREIGN KEY(updated_by) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS rate_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      code TEXT NOT NULL,
      buy_rate TEXT,
      sell_rate TEXT,
      source TEXT NOT NULL,
      changed_at TEXT NOT NULL,
      changed_by INTEGER,
      FOREIGN KEY(code) REFERENCES rates(code),
      FOREIGN KEY(changed_by) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      request_no TEXT NOT NULL UNIQUE,
      user_id INTEGER NOT NULL,
      direction TEXT NOT NULL CHECK(direction IN ('BUY','SELL')),
      currency TEXT NOT NULL,
      amount TEXT NOT NULL,
      rate TEXT NOT NULL,
      fee TEXT NOT NULL DEFAULT '0',
      total_afn TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Submitted',
      customer_note TEXT DEFAULT '',
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(currency) REFERENCES rates(code)
    );

    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      transaction_no TEXT NOT NULL UNIQUE,
      receipt_no TEXT NOT NULL UNIQUE,
      request_id INTEGER,
      user_id INTEGER,
      direction TEXT NOT NULL,
      currency TEXT NOT NULL,
      amount TEXT NOT NULL,
      rate TEXT NOT NULL,
      fee TEXT NOT NULL,
      total_afn TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'Completed',
      staff_id INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      note TEXT DEFAULT '',
      FOREIGN KEY(request_id) REFERENCES requests(id),
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(currency) REFERENCES rates(code),
      FOREIGN KEY(staff_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS conversations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      conversation_id INTEGER NOT NULL,
      sender_id INTEGER NOT NULL,
      body TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(conversation_id) REFERENCES conversations(id),
      FOREIGN KEY(sender_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS tickets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_no TEXT NOT NULL UNIQUE,
      user_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      subject TEXT NOT NULL,
      body TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'New',
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS ticket_replies (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ticket_id INTEGER NOT NULL,
      sender_id INTEGER NOT NULL,
      body TEXT NOT NULL,
      internal INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      FOREIGN KEY(ticket_id) REFERENCES tickets(id),
      FOREIGN KEY(sender_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS audit_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      action TEXT NOT NULL,
      detail TEXT NOT NULL,
      created_at TEXT NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    for code, nd, ne in CURRENCIES:
        db.execute(
            """
            INSERT OR IGNORE INTO rates
            (code, name_dari, name_en, source)
            VALUES (?, ?, ?, 'Not configured')
            """,
            (code, nd, ne)
        )

    db.commit()
    db.close()


def audit(action, detail):
    db = get_db()
    db.execute(
        """
        INSERT INTO audit_log(user_id, action, detail, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (session.get("user_id"), action, detail[:500], now())
    )
    db.commit()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None

    return get_db().execute(
        "SELECT id, name, email, role, created_at FROM users WHERE id=?",
        (uid,)
    ).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("لطفاً ابتدا وارد حساب خود شوید.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def roles_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()

            if not user:
                flash("لطفاً وارد شوید.", "warning")
                return redirect(url_for("login"))

            if user["role"] not in roles:
                abort(403)

            return view(*args, **kwargs)

        return wrapped

    return decorator


def csrf_token():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(24)
    return session["_csrf"]


@app.context_processor
def inject_globals():
    return {
        "business": BUSINESS,
        "current_user": current_user(),
        "csrf_token": csrf_token,
        "year": datetime.now().year
    }


@app.before_request
def protect_post():
    if request.method == "POST":
        token = session.get("_csrf", "")
        supplied = request.form.get("_csrf", "")

        if (
            not token
            or not supplied
            or not hmac.compare_digest(token, supplied)
        ):
            abort(
                400,
                "درخواست نامعتبر است. صفحه را تازه‌سازی کرده و دوباره تلاش کنید."
            )


@app.template_filter("money")
def money(value):
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return "—"


@app.route("/")
def index():
    rates = get_db().execute("""
        SELECT * FROM rates
        ORDER BY
        CASE code
            WHEN 'USD' THEN 0
            WHEN 'EUR' THEN 1
            WHEN 'GBP' THEN 2
            WHEN 'PKR' THEN 3
            ELSE 4
        END,
        code
    """).fetchall()

    return render_template("index.html", rates=rates)


@app.route("/rates")
def rates_page():
    rates = get_db().execute(
        "SELECT * FROM rates ORDER BY code"
    ).fetchall()

    return render_template("rates.html", rates=rates)


@app.route("/convert", methods=["GET", "POST"])
def convert():
    result = None

    if request.method == "POST":
        try:
            code = request.form.get("currency", "").upper()
            amount = float(request.form.get("amount", ""))
            direction = request.form.get("direction", "BUY")

            if not (amount > 0 and amount < 1_000_000_000):
                raise ValueError

            if direction not in ("BUY", "SELL"):
                raise ValueError

            rate = get_db().execute(
                "SELECT * FROM rates WHERE code=?",
                (code,)
            ).fetchone()

            if not rate or not rate["buy_rate"] or not rate["sell_rate"]:
                flash(
                    "نرخ این ارز هنوز توسط مدیر تنظیم نشده است.",
                    "warning"
                )
            else:
                selected = float(
                    rate["sell_rate"]
                    if direction == "BUY"
                    else rate["buy_rate"]
                )

                result = {
                    "currency": code,
                    "amount": amount,
                    "rate": selected,
                    "total": amount * selected,
                    "direction": direction
                }

        except (ValueError, TypeError):
            flash("مقدار و ارز را درست انتخاب کنید.", "danger")

    currencies = get_db().execute(
        "SELECT * FROM rates WHERE code != 'AFN' ORDER BY code"
    ).fetchall()

    return render_template(
        "convert.html",
        currencies=currencies,
        result=result
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if (
            len(name) < 2
            or len(name) > 100
            or "@" not in email
            or len(password) < 10
        ):
            flash(
                "نام و ایمیل معتبر وارد کنید. رمز عبور باید حداقل ۱۰ حرف باشد.",
                "danger"
            )
            return render_template("register.html")

        db = get_db()

        try:
            cur = db.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role, created_at)
                VALUES (?, ?, ?, 'customer', ?)
                """,
                (name, email, hash_password(password), now())
            )

            db.commit()

            session.clear()
            session["user_id"] = cur.lastrowid
            session["_csrf"] = secrets.token_urlsafe(24)

            audit(
                "customer_register",
                f"New customer id={cur.lastrowid}"
            )

            return redirect(url_for("dashboard"))

        except sqlite3.IntegrityError:
            flash("این ایمیل قبلاً ثبت شده است.", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_db().execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user and verify_password(password, user["password_hash"]):
            session.clear()
            session["user_id"] = user["id"]
            session["_csrf"] = secrets.token_urlsafe(24)

            audit(
                "login",
                f"Successful login for user id={user['id']}"
            )

            if user["role"] in ("admin", "staff", "support", "auditor"):
                return redirect(url_for("admin"))

            return redirect(url_for("dashboard"))

        flash("ایمیل یا رمز عبور نادرست است.", "danger")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    db = get_db()

    reqs = db.execute(
        """
        SELECT * FROM requests
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 30
        """,
        (user["id"],)
    ).fetchall()

    tickets = db.execute(
        """
        SELECT * FROM tickets
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 20
        """,
        (user["id"],)
    ).fetchall()

    conv = db.execute(
        """
        SELECT * FROM conversations
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    ).fetchone()

    messages = []

    if conv:
        messages = db.execute(
            """
            SELECT m.*, u.name AS sender_name
            FROM messages m
            JOIN users u ON u.id=m.sender_id
            WHERE conversation_id=?
            ORDER BY m.id ASC
            """,
            (conv["id"],)
        ).fetchall()

    return render_template(
        "dashboard.html",
        user=user,
        requests=reqs,
        tickets=tickets,
        messages=messages,
        conversation=conv
    )


@app.route("/request", methods=["GET", "POST"])
@login_required
def new_request():
    db = get_db()

    currencies = db.execute(
        "SELECT * FROM rates WHERE code != 'AFN' ORDER BY code"
    ).fetchall()

    if request.method == "POST":
        direction = request.form.get("direction", "BUY")
        code = request.form.get("currency", "").upper()
        note = request.form.get("note", "").strip()[:1000]

        try:
            amount = float(request.form.get("amount", ""))

            if (
                direction not in ("BUY", "SELL")
                or not (0 < amount < 1_000_000_000)
            ):
                raise ValueError

            rate_row = db.execute(
                "SELECT * FROM rates WHERE code=?",
                (code,)
            ).fetchone()

            if (
                not rate_row
                or not rate_row["buy_rate"]
                or not rate_row["sell_rate"]
            ):
                flash(
                    "برای این ارز هنوز نرخ معتبر تنظیم نشده است.",
                    "danger"
                )
                return render_template(
                    "request.html",
                    currencies=currencies
                )

            rate = float(
                rate_row["sell_rate"]
                if direction == "BUY"
                else rate_row["buy_rate"]
            )

            total = amount * rate
            request_no = "SR-" + secrets.token_hex(4).upper()
            stamp = now()

            db.execute(
                """
                INSERT INTO requests(
                    request_no, user_id, direction, currency,
                    amount, rate, fee, total_afn, status,
                    customer_note, created_at, updated_at
                )
                VALUES(
                    ?, ?, ?, ?, ?, ?, '0', ?,
                    'Submitted', ?, ?, ?
                )
                """,
                (
                    request_no,
                    current_user()["id"],
                    direction,
                    code,
                    f"{amount:.4f}",
                    f"{rate:.6f}",
                    f"{total:.2f}",
                    note,
                    stamp,
                    stamp
                )
            )

            db.commit()
            audit("request_created", request_no)

            flash(
                f"درخواست شما ثبت شد. شماره پیگیری: {request_no}. "
                "این درخواست هنوز معاملهٔ تکمیل‌شده نیست.",
                "success"
            )

            return redirect(url_for("dashboard"))

        except (ValueError, TypeError):
            flash("مبلغ واردشده معتبر نیست.", "danger")

    return render_template(
        "request.html",
        currencies=currencies
    )


@app.route("/message", methods=["POST"])
@login_required
def send_message():
    body = request.form.get("body", "").strip()

    if not body or len(body) > 3000:
        flash("پیام باید بین ۱ تا ۳۰۰۰ حرف باشد.", "danger")
        return redirect(url_for("dashboard"))

    db = get_db()
    user = current_user()

    conv = db.execute(
        """
        SELECT * FROM conversations
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    ).fetchone()

    if not conv:
        cur = db.execute(
            """
            INSERT INTO conversations(user_id, created_at)
            VALUES(?, ?)
            """,
            (user["id"], now())
        )
        conv_id = cur.lastrowid
    else:
        conv_id = conv["id"]

    db.execute(
        """
        INSERT INTO messages(
            conversation_id, sender_id, body, created_at
        )
        VALUES(?, ?, ?, ?)
        """,
        (conv_id, user["id"], body, now())
    )

    db.commit()
    audit("message_sent", f"conversation={conv_id}")

    flash("پیام شما ارسال شد.", "success")
    return redirect(url_for("dashboard"))


@app.route("/support", methods=["GET", "POST"])
@login_required
def support():
    if request.method == "POST":
        category = request.form.get("category", "General")[:60]
        subject = request.form.get("subject", "").strip()[:150]
        body = request.form.get("body", "").strip()[:3000]

        if len(subject) < 3 or len(body) < 5:
            flash("عنوان و شرح مشکل را کامل وارد کنید.", "danger")
        else:
            db = get_db()
            ticket_no = "SUP-" + secrets.token_hex(4).upper()
            stamp = now()

            db.execute(
                """
                INSERT INTO tickets(
                    ticket_no, user_id, category, subject,
                    body, status, created_at, updated_at
                )
                VALUES(?, ?, ?, ?, ?, 'New', ?, ?)
                """,
                (
                    ticket_no,
                    current_user()["id"],
                    category,
                    subject,
                    body,
                    stamp,
                    stamp
                )
            )

            db.commit()
            audit("support_ticket_created", ticket_no)

            flash(
                f"درخواست پشتیبانی ثبت شد. شماره پیگیری: {ticket_no}",
                "success"
            )

            return redirect(url_for("dashboard"))

    return render_template("support.html")


@app.route("/admin")
@roles_required("admin", "staff", "support", "auditor")
def admin():
    db = get_db()
    user = current_user()

    rates = db.execute(
        "SELECT * FROM rates ORDER BY code"
    ).fetchall()

    requests = db.execute(
        """
        SELECT r.*, u.name AS customer_name
        FROM requests r
        JOIN users u ON u.id=r.user_id
        ORDER BY r.id DESC
        LIMIT 100
        """
    ).fetchall()

    transactions = db.execute(
        """
        SELECT t.*, u.name AS customer_name
        FROM transactions t
        LEFT JOIN users u ON u.id=t.user_id
        ORDER BY t.id DESC
        LIMIT 100
        """
    ).fetchall()

    tickets = db.execute(
        """
        SELECT t.*, u.name AS customer_name
        FROM tickets t
        JOIN users u ON u.id=t.user_id
        ORDER BY t.id DESC
        LIMIT 100
        """
    ).fetchall()

    messages = db.execute(
        """
        SELECT m.*, u.name AS sender_name, c.user_id
        FROM messages m
        JOIN users u ON u.id=m.sender_id
        JOIN conversations c ON c.id=m.conversation_id
        ORDER BY m.id DESC
        LIMIT 100
        """
    ).fetchall()

    stats = {
        "requests": db.execute(
            """
            SELECT COUNT(*) FROM requests
            WHERE status NOT IN ('Completed','Rejected','Cancelled')
            """
        ).fetchone()[0],

        "transactions": db.execute(
            """
            SELECT COUNT(*) FROM transactions
            WHERE status='Completed'
            """
        ).fetchone()[0],

        "tickets": db.execute(
            """
            SELECT COUNT(*) FROM tickets
            WHERE status NOT IN ('Resolved','Closed')
            """
        ).fetchone()[0],

        "customers": db.execute(
            """
            SELECT COUNT(*) FROM users
            WHERE role='customer'
            """
        ).fetchone()[0],
    }

    return render_template(
        "admin.html",
        rates=rates,
        requests=requests,
        transactions=transactions,
        tickets=tickets,
        messages=messages,
        stats=stats,
        role=user["role"]
    )


@app.route("/admin/setup", methods=["GET", "POST"])
def admin_setup():
    db = get_db()

    admin_exists = db.execute(
        "SELECT 1 FROM users WHERE role='admin' LIMIT 1"
    ).fetchone()

    if admin_exists:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        setup_key = request.form.get("setup_key", "")

        expected = os.environ.get("SHARIFI_SETUP_KEY", "")

        if not expected or not hmac.compare_digest(setup_key, expected):
            flash(
                "کلید راه‌اندازی مدیر درست نیست. "
                "ابتدا SHARIFI_SETUP_KEY را در محیط تنظیم کنید.",
                "danger"
            )

        elif (
            len(name) < 2
            or "@" not in email
            or len(password) < 14
        ):
            flash(
                "نام و ایمیل معتبر وارد کنید؛ "
                "رمز عبور مدیر باید حداقل ۱۴ حرف باشد.",
                "danger"
            )
          
        else:
            try:
                cur = db.execute(
                    """
                    INSERT INTO users(
                        name, email, password_hash, role, created_at
                    )
                    VALUES(?, ?, ?, 'admin', ?)
                    """,
                    (
                        name,
                        email,
                        hash_password(password),
                        now()
                    )
                )

                db.commit()

                session.clear()
                session["user_id"] = cur.lastrowid
                session["_csrf"] = secrets.token_urlsafe(24)

                audit(
                    "admin_bootstrap",
                    f"Initial administrator id={cur.lastrowid}"
                )

                return redirect(url_for("admin"))

            except sqlite3.IntegrityError:
                flash("این ایمیل قبلاً ثبت شده است.", "danger")

    return render_template("admin_setup.html")


@app.route("/admin/rates", methods=["POST"])
@roles_required("admin", "staff")
def update_rate():
    code = request.form.get("code", "").upper()
    source = request.form.get(
        "source",
        "Administrator entered"
    )[:120]

    try:
        buy = float(request.form.get("buy_rate", ""))
        sell = float(request.form.get("sell_rate", ""))

        if not (
            0 < buy < 1_000_000_000
            and 0 < sell < 1_000_000_000
        ):
            raise ValueError

    except (ValueError, TypeError):
        flash(
            "نرخ خرید و فروش باید اعداد مثبت و معتبر باشند.",
            "danger"
        )
        return redirect(url_for("admin"))

    db = get_db()

    row = db.execute(
        "SELECT * FROM rates WHERE code=?",
        (code,)
    ).fetchone()

    if not row or code == "AFN":
        flash("ارز انتخاب‌شده معتبر نیست.", "danger")
        return redirect(url_for("admin"))

    stamp = now()

    db.execute(
        """
        UPDATE rates
        SET buy_rate=?, sell_rate=?, updated_at=?,
            updated_by=?, source=?
        WHERE code=?
        """,
        (
            f"{buy:.6f}",
            f"{sell:.6f}",
            stamp,
            current_user()["id"],
            source,
            code
        )
    )

    db.execute(
        """
        INSERT INTO rate_history(
            code, buy_rate, sell_rate, source,
            changed_at, changed_by
        )
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            code,
            f"{buy:.6f}",
            f"{sell:.6f}",
            source,
            stamp,
            current_user()["id"]
        )
    )

    db.commit()

    audit(
        "rate_updated",
        f"{code}: buy={buy}; sell={sell}; source={source}"
    )

    flash(f"نرخ {code} ذخیره شد.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/request/<int:request_id>", methods=["POST"])
@roles_required("admin", "staff")
def update_request(request_id):
    status = request.form.get("status", "")

    allowed = {
        "Under Review",
        "Awaiting Customer Confirmation",
        "Approved",
        "Rejected",
        "Cancelled"
    }

    if status not in allowed:
        abort(400)

    db = get_db()

    req = db.execute(
        "SELECT * FROM requests WHERE id=?",
        (request_id,)
    ).fetchone()

    if not req:
        abort(404)

    db.execute(
        """
        UPDATE requests
        SET status=?, updated_at=?
        WHERE id=?
        """,
        (status, now(), request_id)
    )

    db.commit()

    audit(
        "request_status_changed",
        f"{req['request_no']} -> {status}"
    )

    flash("وضعیت درخواست به‌روزرسانی شد.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/complete/<int:request_id>", methods=["POST"])
@roles_required("admin", "staff")
def complete_request(request_id):
    db = get_db()

    req = db.execute(
        "SELECT * FROM requests WHERE id=?",
        (request_id,)
    ).fetchone()

    if not req:
        abort(404)

    if req["status"] in ("Completed", "Rejected", "Cancelled"):
        flash(
            "این درخواست قبلاً بسته شده یا قابل تکمیل نیست.",
            "danger"
        )
        return redirect(url_for("admin"))

    stamp = now()
    txn = "TX-" + secrets.token_hex(5).upper()
    receipt = "RC-" + secrets.token_hex(5).upper()

    db.execute(
        """
        INSERT INTO transactions(
            transaction_no, receipt_no, request_id, user_id,
            direction, currency, amount, rate, fee,
            total_afn, status, staff_id, created_at, note
        )
        VALUES(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            'Completed', ?, ?, ?
        )
        """,
        (
            txn,
            receipt,
            req["id"],
            req["user_id"],
            req["direction"],
            req["currency"],
            req["amount"],
            req["rate"],
            req["fee"],
            req["total_afn"],
            current_user()["id"],
            stamp,
            "ثبت‌شده توسط کارمند مجاز"
        )
    )

    db.execute(
        """
        UPDATE requests
        SET status='Completed', updated_at=?
        WHERE id=?
        """,
        (stamp, request_id)
    )

    db.commit()

    audit(
        "transaction_completed",
        f"{txn}; receipt={receipt}"
    )

    flash(
        f"معامله ثبت شد. شماره رسید: {receipt}",
        "success"
    )

    return redirect(
        url_for("receipt", transaction_no=txn)
    )


@app.route("/receipt/<transaction_no>")
@login_required
def receipt(transaction_no):
    db = get_db()

    txn = db.execute(
        """
        SELECT
            t.*,
            u.name AS customer_name,
            u.email AS customer_email,
            s.name AS staff_name
        FROM transactions t
        LEFT JOIN users u ON u.id=t.user_id
        JOIN users s ON s.id=t.staff_id
        WHERE t.transaction_no=?
        """,
        (transaction_no,)
    ).fetchone()

    if not txn:
        abort(404)

    user = current_user()

    if (
        user["role"] not in ("admin", "staff", "auditor")
        and txn["user_id"] != user["id"]
    ):
        abort(403)

    return render_template("receipt.html", txn=txn)


@app.route("/admin/ticket/<int:ticket_id>", methods=["POST"])
@roles_required("admin", "support")
def update_ticket(ticket_id):
    status = request.form.get("status", "In Progress")

    if status not in (
        "New",
        "Open",
        "In Progress",
        "Waiting for Customer",
        "Resolved",
        "Closed"
    ):
        abort(400)

    db = get_db()

    ticket = db.execute(
        "SELECT * FROM tickets WHERE id=?",
        (ticket_id,)
    ).fetchone()

    if not ticket:
        abort(404)

    db.execute(
        """
        UPDATE tickets
        SET status=?, updated_at=?
        WHERE id=?
        """,
        (status, now(), ticket_id)
    )

    body = request.form.get("reply", "").strip()[:3000]

    if body:
        db.execute(
            """
            INSERT INTO ticket_replies(
                ticket_id, sender_id, body, internal, created_at
            )
            VALUES(?, ?, ?, 0, ?)
            """,
            (
                ticket_id,
                current_user()["id"],
                body,
                now()
            )
        )

    db.commit()

    audit(
        "ticket_updated",
        f"{ticket['ticket_no']} -> {status}"
    )

    flash("درخواست پشتیبانی به‌روزرسانی شد.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/message/<int:conversation_id>", methods=["POST"])
@roles_required("admin", "staff", "support")
def reply_message(conversation_id):
    body = request.form.get("body", "").strip()

    if not body or len(body) > 3000:
        flash("متن پیام معتبر نیست.", "danger")
        return redirect(url_for("admin"))

    db = get_db()

    conv = db.execute(
        "SELECT * FROM conversations WHERE id=?",
        (conversation_id,)
    ).fetchone()

    if not conv:
        abort(404)

    db.execute(
        """
        INSERT INTO messages(
            conversation_id, sender_id, body, created_at
        )
        VALUES(?, ?, ?, ?)
        """,
        (
            conversation_id,
            current_user()["id"],
            body,
            now()
        )
    )

    db.commit()

    audit(
        "staff_message_reply",
        f"conversation={conversation_id}"
    )

    flash("پاسخ پیام ارسال شد.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/export.csv")
@roles_required("admin", "auditor")
def export_csv():
    rows = get_db().execute(
        """
        SELECT
            transaction_no, receipt_no, direction, currency,
            amount, rate, fee, total_afn, status, created_at
        FROM transactions
        ORDER BY id DESC
        """
    ).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "transaction_no",
        "receipt_no",
        "direction",
        "currency",
        "amount",
        "rate",
        "fee",
        "total_afn",
        "status",
        "created_at"
    ])

    for row in rows:
        writer.writerow(list(row))

    response = make_response("\ufeff" + output.getvalue())

    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        "attachment; filename=sharifi-transactions.csv"
    )

    return response


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(403)
def forbidden(_error):
    return render_template(
        "error.html",
        code=403,
        message="شما اجازهٔ دسترسی به این بخش را ندارید."
    ), 403


@app.errorhandler(404)
def not_found(_error):
    return render_template(
        "error.html",
        code=404,
        message="صفحه یا مورد درخواستی پیدا نشد."
    ), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template(
        "error.html",
        code=400,
        message=getattr(
            error,
            "description",
            "درخواست نامعتبر است."
        )
    ), 400



# SARAI SHAHZADA LIVE EXCHANGE RATES

import requests
import re
import time
from datetime import datetime, timezone
from bs4 import BeautifulSoup

SARAFI_URL = "https://sarafi.af/fa/exchange-rates/sarai-shahzada"

rates_cache = {
    "data": [],
    "updated_at": None,
    "last_fetch": 0
}


def get_sarai_shahzada_rates():
    now = time.time()

    if rates_cache["data"] and now - rates_cache["last_fetch"] < 60:
        return rates_cache["data"]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        SARAFI_URL,
        headers=headers,
        timeout=15
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    found_rates = []

    allowed_codes = {
        "USD", "EUR", "GBP", "IRR", "PKR",
        "SAR", "AED", "CHF", "AUD", "CAD",
        "RUB", "DKK", "SEK", "NOK", "TRY",
        "CNY", "KWD", "QAR", "BHD", "JPY"
    }

    for row in soup.select("table tr"):
        cells = row.find_all(["td", "th"], recursive=False)

        if len(cells) < 3:
            continue

        values = [
            cell.get_text(" ", strip=True)
            for cell in cells
        ]

        row_text = " ".join(values)
        match = re.search(r"\b([A-Z]{3})\b", row_text)

        if not match:
            continue

        code = match.group(1)

        if code not in allowed_codes:
            continue

        numbers = []

        for value in values:
            cleaned = value.replace(",", "").strip()

            if re.fullmatch(r"\d+(?:\.\d+)?", cleaned):
                numbers.append(float(cleaned))

        if len(numbers) < 2:
            continue

        found_rates.append({
            "code": code,
            "name": values[0],
            "buy": numbers[0],
            "sell": numbers[1],
            "unit": 1000 if code in ["IRR", "PKR", "JPY"] else 1
        })

    if not found_rates:
        if rates_cache["data"]:
            return rates_cache["data"]

        raise ValueError("No rates found")

    unique_rates = {
        rate["code"]: rate
        for rate in found_rates
    }

    rates_cache["data"] = list(unique_rates.values())
    rates_cache["last_fetch"] = now
    rates_cache["updated_at"] = datetime.now(timezone.utc).isoformat()

    return rates_cache["data"]


@app.route("/api/live-rates")
def live_rates_api():
    try:
        data = get_sarai_shahzada_rates()

        return jsonify({
            "success": True,
            "source": SARAFI_URL,
            "updated_at": rates_cache["updated_at"],
            "rates": data
        })

    except Exception as error:
        if rates_cache["data"]:
            return jsonify({
                "success": True,
                "cached": True,
                "updated_at": rates_cache["updated_at"],
                "rates": rates_cache["data"]
            })

        return jsonify({
            "success": False,
            "message": str(error)
        }), 503
init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=False
        
    )
