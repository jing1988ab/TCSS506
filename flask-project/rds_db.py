import pymysql
import aws_credentials as rds
conn = pymysql.connect(
        host= "database-sql.c9xp7kbwvtsm.us-east-1.rds.amazonaws.com",
        port = "3306",
        user = "tcss506",
        password = "Tcss_506_restaurant!",
        db = "tcss506",
        
        )

# Table Creation
# cursor=conn.cursor()
# create_table="""
# create table Details (email varchar(200),password varchar(200))

# """
# cursor.execute(create_table)


def insert_details(email,password):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (email,password) VALUES (%s,%s)", (email,password))
    conn.commit()

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM Details")
    details = cur.fetchall()
    return details