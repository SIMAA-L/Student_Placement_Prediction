import sqlite3
import pandas as pd

DB_PATH = "data/placement.db"


def save_prediction(
    gender,
    ssc,
    hsc,
    degree,
    mba,
    prediction,
    probability
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (gender, ssc, hsc, degree, mba, prediction, probability)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        gender,
        ssc,
        hsc,
        degree,
        mba,
        prediction,
        probability
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        conn
    )

    conn.close()

    return df