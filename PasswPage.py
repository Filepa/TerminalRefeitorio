from tkinter import *
from pickle import *

class PasswPage(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.matricula = matricula

        self.title("Redefinir Senha")
        self.titulo = Label(self, text="Redefinir Senha", font=["Arial", "10", "bold"])
        self.titulo.grid(row=0, column=0)

        self['padx'] = 50
        self['pady'] = 20

        self.lb1 = LabelFrame(self, text='Senha Atual')
        self.lb1.grid(row=1, column=0, sticky='news', pady=15)

        self.l0 = Label(self.lb1, text='Digite sua senha atual:')
        self.l0.grid(row=2, column=0)
        self.entry_senha_atual = Entry(self.lb1)
        self.entry_senha_atual.grid(row=3, column=0)

        self.lb2 = LabelFrame(self, text='Senha Nova')
        self.lb2.grid(row=2, column=0)

        self.l1 = Label(self.lb2, text='Digite sua nova senha:')
        self.l1.grid(row=3, column=0)
        self.entry_senha_nova = Entry(self.lb2)
        self.entry_senha_nova.grid(row=4, column=0)

        self.l2 = Label(self.lb2, text='Confirme sua nova senha:')
        self.l2.grid(row=5, column=0)
        self.entry_confirm = Entry(self.lb2)
        self.entry_confirm.grid(row=6, column=0)

        for widget in self.lb1.winfo_children() + self.lb2.winfo_children():
            widget.grid_configure(padx=10, pady=3)

        self.msg = Label(self, text='')
        self.msg.grid(row=7, column=0)

        self.redefinirbttn = Button(self, text='Redefinir', command=self.redefinir)
        self.redefinirbttn.grid(row=8, column=0, pady=5)

        self.voltar_pag = Button(self, text='Voltar', command=self.voltar, bg='red', fg='white')
        self.voltar_pag.grid(row=9, column=0)

        self.mainloop()

    def voltar(self):
        from UserPage import UserPage
        self.destroy()
        UserPage(self.matricula)

    def redefinir(self):
        senha_atual = self.entry_senha_atual.get()
        senha_nova = self.entry_senha_nova.get()
        if senha_nova != self.entry_confirm.get():
            self.msg.config(text='Senhas diferentes.')
            self.after(3000, lambda: self.msg.config(text=''))
        else:
            with open('usuarios.txt', 'rb') as arquivoDados:
                lista_usuarios = load(arquivoDados)
                for user in lista_usuarios:
                    if user.matricula == self.matricula and user.getSenha() == senha_atual:
                        user.setSenha(senha_nova)
                        break
                else:
                    self.msg.config(text='Senha atual incorreta.')
                    self.after(3000, lambda: self.msg.config(text=''))
                    return
            with open('usuarios.txt', 'wb') as arquivoDados:
                dump(lista_usuarios, arquivoDados)

            from LoginPage import LoginPage
            self.destroy()
            LoginPage()

#if __name__ == '__main__':
#    PasswPage(input())