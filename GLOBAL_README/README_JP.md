<a href="/README.md">📕 English</a> <a href="/GLOBAL_README/README_KR.md">📕 한국어</a><a href="/GLOBAL_README/README_JP.md">📕 日本語</a><a href="/GLOBAL_README/README_CN.md">📕 中文</a><a href="/GLOBAL_README/README_RU.md">📕 Pусский</a>  
# dcinside-crawler
<p align="center"><img src="/GLOBAL_README/icon.png" alt="Dcinside crawler logo" height="200"></p>

dcinside-crawler は、<a href="https://www.dcinside.com/">dcinside</a> をターゲットとした Web クローラです  
知人の警察から<a href="https://www.dcinside.com/">dcinside</a>を対象にしたウェブクローラーが必要だと頼まれて開発することになりました。  

<img src="https://img.shields.io/badge/python%203.12.0-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="made with Python 3.12.0">  

---

## 必要ライブラリ
| 名前 | バージョン | 説明 |
|:---:|:---:|:---|
| BeautifulSoup | 4 | ウェブページをスクレイピングする場合 |  
| csv |  | CSVファイルのエクスポート |  
| datetime |  | 時刻形式 | 
| json |  | 解析設定ファイル用 |   
| random |  | ランダムディレイの場合 |  
| requests |  | ウェブページをスクレイピングする場合 |  
| sqlite3 | 3 | データ管理用 |  
| threading |  | マルチスレッド用 |  
| time |  | 遅延の場合 |  

---

## 使用方法
### 0. 検索対象設定
<p align="center"><img src="/GLOBAL_README/00_config.png" alt="configuration" height="200"></p>  
<ul>
  <li>データ収集が進むページのギャラリーIDをjsonファイルのkey値として、**search_target.json**設定ファイルを自分の使用目的に合わせて変更します。</li>
</ul>
<ol>
  <li>name: CSVエクスポート時はギャラリー名として出力されます。</li>
  <li>url: コンソール画面に表示されます。</li>
  <li>keyword: タイトルまたはコンテキストで検索する単語のコレクション。</li>
  <li>is_mini_gallery: ミニギャラリーかどうかを指定します。</li>
  <li>search_start_date: 過去の投稿検索制限を指定します。</li>
  <li>search_end_date: 投稿検索制限を指定します。</li>
</ol>

### 1. スクリプトを実行する
<p align="center"><img src="/GLOBAL_README/01_run.png" alt="python dc_crawler.py" height="200"></p>  
<ul>
  <li>python dc_crawler.py</li>
</ul>

### 2. メニューを選択
<p align="center"><img src="/GLOBAL_README/02_menu.png" alt="Menu" height="200"></p>  
<ol>
  <li>Show Search Targets: 検索対象と設定を表示します。</li>
  <p align="center"><img src="/GLOBAL_README/03_show_targets.png" alt="Target list" height="150"></p>
  <li>Edit Search Targets: 検索ターゲットを編集するか、新しいターゲットを追加します。</li>
  <p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="150"></p>
  <li>Export CSV File: データを csv 形式でエクスポートします。</li>
  <p align="center"><img src="/GLOBAL_README/07_export_csv.png" alt="Export CSV" height="150"></p>
  <li>Exit Program: プログラムを安全に終了します。</li>
</ol>

### 3. ターゲットを編集
<p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="200"></p>  
<ol>
  <li>Add Search Target Gallery: 新しいターゲットを追加できます。</li>
  <p align="center"><img src="/GLOBAL_README/05_add_targets.png" alt="Add target" height="150"></p>
  <li>Select specific gallery: ターゲットを編集できます。</li>
  <p align="center"><img src="/GLOBAL_README/06_edit_settings.png" alt="Edit target" height="150"></p>
</ol>

---

## アップデート
| 日付 | 仕事 | 説明 |
|:---:|:---:|:---|
| 2024. 05. 29. | ADD | このスクリプトは書かれました。 |
