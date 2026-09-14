from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

from matching import calculate_match


app = Flask(__name__)

app.secret_key = "senior_junior_connect_secret"


# ==================================================
# DATABASE
# ==================================================

def create_database():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # ------------------------------------------
    # SENIORS
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seniors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            year TEXT,
            status TEXT,
            current_work TEXT,
            location TEXT,
            skills TEXT,
            projects TEXT,
            hackathon TEXT,
            internship TEXT,
            guidance TEXT,
            mode TEXT,
            username TEXT,
            password TEXT,
            availability TEXT DEFAULT 'Available'
        )
    """)

    # Existing databases need these columns
    try:
        cursor.execute(
            "ALTER TABLE seniors ADD COLUMN username TEXT"
        )
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
            "ALTER TABLE seniors ADD COLUMN password TEXT"
        )
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
            "ALTER TABLE seniors ADD COLUMN availability TEXT DEFAULT 'Available'"
        )
    except sqlite3.OperationalError:
        pass

    # Unique username
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_senior_username
        ON seniors(username)
        WHERE username IS NOT NULL
    """)


    # ------------------------------------------
    # JUNIORS
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS juniors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            year TEXT,
            location TEXT,
            skills TEXT,
            requirement TEXT,
            mode TEXT,
            username TEXT,
            password TEXT
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE juniors ADD COLUMN username TEXT"
        )
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute(
            "ALTER TABLE juniors ADD COLUMN password TEXT"
        )
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_junior_username
        ON juniors(username)
        WHERE username IS NOT NULL
    """)


    # ------------------------------------------
    # REQUESTS
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            junior_id INTEGER,
            senior_id INTEGER,
            status TEXT DEFAULT 'Pending'
        )
    """)


    # ------------------------------------------
    # MESSAGES
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            sender TEXT,
            message TEXT
        )
    """)


    # ------------------------------------------
    # FEEDBACK
    # ------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            junior_id INTEGER,
            senior_id INTEGER,
            rating INTEGER,
            comment TEXT
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# LOGIN
# ==================================================

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login-check", methods=["POST"])
def login_check():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if role == "Senior":

        cursor.execute("""
            SELECT *
            FROM seniors
            WHERE username = ?
            AND password = ?
        """, (username, password))

    else:

        cursor.execute("""
            SELECT *
            FROM juniors
            WHERE username = ?
            AND password = ?
        """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:

        session["role"] = role
        session["user_id"] = user[0]
        session["username"] = username
        session["name"] = user[1]

        if role == "Senior":
            return redirect(url_for("senior_dashboard"))

        return redirect(url_for("junior_home"))

    return "Invalid username or password!"


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return redirect(url_for("login"))


# ==================================================
# SENIOR REGISTER PAGE
# ==================================================

@app.route("/senior-register")
def senior_register_page():

    return render_template(
        "senior_register.html"
    )


# ==================================================
# SENIOR REGISTER
# ==================================================

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    department = request.form["department"]
    year = request.form["year"]
    status = request.form["status"]
    current_work = request.form["current_work"]
    location = request.form["location"]
    skills = request.form["skills"]
    projects = request.form["projects"]
    hackathon = request.form["hackathon"]
    internship = request.form["internship"]

    guidance = request.form.getlist("guidance")

    mode = request.form["mode"]

    username = request.form["username"]
    password = request.form["password"]

    # New feature
    availability = request.form.get(
        "availability",
        "Available"
    )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO seniors
            (
                name,
                department,
                year,
                status,
                current_work,
                location,
                skills,
                projects,
                hackathon,
                internship,
                guidance,
                mode,
                username,
                password,
                availability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            department,
            year,
            status,
            current_work,
            location,
            skills,
            projects,
            hackathon,
            internship,
            ", ".join(guidance),
            mode,
            username,
            password,
            availability
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    except sqlite3.IntegrityError:

        conn.close()

        return "Username already exists. Please choose another username."


# ==================================================
# JUNIOR REGISTER PAGE
# ==================================================

@app.route("/junior")
def junior():

    return render_template(
        "junior_register.html"
    )


# ==================================================
# JUNIOR REGISTER
# ==================================================

@app.route("/junior-register", methods=["POST"])
def junior_register():

    name = request.form["name"]
    department = request.form["department"]
    year = request.form["year"]
    location = request.form["location"]
    skills = request.form["skills"]
    requirement = request.form["requirement"]
    mode = request.form["mode"]

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO juniors
            (
                name,
                department,
                year,
                location,
                skills,
                requirement,
                mode,
                username,
                password
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            department,
            year,
            location,
            skills,
            requirement,
            mode,
            username,
            password
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    except sqlite3.IntegrityError:

        conn.close()

        return "Username already exists. Please choose another username."


# ==================================================
# JUNIOR HOME
# ==================================================

@app.route("/junior-home")
def junior_home():

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    return render_template(
        "junior.html",
        name=session.get("name")
    )


# ==================================================
# SENIOR PROFILE
# ==================================================

@app.route("/profile/<int:senior_id>")
def profile(senior_id):

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM seniors WHERE id = ?",
        (senior_id,)
    )

    senior = cursor.fetchone()

    conn.close()

    if senior is None:
        return "Senior not found!"

    return render_template(
        "profile.html",
        senior=senior
    )


# ==================================================
# AI MATCHES
# ==================================================

@app.route("/matches", methods=["GET", "POST"])
def matches():

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    junior_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM juniors WHERE id = ?",
        (junior_id,)
    )

    junior = cursor.fetchone()

    if junior is None:

        conn.close()

        return "Junior not found!"

    junior_skills = junior[5]
    junior_requirement = junior[6]

    # Allow current requirement from Junior Home
    if request.method == "POST":

        new_requirement = request.form.get(
            "requirement",
            ""
        ).strip()

        if new_requirement:
            junior_requirement = new_requirement

    cursor.execute(
        "SELECT * FROM seniors"
    )

    seniors = cursor.fetchall()

    results = []

    for senior in seniors:

        senior_id = senior[0]

        senior_skills = senior[7]
        senior_projects = senior[8]
        senior_hackathon = senior[9]
        senior_guidance = senior[11]

        # ----------------------------------
        # Average feedback rating
        # ----------------------------------

        cursor.execute("""
            SELECT AVG(rating)
            FROM feedback
            WHERE senior_id = ?
        """, (senior_id,))

        rating_result = cursor.fetchone()

        average_rating = (
            rating_result[0]
            if rating_result[0] is not None
            else 0
        )

        # ----------------------------------
        # AI matching
        # ----------------------------------

        score, matched, breakdown = calculate_match(
            junior_skills,
            junior_requirement,
            senior_skills,
            senior_projects,
            senior_hackathon,
            senior_guidance,
            average_rating
        )

        # ----------------------------------
        # Availability boost
        # ----------------------------------

        availability = (
            senior[15]
            if len(senior) > 15
            else "Available"
        )

        if availability == "Available":
            score = min(100, score + 5)

        results.append(
            (
                score,
                matched,
                breakdown,
                senior,
                average_rating,
                availability
            )
        )

    # Highest score first
    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    conn.close()

    return render_template(
        "matches.html",
        results=results,
        junior=junior
    )


# ==================================================
# SEND REQUEST
# ==================================================

@app.route("/send-request/<int:senior_id>")
def send_request(senior_id):

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    junior_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM seniors WHERE id = ?",
        (senior_id,)
    )

    senior = cursor.fetchone()

    if senior is None:

        conn.close()

        return "Senior not found!"

    cursor.execute("""
        SELECT id
        FROM requests
        WHERE junior_id = ?
        AND senior_id = ?
    """, (
        junior_id,
        senior_id
    ))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return "Request already sent to this senior!"

    cursor.execute("""
        INSERT INTO requests
        (
            junior_id,
            senior_id,
            status
        )
        VALUES (?, ?, 'Pending')
    """, (
        junior_id,
        senior_id
    ))

    conn.commit()
    conn.close()

    return f"Guidance request sent to {senior[1]}!"


# ==================================================
# SENIOR DASHBOARD
# ==================================================

@app.route("/senior-dashboard")
def senior_dashboard():

    if session.get("role") != "Senior":
        return redirect(url_for("login"))

    senior_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            requests.id,
            juniors.name,
            juniors.department,
            juniors.year,
            juniors.requirement,
            requests.status
        FROM requests
        JOIN juniors
        ON requests.junior_id = juniors.id
        WHERE requests.senior_id = ?
        ORDER BY requests.id DESC
    """, (senior_id,))

    requests_data = cursor.fetchall()

    cursor.execute("""
        SELECT availability
        FROM seniors
        WHERE id = ?
    """, (senior_id,))

    availability_result = cursor.fetchone()

    availability = (
        availability_result[0]
        if availability_result
        else "Available"
    )

    conn.close()

    return render_template(
        "senior_dashboard.html",
        requests=requests_data,
        name=session.get("name"),
        availability=availability
    )


