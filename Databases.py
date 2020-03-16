import sqlite3


with sqlite3.connect("learners.db") as connection:
    for every in ("learners", "courses", "attendance"):
        connection.execute("DROP TABLE IF EXISTS %s" % every)
    connection.execute("""CREATE TABLE IF NOT EXISTS learners(learner_id INTEGER PRIMARY KEY,
                                                              first_name TEXT,
                                                              last_name TEXT,
                                                              sex INTEGER,
                                                              UNIQUE (first_name, last_name, sex))""")
    connection.execute('''CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY,
        course TEXT UNIQUE
        )''')
    connection.execute('''CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY,
        course_id INTEGER,
        learner_id INTEGER UNIQUE,
        FOREIGN KEY (course_id) REFERENCES courses (cource_id),
        FOREIGN KEY (learner_id) REFERENCES learners (learner_id)
        )''')
    query = "INSERT INTO learners (first_name, last_name, sex) VALUES ('Dima', 'Biba', 0)"
    connection.execute(query)
    query = "INSERT INTO learners (first_name, last_name, sex) VALUES (?, ?, ?)"
    connection.execute(query, ["Shamil", "Urazbakchtin", 0])
    other_learners = [("Lolita", "Alekseeva", 1),
                      ("Katya", "Yakovleva", 1),
                      ("Olya", "Mazur", 1)]
    connection.executemany(query, other_learners)
    query = """INSERT INTO courses (course) VALUES (?)"""
    connection.executemany(query, [("python",), ("machine learning",)])
    connection.execute("INSERT INTO attendance (course_id, learner_id) VALUES (1, 1)")
    query = """SELECT * FROM attendance JOIN learners USING (learner_id)"""
    res = connection.execute(query)
    print(res.fetchall())
    connection.commit()