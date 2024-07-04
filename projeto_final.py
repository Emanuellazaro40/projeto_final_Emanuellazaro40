import tkinter as tk
from tkinter import messagebox, Menu
from reportlab.pdfgen import canvas
import webbrowser
import pickle
import os

class Relatorio():
    def print_funcionario(self):
        webbrowser.open("funcionario.pdf")
    
    def geraRelatofuncionario(self, funcionario):
        self.c = canvas.Canvas("funcionario.pdf")
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(170, 790, 'Relatorio do Funcionário')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Nome: ')
        self.c.drawString(50, 670, 'Id: ' )
        self.c.drawString(50, 635, 'Salario base: ')
        self.c.drawString(50, 600, 'Faltas: ')
        self.c.drawString(50, 570, 'Carga horaria: ')
        self.c.drawString(50, 535, 'Entrada: ')
        self.c.drawString(50, 500, 'Saida: ')
        self.c.drawString(50, 470, 'Salario: ')


        self.c.setFont("Helvetica", 18)
        self.c.drawString(250, 700, funcionario.nome)
        self.c.drawString(250, 670, str(funcionario.id))
        self.c.drawString(250, 630, f"{funcionario.salario_base:.2f}€")
        self.c.drawString(250, 600, str(funcionario.faltas))
        self.c.drawString(250, 570, f"{funcionario.carga_horaria_mensal} horas")
        self.c.drawString(250, 535, f"{funcionario.h_entrada}h")
        self.c.drawString(250, 500, f"{funcionario.h_saida}h")
        self.c.drawString(250, 470, f"{funcionario.calcular_salario()}€")

        self.c.showPage()
        self.c.save()
        self.print_funcionario()

class Funcionario:
    def __init__(self, nome, id, salario_base, carga_horaria_mensal, h_entrada, h_saida, faltas):
        self.nome = nome
        self.id = id
        self.salario_base = salario_base
        self.carga_horaria_mensal = carga_horaria_mensal
        self.h_entrada = h_entrada
        self.h_saida = h_saida
        self.faltas = faltas

    def calcular_salario(self):
        salario_proporcional = self.salario_base * (1 - (self.faltas / 30)) 
        return salario_proporcional

