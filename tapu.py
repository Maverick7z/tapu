import json
import requests
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="",
    database="tapu"
)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tapu (
        id INT AUTO_INCREMENT PRIMARY KEY,
        response JSON
    )
''')
for i in range(1111, 200000000):
    url = f'https://cbsapi.tkgm.gov.tr/megsiswebapi.v3/api/zemin/{i}'
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        continue 
    
    data = response.json()
    json_data = json.dumps(data)
    cursor.execute('INSERT INTO tapu (response) VALUES (%s)', (json_data,))
    conn.commit()
    print(f'Durum - {i}: {response.status_code}')
cursor.close()
conn.close()