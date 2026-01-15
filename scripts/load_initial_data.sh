#!/bin/sh
set -e

echo "=== Django initial setup started ==="

# 1. Применяем миграции
echo "Running migrations..."
python src/manage.py migrate --noinput

# 2. Создание суперпользователя (если не существует)
echo "Checking superuser..."
python src/manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "1234"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

# 3. Проверка и загрузка initial данных
echo "Checking and loading initial data..."

# Самый надёжный способ получить чистое число
DATA_COUNT=$(python src/manage.py shell <<EOF 2>/dev/null | tail -n 1
from services.models import Category
print(Category.objects.count())
EOF
)

# Защита от пустой/битой переменной
if [ -z "$DATA_COUNT" ]; then
    DATA_COUNT=0
fi

if [ "$DATA_COUNT" -eq 0 ]; then
    echo "No initial data found → loading fixtures..."
    python src/manage.py loaddata fixtures/categories.json
    python src/manage.py loaddata fixtures/products.json
    python src/manage.py loaddata fixtures/packages.json
    python src/manage.py loaddata fixtures/additional_services.json
    python src/manage.py loaddata fixtures/faqs.json
    echo "→ Initial fixtures successfully loaded"
else
    echo "Initial data already exists ($DATA_COUNT categories), skipping fixtures."
fi

echo "=== Django initial setup finished ==="