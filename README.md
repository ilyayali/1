<h1 align="center">Hi there, I'm <a href="https://github.com/DenisKhudyakov/drf_course_paper" target="_blank">Denis</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Парсер всех товаров с кэшбэком с WB 🇷🇺</h3>


![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
	![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

<h3>Контекст</h3>
<p>В современном мире всем необходимы помощники, даже самые банальные, которые показывают погоду, не выходя из чата</p>
<p>В рамках учебного дипломного проекта реализован телеграмм бот который взаимодействует с API Weather</p>

	Установка и запуск:
		1) Установите Python и Poetry если они не установлены.
            https://www.python.org/
            https://python-poetry.org/docs/#installation
		2) Клонируйте репозиторий git@github.com:DenisKhudyakov/parser_wb.git
		3) Активируйте виртульное окружение командой "poetry shell"
		4) Установите пакеты командой "poetry install"
		5) Создайте вашего бота в телеграмм, получите токен и введите его в .env файл
		6) Запустите Celery Worker:
			celery -A tasks worker --loglevel=info
		7) Запустите Celery Beat:
			celery -A tasks beat --loglevel=info
		9) Запустите проект командой "python main.py"
		