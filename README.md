<a href="/README.md">📕 English</a> <a href="/GLOBAL_README/README_KO.md">📕 한국어</a>  
# dcinside-crawler
<p align="center"><img src="/GLOBAL_README/icon.png" alt="Dcinside crawler logo" height="350"></p>

dcinside-crawler is a web crawler that targeted <a href="https://www.dcinside.com/">dcinside</a>.  
Created this because a police officer I know said he needed a web crawler for the <a href="https://www.dcinside.com/">dcinside</a>.  

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="made with Python 3.12.0">  

---

## Requires
| Name | Version | Description |
|:---:|:---:|:---|
| BeautifulSoup | 4 | For scrap web page |  
| csv |  | For CSV file export |  
| datetime |  | For time format | 
| json |  | For parse config file |   
| random |  | For random delay |  
| requests |  | For scrap web page |  
| sqlite3 | 3 | For data management |  
| threading |  | For multi threading |  
| time |  | For sleep |  

---

## Usage
### 0. Search target setting
<p align="center"><img src="/GLOBAL_README/00_config.png" alt="configuration" height="350"></p>  
<ul>
  <li>Set the gallery ID to be crawled as the key value of the json file, and modify the **search_target.json** configuration file to suit your purpose of use.</li>
</ul>
<ol>
  <li>name: When export CSV, it is output as the gallery name.</li>
  <li>url: Displayed on the console screen.</li>
  <li>keyword: A collection of words to find in the title or context.</li>
  <li>is_mini_gallery: Specifies whether to have a mini gallery.</li>
  <li>search_start_date: Specifies a limit for crawling past posts.</li>
  <li>search_end_date: Specifies a limit for crawling posts.</li>
</ol>

### 1. Run script
<p align="center"><img src="/GLOBAL_README/01_run.png" alt="python dc_crawler.py" height="350"></p>  
<ul>
  <li>python dc_crawler.py</li>
</ul>

### 2. Select menu
<p align="center"><img src="/GLOBAL_README/02_menu.png" alt="Menu" height="350"></p>  
<ol>
  <li><p align="center"><img src="/GLOBAL_README/03_show_targets.png" alt="Target list" height="350"></p>Show Search Targets: Show search targets and settings.</li>
  <li><p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="350"></p>Edit Search Targets: Edit search targets or add new target.</li>
  <li><p align="center"><img src="/GLOBAL_README/07_export_csv.png" alt="Export CSV" height="350"></p>Export CSV File: Export data as csv format.</li>
  <li>Exit Program: Exit program safely.</li>
</ol>

### 3. Edit target
<p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="350"></p>  
<ol>
  <li><p align="center"><img src="/GLOBAL_README/05_add_targets.png" alt="Add target" height="350"></p>Add Search Target Gallery: You can add new target.</li>
  <li><p align="center"><img src="/GLOBAL_README/06_edit_settings.png" alt="Edit target" height="350"></p>Select specific gallery: You can edit target.</li>
</ol>

---

## Update
| Date | Work | Description |
|:---:|:---:|:---|
| 2024. 05. 29. | ADD | This script was written. |
