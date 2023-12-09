import sqlite3
import json
import os

def sqlite_to_json(db_path, json_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        all_data = {}

        for table_name in tables:
            cursor.execute(f"SELECT * FROM {table_name[0]};")
            rows = cursor.fetchall()

            columns = [column[0] for column in cursor.description]

            table_data = [dict(zip(columns, row)) for row in rows]

            all_data[table_name[0]] = table_data

        with open(json_path, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)

        conn.close()
        return True

    except sqlite3.DatabaseError as e:
        print(f"Error processing {db_path}: {e}")
        return False

def extract_sqlite_to_json(directory):
    total_files = 0
    success_files = 0
    failed_files = 0
    failed_filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.sqlite') or filename.endswith('.db'):
            total_files += 1
            db_path = os.path.join(directory, filename)
            json_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}.json")
            
            if sqlite_to_json(db_path, json_path):
                print(f"Converted {filename} to JSON.")
                success_files += 1
            else:
                failed_filenames.append(filename)
                failed_files += 1

    with open(os.path.join(directory, 'failed.txt'), 'w') as f:
        for file in failed_filenames:
            f.write(file + '\n')

    print(f"All Done. Processed {total_files} files. Successfully converted {success_files}, failed {failed_files}.")

extract_sqlite_to_json(os.path.dirname(os.path.realpath(__file__)))