# ==================================================
# ACCEPT REQUEST
# ==================================================

@app.route("/accept-request/<int:request_id>")
def accept_request(request_id):

    if session.get("role") != "Senior":
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requests
        SET status = 'Accepted'
        WHERE id = ?
        AND senior_id = ?
    """, (
        request_id,
        session.get("user_id")
    ))

    conn.commit()
    conn.close()

    return redirect(
        url_for("senior_dashboard")
    )


# ==================================================
# DECLINE REQUEST
# ==================================================

@app.route("/decline-request/<int:request_id>")
def decline_request(request_id):

    if session.get("role") != "Senior":
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requests
        SET status = 'Declined'
        WHERE id = ?
        AND senior_id = ?
    """, (
        request_id,
        session.get("user_id")
    ))

    conn.commit()
    conn.close()

    return redirect(
        url_for("senior_dashboard")
    )


# ==================================================
# MY REQUESTS
# ==================================================

@app.route("/my-requests")
def my_requests():

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    junior_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            requests.id,
            seniors.name,
            seniors.department,
            seniors.year,
            juniors.requirement,
            requests.status
        FROM requests

        JOIN seniors
        ON requests.senior_id = seniors.id

        JOIN juniors
        ON requests.junior_id = juniors.id

        WHERE requests.junior_id = ?

        ORDER BY requests.id DESC
    """, (junior_id,))

    requests_data = cursor.fetchall()

    conn.close()

    return render_template(
        "my_requests.html",
        requests=requests_data
    )


# ==================================================
# DISCUSSION
# ==================================================

@app.route("/discussion/<int:request_id>")
def discussion(request_id):

    if session.get("role") not in [
        "Junior",
        "Senior"
    ]:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            requests.id,
            juniors.name,
            seniors.name,
            requests.status,
            requests.junior_id,
            requests.senior_id
        FROM requests

        JOIN juniors
        ON requests.junior_id = juniors.id

        JOIN seniors
        ON requests.senior_id = seniors.id

        WHERE requests.id = ?
    """, (request_id,))

    request_data = cursor.fetchone()

    if request_data is None:

        conn.close()

        return "Request not found!"

    # Security check
    if session["role"] == "Junior":

        if session["user_id"] != request_data[4]:

            conn.close()

            return "Access denied!"

    else:

        if session["user_id"] != request_data[5]:

            conn.close()

            return "Access denied!"

    if request_data[3] != "Accepted":

        conn.close()

        return "Discussion is available only after the request is accepted."

    cursor.execute("""
        SELECT sender, message
        FROM messages
        WHERE request_id = ?
        ORDER BY id
    """, (request_id,))

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "discussion.html",
        request_data=request_data,
        messages=messages,
        request_id=request_id,
        role=session.get("role")
    )


