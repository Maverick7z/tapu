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
proxies = []
with open('proxy.txt', 'r') as file:
    for line in file:
        proxies.append(line.strip())
proxy_index = 0
for i in range(1111, 200000000):
    url = f'https://cbsapi.tkgm.gov.tr/megsiswebapi.v3/api/zemin/{i}'
    proxy = proxies[proxy_index % len(proxies)]
    proxies_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    try:
        response = requests.get(url, proxies=proxies_dict)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f'Hata oluştu: {e}')
        proxy_index += 1
        continue 
    
    data = response.json()
    json_data = json.dumps(data)
    cursor.execute('INSERT INTO tapu (response) VALUES (%s)', (json_data,))
    conn.commit()
    print(f'Durum - {i}: {response.status_code}')
    with open('veriler.js', 'a') as file:
        file.write(f'var veri_{i} = {json_data};\n')
    proxy_index += 1
cursor.close()
conn.close()