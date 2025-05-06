# Agenda Vet - Projeto de Agendamento Veterinário

Este projeto consiste em uma API Django para gerenciar agendamentos veterinários e um frontend Vue.js para a interface do usuário. Ele utiliza Docker para facilitar a configuração e execução do ambiente de desenvolvimento.

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

* **Docker:** Para containerizar e gerenciar os serviços da aplicação. Você pode instalá-lo seguindo as instruções em [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).
* **Docker Compose:** Geralmente instalado junto com o Docker Desktop. Se você instalou o Docker Engine separadamente, pode precisar instalar o Docker Compose seguindo as instruções em [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/).
* **Node.js e npm (ou yarn):** Necessários para executar o servidor de desenvolvimento do frontend Vue.js localmente (opcional, se você optar por rodar o frontend via Docker também). Você pode instalá-los em [https://nodejs.org/](https://nodejs.org/).

## Instruções para Rodar o Projeto

Existem duas formas principais de rodar o projeto para desenvolvimento: rodando o frontend localmente e o backend com Docker, ou rodando ambos (frontend e backend) com Docker.

### Opção 1: Backend com Docker e Frontend Localmente (Recomendado para desenvolvimento)

Esta opção permite aproveitar o hot-reloading do Vite para o frontend, tornando o desenvolvimento mais rápido.

1.  **Clone o repositório do projeto:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd agenda-vet
    ```

2.  **Configure as variáveis de ambiente (opcional):**
    ```bash
    cp .env.example .env
    ```

3.  **Inicie os serviços do backend (Django API e PostgreSQL):**
    ```bash
    docker-compose up -d db api
    ```
    Isso irá construir as imagens Docker (se necessário) e iniciar os containers para o banco de dados PostgreSQL (`db`) e a API Django (`api`) em segundo plano.

4.  **Acesse a API Django:**
    A API Django estará disponível em `http://localhost:8000`.

5.  **Inicie o servidor de desenvolvimento do frontend Vue.js localmente:**
    Navegue até a pasta `web` no seu terminal:
    ```bash
    cd web
    ```
    Instale as dependências:
    ```bash
    npm install  # ou yarn install
    ```
    Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev  # ou yarn dev
    ```
    O frontend estará geralmente disponível em `http://localhost:5173`. Certifique-se de que a variável de ambiente `VUE_APP_API_BASE_URL` no seu frontend (`.env.development` ou outro arquivo de configuração) esteja apontando para `http://localhost:8000`.

### Opção 2: Backend e Frontend com Docker

Esta opção roda todo o projeto dentro de containers Docker.

1.  **Clone o repositório do projeto:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd agenda-vet
    ```

2.  **Configure as variáveis de ambiente (opcional):**
    Se você tiver um arquivo `.env` na raiz do projeto com configurações de banco de dados, o Docker Compose irá carregá-las automaticamente.

3.  **Inicie todos os serviços (backend, frontend e banco de dados):**
    ```bash
    docker-compose up -d --build
    ```
    Isso irá construir as imagens Docker (se necessário) e iniciar os containers para o banco de dados PostgreSQL (`db`), a API Django (`api`) e o frontend Vue.js (`web`) em segundo plano.

4.  **Acesse o Frontend:**
    O frontend estará disponível em `http://localhost:8080` (conforme configurado no `docker-compose.yml`).

5.  **Acesse a API Django:**
    A API Django estará disponível em `http://localhost:8000`.

### Executando as Migrações do Django

Após iniciar os serviços do backend pela primeira vez, você precisará executar as migrations do Django para criar as tabelas do banco de dados com base nos seus modelos definidos.

1.  **Encontre o ID do container da API Django:**
    ```bash
    docker ps
    ```
    Procure pelo serviço chamado `api` e copie o seu `CONTAINER ID`.

2.  **Execute o comando `makemigrations` para criar os arquivos de migração (se você fez alterações nos modelos):**
    ```bash
    docker exec -it <ID_DO_CONTAINER_API> python manage.py makemigrations
    ```
    Se você criou novas apps, pode especificar o nome da app:
    ```bash
    docker exec -it <ID_DO_CONTAINER_API> python manage.py makemigrations <nome_da_app>
    ```
    Ou para todas as apps:
    ```bash
    docker exec -it <ID_DO_CONTAINER_API> python manage.py makemigrations
    ```

3.  **Execute o comando `migrate` para aplicar as migrations e criar as tabelas no banco de dados:**
    ```bash
    docker exec -it <ID_DO_CONTAINER_API> python manage.py migrate
    ```

Esses comandos garantem que o esquema do seu banco de dados esteja sincronizado com as definições dos seus modelos Django. Você precisará executar `makemigrations` sempre que fizer alterações nos seus modelos e, em seguida, executar `migrate` para aplicar essas alterações ao banco de dados.

## Comandos Úteis do Docker Compose

* **Listar os containers em execução:**
    ```bash
    docker-compose ps
    ```
* **Ver os logs de um serviço:**
    ```bash
    docker-compose logs <nome_do_servico>
    ```
    Exemplo: `docker-compose logs api` ou `docker-compose logs web`
* **Parar os serviços:**
    ```bash
    docker-compose down
    ```
* **Parar e remover os containers, redes e volumes:**
    ```bash
    docker-compose down -v
    ```
* **Reconstruir as imagens (útil após fazer alterações nos Dockerfiles):**
    ```bash
    docker-compose build
    ```
    Para reconstruir uma imagem específica sem usar o cache:
    ```bash
    docker-compose build --no-cache <nome_do_servico>
    ```

## Configuração Adicional

* Você pode configurar variáveis de ambiente para o banco de dados e outras configurações no arquivo `.env` na raiz do projeto.
* As configurações específicas do Django estão no arquivo `api/agenda_vet_api/settings.py`.
* As configurações específicas do Vue.js estão na pasta `web` (arquivos como `.env.development`, `vite.config.js`, etc.).

Sinta-se à vontade para explorar o código e contribuir para o projeto!