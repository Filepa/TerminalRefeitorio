from tkinter import *
from tkinter import ttk
from pickle import *

class Usuario:
    def __init__(self, nome, matricula, senha):
        self.nome = nome
        self.matricula = matricula
        self.__senha = senha

    def getSenha(self):
        return self.__senha

    def setSenha(self, senha):
        self.__senha = senha

class Aluno(Usuario):
    def __init__(self, nome, matricula, senha, telefone, idade, turma, email, endereco):
        super().__init__(nome, matricula, senha)
        self.telefone = telefone
        self.idade = idade
        self.turma = turma
        self.email = email
        self.endereco = endereco
        self.faltas = 0
        self.suspenso = False

class Administrador(Usuario):
    def __init__(self, nome, matricula, senha):
        super().__init__(nome, matricula, senha)
        self.salario = 300

class SingupPage(Tk):
    def __init__(self):
        super().__init__()
        self.title("Criar conta")
        self["padx"] = 50
        self["pady"] = 10

        self.dados = LabelFrame(self, text="Dados do Usuário")
        self.dados.grid(row=0, column=0, padx=10, pady=10)

        self.l1 = Label(self.dados, text='Primeiro Nome: ')
        self.l1.grid(row=0, column=0)
        self.entry_nome = Entry(self.dados)
        self.entry_nome.grid(row=1, column=0)

        self.l2 = Label(self.dados, text='Segundo Nome: ')
        self.l2.grid(row=0, column=1)
        self.entry_snome = Entry(self.dados)
        self.entry_snome.grid(row=1, column=1)

        self.l3 = Label(self.dados, text='Matricula: ')
        self.l3.grid(row=0, column=2)
        self.entry_matricula = Entry(self.dados)
        self.entry_matricula.grid(row=1, column=2)

        self.l4 = Label(self.dados, text='Idade: ')
        self.l4.grid(row=2, column=0)
        self.spinbox_idade = ttk.Spinbox(self.dados, from_='14', to='110')
        self.spinbox_idade.grid(row=3, column=0)

        self.l5 = Label(self.dados, text="Curso -Ano - Turno: ")
        self.l5.grid(row=2, column=1)
        self.combo_turma = ttk.Combobox(self.dados, values=["INFO1M", "INFO1V", "INFO2M", "INFO3M", "INFO3V", "INFO4M", "INFO4V"])
        self.combo_turma.grid(row=3, column=1)

        self.l6 = Label(self.dados, text="Número de Telefone: ")
        self.l6.grid(row=2, column=2)
        self.entry_telefone = Entry(self.dados)
        self.entry_telefone.grid(row=3, column=2)

        self.l7 = Label(self.dados, text='Função: ')
        self.l7.grid(row=4, column=0)
        self.combo_funcao = ttk.Combobox(self.dados, values=["Aluno", "Administrador"])
        self.combo_funcao.grid(row=5, column=0)

        self.l8 = Label(self.dados, text='Endereço: ')
        self.l8.grid(row=4, column=1)
        self.entry_endereco = Entry(self.dados)
        self.entry_endereco.grid(row=5, column=1)

        self.l9 = Label(self.dados, text="E-mail: ")
        self.l9.grid(row=4, column=2)
        self.entry_email = Entry(self.dados)
        self.entry_email.grid(row=5, column=2)

        for widget in self.dados.winfo_children():
            widget.grid_configure(padx=10, pady=3)

        self.lfsenha = LabelFrame(self, text='Crie sua Senha')
        self.lfsenha.grid(row=1, column=0, sticky='news', padx=10, pady=10)

        self.l10 = Label(self.lfsenha, text="Senha: ")
        self.l10.grid(row=1, column=0, padx=10, pady=10)
        self.entry_senha = Entry(self.lfsenha)
        self.entry_senha.grid(row=1, column=1)

        self.l11 = Label(self.lfsenha, text="Confirme sua senha: ")
        self.l11.grid(row=1, column=2, padx=10, pady=10)
        self.entry_senhac = Entry(self.lfsenha)
        self.entry_senhac.grid(row=1, column=3)

        self.confirm = LabelFrame(self, text="Termos de Consentimento")
        self.confirm.grid(row=2, column=0, sticky='news', padx=10, pady=10)

        self.terms = StringVar()

        self.l12 = Label(self.confirm, text='Confirmo que li as 100 mil páginas do termo de consentimento.')
        self.l12.grid(row=3, column=0)
        self.check = ttk.Checkbutton(self.confirm, text="Confirmar", variable=self.terms, onvalue=True, off=False)
        self.check.grid(row=4, column=0)

        self.enterdata = Button(self, text='Enviar dados', command=self.cadastrar)
        self.enterdata.grid(row=5, column=0, sticky="news", padx=10, pady=10)

        self.voltar = Button(self, text='Voltar', command=self.voltar_pagina)
        self.voltar.grid(row=6, column=0, sticky="news", padx=10, pady=10)

        self.lalert = Label(self, text="", fg='red')
        self.lalert.grid(row=7, column=0)

        self.mainloop()
    
    def voltar_pagina(self):
        self.destroy()
        from LoginPage import LoginPage
        LoginPage()    

    def cadastrar(self):
        nome = str(self.entry_nome.get())
        snome = str(self.entry_snome.get())
        nomecompleto = nome+' '+snome
        matricula = self.entry_matricula.get()
        senha = self.entry_senha.get()
        funcao = self.combo_funcao.get()
        telefone = self.entry_telefone.get()
        endereco = self.entry_endereco.get()
        turma = self.combo_turma.get()
        idade = self.spinbox_idade.get()
        email = self.entry_email.get()
        termos = self.terms.get()

        if self.entry_senha.get() != self.entry_senhac.get():
            self.lalert.config(text='Senhas diferentes!')
            self.after(3000, lambda: self.lalert.config(text=''))
        elif funcao == '':
            self.lalert.config(text='Por favor, preencha sua função.')
            self.after(3000, lambda: self.lalert.config(text=''))
        elif funcao == 'Aluno' and any([var == "" for var in [termos, nome, snome, matricula, senha, telefone, endereco, idade, turma, email]]):
            self.lalert.config(text='Por favor, preencha os dados necessários para os alunos.')
            self.after(3000, lambda: self.lalert.config(text=''))
        elif funcao == 'Administrador' and any([var == "" for var in [termos, nome, snome, matricula, senha]]):
            self.lalert.config(text='Por favor, preencha os dados necessários para os administradores.')
            self.after(3000, lambda: self.lalert.config(text=''))
        else:
            try:
                with open("usuarios.txt", "rb") as arquivoDados:
                    try:
                        lista = load(arquivoDados)
                    except EOFError:
                        lista = []
            except FileNotFoundError:
                lista = []

            if matricula in [x.matricula for x in lista]:
                self.lalert.config(text='Dados já existentes!')
                self.after(3000, lambda: self.lalert.config(text=''))
            else:
                if funcao == 'Aluno':
                    user = Aluno(nomecompleto, matricula, senha, telefone, idade, turma, email, endereco)
                else:
                    user = Administrador(nomecompleto, matricula, senha)
                lista.append(user)

                with open("usuarios.txt", "wb") as arquivoDados:
                    dump(lista, arquivoDados)

                self.voltar_pagina()

#if __name__ == '__main__':
#    SignupPage()