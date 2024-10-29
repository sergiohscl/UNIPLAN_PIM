# Projeto Django (Universidade Uniplan)
## Objetivo do projeto e implementar site de clinicas médicas

<hr>

## Documentação do django
https://www.djangoproject.com/

## Instalando ambiente virtual
    python3 -m venv venv

## Ativando e desativando ambiente virtual
### Linux
    . venv/bin/activate
    deactivate

### Windows
    source venv\Scripts\Activate.ps1   # terminal powersheel        
    source venv\Scripts\Activate.bat   # terminal cmd

## Instalando django no ambiente virtual
    pip install django

## Iniciando project django
    django-admin startproject <nome-project> .

## Criar o arquivo requirements.txt
    pip freeze > requirements.txt

## Instale as dependências no projeto
    pip install -r requirements.txt

## Rodando django-admin
    python manage.py runserver

## Migrando a base de dados do Django
    python manage.py makemigrations
    python manage.py migrate

## Criando e modificando a senha de um super usuário
    python manage.py createsuperuser
    python manage.py changepassword USERNAME

## criando app
    python manage.py startapp <nomeapp>

## Configurar o git
    git config --global user.name 'Seu nome'
    git config --global user.email 'seu_email@gmail.com'
    git config --global init.defaultBranch main
    git init
    git add .
    git commit -m 'Mensagem'
    git remote add origin URL_DO_GIT

## Django-allauth
https://docs.allauth.org/en/latest/installation/quickstart.html

https://console.developers.google.com/

## Popular banco de dados
    ./manage.py shell
    from utils.<nome_arquivo> import <nome_função>
    <nome_função>(coloque argumento se existir)

    Obs.: senha para todos: Django13$

<hr>

# Configuração no admin para autenticação

### SITES (Sites)
    ADICIONAR SITE
    Nome do domínio: 127.0.0.1:8000
    Nome para Exibição: localhost

### CONTAS SOCIAIS (Aplicativos sociais)
    ADICIONAR APLICATIVO SOCIAL
    Provider: Google
    ID do provedor: django-auth-430317
    Nome: Goolge
    ID do cliente: 939291961852-j1u5sos2dagfuf1g838iffnp20sh7smc.apps.googleusercontent.com
    Chave secreta: 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
    Chave: não precisa(fica em branco)
    Settings: {}
    Sites: 127.0.0.1:8000(basta escolher e clicar na seta)

### colocar o id do sites no settings do django(core)
    SITE_ID = 15 (coloque conforme o id que foi gerado no seu projeto),(olhe na tabela django_site)

    instale a extensão SQLite Viewer para visualizar o banco de dados(db.sqlite3)

<hr>

# URL's do Projeto

## Home
    http://127.0.0.1:8000

### Sobre Nós
    http://127.0.0.1:8000/#about

### Especialidades
    http://127.0.0.1:8000/#departments

    NOSSAS ESPECIALIDADES
    http://127.0.0.1:8000/doctors/list_specialty/Neurologia/

### Medicos
    http://127.0.0.1:8000/patient/marcar_consulta/

    Ver Perfil
    http://127.0.0.1:8000/doctors/doctor/4/

### Contato
    http://127.0.0.1:8000/contact/

    Obs. E disparado um email para o usuario ao clicar em enviar.

### Login
    http://127.0.0.1:8000/auth/login/

    Criar Conta:
    http://127.0.0.1:8000/create_account/

    Esqueceu senha:
    http://127.0.0.1:8000/auth/password_reset/

    Autententicar com o Google:
    http://127.0.0.1:8000/accounts/google/login/

### Paciente Logado
    Marcar Consulta:
    http://127.0.0.1:8000/patient/marcar_consulta/

    Minhas Consultas:
    http://127.0.0.1:8000/patient/my_queries/

    Cancelar consulta:
    http://127.0.0.1:8000/patient/cancelar_consulta/<int:consulta_id>/

### Medico Logado
    Área do médico
        abrir horários:
        http://127.0.0.1:8000/doctors/open_schedule/

        Suas Consultas:
        http://127.0.0.1:8000/doctors/doctor_queries/

        Cancelar consulta:
        http://127.0.0.1:8000/doctors/cancelar_consulta_medico/<int:consulta_id>/

        Obs.: Quando o medico cancela a consulta  dispara um email avisando o usuario.

        Iniciar Cosnulta(clicar nome paciente):
            1. clicar no link do Google Meet(abrir video conferencia)
            2. Copia o link e cola no input.
            3. clicar botão Iniciar Consulta 

        http://127.0.0.1:8000/doctors/initialize_query/12/

        Obs.: E disparado um email com o link da sala para o paciente.

        O médico poderá enviar documentos para o paciente:
            1. Titiulo do documeto(Ex. Receita Media, Atestado Medido)
            2. Fazer o upload do arquivo
            3. clicar no botao + 

        http://127.0.0.1:8000/doctors/add_documento/12/

        Obs.: Disparado email para o paciente com os documentos medicos anexados.

        Finalizar Consulta:

        http://127.0.0.1:8000/doctors/finalizar_consulta/12/
