from email.policy import strict
import os
import concurrent.futures
import pandas as pd
from modules.fetch import fetch_data
from modules.utils import file_for_repo_exists
from modules.csv import build_csv

def process_repo(data_list, secondary_key):
  """ Processes a repo """
  for data in data_list:
    new_data = fetch_data(
      repo_name=data['name'],
      repo_owner=data['owner'],
      query=data['query'],
      secondary_key=secondary_key,
      row_count=data['row_count']
    )
    if new_data is not None:
      build_csv(data['owner'], data['name'], new_data)
      print(f'===== Repo {data["owner"]}/{data["name"]} processed')
    else:
      print(f'=xxx= Repo {data["owner"]}/{data["name"]} already valid')

  return '=================> Finished stack'


if __name__ == '__main__':
  print('init pr-fetch')
  input_df = pd.read_csv('in/lab03.csv')

  STRICT_MODE = True

  input_data = []

  for row in input_df.itertuples(index=True):
    with open(os.path.join('queries', 'getpq.graphql'), 'r') as f:
      query = f.read()

    row_count = file_for_repo_exists(owner=row.ownerLogin, name=row.name)
    if STRICT_MODE and not row_count:
      input_data.append({
        'name': row.name,
        'owner': row.ownerLogin,
        'query': query,
        'row_count': row_count
      })
  
  print(f'====== INITIALIZING with {len(input_data)} Repos to analyze')
  list_1 = input_data[::2]
  list_2 = input_data[1::2]

  with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    futures.append(executor.submit(process_repo, data_list=list_1, secondary_key=False))
    futures.append(executor.submit(process_repo, data_list=list_2, secondary_key=True))
    for future in concurrent.futures.as_completed(futures):
      print(future.result())
