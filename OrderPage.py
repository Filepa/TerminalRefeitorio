from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from pickle import *

class OrderPage(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.matricula = matricula

        self.title("Solicitar Refeição")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0, padx=100, pady=10)

        self.titulo = Label(self.f1, text="Solicitar refeição", font=["Arial", "10", "bold"])
        self.titulo.grid(row=0, column=0)

        self.f2 = Frame(self, bg='moccasin')
        self.f2.grid(row=1, column=0)

        self.l1 = Label(self.f2, text='Almoço:', bg='moccasin', font=["Times New Roman", "8", "bold"])
        self.l1.grid(row=1, column=0)
        self.l1n = Label(self.f2, bg='moccasin', text='Deve ser solicitado entre 11 a.m. do Dia anterior e 4 p.m. do Dia anterior.')
        self.l1n.grid(row=1, column=1)

        self.l2 = Label(self.f2, text='Jantar:', bg='moccasin', font=["Times New Roman", "8", "bold"])
        self.l2.grid(row=2, column=0)
        self.l2n = Label(self.f2, bg='moccasin', text='Deve ser solicitado entre 6 a.m. do Mesmo dia e 11 a.m. do Mesmo dia.    ')
        self.l2n.grid(row=2, column=1)

        self.f3 = Frame(self)
        self.f3.grid(row=3, column=0)
        self.f4 = LabelFrame(self, text="Informes da Solicitação")
        self.f4.grid(row=4, column=0)
        self.l3 = Label(self.f4, text='Tipo de Refeição:')
        self.l3.grid(row=4, column=0, padx=5, pady=5)

        hora = int(datetime.now().strftime("%H"))
        dia = datetime.now().strftime("%A")

        if hora >= 6 and hora < 18 and not (dia=="Saturday" or dia=='Sunday'):
            if hora < 11:
                self.combo1 = ttk.Combobox(self.f4, values=["Jantar"])
                self.combo1.grid(row=5, column=0)
            else:
                self.combo1 = ttk.Combobox(self.f4, values=["Almoco"])  
                self.combo1.grid(row=5, column=0)
            self.l4 = Label(self.f4, text='Selecione o motivo da solicitação:')
            self.l4.grid(row=6, column=0, padx=5, pady=5)

            self.combo2 = ttk.Combobox(self.f4, values=["TCC", "Prova", "Gremio", "Bolsa", "Outros"])
            self.combo2.grid(row=7, column=0)

            self.button1 = Button(self.f4, text='Enviar', bg='green', fg='white', command=self.registrar)
            self.button1.grid(row=8, column=0, padx=5, pady=10)
        else:
            self.l3.config(text='Nenhuma refeição pode ser solicitada neste horário.', bg='moccasin', font='Times 10 bold')

        self.f5 = Frame(self)
        self.f5.grid(row=5, column=0)
        self.button2 = Button(self.f5, text='Voltar', command=self.voltar)
        self.button2.grid(row=5, column=0, pady=5)

        self.l5 = Label(self.f3, text='')
        self.l5.grid(row=3, column=0, sticky='news')

        self.mainloop()

    def verificar(func):
        def wrapper(self):
            with open('solicitacoes.txt') as solicitacoes:
                for dados in solicitacoes.readlines():
                    dados = dados.strip().split()
                    if dados[-2] == self.matricula and dados[-1] == 'solicitado':
                        return self.l5.config(text='A refeição já foi solicitada.', fg='green')
            return func(self)
        return wrapper 

    @verificar
    def registrar(self):
        tipo = self.combo1.get()
        motivo = self.combo2.get()

        with open('usuarios.txt', 'rb') as arquivoDados:
            lista_usuarios = load(arquivoDados)
            
            for user in lista_usuarios:
                if user.matricula == self.matricula and user.__class__.__name__ == "Administrador":
                    self.l5.config(text='O usuário não pode solicitar a refeição.', fg='red')
                    break
                elif user.matricula == self.matricula and user.suspenso == True:
                    self.l5.config(text='O usuário está suspenso.', fg='red')
                    break
            else:
                if tipo == '' or motivo == '':
                    self.l5.config(text='Por favor, corrija os erros', fg='red')
                else:
                    with open("solicitacoes.txt", "a") as solicitacoes:
                        if tipo == 'Almoco':
                            data_solicitacao = datetime.now()+timedelta(days=1)
                            if data_solicitacao.strftime("%A") == 'Saturday':
                                data_solicitacao = datetime.now()+timedelta(days=3)
                            solicitacoes.write(data_solicitacao.strftime("%A %d/%m/%y")+' '+tipo+' '+motivo+' '+self.matricula+' '+"solicitado"+'\n')
                        else:
                            solicitacoes.write(datetime.now().strftime("%A %d/%m/%y")+' '+tipo+' '+motivo+' '+self.matricula+' '+"solicitado"+'\n')
                    self.l5.config(text='Refeição solicitada.', fg='green')
        self.after(5000, lambda: self.l5.config(text=''))

    def voltar(self):
        self.destroy()
        from MenuPage import MenuPage
        MenuPage("Aluno", self.matricula)

#if __name__ == '__main__':
#    OrderPage(input())