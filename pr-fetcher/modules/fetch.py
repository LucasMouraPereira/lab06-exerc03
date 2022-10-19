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
  rate_limit_info: dict,
  row_count: int,
  retry_count: int,
  ) -> dict:
  """ Makes GraphQL queries that are paginated """
  if max_value and total_count >= max_value:
    return results

  print(f'**{owner}/{name} [{total_count}/{max_value} reqs made]: Running cursor {cursor}')
  
  edited_query = query
  cursor_text = 'null' if cursor is None else f'"{cursor}"'

  edited_query = edited_query.replace('$after', cursor_text)
  edited_query = edited_query.replace('$name', f'"{name}"')
  edited_query = edited_query.replace('$owner', f'"{owner}"')
  response = api_call(edited_query, use_backup_token, rate_limit_info)

  # Handles reponse errors
  try:
    pull_requests = response['data']['repository']['pullRequests']
  except:
    print(response)
    print('***** ERROR')
    # Tries up to 3 times
    if retry_count < 3:
      print(f'Retrying {owner}/{name}: #{retry_count+1}')
      return get_paginated(
        name = name,
        owner = owner,
        max_value = max_value,
        total_count = total_count,
        page_size = page_size,
        cursor = cursor,
        query = query,
        results = results,
        use_backup_token = use_backup_token,
        rate_limit_info = rate_limit_info,
        row_count = row_count,
        retry_count = retry_count+1
      )
    else:
      return None

  # Transforms data and adds to array
  tranformed_data = transform_pr_data(pull_requests['nodes'], f'{owner}/{name}')
  results += tranformed_data

  total_count_from_req = pull_requests['totalCount']

  # If total count of PRs is about the same as the supplied row count, don't recalculate
  print('*********', cursor, row_count, total_count_from_req)
  if cursor is None and row_count is not None and abs(total_count_from_req - row_count) < 30:
    return None
    
  max_value = total_count_from_req

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
    row_count = row_count,
    retry_count = 0
  )


def fetch_data(repo_name: str, repo_owner: str, query: str, secondary_key: bool, row_count: int):
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
    rate_limit_info = None,
    row_count = row_count,
    retry_count = 0
  )
  if result is None:
    return None
  
  data.append(result)
  return data
