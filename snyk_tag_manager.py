import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
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

    tags_treeview.delete(*tags_treeview.get_children())  # Clear the treeview before displaying new tags
    start_index = page * 25
    end_index = start_index + 25
    for tag in tag_data['tags'][start_index:end_index]:
        tags_treeview.insert("", tk.END, text="", values=(f"{tag['key']}: {tag['value']}", "Delete"))

    # Update navigation buttons state
    back_button.config(state=tk.NORMAL if page > 0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if end_index < len(tag_data['tags']) else tk.DISABLED)

def delete_tag(api_key, group_id, tag_key, tag_value):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {api_key}"
    }
    url = f"https://api.snyk.io/v1/group/{group_id}/tags/delete"
    payload = {
        "key": tag_key,
        "value": tag_value,
        "force": False
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.json()

def on_treeview_click(event):
    item = tags_treeview.identify("item", event.x, event.y)
    column = tags_treeview.identify("column", event.x, event.y)
    if column == "#2":
        tag = tags_treeview.item(item, "values")[0]
        tag_key, tag_value = tag.split(": ")
        api_key = api_key_entry.get()
        group_id = group_id_entry.get()
        response_status, response_json = delete_tag(api_key, group_id, tag_key, tag_value)

        if response_status == 200:
            tags_treeview.delete(item)
        else:
            if response_status == 403:
                message = f"Error deleting tag:\n\n{response_json['message']}. \n\nThis likely means there are projects using this tag."
            else:
                message = f"Failed to delete tag. Error code: {response_status}"
            messagebox.showerror("Error", message)

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
api_key_entry = tk.Entry(root, width=40)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)

group_id_label = tk.Label(root, text="Group ID:")
group_id_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
group_id_entry = tk.Entry(root, width=40)
group_id_entry.grid(row=1, column=1, padx=5, pady=5)

list_tags_button = tk.Button(root, text="List Tags", command=list_tags)
list_tags_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

tags_treeview = ttk.Treeview(root, columns=("Tag", "Delete"), show="headings", height=28)
tags_treeview.heading("Tag", text="Tag")
tags_treeview.column("Tag", width=300)
tags_treeview.heading("Delete", text="Delete")
tags_treeview.column("Delete", width=75)
tags_treeview.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

tags_treeview.bind("<1>", on_treeview_click)

back_button = tk.Button(root, text="Back", command=go_back, state=tk.DISABLED)
back_button.grid(row=4, column=0, padx=5, pady=5)

next_button = tk.Button(root, text="Next", command=go_next, state=tk.DISABLED)
next_button.grid(row=4, column=1, padx=5, pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

