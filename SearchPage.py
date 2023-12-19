from tkinter import *
from pickle import *

class SearchPage(Tk):
    def __init__(self):
        super().__init__()
        self.matricula = ''
        self.nome = ''
        self.turma = ''
        self.idade = 0
        self.telefone = ''
        self.endereco = ''
        self.email = ''
        self.faltas = 0
        self.suspenso = False

        self.show = False

        self.title("Busca")
        self["padx"] = 50
        self["pady"] = 10

        self.lpesquisa = Label(self, text='Pesquise o nome ou matricula do usuário:')
        self.lpesquisa.grid(row=1, column=0)

        self.lpesquisa_entry = Entry(self)
        self.lpesquisa_entry.grid(row=1, column=1, padx=10)

        self.buscar = Button(self, text='Buscar', fg='white', bg='blue', command=self.mostrar)
        self.buscar.grid(row=1, column=2, pady=3)

        self.remover = Button(self, text='Remover suspensão', fg='white', bg='red', command=self.removersus)

        self.voltar_tela = Button(self, text='Voltar', command=self.voltar)
        self.voltar_tela.grid(row=2, column=2, pady=3)

        self.msg = Label(self, text='')
        self.msg.grid(row=3, column=0)
        
        self.dados = LabelFrame(self, text="Dados do Usuário:")
        self.refeitorio = LabelFrame(self, text='Status:')
        self.contato = LabelFrame(self, text="Para Contato:")

        self.mainloop()

    def reset(self):
        self.matricula = ''
        self.nome = ''
        self.turma = ''
        self.idade = 0
        self.telefone = ''
        self.endereco = ''
        self.email = ''
        self.faltas = 0
        self.suspenso = False

    def update(self):
        if self.show:

            self.remover.grid(row=2, column=1)
            
            for widget in self.dados.winfo_children():
                widget.destroy()
            for widget in self.refeitorio.winfo_children():
                widget.destroy()
            for widget in self.contato.winfo_children():
                widget.destroy()
            
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

            self.refeitorio.grid(row=1, column=0, sticky='news', padx=10, pady=10)

            self.l5 = Label(self.refeitorio, text='Número de faltas: %s' % self.faltas)
            self.l5.grid(row=2, column=0, padx=40)

            self.l6 = Label(self.refeitorio, text='Aluno Suspenso? %s' % self.suspenso)
            self.l6.grid(row=2, column=1)

            self.contato.grid(row=2, column=0, sticky='news', padx=10, pady=10)

            self.l7 = Label(self.contato, text='Endereço: \n %s' % self.endereco)
            self.l7.grid(row=3, column=0)

            self.l8 = Label(self.contato, text='Número de Telefone: \n %s' % self.telefone)
            self.l8.grid(row=3, column=1)

            self.l9 = Label(self.contato, text='Email: \n %s' % self.email)
            self.l9.grid(row=3, column=2)
        else:
            self.dados.grid_remove()
            self.contato.grid_remove()
            self.refeitorio.grid_remove()

    def mostrar(self):
        self.reset()
        self.update()

        if self.lpesquisa_entry.get() == '':
            self.msg.config(text='Por .')
            self.after(3000, lambda: self.msg.config(text=''))

        try:
            int(self.lpesquisa_entry.get())
            self.matricula = self.lpesquisa_entry.get()
        except ValueError:
            self.nome = self.lpesquisa_entry.get()

        with open("usuarios.txt", "rb") as arquivoDados:
            lista_usuarios = load(arquivoDados)
            for user in lista_usuarios:
                if user.matricula == self.matricula and user.__class__.__name__ == 'Administrador':
                    self.msg.config(text='O buscador acessa apenas alunos e o alvo é administrador.')
                    self.after(3000, lambda: self.msg.config(text=''))
                    break
                elif user.matricula == self.matricula or user.nome == self.nome:
                    self.nome = user.nome
                    self.matricula = user.matricula
                    self.turma = user.turma
                    self.idade = user.idade
                    self.telefone = user.telefone
                    self.endereco = user.endereco
                    self.email = user.email
                    self.faltas = user.faltas
                    self.suspenso = user.suspenso
                    self.show = True
                    break
            else:
                self.msg.config(text='Corrija os erros.')
                self.after(3000, lambda: self.msg.config(text=''))
        self.update()
        self.show = False

    def removersus(self):
        with open("usuarios.txt", "rb") as arquivoDados:
            lista_usuarios = load(arquivoDados)
            for user in lista_usuarios:
                if user.matricula == self.matricula and self.suspenso == True:
                    user.suspenso = False
                    break
                elif user.matricula == self.matricula and self.suspenso == False:
                    self.msg.config(text='O usuário não está suspenso.')
                    self.after(3000, lambda: self.msg.config(text=''))
                    break

        with open("usuarios.txt", 'wb') as arquivoDados:
            dump(lista_usuarios, arquivoDados)

    def voltar(self):
        from ReportPage import ReportPage
        self.destroy()
        ReportPage(self.matricula)

#if __name__ == '__main__':
#    SearchPage()