class Application(tk.Tk, Relatorio):
    def __init__(self):
        super().__init__()
        self.title("Registro de Funcionários")
        self.configure(background='lightblue')
        self.geometry('700x500')
        self.resizable(True, True)
        self.maxsize(width=None, height=None)
        self.minsize(width=400, height=300)
        
        self.funcionarios = self.carregar_dados()
        
        self.login_frame = tk.Frame(self,  bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.login_frame.pack(pady=10)
        self.login_label = tk.Label(self.login_frame, text="Digite a senha:")
        self.login_label.pack(side="left")
        
        self.login_entry = tk.Entry(self.login_frame, show="*")
        self.login_entry.pack(side="left")
        
        self.login_button = tk.Button(self.login_frame, text="Entrar", bd=3, bg='#107db2', fg='white', font=('verdana', 7, 'bold'), command=self.check_password)
        self.login_button.pack(side="left")

        self.register_frame = tk.Frame(self)
        self.nome_label = tk.Label(self.register_frame, text="Nome:", bg='#dfe3ee', fg='#107db2')
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self.register_frame)
        self.nome_entry.pack()

        self.id_label = tk.Label(self.register_frame, text="ID:", bg='#dfe3ee', fg='#107db2')
        self.id_label.pack()
        self.id_entry = tk.Entry(self.register_frame)
        self.id_entry.pack()

        self.salario_label = tk.Label(self.register_frame, text="Salário Base:", bg='#dfe3ee', fg='#107db2')
        self.salario_label.pack()
        self.salario_entry = tk.Entry(self.register_frame)
        self.salario_entry.pack()

        self.faltas_label = tk.Label(self.register_frame, text="Faltas:", bg='#dfe3ee', fg='#107db2')
        self.faltas_label.pack()
        self.faltas_entry = tk.Entry(self.register_frame)
        self.faltas_entry.pack()

        self.carga_horaria_label = tk.Label(self.register_frame, text="Carga Horária Mensal:", bg='#dfe3ee', fg='#107db2')
        self.carga_horaria_label.pack()
        self.carga_horaria_entry = tk.Entry(self.register_frame)
        self.carga_horaria_entry.pack()

        self.entrada_label = tk.Label(self.register_frame, text="Horário de Entrada:", bg='#dfe3ee', fg='#107db2')
        self.entrada_label.pack()
        self.entrada_entry = tk.Entry(self.register_frame)
        self.entrada_entry.pack()

        self.saida_label = tk.Label(self.register_frame, text="Horário de Saída:", bg='#dfe3ee', fg='#107db2')
        self.saida_label.pack()
        self.saida_entry = tk.Entry(self.register_frame)
        self.saida_entry.pack()
        
        self.add_button = tk.Button(self.register_frame, text="Adicionar Funcionário", bd=3, bg='#107db2', fg='white', font=('verdana', 7, 'bold'), command=self.add_funcionario)
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(self.register_frame, text="Ver Funcionários", bd=3, bg='#107db2', fg='white', font=('verdana', 7, 'bold'), command=self.view_funcionarios)
        self.view_button.pack(pady=10)
         
        self.view_button.pack(pady=10)
        self.Menus()

    def carregar_dados(self):
        if os.path.exists("funcionarios.pkl"):
            with open("funcionarios.pkl", "rb") as f:
                return pickle.load(f)
        return []

    def salvar_dados(self):
        with open("funcionarios.pkl", "wb") as f:
            pickle.dump(self.funcionarios, f)

    def select_funcionario_for_report(self):
        select_window = tk.Toplevel(self)
        select_window.title("Selecionar Funcionário")
        select_window.configure(background='lightblue')
        select_window.geometry('500x500')
        select_window.resizable(True, True)
        select_window.maxsize(width=None, height=None)
        select_window.minsize(width=400, height=300)

        tk.Label(select_window, text="Selecione um funcionário:").pack(pady=10)

        listbox = tk.Listbox(select_window)
        listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        for i, funcionario in enumerate(self.funcionarios):
            listbox.insert(tk.END, f"{funcionario.nome} (ID: {funcionario.id})")

        def on_select():
            selected_index = listbox.curselection()[0]
            self.geraRelatofuncionario(self.funcionarios[selected_index])
            select_window.destroy()

        tk.Button(select_window, text="Gerar Relatório", bd=3, bg='#107db2', fg='white', font=('verdana',
        7, 'bold'), command=on_select).pack(pady=10)

    def check_password(self):
        if self.login_entry.get() == "Adimin":
            self.login_frame.pack_forget()
            self.register_frame.pack(pady=10)
        else:
            messagebox.showerror("Erro", "Senha errada, tente novamente!")

    def add_funcionario(self):
        nome = self.nome_entry.get()
        id = int(self.id_entry.get())
        salario_base = float(self.salario_entry.get())
        faltas = int(self.faltas_entry.get())
        carga_horaria_mensal = int(self.carga_horaria_entry.get())
        h_entrada = self.entrada_entry.get()
        h_saida = self.saida_entry.get()

        novo_funcionario = Funcionario(nome, id, salario_base, carga_horaria_mensal, h_entrada, h_saida, faltas)
        self.funcionarios.append(novo_funcionario)
        self.salvar_dados()
        messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
        
        self.clear_entries()

    def clear_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.salario_entry.delete(0, tk.END)
        self.faltas_entry.delete(0, tk.END)
        self.carga_horaria_entry.delete(0, tk.END)
        self.entrada_entry.delete(0, tk.END)
        self.saida_entry.delete(0, tk.END)

    def view_funcionarios(self):
        view_window = tk.Toplevel(self)
        view_window.title("Funcionários")
        view_window.geometry("400x400")
        view_window.configure(background='lightblue')
        view_window.resizable(True, True)
        view_window.maxsize(width=None, height=None)
        view_window.minsize(width=400, height=300)

        for i, funcionario in enumerate(self.funcionarios):
            salario_final = funcionario.calcular_salario()

            tk.Label(view_window, text=f"Funcionario {i+1}:").pack()
            tk.Label(view_window, text=f"Nome: {funcionario.nome}").pack()
            tk.Label(view_window, text=f"ID: {funcionario.id}").pack()
            tk.Label(view_window, text=f"Salário Base: {funcionario.salario_base:.2f}€").pack()
            tk.Label(view_window, text=f"Carga Horária Mensal: {funcionario.carga_horaria_mensal} horas").pack()
            tk.Label(view_window, text=f"Registros de Ponto:").pack()
            tk.Label(view_window, text=f"  Entrada: {funcionario.h_entrada}").pack()
            tk.Label(view_window, text=f"  Saída: {funcionario.h_saida}").pack()
            tk.Label(view_window, text=f"Faltas: {funcionario.faltas}").pack()
            tk.Label(view_window, text=f"Salário ao fim do mês: {salario_final:.2f}€").pack()
            tk.Label(view_window, text="").pack()

    def Menus(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Ver", menu=filemenu2)
        filemenu.add_command(label="Sair", command=self.quit)
        filemenu2.add_command(label="Relatorio", command=self.select_funcionario_for_report)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
