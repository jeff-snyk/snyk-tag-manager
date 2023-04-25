import tkinter as tk
from tkinter import ttk
import requests
import json

def fetch_tags(api_key, group_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {api_key}"
    }
    url = f"https://api.snyk.io/v1/group/{group_id}/tags"
    response = requests.get(url, headers=headers)
    return response.json()

def list_tags(page=0):
    api_key = api_key_entry.get()
    group_id = group_id_entry.get()
    tag_data = fetch_tags(api_key, group_id)

    tags_listbox.delete(0, tk.END)  # Clear the listbox before displaying new tags
    start_index = page * 25
    end_index = start_index + 25
    for tag in tag_data['tags'][start_index:end_index]:
        tags_listbox.insert(tk.END, f"{tag['key']}: {tag['value']}")

    # Update navigation buttons state
    back_button.config(state=tk.NORMAL if page > 0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if end_index < len(tag_data['tags']) else tk.DISABLED)

def go_back():
    global current_page
    current_page -= 1
    list_tags(current_page)

def go_next():
    global current_page
    current_page += 1
    list_tags(current_page)

root = tk.Tk()
root.title("Snyk Tag Manager")

current_page = 0

api_key_label = tk.Label(root, text="Snyk API Token:")
api_key_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
api_key_entry = tk.Entry(root)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)

group_id_label = tk.Label(root, text="Group ID:")
group_id_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
group_id_entry = tk.Entry(root)
group_id_entry.grid(row=1, column=1, padx=5, pady=5)

list_tags_button = tk.Button(root, text="List Tags", command=list_tags)
list_tags_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

tags_listbox = tk.Listbox(root)
tags_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

back_button = tk.Button(root, text="Back", command=go_back, state=tk.DISABLED)
back_button.grid(row=4, column=0, padx=5, pady=5)

next_button = tk.Button(root, text="Next", command=go_next, state=tk.DISABLED)
next_button.grid(row=4, column=1, padx=5, pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)



root.mainloop()

