import csv
from modules.utils import build_json

def build_csv(owner: str, name: str, data: list):

    try:
        data = data[0] 
        keys = data[0].keys()

        with open(f'out/{owner}---{name}.csv', 'w', newline='') as data_file:
            csv_writer = csv.DictWriter(data_file, keys)
            csv_writer.writeheader()
            csv_writer.writerows(data)
    except:
        build_json(data, f'{owner}---{name}')
