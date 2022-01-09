import psycopg2
from config import config

def setup_db():
    print ("Setting up the database...")
    commands = (
        """CREATE SEQUENCE IF NOT EXISTS company_id_seq;""",
        """CREATE SEQUENCE IF NOT EXISTS job_id_seq;""",
        """CREATE SEQUENCE IF NOT EXISTS job_application_id_seq;""",
        """ CREATE TABLE IF NOT EXISTS company (
                company_id integer PRIMARY KEY DEFAULT nextval('company_id_seq'),
                company_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS job (
            job_id integer PRIMARY KEY DEFAULT nextval('job_id_seq'),
            company_id integer,
            job_title VARCHAR(255),
            application_url VARCHAR(1024),
            salary integer,
            active integer,
            status_id integer,
            CONSTRAINT fk_company
                FOREIGN KEY(company_id) 
	            REFERENCES company(company_id)
        )
        """,
        
        """ CREATE TABLE IF NOT EXISTS status (
                status_id integer PRIMARY KEY,
                status_text varchar(64)
                )
        """,
        """INSERT INTO status (status_id,status_text) VALUES (1, 'None')""",
        """INSERT INTO status (status_id,status_text) VALUES (2, 'Applied')""",
        """INSERT INTO status (status_id,status_text) VALUES (3, 'Applied stale')""",
        """INSERT INTO status (status_id,status_text) VALUES (4, 'Interview upcoming')""",
        """INSERT INTO status (status_id,status_text) VALUES (5, 'Interview process in progress')""",
        """INSERT INTO status (status_id,status_text) VALUES (6, 'OA')""",
        """INSERT INTO status (status_id,status_text) VALUES (7, 'Rejected')""")
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
       
    finally:
        if conn is not None:
            conn.close()

def insert_job(job_title,application_url,salary,company_id):
    conn = None
    sql = """INSERT INTO job (job_title,application_url,salary,company_id,active,status_id) VALUES (%s,%s,%s,%s,1,1);"""
    try:
        
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql, (job_title,application_url,salary,company_id))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        
        print ("fff")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
       
    finally:
        if conn is not None:
            conn.close()
def edit_job( job_title,application_url,salary,company_id,job_id):
    conn = None
    sql = """UPDATE job SET job_title = %s, application_url = %s, salary = %s, company_id = %s where job_id = %s;"""
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql, (job_title,application_url,salary,company_id,job_id))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
       
    finally:
        if conn is not None:
            conn.close()
def remove_job (job_id):
    conn = None
    sql = """UPDATE job SET active = 0 where job_id = %s;"""
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql, (job_id,))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def insert_company(company_name):
    conn = None
    sql = """INSERT INTO company (company_name) SELECT %s WHERE NOT EXISTS ( SELECT company_name FROM company WHERE company_name = %s);"""
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql, (company_name,company_name))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
       
    finally:
        if conn is not None:
            conn.close()
def remove_company(company_id):
    conn = None
    sql = """DELETE FROM company WHERE company_id = %s;"""
    sql2 = """DELETE FROM job where company_id = %s;"""
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql2, (company_id,))
        cur.execute(sql, (company_id,))
        
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
       
    finally:
        if conn is not None:
            conn.close()


def get_job_apps():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT status_text,b.status_id,job_title,company_name,status_text,salary FROM job as \"b\" cross join company as \"c\" cross join status as \"d\" where b.company_id = c.company_id and b.status_id = d.status_id and active = 1; ")
        rows = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def get_companies():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("select * from company;")
        rows = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows



def update_job_status(job_id,status_id):
    sql = """UPDATE job SET status_id = %s where job_id = %s;"""
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql, (status_id,job_id))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print ("Done")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

