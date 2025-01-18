import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os

class ItemList:
    def __init__(self):
        self.items = []
        self.load_items()

    def add_item(self, name, stats, rating):
        if any(item[0] == name for item in self.items):
            return "Name already in your list"
        if isinstance(rating, int) and 0 <= rating <= 10:
            self.items.append((name, stats, rating))
            self.save_items()
            return f"Added item: {name}"
        else:
            return "Rating must be between 0 to 10 only"

    def del_item(self, name):
        for index, item in enumerate(self.items):
            if item[0] == name:
                del self.items[index]
                self.save_items()
                return f"Item '{name}' has been removed from the list."
        return "Item not in the list."

    def update_item(self, name, new_name, stats, rating):
        for index, item in enumerate(self.items):
            if item[0] == name:
                if new_name and any(existing[0] == new_name for existing in self.items if existing[0] != name):
                    return "New name already exists in the list."
                if isinstance(rating, int) and 0 <= rating <= 10:
                    self.items[index] = (new_name or name, stats, rating)
                    self.save_items()
                    return f"Updated item: {new_name or name}"
                else:
                    return "Rating must be between 0 to 10 only."
        return "Item not found."

    def display_items(self):
        if not self.items:
            return "No items in the list."
        return "\n".join(f"Name: {item[0]}\nStats: {item[1]}\nRating: {item[2]}\n" for item in self.items)

    def save_items(self):
        with open("items.json", "w") as file:
            json.dump(self.items, file)

    def load_items(self):
        if os.path.exists("items.json"):
            with open("items.json", "r") as file:
                self.items = json.load(file)


class ItemListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Item List App")

        self.item_list = ItemList()

        self.add_button = tk.Button(root, text="Add Item", command=self.show_add_fields)
        self.add_button.pack(pady=10)

        self.del_button = tk.Button(root, text="Delete Item", command=self.show_delete_window)
        self.del_button.pack(pady=10)

        self.update_button = tk.Button(root, text="Update Item", command=self.show_update_window)
        self.update_button.pack(pady=10)

        self.display_button = tk.Button(root, text="Display Items", command=self.display_items)
        self.display_button.pack(pady=10)

        self.entries_frame = None

    def show_add_fields(self):
        if self.entries_frame:
            self.entries_frame.destroy()

        self.entries_frame = tk.Frame(self.root)
        self.entries_frame.pack(pady=10)

        self.name_var = tk.StringVar()
        self.stats_var = tk.StringVar()
        self.rating_var = tk.StringVar()

        tk.Label(self.entries_frame, text="Enter item name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.entries_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.entries_frame, text="Enter item stats (e.g., genre):").grid(row=1, column=0)
        self.stats_entry = tk.Entry(self.entries_frame, textvariable=self.stats_var)
        self.stats_entry.grid(row=1, column=1)

        tk.Label(self.entries_frame, text="Enter item rating (0-10):").grid(row=2, column=0)
        self.rating_entry = tk.Entry(self.entries_frame, textvariable=self.rating_var)
        self.rating_entry.grid(row=2, column=1)

        self.name_entry.bind("<Return>", lambda event: self.stats_entry.focus_set())
        self.stats_entry.bind("<Return>", lambda event: self.rating_entry.focus_set())
        self.rating_entry.bind("<Return>", lambda event: self.submit_item())

        add_button = tk.Button(self.entries_frame, text="Add", command=self.submit_item, state='disabled')
        add_button.grid(row=3, columnspan=2, pady=10)

        self.name_var.trace("w", lambda *args: self.check_fields(add_button))
        self.stats_var.trace("w", lambda *args: self.check_fields(add_button))
        self.rating_var.trace("w", lambda *args: self.check_fields(add_button))

    def show_update_window(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Item")

        if not self.item_list.items:
            tk.Label(update_window, text="No items to update").pack()
            return

        tk.Label(update_window, text="Click an item to update").pack()

        for item in self.item_list.items:
            item_button = tk.Button(
                update_window, text=f"Name: {item[0]}, Stats: {item[1]}, Rating: {item[2]}",
                command=lambda name=item[0]: self.populate_update_fields(name, update_window)
            )
            item_button.pack(pady=2)

    def populate_update_fields(self, name, window):
        if hasattr(self, 'entries_frame') and self.entries_frame is not None:
            self.entries_frame.destroy()

        self.entries_frame = tk.Frame(window)
        self.entries_frame.pack(pady=10)

        item_to_update = next((item for item in self.item_list.items if item[0] == name), None)

        if item_to_update:
            current_name, current_stats, current_rating = item_to_update

            tk.Label(self.entries_frame, text="Update item name:").grid(row=0, column=0)
            self.name_var = tk.StringVar(value=current_name)
            self.name_entry = tk.Entry(self.entries_frame, textvariable=self.name_var)
            self.name_entry.grid(row=0, column=1)

            tk.Label(self.entries_frame, text="Update item stats (e.g., genre):").grid(row=1, column=0)
            self.stats_var = tk.StringVar(value=current_stats)
            self.stats_entry = tk.Entry(self.entries_frame, textvariable=self.stats_var)
            self.stats_entry.grid(row=1, column=1)

            tk.Label(self.entries_frame, text="Update item rating (0-10):").grid(row=2, column=0)
            self.rating_var = tk.StringVar(value=current_rating)
            self.rating_entry = tk.Entry(self.entries_frame, textvariable=self.rating_var)
            self.rating_entry.grid(row=2, column=1)

            self.name_entry.bind("<Return>", lambda event: self.stats_entry.focus_set())
            self.stats_entry.bind("<Return>", lambda event: self.rating_entry.focus_set())
            self.rating_entry.bind("<Return>", lambda event: self.update_item(name, window))

            update_button = tk.Button(self.entries_frame, text="Update", command=lambda: self.update_item(name, window))
            update_button.grid(row=3, columnspan=2, pady=10)

    def update_item(self, old_name, window):
        new_name = self.name_var.get().strip()
        stats = self.stats_var.get().strip()
        rating = self.rating_var.get().strip()

        if not new_name or not stats or not rating:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            rating = int(rating)
            result = self.item_list.update_item(old_name, new_name, stats, rating)
            messagebox.showinfo("Result", result)
            window.destroy()
        except ValueError:
            messagebox.showwarning("Input Error", "Rating must be a valid integer between 0-10.")

    def check_fields(self, add_button):
        if self.name_var.get().strip() and self.stats_var.get().strip() and self.rating_var.get().strip():
            add_button.config(state='normal')
        else:
            add_button.config(state='disabled')

    def submit_item(self):
        name = self.name_var.get().strip()
        stats = self.stats_var.get().strip()
        rating = self.rating_var.get().strip()

        if not name or not stats or not rating:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            rating = int(rating)
            result = self.item_list.add_item(name, stats, rating)
            messagebox.showinfo("Result", result)
            self.entries_frame.destroy()
        except ValueError:
            messagebox.showwarning("Input Error", "Rating must be a valid integer between 0-10.")

    def show_delete_window(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Item")

        if not self.item_list.items:
            tk.Label(delete_window, text="No items to delete").pack()
            return

        tk.Label(delete_window, text="Click an item to delete").pack()

        for item in self.item_list.items:
            item_button = tk.Button(
                delete_window, text=f"Name: {item[0]}, Stats: {item[1]}, Rating: {item[2]}",
                command=lambda name=item[0]: self.delete_item(name, delete_window)
            )
            item_button.pack(pady=2)

    def delete_item(self, name, window):
        result = self.item_list.del_item(name)
        messagebox.showinfo("Result", result)
        window.destroy()

    def display_items(self):
        items_display = tk.Toplevel(self.root)
        items_display.title("Display Items")
        
        text_area = scrolledtext.ScrolledText(items_display, width=40, height=10)
        text_area.pack(pady=10)

        items = self.item_list.display_items()
        text_area.insert(tk.END, items)
        text_area.configure(state='disabled')


root = tk.Tk()
app = ItemListApp(root)
root.mainloop()
