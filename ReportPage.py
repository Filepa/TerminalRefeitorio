from tkinter import *
from tkinter import ttk

class Deferir():
    def __init__(self):
        self.dias = []
        self.tipos = []
        self.motivos = []
        self.matriculas = []
        self.situacoes = []

    def deferir(self, num):
        with open("solicitacoes.txt", "r") as solicitacoes:
            for dados in solicitacoes:
                dia_s, dia, tipo, motivo, matricula, situacao = dados.strip().split()
                self.dias.append(str(dia_s+" "+dia))
                self.tipos.append(tipo)
                self.motivos.append(motivo)
                self.matriculas.append(matricula)
                self.situacoes.append(situacao)

        for i in range(len(self.situacoes)):
            if i >= num:
                self.situacoes[i] = "indeferido"
            else:
                self.situacoes[i] = "deferido"

        with open("solicitacoes.txt", "w") as solicitacoes:
            for i in range(len(self.matriculas)):
                solicitacoes.write(self.dias[i]+' '+self.tipos[i]+' '+self.motivos[i]+' '+self.matriculas[i]+' '+self.situacoes[i]+"\n")
            
class ReportPage(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.matricula = matricula

        self.title("Relatório")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0, padx=100, pady=20)

        self.titulo = Label(self.f1, text="Relatório", fg='blue', font=["Arial", "10", "bold"])
        self.titulo.grid(row=1, column=0)

        self.mostrar = Button(self.f1, text='Mostrar', command=self.mostrar_relatorio)
        self.mostrar.grid(row=2, column=0)

        self.l1 = Label(self.f1, text='')
        self.l1.grid(row=3, column=0)

        self.spinbox = ttk.Spinbox(self.f1, from_=0, to=120)

        self.deferir = Button(self.f1, text='Deferir', fg='white', bg='green', command=self.deferir_mat)

        self.consultar = Button(self.f1, text='Buscar', fg='white', bg='blue', command=self.buscar)
        self.consultar.grid(row=6, column=0)

        self.voltar = Button(self.f1, text='Sair', fg='white', bg='red', command=self.sair)
        self.voltar.grid(row=7, column=0)

        self.mainloop()

    def func(self):
        with open('solicitacoes.txt') as solicitacoes:
            for dados in solicitacoes.readlines():
                dados = dados.strip().split()
                if dados[-1] == 'solicitado':
                    self.deferir.grid(row=5, column=0)
                    self.spinbox.grid(row=4, column=0)
                elif dados[-1] == 'atendido':
                    self.l1.config(text='Ainda não há pedidos')
                else:
                    self.spinbox.grid_remove()
                    self.deferir.grid_remove()
            self.mostrar.grid_remove()

    def mostrar_relatorio(self):
        with open('solicitacoes.txt') as solicitacoes:
            relatorio_texto = ''
            for dados in solicitacoes.readlines():
                dados = dados.strip().split()
                relatorio_texto += f'Matricula: {dados[-2]}, Situacao: {dados[-1]}\n'
        self.l1.config(text=relatorio_texto)
        self.func()

    def deferir_mat(self):
        a = Deferir()
        num = int(self.spinbox.get())
        a.deferir(num)
        self.mostrar_relatorio()
        
    def buscar(self):
        from SearchPage import SearchPage
        self.destroy()
        SearchPage()

    def sair(self):
        from MenuPage import MenuPage
        self.destroy()
        MenuPage("Administrador", self.matricula)

#if __name__ == '__main__':
#    ReportPage('2022')