from tkinter import *
from pickle import *
from datetime import datetime

class TerminalWidget(Tk):
    def __init__(self, matricula, matricula_de_nivel):
        super().__init__()
        self.matricula = matricula
        self.matricula_nivel = matricula_de_nivel
        self.nome = ''
        self.senha = ''
        self.reservas = {
            'Monday': 'Sem reserva',
            'Tuesday': 'Sem reserva',
            'Wednesday': 'Sem reserva',
            'Thursday': 'Sem reserva',
            'Friday': 'Sem reserva',
            'Saturday': 'Sem reserva',
            'Sunday': 'Sem reserva'
        }

        self.dia_atual = datetime.now().strftime("%A")

        with open("usuarios.txt", "rb") as arquivoDados:
            lista_usuarios = load(arquivoDados)
            for user in lista_usuarios:
                if user.matricula == self.matricula:
                    self.nome = user.nome
                    self.senha = user.getSenha()
                    break

        hora = int(datetime.now().strftime("%H"))

        with open('historico.txt') as historico:
            for linha in historico.readlines():
                partes = linha.split()
                data_formatada = datetime.strptime(partes[1], "%d/%m/%y")
                if partes[-2] == self.matricula and data_formatada.strftime("%U") == datetime.now().strftime("%U"):
                    if hora >= 7 and hora < 17 and partes[2] == 'Almoco':
                        dia_semana = partes[0]
                        situacao = partes[-1]
                        self.reservas[dia_semana] = situacao
                    elif hora >= 18 and hora < 22 and partes[2] == 'Jantar':
                        dia_semana = partes[0]
                        situacao = partes[-1]
                        self.reservas[dia_semana] = situacao

        with open('solicitacoes.txt') as solicitacoes:
            for dados in solicitacoes.readlines():
                dados = dados.strip().split()
                data_formatada = datetime.strptime(dados[1], "%d/%m/%y")
                if dados[-2] == self.matricula and data_formatada.strftime("%U") == datetime.now().strftime("%U"):
                    if hora >= 7 and hora < 17 and dados[2] == 'Almoco':
                        dia_semana = dados[0]
                        situacao = dados[-1]
                        self.reservas[dia_semana] = situacao
                    elif hora >= 18 and hora < 22 and dados[2] == 'Jantar':
                        dia_semana = dados[0]
                        situacao = dados[-1]
                        self.reservas[dia_semana] = situacao
                          
        self.title("Deferir Refeição")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0, pady=10)

        self.titulo = Label(self.f1, text="Deferir Refeição", font=["Arial", "10", "bold"])
        self.titulo.grid(row=0, column=0)

        self.f2 = Frame(self)
        self.f2.grid(row=1, column=0, padx=10)

        self.ffrequencia = LabelFrame(self.f2, text="Frequência")
        self.ffrequencia.grid(row=1, column=0)

        self.fextra = Frame(self.ffrequencia)
        self.fextra.grid(row=0, column=1)

        self.fextra2 = Frame(self.ffrequencia)
        self.fextra2.grid(row=0, column=0)

        self.l1 = Label(self.fextra2, text="Monday: ")
        self.l1.grid(row=1, column=0)
        self.l1a = Label(self.fextra, text=self.reservas['Monday'])
        self.l1a.grid(row=1, column=1)

        self.l2 = Label(self.fextra2, text="Tuesday: ")
        self.l2.grid(row=2, column=0)
        self.l2a = Label(self.fextra, text=self.reservas['Tuesday'])
        self.l2a.grid(row=2, column=1)

        self.l3 = Label(self.fextra2, text="Wednesday: ")
        self.l3.grid(row=3, column=0)
        self.l3a = Label(self.fextra, text=self.reservas['Wednesday'])
        self.l3a.grid(row=3, column=1)

        self.l4 = Label(self.fextra2, text="Thursday: ")
        self.l4.grid(row=4, column=0)
        self.l4a = Label(self.fextra, text=self.reservas['Thursday'])
        self.l4a.grid(row=4, column=1)

        self.l5 = Label(self.fextra2, text="Friday: ")
        self.l5.grid(row=5, column=0)
        self.l5a = Label(self.fextra, text=self.reservas['Friday'])
        self.l5a.grid(row=5, column=1)

        for label in self.fextra.winfo_children():
            text = label['text']
            if "Sem reserva" in text or 'falta' in text or 'indeferido' in text:
                label.config(fg='red')
            elif "atendido" in text:
                label.config(fg='green')
            elif 'deferido' in text:
                label.config(fg='black')

        if datetime.now().strftime("%A") == 'Saturday' or datetime.now().strftime("%A") == 'Sunday':
            for label in self.fextra.winfo_children():
                label.grid_remove()

        self.fdata = LabelFrame(self.f2, text='Dados do Usuário')
        self.fdata.grid(row=1, column=1)
        self.l6 = Label(self.fdata, text="Nome Completo: %s" % self.nome)
        self.l6.grid(row=1, column=0)
        self.l7 = Label(self.fdata, text="Matricula: %s" % self.matricula)
        self.l7.grid(row=2, column=0)
        self.f3 = Frame(self.fdata)
        self.f3.grid(row=3, column=0)

        self.l8 = Label(self.f3, text='Digite sua senha: ')
        self.l8.grid(row=0, column=0)
        self.entry_passw = Entry(self.f3)
        self.entry_passw.grid(row=1, column=0)

        self.butdeferir = Button(self.fdata, text='Deferir', bg='green', fg='white', command=self.msgdef)
        self.butdeferir.grid(row=4, column=0)

        self.f4 = Frame(self)
        self.f4.grid(row=2, column=0)

        self.butvoltar = Button(self.f4, text='Voltar', command=self.voltar)
        self.butvoltar.grid(row=1, column=0, pady=10)

        self.lalert = Label(self.f4, text="", fg='red')
        self.lalert.grid(row=0, column=0, sticky='news')

        self.mainloop()

    def msgdef(self):
        with open('solicitacoes.txt') as solicitacoes:
            for dados in solicitacoes.readlines():
                dados = dados.strip().split()
                if dados[-2] == self.matricula:
                    if dados[-1] == 'indeferido':
                        self.lalert.config(text="Indeferido.")
                        self.after(3000, self.voltar)
                    elif dados[-1] == 'atendido':
                        self.lalert.config(text="A sua solicitação já foi atendida.")
                        self.after(3000, self.voltar)
                    else:
                        if self.entry_passw.get() != self.senha:
                            self.lalert.config(text="Senha Incorreta.")
                            self.after(3000, lambda: self.lalert.config(text=''))
                        else:
                            self.atender()
                            self.after(3000, self.voltar)

    def atender(self):
        from tkinter import messagebox
        with open('solicitacoes.txt', 'r') as solicitacoes:
            linhas = solicitacoes.readlines()
            for i, linha in enumerate(linhas):
                dados = linha.strip().split()
                if dados[-2] == self.matricula and dados[-1] == 'deferido':
                    data_formatada = datetime.strptime(dados[1], "%d/%m/%y")
                    if data_formatada.strftime("%d/%m/%y") == datetime.now().strftime("%d/%m/%y"):
                        hora = int(datetime.now().strftime("%H"))
                        if hora >= 7 and hora < 17 and dados[2] == 'Almoco':
                            linhas[i] = dados[0]+' '+dados[1]+' '+dados[2]+' '+dados[3]+' '+dados[4]+' '+"atendido" +'\n'
                            self.lalert.config(text="Deferido.", fg='green')
                            messagebox.showinfo('Sucesso!', 'Sua refeição foi contabilizada.')
                            break
                        elif hora >= 18 and hora < 22 and dados[2] == 'Jantar':
                            linhas[i] = dados[0]+' '+dados[1]+' '+dados[2]+' '+dados[3]+' '+dados[4]+' '+"atendido" +'\n'
                            self.lalert.config(text="Deferido.", fg='green')
                            messagebox.showinfo('Sucesso!', 'Sua refeição foi contabilizada.')
                            break
        
        with open('solicitacoes.txt', 'w') as solicitacoes:
            solicitacoes.write('')
            solicitacoes.writelines(linhas)

    def voltar(self):
        from TerminalPage import TerminalPage
        self.destroy()
        TerminalPage(self.matricula_nivel)

#if __name__ == '__main__':
#    TerminalWidget(input(), 'Aluno')