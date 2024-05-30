<a href="/README.md">📕 English</a> <a href="/GLOBAL_README/README_KR.md">📕 한국어</a><a href="/GLOBAL_README/README_JP.md">📕 日本語</a><a href="/GLOBAL_README/README_CN.md">📕 中文</a><a href="/GLOBAL_README/README_RU.md">📕 Pусский</a>  
# dcinside-crawler
<p align="center"><img src="/GLOBAL_README/icon.png" alt="Dcinside crawler logo" height="200"></p>

dcinside-crawler是针对<a href="https://www.dcinside.com/">dcinside</a>的网页信息收集工具。  
熟人警察要求需要以<a href="https://www.dcinside.com/">dcinside</a>为对象的网络数据收集工具，所以开发了。  

<img src="https://img.shields.io/badge/python%203.12.0-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="made with Python 3.12.0">  

---

## 所需的库
| 姓名 | 版本 | 描述 |
|:---:|:---:|:---|
| BeautifulSoup | 4 | 用于抓取网页 |  
| csv |  | 对于 CSV 文件导出 |  
| datetime |  | 对于时间格式 | 
| json |  | 用于解析配置文件 |   
| random |  | 对于随机延迟 |  
| requests |  | 用于抓取网页 |  
| sqlite3 | 3 | 对于数据管理 |  
| threading |  | 对于多线程 |  
| time |  | 为了延迟 |  

---

## 如何使用
### 0. 搜索目标设定
<p align="center"><img src="/GLOBAL_README/00_config.png" alt="configuration" height="200"></p>  
<ul>
  <li>将要采集数据的页面的gallery ID设置为json文件的键值，并修改**search_target.json**配置文件以适合您的使用目的。</li>
</ul>
<ol>
  <li>name: 导出 CSV 时，以画廊名称输出。</li>
  <li>url: 显示在控制台屏幕上。</li>
  <li>keyword: 要在标题或上下文中查找的单词集合。</li>
  <li>is_mini_gallery: 指定它是否是一个迷你画廊。</li>
  <li>search_start_date: 指定查看过去帖子的限制。</li>
  <li>search_end_date: 指定帖子查看限制。</li>
</ol>

### 1. 运行脚本
<p align="center"><img src="/GLOBAL_README/01_run.png" alt="python dc_crawler.py" height="200"></p>  
<ul>
  <li>python dc_crawler.py</li>
</ul>

### 2. 选择菜单
<p align="center"><img src="/GLOBAL_README/02_menu.png" alt="Menu" height="200"></p>  
<ol>
  <li>Show Search Targets: 显示搜索目标和设置。</li>
  <p align="center"><img src="/GLOBAL_README/03_show_targets.png" alt="Target list" height="150"></p>
  <li>Edit Search Targets: 编辑搜索目标或添加新目标。</li>
  <p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="150"></p>
  <li>Export CSV File: 将数据导出为 csv 格式。</li>
  <p align="center"><img src="/GLOBAL_README/07_export_csv.png" alt="Export CSV" height="150"></p>
  <li>Exit Program: 安全退出程序。</li>
</ol>

### 3. 编辑目标
<p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="200"></p>  
<ol>
  <li>Add Search Target Gallery: 您可以添加新的目标。</li>
  <p align="center"><img src="/GLOBAL_README/05_add_targets.png" alt="Add target" height="150"></p>
  <li>Select specific gallery: 您可以编辑目标。</li>
  <p align="center"><img src="/GLOBAL_README/06_edit_settings.png" alt="Edit target" height="150"></p>
</ol>

---

## 更新
| 日期 | 工作 | 描述 |
|:---:|:---:|:---|
| 2024. 05. 29. | ADD | 这个脚本就写好了。 |
