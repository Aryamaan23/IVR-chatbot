import mysql.connector

def DataUpdate(Name,Email,Contact):
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Vandana@123",
        database="mail_signups",
        auth_plugin='mysql_native_password'
    )

    mycursor=mydb.cursor()

    #sql="CREATE TABLE CustomersInfo (name VARCHAR(255), email VARCHAR(255), contact VARCHAR(255));"
    sql='INSERT INTO CustomersInfo (name, email, contact) VALUES ("{0}","{1}", "{2}");'.format(Name,Email,Contact) 

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount,"record inserted.")

if __name__=="__main__":
    DataUpdate("Aryamaan", "pandeyaryamaan@gmail.com","7355949951")
