<a href="/README.md">📕 English</a> <a href="/GLOBAL_README/README_KR.md">📕 한국어</a><a href="/GLOBAL_README/README_JP.md">📕 日本語</a><a href="/GLOBAL_README/README_CN.md">📕 中文</a><a href="/GLOBAL_README/README_RU.md">📕 Pусский</a>  
# dcinside-crawler
<p align="center"><img src="/GLOBAL_README/icon.png" alt="Dcinside crawler logo" height="200"></p>

dcinside-crawler — программа для сбора веб-данных для <a href="https://www.dcinside.com/">dcinside</a>.  
Я разработал его по просьбе знакомого полицейского, которому нужен инструмент для сбора веб-данных с <a href="https://www.dcinside.com/">dcinside</a>.  

<img src="https://img.shields.io/badge/python%203.12.0-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="made with Python 3.12.0">  

---

## Необходимые библиотеки
| Имя | Версия | Описание |
|:---:|:---:|:---|
| BeautifulSoup | 4 | Для сканирования веб-страницы |  
| csv |  | Для экспорта файла CSV |  
| datetime |  | Для формата времени | 
| json |  | Для анализа файла конфигурации |   
| random |  | Для случайной задержки |  
| requests |  | Для сканирования веб-страницы |  
| sqlite3 | 3 | Для управления данными |  
| threading |  | Для многопоточности |  
| time |  | За задержку |  

---

## Как использовать
### 0. Настройка цели поиска
<p align="center"><img src="/GLOBAL_README/00_config.png" alt="configuration" height="200"></p>  
<ul>
  <li>Установите идентификатор галереи страницы, на которой будет происходить сбор данных, в качестве значения ключа файла json и измените файл конфигурации **search_target.json** в соответствии с вашими целями использования.</li>
</ul>
<ol>
  <li>name: При экспорте CSV оно выводится как имя галереи.</li>
  <li>url: Отображается на экране консоли.</li>
  <li>keyword: Набор слов, которые можно найти в заголовке или контексте.</li>
  <li>is_mini_gallery: Указывает, является ли это мини-галереей.</li>
  <li>search_start_date: Укажите лимит просмотра прошлых сообщений.</li>
  <li>search_end_date: Укажите лимит просмотра поста.</li>
</ol>

### 1. Запустить скрипт
<p align="center"><img src="/GLOBAL_README/01_run.png" alt="python dc_crawler.py" height="200"></p>  
<ul>
  <li>python dc_crawler.py</li>
</ul>

### 2. Выбрать меню
<p align="center"><img src="/GLOBAL_README/02_menu.png" alt="Menu" height="200"></p>  
<ol>
  <li>Show Search Targets: Показать цели и настройки поиска.</li>
  <p align="center"><img src="/GLOBAL_README/03_show_targets.png" alt="Target list" height="150"></p>
  <li>Edit Search Targets: Измените цели поиска или добавьте новую цель.</li>
  <p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="150"></p>
  <li>Export CSV File: Экспортируйте данные в формате csv.</li>
  <p align="center"><img src="/GLOBAL_README/07_export_csv.png" alt="Export CSV" height="150"></p>
  <li>Exit Program: Выйдите из программы безопасно.</li>
</ol>

### 3. Изменить цель
<p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="200"></p>  
<ol>
  <li>Add Search Target Gallery: Вы можете добавить новую цель.</li>
  <p align="center"><img src="/GLOBAL_README/05_add_targets.png" alt="Add target" height="150"></p>
  <li>Select specific gallery: Вы можете редактировать цель.</li>
  <p align="center"><img src="/GLOBAL_README/06_edit_settings.png" alt="Edit target" height="150"></p>
</ol>

---

## Обновлять
| Дата | Работа | Описание |
|:---:|:---:|:---|
| 2024. 05. 29. | ADD | Этот сценарий был написан. |
