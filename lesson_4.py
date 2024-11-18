import requests
import hashlib
import re
import json
import sqlite3


#За допомогою бібліотеки requests отримати контент першої сторінки сайту https://www.lejobadequat.com/emplois 
def post_content():
  url = "https://www.lejobadequat.com/emplois"
  payload = {
   "action":"facetwp_refresh",
   "data":{
      "facets":{
         "recherche":[

         ],
         "ou":[

         ],
         "type_de_contrat":[

         ],
         "fonction":[

         ],
         "load_more":[
            1
         ]
      },
      "frozen_facets":{
         "ou":"hard"
      },
      "http_params":{
         "get":[

         ],
         "uri":"emplois",
         "url_vars":[

         ]
      },
      "template":"wp",
      "extras":{
         "counts":True,
         "sort":"default"
      },
      "soft_refresh":1,
      "is_bfcache":1,
      "first_load":0,
      "paged":1
   }
}
  response = requests.post(url, json = payload)
  print(response.status_code)
  print(response.text)
  return response

def get_content():
  name = hashlib.nd5(url.encode('utf')).hexdigest()
  print(name)

  try:
    with open(name, 'r') as f:
      content = f.read()
      return content

  except:
    response = requests.get(url)
    print('request was sent')
    with open(name, 'w') as f:
      f.write(response.text)
    return response.text

response = post_content()

#За допомогою бібліотеки re отримати всі назви вакансій та посилання (url)
if response.ok:
  pattern = r'<h3 class=\\\DjobCard_title m-0\\\D\>\s*.*?h3>'
  job_titles = re.findall(pattern, response.text)
  job_titles = [title.replace('<h3 class=\\"jobCard_title m-0\\">', '') for title in job_titles]
  job_titles = [title.replace('  H\\/F<\\/h3>', '') for title in job_titles]
  

  pattern_2 = r'https:\\/\\/www\.lejobadequat\.com\\/emplois\\/\d{6}[\w-]+-f-h-fr\\'
  job_urls =  re.findall(pattern_2, response.text)
  job_urls = [url.replace('\\', '') for url in job_urls]
  

else:
    print("No valid response to process.")

jobs_table = []
for idx, (title, url) in enumerate(zip(job_titles, job_urls), start=1):
        jobs_table.append({'id': idx, 'title': title, 'url': url})

print(jobs_table)

#Зберегти результат у форматі JSON
output_file = 'jobs_table.json'
with open(output_file, 'w', encoding='utf-8', indent=4) as file:
  json.dump(jobs_table, file)

  print('JSON saved successfully')

#Зберегти результат в базі даних SQLite
def write_sql(data: list) -> None:
    filename = 'jobs.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = '''
        create table if not exists jobs (
            id integer primary key,
            title text,
            url text
        )
    '''
    cursor.execute(sql)

    for item in data:
        cursor.execute('''
            insert into jobs (id, title, url)
            values (?, ?, ?)
        ''', (item['id'], item['title'], item['url']))

    conn.commit()
    conn.close()

    print('SQL saved successfully')

write_sql(jobs_table)
