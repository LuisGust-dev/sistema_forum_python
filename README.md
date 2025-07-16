# sistema_forum_python
Projeto Feito em Python 

## 📌 Objetivo do Projeto

Este projeto tem como objetivo desenvolver um sistema empresarial completo para empresas médicas corporativas. Ele oferece funcionalidades como:

- Autenticação customizada com permissões de acesso
- Dashboard administrativo
- Fórum de postagens e comentários
- Gerenciamento de usuários com aprovação via e-mail
- Perfil de usuário e páginas dinâmicas


---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.10+
- Git
- Virtualenv (ou venv)
### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/LuisGust-dev/sistema_forum_python.git
cd sistema_forum_python

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