# ==================================================
# SEND MESSAGE
# ==================================================

@app.route(
    "/send-message/<int:request_id>",
    methods=["POST"]
)
def send_message(request_id):

    if session.get("role") not in [
        "Junior",
        "Senior"
    ]:
        return redirect(url_for("login"))

    message = request.form["message"]

    if message.strip() == "":
        return redirect(
            url_for(
                "discussion",
                request_id=request_id
            )
        )

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            junior_id,
            senior_id,
            status
        FROM requests
        WHERE id = ?
    """, (request_id,))

    req = cursor.fetchone()

    if req is None:

        conn.close()

        return "Request not found!"

    if session["role"] == "Junior":

        if session["user_id"] != req[0]:

            conn.close()

            return "Access denied!"

        sender = "Junior"

    else:

        if session["user_id"] != req[1]:

            conn.close()

            return "Access denied!"

        sender = "Senior"

    if req[2] != "Accepted":

        conn.close()

        return "Discussion is not active."

    cursor.execute("""
        INSERT INTO messages
        (
            request_id,
            sender,
            message
        )
        VALUES (?, ?, ?)
    """, (
        request_id,
        sender,
        message
    ))

    conn.commit()
    conn.close()

    return redirect(
        url_for(
            "discussion",
            request_id=request_id
        )
    )


# ==================================================
# FEEDBACK PAGE
# ==================================================

@app.route("/feedback/<int:request_id>")
def feedback(request_id):

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            requests.id,
            seniors.name,
            requests.senior_id,
            requests.status
        FROM requests

        JOIN seniors
        ON requests.senior_id = seniors.id

        WHERE requests.id = ?
        AND requests.junior_id = ?
    """, (
        request_id,
        session.get("user_id")
    ))

    data = cursor.fetchone()

    conn.close()

    if data is None:
        return "Request not found!"

    if data[3] != "Accepted":
        return "Feedback is available after acceptance."

    return render_template(
        "feedback.html",
        request_data=data
    )


