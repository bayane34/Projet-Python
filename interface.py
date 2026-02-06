import customtkinter as ctk

ctk.set_appearance_mode("dark")  # dark = girly moderne 
ctk.set_default_color_theme("pink")  # thème rose !!

app = ctk.CTk()
app.geometry("400x300")
app.title("Ma bibliothèque personnelle")

label = ctk.CTkLabel(app, text="Bienvenue dans ta bibliothèque !", font=("Arial", 18))
label.pack(pady=40)

button = ctk.CTkButton(app, text="Clique moi")
button.pack(pady=10)

app.mainloop()
