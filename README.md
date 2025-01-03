# M2A Pointer

![Static Badge](https://img.shields.io/badge/python-blue)
![Static Badge](https://img.shields.io/badge/orm-django-3fb950)

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

O projeto, inicialmente, foi configurado utilizando `SQLite`, para alterar configurações de conexões com bancos de dados, verificar o arquivo `core/settings.py`.

Com o banco de dados configurado, realize as `migrations` com o comando

```cmd
py manage.py migrate
```

Em seguida, crie um superusuario para ter acesso ao painel administrativo do `DJANGO FRAMEWORK` com o comando a seguir, e forneça as informações solicitadas

```cmd
py manage.py createsuperuser
```

### Executar a aplicação
Execute a aplicação com o comando:
```bash
py manage.py runserver
```

Isso iniciará o servidor de desenvolvimento em http://localhost:8000. Você pode acessar esta URL no seu navegador para visualizar o aplicativo.

## Rotas da Aplicação

Para utilizar a aplicação o usuário tem acesso a algumas rotas, sendo necessário a realização de login para o funcionamento.

- **Homepage `/`** : Página inicial da aplicação, a qual o usuário pode utilizar para as primeiras interações com a aplicação
- **Register `register/`**: Página para o registro de novos usuário da aplicação
- **Register Empresa `empresa/register/`**: Página para o registro de novas empresas
- **Login `login/`**: Página de autenticação, a qual o usuário irá acessar as principais funcionalidades da aplicação
- **Dashboard `dashboard/`**: Página principal da aplicação que contém o registro dos pontos filtrados pelo funcionário(usuário)
- **Diario `empresa/diario/`**: Página que irá exibir os pontos de todos os funcionario da empresa filtrando pela data selecionada pelo usuário.

## Suporte e Dúvidas

### **Matheus Barbosa**

- Github: [souzera](https://github.com/souzera)
- Linkedin: [in/matheus-bsouza](https://www.linkedin.com/in/matheus-bsouza/)


