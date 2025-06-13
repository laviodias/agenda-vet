#!/bin/bash

# Script para gerenciar a aplicação AgendaVet no Docker

case "$1" in
    "start")
        echo "🚀 Iniciando AgendaVet..."
        docker-compose up -d
        echo "✅ AgendaVet iniciado!"
        echo "📱 Frontend: http://localhost:8080"
        echo "🔧 API: http://localhost:8000"
        echo "📊 Admin Django: http://localhost:8000/admin"
        ;;
    
    "stop")
        echo "🛑 Parando AgendaVet..."
        docker-compose down
        echo "✅ AgendaVet parado!"
        ;;
    
    "restart")
        echo "🔄 Reiniciando AgendaVet..."
        docker-compose down
        docker-compose up -d
        echo "✅ AgendaVet reiniciado!"
        ;;
    
    "build")
        echo "🔨 Construindo containers..."
        docker-compose build --no-cache
        echo "✅ Containers construídos!"
        ;;
    
    "logs")
        echo "📋 Mostrando logs..."
        docker-compose logs -f
        ;;
    
    "logs-api")
        echo "📋 Logs da API..."
        docker-compose logs -f api
        ;;
    
    "logs-web")
        echo "📋 Logs do Frontend..."
        docker-compose logs -f web
        ;;
    
    "logs-db")
        echo "📋 Logs do Banco de Dados..."
        docker-compose logs -f db
        ;;
    
    "shell-api")
        echo "🐚 Abrindo shell da API..."
        docker-compose exec api bash
        ;;
    
    "shell-web")
        echo "🐚 Abrindo shell do Frontend..."
        docker-compose exec web sh
        ;;
    
    "shell-db")
        echo "🐚 Abrindo shell do Banco de Dados..."
        docker-compose exec db psql -U agendavet_user -d agendavet_db
        ;;
    
    "migrate")
        echo "🔄 Executando migrações..."
        docker-compose exec api python manage.py makemigrations
        docker-compose exec api python manage.py migrate
        echo "✅ Migrações executadas!"
        ;;
    
    "setup-data")
        echo "📊 Configurando dados iniciais..."
        docker-compose exec api python manage.py setup_initial_data
        echo "✅ Dados iniciais configurados!"
        ;;
    
    "clean")
        echo "🧹 Limpando containers e volumes..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Limpeza concluída!"
        ;;
    
    "status")
        echo "📊 Status dos containers..."
        docker-compose ps
        ;;
    
    *)
        echo "🤖 AgendaVet Docker Manager"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start       - Iniciar aplicação"
        echo "  stop        - Parar aplicação"
        echo "  restart     - Reiniciar aplicação"
        echo "  build       - Construir containers"
        echo "  logs        - Ver logs de todos os serviços"
        echo "  logs-api    - Ver logs da API"
        echo "  logs-web    - Ver logs do Frontend"
        echo "  logs-db     - Ver logs do Banco de Dados"
        echo "  shell-api   - Abrir shell da API"
        echo "  shell-web   - Abrir shell do Frontend"
        echo "  shell-db    - Abrir shell do Banco de Dados"
        echo "  migrate     - Executar migrações"
        echo "  setup-data  - Configurar dados iniciais"
        echo "  clean       - Limpar containers e volumes"
        echo "  status      - Ver status dos containers"
        echo ""
        echo "Exemplo: ./docker-commands.sh start"
        ;;
esac 