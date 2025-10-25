import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")

        self.button = customtkinter.CTkButton(self, text="Dodaj element", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)
        self.title("Zarządzanie wydatkami")

    def button_callbck(self):
        print("Dodano element")

app = App()
app.mainloop()