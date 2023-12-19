from tkinter import *

class MenuPage(Tk):
    def __init__(self, funcao, matricula):
        super().__init__()
        self.nivel = funcao
        self.matricula = matricula

        self.title("Página Principal")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0, padx=100, pady=20)

        self.titulo = Label(self.f1, text="Menu", font=["Arial", "10", "bold"])
        self.titulo.grid(row=1, column=0)

        if self.nivel == "Administrador":
            self.button1 = Button(self.f1, text='Terminal de Refeição', bg='green', fg='white', command=self.acessar_terminal)
            self.button1.grid(row=2, column=0)

            self.button2 = Button(self.f1, text='Relatório', command=self.ver_relatorio)
            self.button2.grid(row=3, column=0, sticky='news', pady=5)
        else:
            with open('solicitacoes.txt') as solicitacoes:
                for linha in solicitacoes.readlines():
                    dados = linha.strip().split() 
                    if self.matricula == dados[-2] and dados[-1] == 'deferido':
                        self.lalert = Label(self.f1, text='Você tem refeição agendada para hoje.', bg='moccasin')
                        self.lalert.grid(row=2, column=0, pady=10)
                        break

            self.button1 = Button(self.f1, text='Solicitar Refeição', bg='green', fg='white', command=self.acessar_pag)
            self.button1.grid(row=3, column=0, sticky='news')

            self.button2 = Button(self.f1, text='Ver dados', command=self.ver_dados)
            self.button2.grid(row=4, column=0, sticky='news', pady=5)

        self.button3 = Button(self.f1, text='Sair', bg='red', fg='white', command=self.sair)
        self.button3.grid(row=5, column=0, sticky='news')

        self.mainloop()

    def acessar_pag(self):
        self.destroy()
        from OrderPage import OrderPage
        OrderPage(self.matricula)

    def ver_dados(self):
        self.destroy()
        from UserPage import UserPage
        UserPage(self.matricula)

    def acessar_terminal(self):
        self.destroy()
        from TerminalPage import TerminalPage
        TerminalPage(self.matricula)

    def ver_relatorio(self):
        self.destroy()
        from ReportPage import ReportPage
        ReportPage(self.matricula)

    def sair(self):
        self.destroy()
        from LoginPage import LoginPage
        LoginPage()

#if __name__ == '__main__':
#    MenuPage(input(), input())