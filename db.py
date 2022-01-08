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
            CONSTRAINT fk_company
                FOREIGN KEY(company_id) 
	            REFERENCES company(company_id)
        )
        """,
        """ CREATE TABLE IF NOT EXISTS job_application (
                app_id integer PRIMARY KEY DEFAULT nextval('job_application_id_seq'),
                company_id integer,
                job_id integer,
                    CONSTRAINT fk_company
                    FOREIGN KEY(company_id) 
	                REFERENCES company(company_id),
                    CONSTRAINT fk_job
                    FOREIGN KEY(job_id) 
	                REFERENCES job(job_id)
                )
        """)
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
    sql = """INSERT INTO job (job_title,application_url,salary,company_id) VALUES (%s,%s,%s,%s);"""
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
        print ("Done!")
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
    sql = """DELETE FROM job WHERE job_id = %s;"""
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
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
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

