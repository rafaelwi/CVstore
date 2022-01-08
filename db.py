import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="jobs",
    user="postgres",
    password="password",
    port="42069")
cur = conn.cursor()
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

def insert_job_data(id,author_id)
