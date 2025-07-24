#!/bin/bash

echo "🔧 Обновляем систему..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Устанавливаем зависимости..."
sudo apt install -y python3 python3-pip python3-venv git libxml2-dev libxslt1-dev build-essential libpq-dev redis postgresql postgresql-contrib

echo "📦 Создаём виртуальное окружение..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Клонируем eScriptorium..."
git clone https://github.com/HTR-United/escriptorium.git
cd escriptorium

echo "⚙️ Устанавливаем Python-зависимости..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗃️ Настраиваем базу данных PostgreSQL..."
sudo -u postgres createuser escriptorium_user
sudo -u postgres createdb escriptorium_db -O escriptorium_user
sudo -u postgres psql -c "ALTER USER escriptorium_user WITH PASSWORD 'password';"

echo "🔐 Копируем .env файл и настраиваем..."
cp .env.template .env
sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://escriptorium_user:password@localhost:5432/escriptorium_db|" .env

echo "📚 Применяем миграции..."
python manage.py migrate

echo "✅ Установка завершена!"
echo "👤 Теперь создайте суперпользователя:"
echo "👉 Выполните вручную следующие команды:"
echo "   source ~/htr_project/venv/bin/activate"
echo "   cd ~/htr_project/escriptorium"
echo "   python manage.py createsuperuser"
echo "   python manage.py runserver"

