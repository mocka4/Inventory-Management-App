import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management App")
        self.root.geometry("800x600")

        # Inventory DataFrame
        self.inventory_df = pd.DataFrame(columns=['Item Name', 'Quantity', 'Price', 'Category'])

        # Creating UI components
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry widgets for input
        ttk.Label(self.root, text="Item Name:").grid(row=0, column=0, padx=10, pady=10)
        self.item_name_entry = ttk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(self.root)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Price:").grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(self.root)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Category:").grid(row=3, column=0, padx=10, pady=10)
        self.category_entry = ttk.Entry(self.root)
        self.category_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.root, text="Add Item", command=self.add_item).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Delete Item", command=self.delete_item).grid(row=4, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Update Item", command=self.update_item).grid(row=4, column=2, padx=10, pady=10)
        ttk.Button(self.root, text="Save to CSV", command=self.save_to_csv).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Load from CSV", command=self.load_from_csv).grid(row=5, column=1, padx=10, pady=10)

        # Search Bar
        ttk.Label(self.root, text="Search Item:").grid(row=6, column=0, padx=10, pady=10)
        self.search_entry = ttk.Entry(self.root)
        self.search_entry.grid(row=6, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Search", command=self.search_item).grid(row=6, column=2, padx=10, pady=10)

        # Inventory display table
        self.tree = ttk.Treeview(self.root, columns=('Item Name', 'Quantity', 'Price', 'Category'), show='headings')
        self.tree.heading('Item Name', text='Item Name', command=lambda: self.sort_table('Item Name'))
        self.tree.heading('Quantity', text='Quantity', command=lambda: self.sort_table('Quantity'))
        self.tree.heading('Price', text='Price', command=lambda: self.sort_table('Price'))
        self.tree.heading('Category', text='Category', command=lambda: self.sort_table('Category'))
        self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Display inventory summary
        self.total_items_label = ttk.Label(self.root, text="Total Items: 0")
        self.total_items_label.grid(row=8, column=0, padx=10, pady=10)
        self.total_value_label = ttk.Label(self.root, text="Total Value: 0")
        self.total_value_label.grid(row=8, column=1, padx=10, pady=10)

    def add_item(self):
        item_name = self.item_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        category = self.category_entry.get()

        if item_name and quantity and price and category:
            try:
                quantity = int(quantity)
                price = float(price)

                if item_name in self.inventory_df['Item Name'].values:
                    messagebox.showerror("Duplicate Error", "Item already exists in inventory.")
                else:
                    new_row = pd.DataFrame([[item_name, quantity, price, category]], 
                                           columns=['Item Name', 'Quantity', 'Price', 'Category'])
                    self.inventory_df = pd.concat([self.inventory_df, new_row], ignore_index=True)
                    self.refresh_table()
                    self.update_summary()
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity should be an integer and Price should be a float.")
        else:
            messagebox.showerror("Input Error", "All fields must be filled.")

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            self.inventory_df = self.inventory_df[self.inventory_df['Item Name'] != item_name]
            self.refresh_table()
            self.update_summary()
        else:
            messagebox.showerror("Selection Error", "No item selected.")

    def update_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item)['values'][0]
            quantity = self.quantity_entry.get()
            price = self.price_entry.get()
            category = self.category_entry.get()

            if quantity and price and category:
                try:
                    quantity = int(quantity)
                    price = float(price)
                    self.inventory_df.loc[self.inventory_df['Item Name'] == item_name, ['Quantity', 'Price', 'Category']] = [quantity, price, category]
                    self.refresh_table()
                    self.update_summary()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Quantity should be an integer and Price should be a float.")
            else:
                messagebox.showerror("Input Error", "All fields must be filled.")
        else:
            messagebox.showerror("Selection Error", "No item selected.")

    def save_to_csv(self):
        self.inventory_df.to_csv('inventory.csv', index=False)
        messagebox.showinfo("Save", "Inventory saved to CSV successfully.")

    def load_from_csv(self):
        try:
            self.inventory_df = pd.read_csv('inventory.csv')
            self.refresh_table()
            self.update_summary()
            messagebox.showinfo("Load", "Inventory loaded from CSV successfully.")
        except FileNotFoundError:
            messagebox.showerror("File Error", "CSV file not found.")

    def search_item(self):
        search_term = self.search_entry.get()
        if search_term:
            filtered_df = self.inventory_df[self.inventory_df['Item Name'].str.contains(search_term, case=False)]
            self.refresh_table(filtered_df)
        else:
            self.refresh_table()

    def sort_table(self, column):
        self.inventory_df = self.inventory_df.sort_values(by=[column])
        self.refresh_table()

    def refresh_table(self, data=None):
        # Clear existing data from treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Add data to treeview
        df = data if data is not None else self.inventory_df
        for index, row in df.iterrows():
            self.tree.insert('', 'end', values=(row['Item Name'], row['Quantity'], row['Price'], row['Category']))

    def update_summary(self):
        total_items = self.inventory_df['Quantity'].sum()
        total_value = (self.inventory_df['Quantity'] * self.inventory_df['Price']).sum()
        self.total_items_label.config(text=f"Total Items: {total_items}")
        self.total_value_label.config(text=f"Total Value: {total_value}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
