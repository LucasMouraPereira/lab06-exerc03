import re
import requests
from .utils import get_token, transform_pr_data, sleep_before_request

API_URL = 'https://api.github.com/graphql'

def api_call(query: str, use_backup_token: bool, rate_limit_info: dict):
  """ Fetches data from github api """
  sleep_before_request(rate_limit_info)
  response = requests.post(API_URL, json={'query': query}, headers={'Authorization': 'Bearer ' + get_token(use_backup_token)})
  return response.json()


def get_paginated(
  name: str,
  owner: str,
  max_value: int,
  total_count: int,
  page_size: int,
  cursor: str,
  query: str,
  results: list,
  use_backup_token: bool,
  rate_limit_info: dict
  ) -> dict:
  """ Makes GraphQL queries that are paginated """
  if max_value and total_count >= max_value:
    return results

  print(f'**{owner}/{name} [{total_count} reqs made]: Running cursor {cursor}')
  
  edited_query = query
  cursor_text = 'null' if cursor is None else f'"{cursor}"'

  edited_query = edited_query.replace('$after', cursor_text)
  edited_query = edited_query.replace('$name', f'"{name}"')
  edited_query = edited_query.replace('$owner', f'"{owner}"')
  response = api_call(edited_query, use_backup_token, rate_limit_info)
  try:
    pull_requests = response['data']['repository']['pullRequests']
  except:
    print(response)
    print('***** ERROR')
    exit()
  tranformed_data = transform_pr_data(pull_requests['nodes'], f'{owner}/{name}')
  results += tranformed_data

  if not pull_requests['pageInfo']['hasNextPage']:
    return results

  return get_paginated(
    name = name,
    owner = owner,
    max_value = max_value,
    total_count = total_count + page_size,
    page_size = page_size,
    cursor = pull_requests['pageInfo']['endCursor'],
    query = query,
    results = results,
    use_backup_token = use_backup_token,
    rate_limit_info = response['data']['rateLimit'],
  )


def fetch_data(repo_name: str, repo_owner: str, query: str, secondary_key: bool):
  """ Entrypoint fetch function """
  data = []
  print(f'Making queries for {repo_owner}/{repo_name}')
  result = get_paginated(
    name = repo_name,
    owner = repo_owner,
    max_value = None,
    total_count = 0,
    page_size = 100,
    cursor = None,
    query = query,
    results = [],
    use_backup_token = secondary_key,
    rate_limit_info = None
  )
  data.append(result)
  print('*** \n')
  return data
