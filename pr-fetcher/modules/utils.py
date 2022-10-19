import os
import json
import time
from datetime import datetime, timedelta
from collections.abc import MutableMapping
import pandas as pd


def flatten_dict(d: MutableMapping, sep: str= '.') -> MutableMapping:
  """ Flattens a dictionary.
    Ref: https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
    (Modified for context)
  """
  return pd.json_normalize(d, sep=sep).to_dict(orient='records')


def get_token(use_backup_token: bool):
  """" Returns github personal access token """
  with open(os.path.join('', f'.token{("2" if not use_backup_token else "")}'), 'r') as f:
    token = f.read()
  return token


def get_queries(query_name: str = None):
  """ Returns an array of graphql queries """
  query_list = []
  
  if query_name is None:
    file_list = os.listdir('queries')
  else:
    file_list = [f'{query_name}.graphql']

  for filename in file_list:
    if '.graphql' in filename:
      with open(os.path.join('queries', filename), 'r') as f:
        query = f.read()
        query_list.append({
          'query': query,
          'name': filename.replace('.graphql', '')
        })
  return query_list


def build_json(data: list, filename: str):
  """ Builds json from fetched data and saves it to out folder """
  json_data = json.dumps(data, indent=2)
  with open(f'out/{filename}.json', 'w') as outfile:
    outfile.write(json_data)


def build_csv(data: list):
  """ Builds csv from fetched data and saves it to out folder """
  for response in data:
    df = pd.DataFrame.from_dict(flatten_dict(response['data']))
    df.to_csv (f'out/{response["name"]}.csv', index = False, header=True)


def date_from_iso(date_str: str):
  """ Returns a datetime object from an iso string """
  if date_str is None:
    return None
  minus_z = date_str.replace('Z', '')
  return datetime.fromisoformat(minus_z)


def transform_pr_data(data: list, repo_name: str):
  """ Transforms PR data into simpler info """
  transformed_data = []
  for item in data:
    created_at = date_from_iso(item['createdAt'])
    closed_at = date_from_iso(item['closedAt'])
    merged_at = date_from_iso(item['mergedAt'])
    is_merged = item['state'] == 'MERGED'
    try:
      finished_at_time = (merged_at if is_merged else closed_at) - created_at
      finished_at = finished_at_time.days
    except:
      finished_at = 0
    transformed_data.append({
      'repo': repo_name,
      'prSize': item['changedFiles'] + item['addedLines'] + item['removedLines'],
      'analysisTimeDays': finished_at,
      'descSize': len(item['bodyText']),
      'interactionCount': item['participants']['totalCount'] + item['comments']['totalCount'],
      'changedFiles': item['changedFiles'],
      'addedLines': item['addedLines'],
      'removedLines': item['removedLines'],
      'participants': item['participants']['totalCount'],
      'comments': item['comments']['totalCount'],
      'state': item['state'],
    })
  return transformed_data


def sleep_before_request(rate_limit_info: dict):
  """ Sleeps to delay requests """
  if not rate_limit_info:
    print('Sleeping for 0ms (none info)')
    return
  
  time.sleep(0.05)
  reqs_left = rate_limit_info['remaining']
  reset_at = date_from_iso(rate_limit_info['resetAt']) - timedelta(hours=3)
  time_left_before_reset = (reset_at - datetime.now()).total_seconds()

  if reqs_left < 50:
    print(f'Sleeping for {time_left_before_reset}sec. {reqs_left} reqs left')
    time.sleep(time_left_before_reset)
  return
