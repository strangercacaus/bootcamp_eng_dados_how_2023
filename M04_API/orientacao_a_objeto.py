#%%

import datetime
import math

class pessoa:
    def __init__(self,
                 nome: str,
                 sobrenome: str,
                 data_de_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome} tem {self.idade} anos.'
    
class curriculo:
    def __init__(self,
                 pessoa:pessoa,
                 experiencias:list[str]):
        self.experiencias = experiencias
        self.pessoa = pessoa
        self.experiencias = experiencias

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]
    
    def adiciona_experienca(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self):
        return f'{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos, já trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha na empresa {self.empresa_atual}'


class vivente:
    def __init__(self, nome: str, d)
#%%

caue = pessoa(nome='Cauê',
              sobrenome='Marchionatti Ausec',
              data_de_nascimento= datetime.date(1997,1,17))

curriculo_caue = curriculo(pessoa=caue,
                           experiencias=['Moskit','Intexfy','Aurum Software'])

#%%

print(curriculo_caue)
print(curriculo_caue.experiencias)

#%%

curriculo_caue.adiciona_experienca(experiencia='Intercom')
print(curriculo_caue)