# ==================================================
# SUBMIT FEEDBACK
# ==================================================

@app.route(
    "/submit-feedback/<int:request_id>",
    methods=["POST"]
)
def submit_feedback(request_id):

    if session.get("role") != "Junior":
        return redirect(url_for("login"))

    rating = int(
        request.form["rating"]
    )

    comment = request.form.get(
        "comment",
        ""
    ).strip()

    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5."

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            junior_id,
            senior_id,
            status
        FROM requests
        WHERE id = ?
    """, (request_id,))

    req = cursor.fetchone()

    if req is None:

        conn.close()

        return "Request not found!"

    if req[0] != session.get("user_id"):

        conn.close()

        return "Access denied!"

    if req[2] != "Accepted":

        conn.close()

        return "Feedback is available only for accepted requests."

    # Prevent duplicate feedback
    cursor.execute("""
        SELECT id
        FROM feedback
        WHERE request_id = ?
    """, (request_id,))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return "Feedback already submitted for this request."

    cursor.execute("""
        INSERT INTO feedback
        (
            request_id,
            junior_id,
            senior_id,
            rating,
            comment
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        request_id,
        req[0],
        req[1],
        rating,
        comment
    ))

    conn.commit()
    conn.close()

    return """
        <h2>⭐ Thank you for your feedback!</h2>
        <a href="/my-requests">
            Back to My Requests
        </a>
    """


# ==================================================
# MANAGE SENIOR PROFILE
# ==================================================

@app.route(
    "/manage-profile",
    methods=["GET", "POST"]
)
def manage_profile():

    if session.get("role") != "Senior":
        return redirect(url_for("login"))

    username = session.get("username")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM seniors
        WHERE username = ?
    """, (username,))

    senior = cursor.fetchone()

    if not senior:

        conn.close()

        return "Senior profile not found!"

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        year = request.form["year"]
        status = request.form["status"]
        current_work = request.form["current_work"]
        location = request.form["location"]
        skills = request.form["skills"]
        projects = request.form["projects"]
        hackathon = request.form["hackathon"]
        internship = request.form["internship"]
        guidance = request.form["guidance"]
        mode = request.form["mode"]
        availability = request.form["availability"]

        cursor.execute("""
            UPDATE seniors

            SET
                name = ?,
                department = ?,
                year = ?,
                status = ?,
                current_work = ?,
                location = ?,
                skills = ?,
                projects = ?,
                hackathon = ?,
                internship = ?,
                guidance = ?,
                mode = ?,
                availability = ?

            WHERE username = ?
        """, (
            name,
            department,
            year,
            status,
            current_work,
            location,
            skills,
            projects,
            hackathon,
            internship,
            guidance,
            mode,
            availability,
            username
        ))

        conn.commit()

        cursor.execute("""
            SELECT *
            FROM seniors
            WHERE username = ?
        """, (username,))

        senior = cursor.fetchone()

        session["name"] = name

        conn.close()

        return render_template(
            "manage_profile.html",
            senior=senior,
            success="Profile updated successfully!"
        )

    conn.close()

    return render_template(
        "manage_profile.html",
        senior=senior
    )


# ==================================================
# RUN
# ==================================================
create_database()
if __name__ == "__main__":

    app.run(debug=True)

