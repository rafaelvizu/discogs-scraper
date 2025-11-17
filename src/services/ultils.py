from dataclasses import asdict


def unique_array_by_key(arr: list[dict], key: str) -> list[dict]:
     """Removes duplicate dictionaries from an array based on a specified key."""
     unique_dict = {item[key]: item for item in arr}
     return list(unique_dict.values())

def unique_array_of_objects_by_key(arr: list[object], key: str) -> list[object]:
     """Removes duplicate objects from an array based on a specified key."""
     unique_dict = {getattr(item, key): item for item in arr}
     return list(unique_dict.values())

def save_array_of_objects_to_jsonl_file(arr: list[object], file_path: str) -> None:
     """Saves an array of dataclass objects to a JSONL file."""
     import json
     import os

     os.makedirs(os.path.dirname(file_path), exist_ok=True)

     with open(file_path, 'w', encoding='utf-8') as f:
          items = list()
          for item in arr:
               items.append(asdict(item))

          json.dump(items, f, ensure_ascii=False, indent=4)
