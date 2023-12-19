from tkinter import *
from pickle import *

class UserPage(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.matricula = matricula
        self.nome = ''
        self.turma = ''
        self.idade = 0
        self.telefone = ''
        self.endereco = ''
        self.email = ''
        self.faltas = 0
        self.suspenso = False

        with open("usuarios.txt", "rb") as arquivoDados:
            lista_usuarios = load(arquivoDados)
            for user in lista_usuarios:
                if user.matricula == self.matricula:
                    self.nome = user.nome
                    self.turma = user.turma
                    self.idade = user.idade
                    self.telefone = user.telefone
                    self.endereco = user.endereco
                    self.email = user.email
                    self.faltas = user.faltas
                    self.suspenso = user.suspenso
                    break

        self.title("Conta:")
        self["padx"] = 50
        self["pady"] = 10

        self.dados = LabelFrame(self, text="Dados do Usuário:")
        self.dados.grid(row=0, column=0, sticky='news', padx=10, pady=10)

        self.l1 = Label(self.dados, text='Nome: \n %s' % self.nome)
        self.l1.grid(row=0, column=0)

        self.l2 = Label(self.dados, text='Matricula: \n %s' % self.matricula)
        self.l2.grid(row=0, column=1)

        self.l3 = Label(self.dados, text='Turma: \n %s' % self.turma)
        self.l3.grid(row=1, column=0)

        self.l4 = Label(self.dados, text='Idade: \n %s anos' % self.idade)
        self.l4.grid(row=1, column=1)

        for widget in self.dados.winfo_children():
            widget.grid_configure(padx=50, pady=3)

        self.refeitorio = LabelFrame(self, text='Status:')
        self.refeitorio.grid(row=1, column=0, sticky='news', padx=10, pady=10)

        self.l5 = Label(self.refeitorio, text='Número de faltas: %s' % self.faltas)
        self.l5.grid(row=2, column=0, padx=40)

        self.l6 = Label(self.refeitorio, text='Aluno Suspenso? %s' % self.suspenso)
        self.l6.grid(row=2, column=1)

        self.contato = LabelFrame(self, text="Para Contato:")
        self.contato.grid(row=2, column=0, sticky='news', padx=10, pady=10)

        self.l7 = Label(self.contato, text='Endereço: \n %s' % self.endereco)
        self.l7.grid(row=3, column=0)

        self.l8 = Label(self.contato, text='Número de Telefone: \n %s' % self.telefone)
        self.l8.grid(row=3, column=1)

        self.l9 = Label(self.contato, text='Email: \n %s' % self.email)
        self.l9.grid(row=3, column=2)

        self.alterarsenha = Button(self, text='Alterar Senha', command=self.alterar)
        self.alterarsenha.grid(row=4, column=0)

        self.button = Button(self, text='Voltar', command=self.voltar)
        self.button.grid(row=5, column=0)

        self.mainloop()
    
    def voltar(self):
        from MenuPage import MenuPage
        self.destroy()
        MenuPage("Aluno", self.matricula)

    def alterar(self):
        from PasswPage import PasswPage
        self.destroy()
        PasswPage(self.matricula)

#if __name__ == '__main__':
#    UserPage(input())