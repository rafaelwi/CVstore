import psycopg2
from config import config






def setup():
    print ("Setting up the database...")
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
	            REFERENCES company(company_id)
        )
        """,
        """ CREATE TABLE IF NOT EXISTS job_application (
                app_id integer PRIMARY KEY,
                company_id integer,
                job_id integer,
                    CONSTRAINT fk_company
                    FOREIGN KEY(company_id) 
	                REFERENCES company(company_id),
                    CONSTRAINT fk_job
                    FOREIGN KEY(job_id) 
	                REFERENCES jobs(job_id)
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
   

setup()