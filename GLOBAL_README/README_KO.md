<a href="/README.md">📕 English</a> <a href="/GLOBAL_README/README_KO.md">📕 한국어</a>  
# dcinside-crawler
<p align="center"><img src="/GLOBAL_README/icon.png" alt="Dcinside crawler logo" height="200"></p>

dcinside-crawler는 <a href="https://www.dcinside.com/">디씨인사이드</a>를 대상으로한 웹 크롤러입니다.  
지인 경찰분이 <a href="https://www.dcinside.com/">디씨인사이드</a>를 대상으로한 크롤러가 필요하다고 부탁하여 개발하게 되었습니다.  

<img src="https://img.shields.io/badge/python%203.12.0-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="made with Python 3.12.0">  

---

## 필요 라이브러리
| 이름 | 버전 | 용도 |
|:---:|:---:|:---|
| BeautifulSoup | 4 | 웹 페이지 파싱 |  
| csv |  | CSV 파일 추출 |  
| datetime |  | 날짜 형식 지정 | 
| json |  | 설정 파일 파싱 |   
| random |  | 임의 연결 지연 시간 설정 |  
| requests |  | 웹 페이지 조회 |  
| sqlite3 | 3 | 데이터 관리 |  
| threading |  | 다중 스레드 설정 |  
| time |  | 대기 시간 설정 |  

---

## 사용 방법
### 0. 검색 대상 설정
<p align="center"><img src="/GLOBAL_README/00_config.png" alt="설정" height="200"></p>  
<ul>
  <li>크롤링을 수행 할 갤러리 ID를 json 파일의 key 값으로 하여, **search_target.json** 설정 파일을 본인의 사용 목적에 맞게 수정합니다.</li>
</ul>
<ol>
  <li>name: CSV 파일 추출시 갤러리 이름으로 출력됩니다.</li>
  <li>url: 콘솔 화면에 표시될 URL 입니다.</li>
  <li>keyword: 제목 혹은 본문에서 찾을 단어 모음입니다.</li>
  <li>is_mini_gallery: 미니 갤러리 여부를 지정합니다.</li>
  <li>search_start_date: 과거 게시글 크롤링 한계를 지정합니다.</li>
  <li>search_end_date: 게시글 크롤링 한계를 지정합니다.</li>
</ol>

### 1. 스크립트 실행
<p align="center"><img src="/GLOBAL_README/01_run.png" alt="python dc_crawler.py" height="200"></p>  
<ul>
  <li>python dc_crawler.py</li>
</ul>

### 2. 메뉴 선택
<p align="center"><img src="/GLOBAL_README/02_menu.png" alt="Menu" height="200"></p>  
<ol>
  <li>Show Search Targets: 검색 대상과 설정을 확인합니다.</li>
  <p align="center"><img src="/GLOBAL_README/03_show_targets.png" alt="Target list" height="150"></p>
  <li>Edit Search Targets: 검색 대상을 수정하거나 추가합니다.</li>
  <p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="150"></p>
  <li>Export CSV File: 데이터를 CSV 파일 포맷으로 출력합니다.</li>
  <p align="center"><img src="/GLOBAL_README/07_export_csv.png" alt="Export CSV" height="150"></p>
  <li>Exit Program: 프로그램을 안전하게 종료합니다.</li>
</ol>

### 3. 검색 대상 수정
<p align="center"><img src="/GLOBAL_README/04_edit_targets.png" alt="Edit target" height="200"></p>  
<ol>
  <li>Add Search Target Gallery: 새로운 검색 대상을 추가합니다.</li>
  <p align="center"><img src="/GLOBAL_README/05_add_targets.png" alt="Add target" height="150"></p>
  <li>Select specific gallery: 검색 대상을 수정합니다.</li>
  <p align="center"><img src="/GLOBAL_README/06_edit_settings.png" alt="Edit target" height="150"></p>
</ol>

---

## 업데이트
| 날짜 | 내용 | 설명 |
|:---:|:---:|:---|
| 2024. 05. 29. | 기능 추가 | 프로그램이 최초로 개발됨. |
