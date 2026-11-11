#!/bin/bash
# ====================================================================
# Script de Despliegue Automatizado para Dulce Arte en AWS EC2 (Ubuntu 22.04 / 24.04)
# ====================================================================
set -e

echo ">>> 1. Actualizando paquetes del sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo ">>> 2. Instalando dependencias (Python, PostgreSQL, Nginx, Git)..."
sudo apt-get install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git libpq-dev

echo ">>> 3. Configurando Base de Datos PostgreSQL..."
sudo -u postgres psql <<EOF
DO \$\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dulce_arte_user') THEN
      CREATE ROLE dulce_arte_user WITH LOGIN PASSWORD 'dulce_arte_pass_2026';
   END IF;
END
\$\$;
SELECT 'CREATE DATABASE dulce_arte_db OWNER dulce_arte_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dulce_arte_db')\gexec
GRANT ALL PRIVILEGES ON DATABASE dulce_arte_db TO dulce_arte_user;
ALTER USER dulce_arte_user CREATEDB;
EOF

echo ">>> 4. Preparando entorno de la aplicación..."
cd /home/ubuntu
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Clonar o actualizar repositorio si aplica, o usar la carpeta existente
APP_DIR="/home/ubuntu/dulce_arte"
cd \$APP_DIR

pip install --upgrade pip
pip install -r requirements.txt

echo ">>> 5. Aplicando migraciones y recolectando estáticos..."
export DB_NAME="dulce_arte_db"
export DB_USER="dulce_arte_user"
export DB_PASSWORD="dulce_arte_pass_2026"
export DB_HOST="localhost"
export DB_PORT="5432"

python manage.py makemigrations pedidos inventario cocina despacho cuentas
python manage.py migrate
python manage.py collectstatic --noinput
python datos_iniciales.py

echo ">>> 6. Configurando Gunicorn como servicio systemd..."
sudo tee /etc/systemd/system/dulce_arte.service > /dev/null <<EOF
[Unit]
Description=Gunicorn daemon para Dulce Arte
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/dulce_arte
Environment="PATH=/home/ubuntu/venv/bin"
Environment="DB_NAME=dulce_arte_db"
Environment="DB_USER=dulce_arte_user"
Environment="DB_PASSWORD=dulce_arte_pass_2026"
Environment="DB_HOST=localhost"
Environment="DB_PORT=5432"
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 dulce_arte.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dulce_arte
sudo systemctl restart dulce_arte

echo ">>> 7. Configurando Nginx como Proxy Inverso..."
sudo tee /etc/nginx/sites-available/dulce_arte > /dev/null <<EOF
server {
    listen 80 default_server;
    server_name _;

    client_max_body_size 20M;

    location /static/ {
        alias /home/ubuntu/dulce_arte/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/dulce_arte/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/dulce_arte /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

PUBLIC_IP=\$(curl -s http://checkip.amazonaws.com || curl -s ifconfig.me || echo "tu-ip-publica")

echo "===================================================================="
echo "✅ DESPLIEGUE EN AWS EC2 COMPLETADO EXITOSAMENTE"
echo "Accede a la aplicación en: http://\$PUBLIC_IP/"
echo "Admin de Django en:        http://\$PUBLIC_IP/admin/"
echo "Usuario administrador:     admin / admin123"
echo "===================================================================="
