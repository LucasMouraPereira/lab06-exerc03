import os
import concurrent.futures
import pandas as pd
from modules.fetch import fetch_data
from modules.csv import build_csv

def process_repo(data_list, secondary_key):
  """ Processes a repo """
  for data in data_list:
    new_data = fetch_data(
      repo_name=data['name'],
      repo_owner=data['owner'],
      query=data['query'],
      secondary_key=secondary_key
    )
    build_csv(data['owner'], data['name'], new_data)
    print(f'===== Repo {data["owner"]}/{data["name"]} processed')

  return '=================> Finished stack'


if __name__ == '__main__':
  print('init pr-fetch')
  input_df = pd.read_csv('in/lab03.csv')

  input_data = []

  for row in input_df.itertuples(index=True):
    with open(os.path.join('queries', 'getpq.graphql'), 'r') as f:
      query = f.read()
    input_data.append({
      'name': row.name,
      'owner': row.ownerLogin,
      'query': query
    })
  
  list_1 = input_data[::2]
  list_2 = input_data[1::2]

  with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    futures.append(executor.submit(process_repo, data_list=list_1, secondary_key=False))
    futures.append(executor.submit(process_repo, data_list=list_2, secondary_key=True))
    for future in concurrent.futures.as_completed(futures):
      print(future.result())
