import os
from datetime import datetime
import time
import threading

BACKUP_DIR = "backups"
LATEST_BACKUP_FILE = "latest_backup.txt"


def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def save_backup(data):
    if not any(data.get(key) for key in ['zeroth_cue', 'first_cue', 'second_cue']) and not data.get('items'):
        print("No data to backup")
        return

    ensure_backup_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.txt"
    filepath = os.path.join(BACKUP_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"0th Cue: {data.get('zeroth_cue', '')}\n")
        f.write(f"1st Cue: {data.get('first_cue', '')}\n")
        f.write(f"2nd Cue: {data.get('second_cue', '')}\n\n")
        for item in data.get('items', []):
            if item and item.get('Item'):
                f.write(f"Item: {item['Item']}\n")
                f.write("******\n")
                f.write(f"Result:\n{item.get('Result', '')}\n\n")

    latest_filepath = os.path.join(BACKUP_DIR, LATEST_BACKUP_FILE)
    os.replace(filepath, latest_filepath)

    print(f"Backup generated: {filename}")


def load_latest_backup():
    latest_filepath = os.path.join(BACKUP_DIR, LATEST_BACKUP_FILE)
    if os.path.exists(latest_filepath):
        try:
            with open(latest_filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            data = {}
            items = []
            current_item = {}
            reading_result = False

            for line in lines:
                line = line.strip()
                if line.startswith("0th Cue: "):
                    data["zeroth_cue"] = line.split(": ", 1)[1]
                elif line.startswith("1st Cue: "):
                    data["first_cue"] = line.split(": ", 1)[1]
                elif line.startswith("2nd Cue: "):
                    data["second_cue"] = line.split(": ", 1)[1]
                elif line.startswith("Item: "):
                    if current_item:
                        items.append(current_item)
                    current_item = {"Item": line.split(": ", 1)[1], "Result": ""}
                    reading_result = False
                elif line == "******":
                    reading_result = True
                elif reading_result:
                    if line == "Result:":
                        continue
                    current_item["Result"] += line + "\n"

            if current_item:
                items.append(current_item)

            data["items"] = items
            return data
        except Exception as e:
            print(f"Error loading backup file: {e}")
    return None


backup_running = False
backup_thread = None

def toggle_auto_backup(get_current_data, interval):
    global backup_running, backup_thread
    if backup_running:
        backup_running = False
        if backup_thread:
            backup_thread.join()
        return "Auto-backup stopped"
    else:
        backup_running = True
        backup_thread = threading.Thread(target=backup_task, args=(get_current_data, interval), daemon=True)
        backup_thread.start()
        return "Auto-backup started"


def backup_task(get_current_data, interval):
    while backup_running:
        current_data = get_current_data()
        print("Current data for backup:")
        print(f"0th Cue: {current_data['zeroth_cue']}")
        print(f"1st Cue: {current_data['first_cue']}")
        print(f"2nd Cue: {current_data['second_cue']}")
        for item in current_data['items']:
            print(f"Item: {item['Item']}")
            print(f"Result: {item['Result']}")
        print("End of current data")

        save_backup(current_data)
        time.sleep(interval)