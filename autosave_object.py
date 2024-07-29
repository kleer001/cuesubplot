import threading
import time
import os
from stage import get_current_data

class Autosave:
    def __init__(self, zeroth_cue, first_cue, second_cue, item_components, settings):
        self.zeroth_cue = zeroth_cue
        self.first_cue = first_cue
        self.second_cue = second_cue
        self.item_components = item_components
        self.settings = settings
        self.last_save_time = time.time()
        self.last_saved_data = None
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.autosave_loop).start()

    def stop(self):
        self.running = False

    def autosave_loop(self):
        while self.running:
            try:
                current_data = get_current_data()
                if current_data != self.last_saved_data:
                    self.save_autosave_file(current_data)
                    self.last_saved_data = current_data
            except Exception as e:
                print(f"Error in autosave loop: {e}")
            time.sleep(self.settings["autosave_interval"])

    def save_autosave_file(self, data):
        with open(".autosave.txt", "w", encoding="utf-8") as f:
            f.write(f"0th Cue: {data['zeroth_cue']}\n")
            f.write(f"1st Cue: {data['first_cue']}\n")
            f.write(f"2nd Cue: {data['second_cue']}\n\n")

            for item in data["items"]:
                f.write(f"Item: {item['Item']}\n")
                if item["Result"]:
                    f.write("******\n")
                    f.write(f"Result:\n{item['Result']}\n")
                f.write("\n")

        print("Autosave file saved")



