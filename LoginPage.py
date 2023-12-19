from tkinter import *
from pickle import *

class LoginPage(Tk):
    def __init__(self):
        super().__init__()
        self.title("Log In")
        self.f1 = Frame(self)
        self.f1.grid(row=0, column=0, padx=100, pady=20)

        self.titulo = Label(self.f1, text="Login", font=["Arial", "10", "bold"])
        self.titulo.grid(row=1, column=0)

        self.f2 = LabelFrame(self, text='Informações do Usuário')
        self.f2.grid(row=1, column=0, padx=20)

        self.l1 = Label(self.f2, text="Matricula: ")
        self.l1.grid(row=2, column=0, padx=5, pady=5)
        self.entry_matricula = Entry(self.f2)
        self.entry_matricula.grid(row=3, column=0, padx=5, pady=5)

        self.l2 = Label(self.f2, text="Senha: ")
        self.l2.grid(row=4, column=0, padx=5, pady=5)
        self.entry_senha = Entry(self.f2, show='*')
        self.entry_senha.grid(row=5, column=0, padx=5, pady=5)

        self.visu = Button(self.f2, text='ver', command=self.ver_senha)
        self.visu.grid(row=5, column=1, padx=5, pady=5)

        self.f3 = Frame(self)
        self.f3.grid(row=2, column=0, pady=5)
        self.enviar = Button(self.f3, text='Acessar', bg='green', fg='white', command=self.pagina_acessada)
        self.enviar.grid(row=3, column=0)

        self.f4 = Frame(self)
        self.f4.grid(row=4, column=0)
        self.l3 = Label(self.f4, text='Ainda não tem uma conta?')
        self.l3.grid(row=4, column=0)
        self.criar = Button(self.f4, text='Criar', command=self.pagina_criar)
        self.criar.grid(row=4, column=1, pady=5)

        self.lalert = Label(self.f1, text='', fg='red')
        self.lalert.grid(row=6, column=0)

        self.mainloop()

    def ver_senha(self):
        if self.entry_senha["show"] == '*':
            self.entry_senha['show'] = ''
        else:
            self.entry_senha['show'] = '*'

    def pagina_acessada(self):
        matricula = self.entry_matricula.get()
        senha = self.entry_senha.get()
        try:
            with open("usuarios.txt", "rb") as arquivoDados:
                lista_usuarios = load(arquivoDados)
                for user in lista_usuarios:
                    if user.matricula == matricula and user.getSenha() == senha:
                        from MenuPage import MenuPage
                        self.destroy()
                        MenuPage(user.__class__.__name__, user.matricula)
                        break
                else:
                    self.lalert.config(text='Não foi possível logar, verifique se os dados estão corretos.')
                    self.after(5000, lambda: self.lalert.config(text=''))
        except EOFError:
            self.lalert.config(text='Não existem usuários.')
            self.after(5000, lambda: self.lalert.config(text=''))

    def pagina_criar(self):
        from SignupPage import SingupPage
        self.destroy()
        SingupPage()
        
if __name__ == '__main__':
    LoginPage()