from tkinter import *
from datetime import datetime
from pickle import *

class TerminalPage(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.matricula = matricula
        self.almocos = 0
        self.jantares = 0

        self.title("Terminal")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0)

        self.titulo = Label(self.f1, text="Terminal de Refeitório", fg='blue', font=["Arial", "10", "bold"])
        self.titulo.grid(row=1, column=0)

        self.f2 = Frame(self, bg='moccasin')
        self.f2.grid(row=2, column=0, padx=20, pady=20)

        self.l1 = Label(self.f2, text='Informe a matrícula para registrar a refeição: ', bg='moccasin')
        self.l1.grid(row=3, column=0, padx=5, pady=5)
        self.entry1 = Entry(self.f2)
        self.entry1.grid(row=4, column=0, pady=5)

        self.button = Button(self.f2, text="Enviar", bg='green', fg='white', command=self.autenticar)
        self.button.grid(row=5, column=0, pady=5)

        self.f3 = Frame(self, bg='gray10')
        self.f3.grid(row=7, column=0)

        self.l2 = Label(self.f3, text='', bg='gray10', fg='green')
        self.l2.grid(row=8, column=0, padx=100, pady=10)

        #método para atualizar os segundos
        self.update_time()

        self.almoco = Label(self.f3, bg='gray10', fg='white', text=f'Almoços: {self.almocos}')
        self.jantar = Label(self.f3, bg='gray10', fg='white', text=f'Jantares: {self.jantares}')

        hora = int(datetime.now().strftime("%H"))

        if hora >= 7 and hora < 17:
            self.almoco.config(fg='green')
        elif hora >= 18 and hora < 22:
            self.jantar.config(fg='green')
        else:
            pass

        self.almoco.grid(row=9, column=0)
        self.jantar.grid(row=10, column=0)

        self.msg = Label(self.f3, text='', fg='white', bg='gray10')
        self.msg.grid(row=11, column=0)

        self.exportar = Button(self.f3, text='Exportar', command=self.exportar_historico)
        self.exportar.grid(row=12, column=0, pady=5)

        self.sair = Button(self.f3, text='Sair', bg='red', fg='white', command=self.sair_terminal)
        self.sair.grid(row=13, column=0, pady=5)

        self.lalert = Label(self.f2, text='', fg='red', bg='moccasin')
        self.lalert.grid(row=6, column=0)

        self.incrementar()
        self.mainloop()

    def sair_terminal(self):
        from MenuPage import MenuPage
        self.destroy()
        MenuPage("Administrador", self.matricula)

    def exportar_historico(self):
        with open('solicitacoes.txt') as solicitacoes:
            linhas = solicitacoes.readlines()

        for i, linha in enumerate(linhas):
            global dados
            dados = linha.strip().split()
            if dados[1] == datetime.now().strftime("%d/%m/%y"):
                if dados[-1] == 'deferido':
                    linhas[i] = dados[0]+' '+dados[1]+' '+dados[2]+' '+dados[-2]+' '+"falta"+'\n'
                    self.salvar()
                else:
                    linhas[i] = dados[0]+' '+dados[1]+' '+dados[2]+' '+dados[-2]+' '+dados[-1]+'\n'

        with open('solicitacoes.txt', 'w') as solicitacoes:
            solicitacoes.write('')
            self.msg.config(text="Exportando...")
            self.after(2500, self.sair_terminal)

        with open('historico.txt', 'a') as historico:
            historico.writelines(linhas)

    def salvar(self):
        with open('usuarios.txt', 'rb') as arquivoDados:
            lista_usuarios = load(arquivoDados)

        for user in lista_usuarios:
            if user.matricula == dados[-2]:
                user.faltas += 1
                if user.faltas % 5 == 0:
                    user.suspenso = True

        with open('usuarios.txt', 'wb') as arquivoDados:
            dump(lista_usuarios, arquivoDados)

    def incrementar(self):
        with open('solicitacoes.txt') as solicitacoes:
            for linha in solicitacoes.readlines():
                dados = linha.strip().split()
                if dados[-1] == 'atendido' and dados[2] == "Almoco":
                    self.almocos += 1
                    self.almoco.config(text=f'Almoços: {self.almocos}')
                elif dados[-1] == 'atendido' and dados[2] == 'Jantar':   
                    self.jantares += 1
                    self.jantar.config(text=f'Jantares: {self.jantares}')
                else:
                    continue

    def update_time(self):
        data_n = datetime.now().strftime("%A %d %B 20%y %H:%M:%S")
        self.l2.config(text=data_n)
        self.after(1000, self.update_time)

    def autenticar(self):
        global matricula
        matricula = self.entry1.get()

        if datetime.now().strftime("%A") == 'Saturday' or datetime.now().strftime("%A") == 'Sunday':
            self.lalert.config(text='Refeições não disponíveis para o final de semana.')
            self.after(5000, lambda: self.lalert.config(text=''))
        else:

            with open('usuarios.txt', 'rb') as arquivoDados:
                lista_usuarios = load(arquivoDados)

            for user in lista_usuarios:
                if user.matricula == matricula and user.__class__.__name__ == 'Aluno' and user.suspenso == True:
                    self.lalert.config(text='Usuário Suspenso.')
                    self.after(5000, lambda: self.lalert.config(text=''))
                    break
                elif user.matricula == matricula and user.__class__.__name__ != "Administrador":
                    from TerminalWidget import TerminalWidget
                    self.destroy()
                    TerminalWidget(matricula, self.matricula)
            else:
                self.lalert.config(text='Matrícula não encontrada.')
                self.after(5000, lambda: self.lalert.config(text=''))

#if __name__ == '__main__':
#    TerminalPage('2022')