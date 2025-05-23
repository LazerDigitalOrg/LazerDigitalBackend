# Задаем путь к проекту
$projectPath = "C:\Users\George\PycharmProjects\LazerDigital"

# Переходим в директорию проекта
Set-Location -Path $projectPath

# Останавливаем контейнеры Docker
docker-compose down -v

# Ждем 2 секунды
Start-Sleep -Seconds 2

# Запускаем контейнеры в фоне
docker-compose up -d

# Ждем 2 секунды
Start-Sleep -Seconds 2


. "$projectPath\venv\Scripts\activate"

# Устанавливаем PYTHONPATH
$env:PYTHONPATH = $projectPath

# Запускаем Python-скрипты
python "$projectPath\src\database\models.py"
python "$projectPath\src\insert_data.py"
python "$projectPath\src\main.py"