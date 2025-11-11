import customtkinter
import mysql.connector
import database
from tkinter import messagebox



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1080x720")
        self.title("Zarządzanie wydatkami")

        database.init_database()

        # Main layout frames
        self.frame_left = customtkinter.CTkFrame(self)
        self.frame_left.pack(side="left", fill="both", expand=False, padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(self, width=400)
        self.frame_right.pack(side="right", fill="y", padx=20, pady=20)

        # Left side: expenses list
        self.label_list = customtkinter.CTkLabel(
            self.frame_left,
            text='Lista wydatków',
            font=customtkinter.CTkFont(size=22, weight='bold')
        )
        self.label_list.pack(pady=15)

        self.frame_list = customtkinter.CTkScrollableFrame(self.frame_left, width=800, height=800)
        self.frame_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Header row
        headers = ["ID", "Produkt", "Kategoria", "Cena", "Miejsce"]
        header_sizes = [50, 150, 150, 100, 150]
        
        header_frame = customtkinter.CTkFrame(self.frame_list)
        header_frame.pack(fill="x", pady=(0, 5))

        for i, (text, size) in enumerate(zip(headers, header_sizes)):
            label = customtkinter.CTkLabel(header_frame, text=text, width=size, anchor="w",
                                           font=customtkinter.CTkFont(size=18, weight='bold'))
            label.grid(row=0, column=i, padx=10, sticky="w"),
            

        # Right side: add new expense form
        self.label_title = customtkinter.CTkLabel(
            self.frame_right,
            text='Dodaj pozycję',
            font=customtkinter.CTkFont(size=20, weight='bold')
        )
        self.label_title.pack(pady=20)

        self.entry_name = customtkinter.CTkEntry(self.frame_right, placeholder_text='Produkt')
        self.entry_name.pack(pady=10, padx=20)

        self.entry_category = customtkinter.CTkEntry(self.frame_right, placeholder_text='Kategoria')
        self.entry_category.pack(pady=10, padx=20)

        self.entry_cost = customtkinter.CTkEntry(self.frame_right, placeholder_text='Cena')
        self.entry_cost.pack(pady=10, padx=20)

        self.entry_place = customtkinter.CTkEntry(self.frame_right, placeholder_text='Miejsce')
        self.entry_place.pack(pady=10, padx=20)

        self.button_add = customtkinter.CTkButton(
            self.frame_right,
            text='Dodaj pozycję',
            command=self.add_expense
        )
        self.button_add.pack(pady=25)

        # Load data initially
        self.load_expenses()

    def add_expense(self):
        name = self.entry_name.get().strip()
        category = self.entry_category.get().strip()
        cost = self.entry_cost.get().strip()
        place = self.entry_place.get().strip()

        if not (name and category and cost and place):
            messagebox.showwarning('Brakujące dane', 'Wypełnij wszystkie pola!')
            return
        
        try:
            cost = float(cost)
        except ValueError:
            messagebox.showwarning('Błąd', 'Cena musi być liczbą!')
            return
        
        try:
            database.insert_expense(name, category, cost, place)
            messagebox.showinfo('Sukces', 'Dodano pozycję')
            self.entry_name.delete(0, 'end')
            self.entry_category.delete(0, 'end')
            self.entry_cost.delete(0, 'end')
            self.entry_place.delete(0, 'end')

            self.load_expenses()
        except Exception as exc:
            messagebox.showerror('Błąd bazy danych', str(exc))

    def load_expenses(self):
        for widget in self.frame_list.winfo_children()[1:]:
            if isinstance(widget, customtkinter.CTkFrame) and widget != self.frame_list._parent_frame:
                widget.destroy()
        
        expenses = database.get_all_expenses()

        for exp in expenses:
            row = customtkinter.CTkFrame(self.frame_list)
            row.pack(fill="x", pady=2)
            customtkinter.CTkLabel(row, text=str(exp["id"]), width=50, anchor="w").grid(row=0, column=0, padx=10)
            customtkinter.CTkLabel(row, text=exp["name"], width=150, anchor="w").grid(row=0, column=1, padx=10)
            customtkinter.CTkLabel(row, text=exp["category"], width=150, anchor="w").grid(row=0, column=2, padx=10)
            customtkinter.CTkLabel(row, text=f'{exp["cost"]:.2f}', width=100, anchor="w").grid(row=0, column=3, padx=10)
            customtkinter.CTkLabel(row, text=exp["place"], width=150, anchor="w").grid(row=0, column=4, padx=10)
            

if __name__ == '__main__':
    app = App()
    app.mainloop()