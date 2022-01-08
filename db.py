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

def setup():
    commands = (
        """ CREATE TABLE IF NOT EXISTS company (
                company_id integer PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id integer PRIMARY KEY,
            company_id integer,
            job_title VARCHAR(255),
            application_url VARCHAR(1024),
            salary integer,
            CONSTRAINT fk_company
                FOREIGN KEY(company_id) 
	            REFERENCES company(customer_id)
        )
        """,
        """ CREATE TABLE IF NOT EXISTS job_application (
                app_id integer PRIMARY KEY,
                company_id VARCHAR(255) NOT NULL,
                job_id integer,
                    CONSTRAINT fk_company
                    FOREIGN KEY(company_id) 
	                REFERENCES company(customer_id),
                    CONSTRAINT fk_job
                    FOREIGN KEY(job_id) 
	                REFERENCES jobs(job_id)
                )
        """)

def insert_job_data(id,author_id)
