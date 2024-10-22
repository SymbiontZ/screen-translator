import tkinter as tk

class ErrorHandler(tk.Frame):
    def __init__(self, parent, controller, tl):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        headerFont = ("Cascadia Code", 16, "bold")
        errorFont = ("Cascadia code", 12)

        headerLabel = tk.Label(self, text="An error ocurred!", font=headerFont)
        headerLabel.grid(row=0,column=0, padx=10, pady=20, sticky="nsew")

        self.errorLabel = tk.Label(self, text="None", font= errorFont)
        self.errorLabel.grid(row=1,column=0, padx=20, pady=20, sticky="nsew")

    def set_error(self, error):
        self.errorLabel.config(text=error)