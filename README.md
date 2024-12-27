# M2A Pointer

## Guia de Instalação

### 1. Pré-Requisitos

Antes de começar, verifique a instalação dos componentes a seguir:

- Python 3 instalado
- Um editor de código, como VS Code, PyCharm ou similar
- Repositório clonado

```cmd
git clone https://github.com/souzera/m2a_pointer.git
```

### 2. Instalando as dependências

Na raiz do projeto (`./`), crie e ative um ambiente virtual python

```cmd
py -m venv .venv
```

```cmd
.venv\Scripts\activate
```

Em seguida, instale as dependências do projetos com o comando a seguir

```cmd
pip install -r requirements.txt
```

### Inicializando Banco de Dados

O projeto, inicialmente, foi configurado utilizando `SQLite`, para alterar configurações de conexões com bancos de dados verificar o arquivo `core/settings.py`.

Com o banco de dados configurado, realize as `migrations` com o comando

```cmd
py manage.py migrate
```

Em seguida, crie um superusuario para ter acesso ao painel administrativo do `DJANGO FRAMEWORK`

```cmd
py manage.py createsuperuser
```
