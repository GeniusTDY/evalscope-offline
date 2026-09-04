import base64
import json
import pickle
import sqlite3

db_path = 'your db path'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute('PRAGMA table_info(result)')
columns = [info[1] for info in cursor.fetchall()]
print('列名：', columns)

cursor.execute('SELECT * FROM result WHERE success=1 AND first_chunk_latency > 1')
rows = cursor.fetchall()
print(f'len(rows): {len(rows)}')

for row in rows:
    row_dict = dict(zip(columns, row))

    row_dict['request'] = pickle.loads(base64.b64decode(row_dict['request']))

    row_dict['response_messages'] = pickle.loads(base64.b64decode(row_dict['response_messages']))
    # print(row_dict)
    print(
        f'request_id: {json.loads(row_dict["response_messages"][0])["id"]}, first_chunk_latency: {row_dict["first_chunk_latency"]}'  # noqa: E501
    )

    # break
