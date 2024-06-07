import psycopg2
 
conn = psycopg2.connect(database="db",
                        user="testuser",
                        password="1234",
                        host="/cloudsql/uslugi-gcp:europe-central2:pgsql1",
                        port="5432")
 
crsr = conn.cursor()
 
# Odczyt zapisanej tabeli
crsr.execute("SELECT * FROM TEST")
rslt = crsr.fetchall()
for row in rslt:
    print(row)
 
 
# Zwolnienie zasobów i zamknięcie połączenia
crsr.close()
conn.close()