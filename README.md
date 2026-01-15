# Agenda Cultural - Sistema de Gestão de Eventos

Este projeto é um sistema de gerenciamento de eventos culturais desenvolvido em Python utilizando **Panel** para a interface web e **PostgreSQL** para o banco de dados.

## 🚀 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

*   **Python 3.10+**
*   **PostgreSQL** (com um banco de dados criado, ex: `AgendaCultural`)
*   **Git**

## 🛠️ Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd conexao-bd/python
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Banco de Dados:**
    Crie um arquivo `.env` na pasta `python/` com as credenciais do seu banco de dados (ajuste conforme sua configuração):

    ```ini
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=AgendaCultural
    DB_USER=postgres
    DB_PASS=sua_senha
    ```

    > **Nota:** Certifique-se de que o banco de dados `AgendaCultural` (ou o nome que escolher) já exista no PostgreSQL. As tabelas serão criadas automaticamente pelo SQLAlchemy se não existirem (verifique o script de inicialização se necessário).

## ▶️ Como Executar

Para iniciar a aplicação web, execute o seguinte comando dentro da pasta `python/`:

```bash
panel serve GestaoCultural.ipynb --autoreload
```

A aplicação estará disponível em seu navegador, geralmente em: `http://localhost:5006/GestaoCultural`

## 🧪 Funcionalidades Principais

*   **Dashboard:** Visão geral de eventos por mês.
*   **Eventos:** Cadastro, edição, exclusão e consulta de eventos.
*   **Espaços:** Gerenciamento de locais dos eventos.
*   **Usuários:** (Admin) Gerenciamento de usuários e permissões.
*   **Relatórios:** Exportação de inscritos por categoria e local (PDF).
*   **Minha Conta:** Atualização de perfil e senha.

## 👤 Perfis de Acesso

*   **Visitante:** Visualiza eventos públicos.
*   **Comum:** Inscreve-se em eventos, avalia e denuncia.
*   **Gerente:** Gerencia eventos e espaços.
*   **Admin:** Acesso total ao sistema.
