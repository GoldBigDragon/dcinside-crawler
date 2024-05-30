# -*- coding: utf-8 -*-
"""
Created: 2024-05-29
Purpose: Web crawler for dcinside.com
Reason: I created this because a police officer I know said he needed a web crawler for the Korean community site(https://gall.dcinside.com/).
Author: GoldBigDragon
Github: https://goldbigdragon.github.io/
"""
import threading
import time
import random
import json
import requests
import sqlite3
import datetime
import csv 
from bs4 import BeautifulSoup

global LANGUAGE
global STOP_PROGRAM
global POST_BUFFER
global POST_MUTEX
global DB_MUTEX
global KEYWORD
global START_DATE
global END_DATE
global HEADERS
global GALLERY_ID_AND_SETTINGS

# You can fix headers
HEADERS = {
    "Connection" : "keep-alive",
    "Cache-Control" : "max-age=0",
    "sec-ch-ua-mobile" : "?0",
    "DNT" : "1",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site" : "none",
    "Sec-Fetch-Mode" : "navigate",
    "Sec-Fetch-User" : "?1",
    "Sec-Fetch-Dest" : "document",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "ko-KR,ko;q=0.9",
    "Referer": "https://gall.dcinside.com/"
}

SELECTED_LANGUAGE = "en"

# Various settings are stored using the gallery ID value as the key
GALLERY_ID_AND_SETTINGS = {}

# Post ID check variable to avoid repeated views
LATEST_POST_ID = {}
FIRST_POST_ID = {}

# Next page number
NEXT_PAGE = {}

# All pages have already been viewed
ROLL_BACK = []

# Data storage buffer until saved to sqlite db
POST_BUFFER = {}
CONTEXT_BUFFER = {}

# Multi threading mutex
POST_MUTEX = threading.Lock()
CONTEXT_MUTEX = threading.Lock()
DB_MUTEX = threading.Lock()

# Safely flush buffers and exit
STOP_PROGRAM = True

# They told me to make this portable,
# (They wanted single Python script.)
# so I erased the /res folder
# and just stuck a language file inside. LOL
LANGUAGE = {
	"en":{
        "SAVE_POST_INIT": "[！] Starting database recording thread...",
        "SAVE_POST_EXIT": "[！] Stopping database recording thread...",
        "CREATE_DB_INIT": "[！] Creating database...",
        "CREATE_DB_SUCCESS": "[○] Database created successfully!",
        "CREATE_DB_FAILED": "[×] Failed to create database!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID": "1. Enter the gallery ID. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST": "[！] Gallery ID already exists!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME": "2. Enter the gallery name. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT": "[！] The name must be at least 1 character long!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG": "[！] The name cannot exceed 16 characters!",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS": "3. List the collection keywords separated by commas. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT": "[！] At least one collection target must be registered!",
        "ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY": "4. Is this gallery a mini-gallery? (y/N) > ",
        "CHANGE_START_DATE_AND_END_DATE": "[！] The start date is entered as a future date compared to the end date, so both settings have been changed!",
        "SET_GALLERY_SEARCH_DATE_START_DATE": "Start Date",
        "SET_GALLERY_SEARCH_DATE_END_DATE": "End Date",
        "SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE": "Enter the search {date_string} for {name}. (yyyy-mm-dd) > ",
        "SET_GALLERY_SEARCH_DATE_SUCCESS": "[○] Search {date_string} has been changed!",
        "SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT": "[！] The search {date_string} should be in the format 1995-05-19!",
        "SET_GALLERY_IS_MINI_TYPE_YES_OR_NO": "Is {name} a mini-gallery? (Y/n) > ",
        "SET_GALLERY_IS_MINI_SUCCESS": "[○] Mini-gallery status has been changed!",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS": "List the collection keywords for {name} separated by commas. > ",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS": "[○] Collection keywords have been changed！",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT": "[！] At least one collection target must be registered!",
        "SET_GALLERY_URL_TYPE_URL": "Enter the URL for {name}. > ",
        "SET_GALLERY_URL_TYPE_URL_SUCCESS": "[○] URL of the collection target has been changed!",
        "SET_GALLERY_URL_REMOVE_URL_SUCCESS": "[○] URL of the collection target has been removed!",
        "SET_GALLERY_NAME_TYPE_NAME": "Enter the new name for {name}. > ",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT": "[！] The name must be at least 1 character long!",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG": "[！] The name cannot exceed 16 characters!",
        "SET_GALLERY_NAME_TYPE_NAME_SUCCESS": "[○] Name of the collection target has been changed！",
        "SELECT_EDIT_PARAMETER_CONTEXT": "\n┌───────────[Edit Items]───────────┐\n├ 1. Name ({name})\n├ 2. URL ({url})\n├ 3. Collection Keywords ({keyword})\n├ 4. Mini Gallery Status ({is_mini_gallery})\n├ 5. Search Start Date ({search_start_date})\n├ 6. Search End Date ({search_end_date})\n├ 7. Remove\n├ 8. Back\n└───────────[Edit Items]───────────┘",
        "SELECT_EDIT_PARAMETER_QUESTION": "Which item of {gallery_id} ({name}) do you want to modify? > ",
        "SELECT_EDIT_PARAMETER_DELETE_QUESTION": "Do you want to remove {gallery_id} ({name}) from the search targets? (y/N) > ",
        "SELECT_EDIT_PARAMETER_DELETE_SUCCESS": "[！] {gallery_id} ({name}) has been removed from the search targets!",
        "SELECT_EDIT_TARGET_CONTEXT_1": "\n┌───────────[Edit Search Targets]───────────┐",
        "SELECT_EDIT_TARGET_CONTEXT_2": "├ {index}. {gallery_id} ({name})",
        "SELECT_EDIT_TARGET_CONTEXT_3": "├ {add_index}. Add Search Target Gallery\n├ {exit_index}. Back\n└───────────[Edit Search Targets]───────────┘",
        "SELECT_EDIT_TARGET_QUESTION": "Select the target to edit. > ",
        "SELECT_EDIT_TARGET_ERROR_NOT_EXIST": "[！] The edit target cannot be found!",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_1": "\n┌───────────[Search Targets]───────────┐",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_2": "├┬ {name} ({url})\n│├ Collection Keywords: {keyword}\n│└ Search Range: {search_start_date} ~ {search_end_date}",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_3": "└───────────[Search Targes]───────────┘\n",
        "PRINT_MENU": "\n┌────────────────────────────────┐\n├ 1. Show Search Targets\n├ 2. Edit Search Targets\n├ 3. Export CSV File\n├ 4. Exit Program\n└────────────────────────────────┘",
        "SEARCH_GALLERY_THREAD_INIT": "[！] Starting post search thread...",
        "READ_POST_THREAD_INIT": "[！] Starting post reading thread...",
        "EXPORT_CSV_FIELDS": ["Gallery ID","Gallery Name","Post ID","URL","Title","Author","IP","Date","Keywords Found in Title", "Keywords Found in Post", "Number of Keywords Found in Title", "Number of Keywords Found in Post", "Total Number of Keywords Found"],
        "EXPORT_CSV_SUCCESS": "[○] CSV file has been created！ ({filename})",
        "CONVERT_DB_TO_CSV_CONTEXT": "\n┌───────────[Export CSV]───────────┐\n├ 1. All Data\n├ 2. Data with at least 1 matching keyword\n├ 3. Back\n└───────────[Export CSV]───────────┘",
        "CONVERT_DB_TO_CSV_QUESTION": "What data would you like to export? > ",
        "READ_SEARCH_TARGET_INIT": "[！] Loading search targets from ./search_target.json file...",
        "READ_SEARCH_TARGET_SUCCESS": "[○] Search targets have been registered from the ./search_target.json file! ({gallery_id} - {name})",
        "READ_SEARCH_TARGET_FAILED": "[×] Failed to load search targets from the ./search_target.json file!",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_1": "[！] Example search target has been added！ (policeofficer - Police Officer Gallery)",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_2": "[！] Example search target has been added！ (gong - Current Civil Servant Gallery)",
        "SAVE_POST_SUCCESS": "[○] Database recording thread completed!",
        "SEARCH_GALLERY_THREAD_SUCCESS": "[○] Post search thread completed!",
        "READ_POST_THREAD_SUCCESS": "[○] Post reading thread completed!",
        "DAEMON_IS_RUNNING": "(Web crawler is ongoing in the background)",
        "MAIN_TYPE_MENU": "Please input your desired action. > ",
        "MAIN_EXIT_PROGRAM": "[！] Stopping the program safely!"
	},
	"kr":{
		"SAVE_POST_INIT": "[！] 데이터베이스 기록 스레드 구동 중...",
		"SAVE_POST_EXIT": "[！] 데이터베이스 기록 스레드 종료 중...",
		"CREATE_DB_INIT": "[！] 데이터베이스 생성 중...",
		"CREATE_DB_SUCCESS": "[○] 데이터베이스 생성 완료!",
		"CREATE_DB_FAILED": "[×] 데이터베이스 생성 실패!",
		"ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID": "1. 갤러리 ID를 입력하세요. > ",
		"ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST": "[！] 이미 등록된 갤러리ID입니다!",
		"ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME": "2. 갤러리 이름을 입력하세요. > ",
		"ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT": "[！] 이름은 최소 1글자 이상이어야 합니다!",
		"ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG": "[！] 이름은 16글자를 초과할 수 없습니다!",
		"ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS": "3. 수집 대상 키워드를 쉼표(,)를 통해 나열해 주세요. > ",
		"ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT": "[！] 수집 대상은 최소 1개 이상 등록해야 합니다!",
		"ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY": "4. 해당 갤러리는 미니 갤러리인가요? (y/N) > ",
		"CHANGE_START_DATE_AND_END_DATE": "[！] 검색 시작일이 검색 종료일보다 미래로 입력되어, 두 설정값을 변경하였습니다!",
		"SET_GALLERY_SEARCH_DATE_START_DATE": "시작일",
		"SET_GALLERY_SEARCH_DATE_END_DATE": "종료일",
		"SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE": "[{name}]의 검색 {date_string}을 입력 해 주세요. (yyyy-mm-dd) > ",
		"SET_GALLERY_SEARCH_DATE_SUCCESS": "[○] 검색 {date_string}이 변경되었습니다!",
		"SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT": "[！] 검색 {date_string}은 1995-05-19 형태여야합니다!",
		"SET_GALLERY_IS_MINI_TYPE_YES_OR_NO": "[{name}]는 미니 갤러리인가요? (Y/n) > ",
		"SET_GALLERY_IS_MINI_SUCCESS": "[○] 미니 갤러리 여부가 변경되었습니다!",
		"SET_GALLERY_KEYWORD_TYPE_KEYWORDS": "[{name}]의 수집 대상 키워드를 쉼표(,)를 통해 나열해 주세요. > ",
		"SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS": "[○] 수집 대상 키워드가 변경되었습니다!",
		"SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT": "[！] 수집 대상은 최소 1개 이상 등록해야 합니다!",
		"SET_GALLERY_URL_TYPE_URL": "[{name}]의 URL을 입력해 주세요. > ",
		"SET_GALLERY_URL_TYPE_URL_SUCCESS": "[○] 수집 대상의 URL이 변경되었습니다!",
		"SET_GALLERY_URL_REMOVE_URL_SUCCESS": "[○] 수집 대상의 URL을 제거하였습니다!",
		"SET_GALLERY_NAME_TYPE_NAME": "[{name}]의 새로운 이름을 작성해 주세요. > ",
		"SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT": "[！] 이름은 최소 1글자 이상이어야 합니다!",
		"SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG": "[！] 이름은 16글자를 초과할 수 없습니다!",
		"SET_GALLERY_NAME_TYPE_NAME_SUCCESS": "[○] 수집 대상의 이름이 변경되었습니다!",
		"SELECT_EDIT_PARAMETER_CONTEXT": "\n┌───────────[편집　항목]───────────┐\n├ 1. 이름 ({name})\n├ 2. URL ({url})\n├ 3. 수집 키워드 ({keyword})\n├ 4. 미니 갤러리 여부 ({is_mini_gallery})\n├ 5. 검색 시작일 ({search_start_date})\n├ 6. 검색 종료일 ({search_end_date})\n├ 7. 제거\n├ 8. 뒤로\n└───────────[편집　항목]───────────┘",
		"SELECT_EDIT_PARAMETER_QUESTION": "{gallery_id} ({name})의 어떤 항목을 수정하시겠습니까? > ",
		"SELECT_EDIT_PARAMETER_DELETE_QUESTION": "{gallery_id} ({name})을 검색 대상에서 제거하시겠습니까? (y/N) > ",
		"SELECT_EDIT_PARAMETER_DELETE_SUCCESS": "[！] {gallery_id} ({name})가 검색 대상에서 제거되었습니다!",
		"SELECT_EDIT_TARGET_CONTEXT_1": "\n┌───────────[검색대상　편집]───────────┐",
		"SELECT_EDIT_TARGET_CONTEXT_2": "├ {index}. {gallery_id} ({name})",
		"SELECT_EDIT_TARGET_CONTEXT_3": "├ {add_index}. 검색대상 갤러리 추가\n├ {exit_index}. 뒤로\n└───────────[검색대상　편집]───────────┘",
		"SELECT_EDIT_TARGET_QUESTION": "편집 대상을 선택하세요. > ",
		"SELECT_EDIT_TARGET_ERROR_NOT_EXIST": "[！] 편집 대상을 찾을 수 없습니다!",
		"PRINT_SEARCH_TARGET_LIST_CONTEXT_1": "\n┌───────────[검색대상　확인]───────────┐",
		"PRINT_SEARCH_TARGET_LIST_CONTEXT_2": "├┬ {name} ({url})\n│├ 검색 키워드: {keyword}\n│└ 검색 범위: {search_start_date} ~ {search_end_date}",
		"PRINT_SEARCH_TARGET_LIST_CONTEXT_3": "└───────────[검색대상　확인]───────────┘\n",
		"PRINT_MENU": "\n┌────────────────────────────────┐\n├ 1. 검색 대상 확인\n├ 2. 검색 대상 편집\n├ 3. CSV 파일 출력\n├ 4. 프로그램 종료\n└────────────────────────────────┘",
		"SEARCH_GALLERY_THREAD_INIT": "[！] 게시글 검색 스레드 구동 중...",
		"READ_POST_THREAD_INIT": "[！] 게시글 열람 스레드 구동 중...",
		"EXPORT_CSV_FIELDS": ["갤러리ID","갤러리 이름","게시글ID","URL","제목","작성자","IP","작성일","제목에서 발견된 키워드", "게시글에서 발견된 키워드", "제목에서 발견된 키워드 개수", "게시글에서 발견된 키워드 개수", "총 발견된 키워드 개수"],
		"EXPORT_CSV_SUCCESS": "[○] CSV 파일이 생성되었습니다! ({filename})",
		"CONVERT_DB_TO_CSV_CONTEXT": "\n┌───────────[출력　대상]───────────┐\n├ 1. 전체 데이터\n├ 2. 키워드가 1개 이상 매칭된 데이터만\n├ 3. 뒤로\n└───────────[출력　대상]───────────┘",
		"CONVERT_DB_TO_CSV_QUESTION": "어떤 데이터를 출력하시겠습니까? > ",
		"READ_SEARCH_TARGET_INIT": "[！] ./search_target.json 파일로부터 검색 대상을 불러오는 중...",
		"READ_SEARCH_TARGET_SUCCESS": "[○] ./search_target.json 파일로부터 검색 대상을 등록하였습니다! ({gallery_id} - {name})",
		"READ_SEARCH_TARGET_FAILED": "[×] ./search_target.json 파일로부터 검색 대상을 불러오는데 실패하였습니다!",
		"READ_SEARCH_TARGET_ADDED_EXAMPLE_1": "[！] 예시 검색 대상을 등록하였습니다! (policeofficer - 순경 갤러리)",
		"READ_SEARCH_TARGET_ADDED_EXAMPLE_2": "[！] 예시 검색 대상을 등록하였습니다! (gong - 현직 공무원 갤러리)",
		"SAVE_POST_SUCCESS": "[○] 데이터베이스 기록 스레드 구동 완료!",
		"SEARCH_GALLERY_THREAD_SUCCESS": "[○] 게시글 검색 스레드 구동 완료!",
		"READ_POST_THREAD_SUCCESS": "[○] 게시글 열람 스레드 구동 완료!",
		"DAEMON_IS_RUNNING": "(백그라운드에서 갤러리 검색이 진행 중입니다)",
		"MAIN_TYPE_MENU": "원하시는 동작을 입력하세요. > ",
		"MAIN_EXIT_PROGRAM": "[！] 프로그램을 안전하게 종료 중입니다!"
	},
	"jp":{
        "SAVE_POST_INIT": "[！] データベース記録スレッドの起動中...",
        "SAVE_POST_EXIT": "[！] データベース記録スレッドの終了中...",
        "CREATE_DB_INIT": "[！] データベースの作成中...",
        "CREATE_DB_SUCCESS": "[○] データベースが正常に作成されました！",
        "CREATE_DB_FAILED": "[×] データベースの作成に失敗しました！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID": "1. ギャラリーIDを入力してください。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST": "[！] 既に存在するギャラリーIDです！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME": "2. ギャラリー名を入力してください。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT": "[！] 名前は少なくとも1文字以上である必要があります！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG": "[！] 名前は16文字を超えることはできません！",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS": "3. コンマ(,)で区切られた収集キーワードのリストを入力してください。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT": "[！] 少なくとも1つの収集対象が登録されている必要があります！",
        "ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY": "4. このギャラリーはミニギャラリーですか？ (y/N) > ",
        "CHANGE_START_DATE_AND_END_DATE": "[！] 開始日が終了日より未来に入力されたため、両方の設定が変更されました！",
        "SET_GALLERY_SEARCH_DATE_START_DATE": "開始日",
        "SET_GALLERY_SEARCH_DATE_END_DATE": "終了日",
        "SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE": "{name}の検索{date_string}を入力してください。 (yyyy-mm-dd) > ",
        "SET_GALLERY_SEARCH_DATE_SUCCESS": "[○] 検索{date_string}が変更されました！",
        "SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT": "[！] 検索{date_string}は1995-05-19の形式でなければなりません！",
        "SET_GALLERY_IS_MINI_TYPE_YES_OR_NO": "{name}はミニギャラリーですか？ (Y/n) > ",
        "SET_GALLERY_IS_MINI_SUCCESS": "[○] ミニギャラリーのステータスが変更されました！",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS": "{name}の収集キーワードをコンマ(,)で区切ってリストアップしてください。 > ",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS": "[○] 収集キーワードが変更されました！",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT": "[！] 少なくとも1つの収集対象が登録されている必要があります！",
        "SET_GALLERY_URL_TYPE_URL": "{name}のURLを入力してください。 > ",
        "SET_GALLERY_URL_TYPE_URL_SUCCESS": "[○] 収集対象のURLが変更されました！",
        "SET_GALLERY_URL_REMOVE_URL_SUCCESS": "[○] 収集対象のURLが削除されました！",
        "SET_GALLERY_NAME_TYPE_NAME": "{name}の新しい名前を入力してください。 > ",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT": "[！] 名前は少なくとも1文字以上である必要があります！",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG": "[！] 名前は16文字を超えることはできません！",
        "SET_GALLERY_NAME_TYPE_NAME_SUCCESS": "[○] 収集対象の名前が変更されました！",
        "SELECT_EDIT_PARAMETER_CONTEXT": "\n┌───────────[項目の編集]───────────┐\n├ 1. 名前 ({name})\n├ 2. URL ({url})\n├ 3. 収集キーワード ({keyword})\n├ 4. ミニギャラリーステータス ({is_mini_gallery})\n├ 5. 検索開始日 ({search_start_date})\n├ 6. 検索終了日 ({search_end_date})\n├ 7. 削除\n├ 8. 戻る\n└───────────[項目の編集]───────────┘",
        "SELECT_EDIT_PARAMETER_QUESTION": "{gallery_id} ({name})のどの項目を変更しますか？ > ",
        "SELECT_EDIT_PARAMETER_DELETE_QUESTION": "{gallery_id} ({name})を検索対象から削除しますか？ (y/N) > ",
        "SELECT_EDIT_PARAMETER_DELETE_SUCCESS": "[！] {gallery_id} ({name})が検索対象から削除されました！",
        "SELECT_EDIT_TARGET_CONTEXT_1": "\n┌───────────[検索対象の編集]───────────┐",
        "SELECT_EDIT_TARGET_CONTEXT_2": "├ {index}. {gallery_id} ({name})",
        "SELECT_EDIT_TARGET_CONTEXT_3": "├ {add_index}. 検索対象ギャラリーの追加\n├ {exit_index}. 戻る\n└───────────[検索対象の編集]───────────┘",
        "SELECT_EDIT_TARGET_QUESTION": "編集対象を選択してください。 > ",
        "SELECT_EDIT_TARGET_ERROR_NOT_EXIST": "[！] 編集対象が見つかりません！",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_1": "\n┌───────────[検索対象の確認]───────────┐",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_2": "├┬ {name} ({url})\n│├ 収集キーワード: {keyword}\n│└ 検索範囲: {search_start_date} ~ {search_end_date}",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_3": "└───────────[検索対象の確認]───────────┘\n",
        "PRINT_MENU": "\n┌────────────────────────────────┐\n├ 1. 検索対象の表示\n├ 2. 検索対象の編集\n├ 3. CSVファイルの出力\n├ 4. プログラムの終了\n└────────────────────────────────┘",
        "SEARCH_GALLERY_THREAD_INIT": "[！] 投稿検索スレッドの起動中...",
        "READ_POST_THREAD_INIT": "[！] 投稿読み込みスレッドの起動中...",
        "EXPORT_CSV_FIELDS": ["Gallery ID","Gallery Name","Post ID","URL","Title","Author","IP","Date","Keywords Found in Title", "Keywords Found in Post", "Number of Keywords Found in Title", "Number of Keywords Found in Post", "Total Number of Keywords Found"],
        #"EXPORT_CSV_FIELDS": ["ギャラリーID","ギャラリー名","投稿ID","URL","タイトル","著者","IP","日付","タイトル内のキーワード", "投稿内のキーワード", "タイトル内のキーワード数", "投稿内のキーワード数", "合計キーワード数"],
        "EXPORT_CSV_SUCCESS": "[○] CSVファイルが作成されました！ ({filename})",
        "CONVERT_DB_TO_CSV_CONTEXT": "\n┌───────────[CSVの出力対象]───────────┐\n├ 1. 全データ\n├ 2. 少なくとも1つの一致するキーワードを持つデータ\n├ 3. 戻る\n└───────────[CSVの出力対象]───────────┘",
        "CONVERT_DB_TO_CSV_QUESTION": "どのデータをエクスポートしますか？ > ",
        "READ_SEARCH_TARGET_INIT": "[！] ./search_target.jsonファイルから検索対象を読み込んでいます...",
        "READ_SEARCH_TARGET_SUCCESS": "[○] search_target.jsonファイルから検索対象が登録されました！ ({gallery_id} - {name})",
        "READ_SEARCH_TARGET_FAILED": "[×] search_target.jsonファイルから検索対象を読み込むのに失敗しました！",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_1": "[！] サンプル検索対象が追加されました！ (policeofficer - 警察官ギャラリー)",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_2": "[！] サンプル検索対象が追加されました！ (gong - 現職公務員ギャラリー)",
        "SAVE_POST_SUCCESS": "[○] データベース記録スレッドが正常に完了しました！",
        "SEARCH_GALLERY_THREAD_SUCCESS": "[○] 投稿検索スレッドが正常に完了しました！",
        "READ_POST_THREAD_SUCCESS": "[○] 投稿読み込みスレッドが正常に完了しました！",
        "DAEMON_IS_RUNNING": "(バックグラウンドでウェブクローラーが実行中です)",
        "MAIN_TYPE_MENU": "ご希望のアクションを入力してください。 > ",
        "MAIN_EXIT_PROGRAM": "[！] プログラムを安全に終了しています！"
	},
	"cn":{
        "SAVE_POST_INIT": "[！] 启动数据库记录线程...",
        "SAVE_POST_EXIT": "[！] 停止数据库记录线程...",
        "CREATE_DB_INIT": "[！] 创建数据库...",
        "CREATE_DB_SUCCESS": "[○] 数据库创建成功！",
        "CREATE_DB_FAILED": "[×] 数据库创建失败！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID": "1. 输入画廊ID。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST": "[！] 画廊ID已存在！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME": "2. 输入画廊名称。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT": "[！] 名称必须至少为1个字符！",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG": "[！] 名称不能超过16个字符！",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS": "3. 用逗号分隔列出收集关键词。 > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT": "[！] 必须注册至少一个收集目标！",
        "ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY": "4. 这个画廊是迷你画廊吗？ (y/N) > ",
        "CHANGE_START_DATE_AND_END_DATE": "[！] 开始日期输入为未来日期，因此已更改两个设置！",
        "SET_GALLERY_SEARCH_DATE_START_DATE": "开始日期",
        "SET_GALLERY_SEARCH_DATE_END_DATE": "结束日期",
        "SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE": "请输入{name}的搜索{date_string}。（yyyy-mm-dd） > ",
        "SET_GALLERY_SEARCH_DATE_SUCCESS": "[○] 搜索{date_string}已更改！",
        "SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT": "[！] 搜索{date_string}应为1995-05-19格式！",
        "SET_GALLERY_IS_MINI_TYPE_YES_OR_NO": "{name}是迷你画廊吗？ (Y/n) > ",
        "SET_GALLERY_IS_MINI_SUCCESS": "[○] 迷你画廊状态已更改！",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS": "用逗号分隔列出{name}的收集关键词。 > ",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS": "[○] 收集关键词已更改！",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT": "[！] 必须注册至少一个收集目标！",
        "SET_GALLERY_URL_TYPE_URL": "请输入{name}的URL。 > ",
        "SET_GALLERY_URL_TYPE_URL_SUCCESS": "[○] 收集目标的URL已更改！",
        "SET_GALLERY_URL_REMOVE_URL_SUCCESS": "[○] 收集目标的URL已移除！",
        "SET_GALLERY_NAME_TYPE_NAME": "请输入{name}的新名称。 > ",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT": "[！] 名称必须至少为1个字符！",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG": "[！] 名称不能超过16个字符！",
        "SET_GALLERY_NAME_TYPE_NAME_SUCCESS": "[○] 收集目标的名称已更改！",
        "SELECT_EDIT_PARAMETER_CONTEXT": "\n┌───────────[编辑项目]───────────┐\n├ 1. 名称（{name}）\n├ 2. URL（{url}）\n├ 3. 收集关键词（{keyword}）\n├ 4. 迷你画廊状态（{is_mini_gallery}）\n├ 5. 搜索开始日期（{search_start_date}）\n├ 6. 搜索结束日期（{search_end_date}）\n├ 7. 删除\n├ 8. 返回\n└───────────[编辑项目]───────────┘",
        "SELECT_EDIT_PARAMETER_QUESTION": "您想修改{gallery_id}（{name}）的哪个项目？ > ",
        "SELECT_EDIT_PARAMETER_DELETE_QUESTION": "您想从搜索目标中删除{gallery_id}（{name}）吗？ (y/N) > ",
        "SELECT_EDIT_PARAMETER_DELETE_SUCCESS": "[！] 已从搜索目标中删除{gallery_id}（{name}）！",
        "SELECT_EDIT_TARGET_CONTEXT_1": "\n┌───────────[编辑搜索目标]───────────┐",
        "SELECT_EDIT_TARGET_CONTEXT_2": "├ {index}. {gallery_id}（{name}）",
        "SELECT_EDIT_TARGET_CONTEXT_3": "├ {add_index}. 添加搜索目标画廊\n├ {exit_index}. 返回\n└───────────[编辑搜索目标]───────────┘",
        "SELECT_EDIT_TARGET_QUESTION": "请选择要编辑的目标。 > ",
        "SELECT_EDIT_TARGET_ERROR_NOT_EXIST": "[！] 找不到要编辑的目标！",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_1": "\n┌───────────[搜索目标]───────────┐",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_2": "├┬ {name}（{url}）\n│├ 收集关键词：{keyword}\n│└ 搜索范围：{search_start_date} ~ {search_end_date}",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_3": "└───────────[搜索目标]───────────┘\n",
        "PRINT_MENU": "\n┌────────────────────────────────┐\n├ 1. 显示搜索目标\n├ 2. 编辑搜索目标\n├ 3. 导出CSV文件\n├ 4. 退出程序\n└────────────────────────────────┘",
        "SEARCH_GALLERY_THREAD_INIT": "[！] 启动帖子搜索线程...",
        "READ_POST_THREAD_INIT": "[！] 启动帖子阅读线程...",
        "EXPORT_CSV_FIELDS": ["Gallery ID","Gallery Name","Post ID","URL","Title","Author","IP","Date","Keywords Found in Title", "Keywords Found in Post", "Number of Keywords Found in Title", "Number of Keywords Found in Post", "Total Number of Keywords Found"],
        # "EXPORT_CSV_FIELDS": ["画廊ID","画廊名称","帖子ID","URL","标题","作者","IP","日期","标题中的关键词", "帖子中的关键词", "标题中的关键词数量", "帖子中的关键词数量", "关键词总数量"],
        "EXPORT_CSV_SUCCESS": "[○] CSV文件已创建！（{filename}）",
        "CONVERT_DB_TO_CSV_CONTEXT": "\n┌───────────[导出CSV]───────────┐\n├ 1. 所有数据\n├ 2. 至少有1个匹配关键词的数据\n├ 3. 返回\n└───────────[导出CSV]───────────┘",
        "CONVERT_DB_TO_CSV_QUESTION": "您要导出哪些数据？ > ",
        "READ_SEARCH_TARGET_INIT": "[！] 正在从./search_target.json文件加载搜索目标...",
        "READ_SEARCH_TARGET_SUCCESS": "[○] 已从./search_target.json文件注册搜索目标！（{gallery_id} - {name}）",
        "READ_SEARCH_TARGET_FAILED": "[×] 无法从./search_target.json文件加载搜索目标！",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_1": "[！] 已添加示例搜索目标！（policeofficer - 警察官画廊）",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_2": "[！] 已添加示例搜索目标！（gong - 现职公务员画廊）",
        "SAVE_POST_SUCCESS": "[○] 数据库记录线程已完成！",
        "SEARCH_GALLERY_THREAD_SUCCESS": "[○] 帖子搜索线程已完成！",
        "READ_POST_THREAD_SUCCESS": "[○] 帖子阅读线程已完成！",
        "DAEMON_IS_RUNNING": "（后台正在运行网络爬虫）",
        "MAIN_TYPE_MENU": "请输入您想执行的操作。 > ",
        "MAIN_EXIT_PROGRAM": "[！] 正在安全地停止程序！"
	},
	"ru":{
        "SAVE_POST_INIT": "[！] Запуск потока записи базы данных...",
        "SAVE_POST_EXIT": "[！] Остановка потока записи базы данных...",
        "CREATE_DB_INIT": "[！] Создание базы данных...",
        "CREATE_DB_SUCCESS": "[○] База данных успешно создана!",
        "CREATE_DB_FAILED": "[×] Ошибка создания базы данных!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID": "1. Введите идентификатор галереи. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST": "[！] Идентификатор галереи уже существует!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME": "2. Введите название галереи. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT": "[！] Название должно содержать как минимум 1 символ!",
        "ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG": "[！] Название не может превышать 16 символов!",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS": "3. Укажите ключевые слова для сбора, разделяя их запятыми. > ",
        "ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT": "[！] Должно быть зарегистрировано как минимум одно целевое слово для сбора!",
        "ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY": "4. Это мини-галерея? (y/N) > ",
        "CHANGE_START_DATE_AND_END_DATE": "[！] Введена дата начала, предшествующая дате окончания, поэтому оба параметра были изменены!",
        "SET_GALLERY_SEARCH_DATE_START_DATE": "Дата начала",
        "SET_GALLERY_SEARCH_DATE_END_DATE": "Дата окончания",
        "SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE": "Введите дату {date_string} для поиска {name}. (гггг-мм-дд) > ",
        "SET_GALLERY_SEARCH_DATE_SUCCESS": "[○] Дата поиска {date_string} была изменена!",
        "SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT": "[！] Дата {date_string} для поиска должна иметь формат 1995-05-19!",
        "SET_GALLERY_IS_MINI_TYPE_YES_OR_NO": "{name} - это мини-галерея? (Y/n) > ",
        "SET_GALLERY_IS_MINI_SUCCESS": "[○] Статус мини-галереи был изменен!",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS": "Укажите ключевые слова для сбора в галерее {name}, разделяя их запятыми. > ",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS": "[○] Ключевые слова для сбора были изменены!",
        "SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT": "[！] Должно быть зарегистрировано как минимум одно целевое слово для сбора!",
        "SET_GALLERY_URL_TYPE_URL": "Введите URL для галереи {name}. > ",
        "SET_GALLERY_URL_TYPE_URL_SUCCESS": "[○] URL цели сбора был изменен!",
        "SET_GALLERY_URL_REMOVE_URL_SUCCESS": "[○] URL цели сбора был удален!",
        "SET_GALLERY_NAME_TYPE_NAME": "Введите новое название для {name}. > ",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT": "[！] Название должно содержать как минимум 1 символ!",
        "SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG": "[！] Название не может превышать 16 символов!",
        "SET_GALLERY_NAME_TYPE_NAME_SUCCESS": "[○] Название цели сбора было изменено!",
        "SELECT_EDIT_PARAMETER_CONTEXT": "\n┌───────────[Элементы редактирования]───────────┐\n├ 1. Название ({name})\n├ 2. URL ({url})\n├ 3. Ключевые слова сбора ({keyword})\n├ 4. Статус мини-галереи ({is_mini_gallery})\n├ 5. Дата начала поиска ({search_start_date})\n├ 6. Дата окончания поиска ({search_end_date})\n├ 7. Удалить\n├ 8. Назад\n└───────────[Элементы редактирования]───────────┘",
        "SELECT_EDIT_PARAMETER_QUESTION": "Какой элемент {gallery_id} ({name}) вы хотите изменить? > ",
        "SELECT_EDIT_PARAMETER_DELETE_QUESTION": "Вы хотите удалить {gallery_id} ({name}) из целей поиска? (y/N) > ",
        "SELECT_EDIT_PARAMETER_DELETE_SUCCESS": "[！] {gallery_id} ({name}) был удален из целей поиска!",
        "SELECT_EDIT_TARGET_CONTEXT_1": "\n┌───────────[Редактирование целей поиска]───────────┐",
        "SELECT_EDIT_TARGET_CONTEXT_2": "├ {index}. {gallery_id} ({name})",
        "SELECT_EDIT_TARGET_CONTEXT_3": "├ {add_index}. Добавить галерею в список целей поиска\n├ {exit_index}. Назад\n└───────────[Редактирование целей поиска]───────────┘",
        "SELECT_EDIT_TARGET_QUESTION": "Выберите цель для редактирования. > ",
        "SELECT_EDIT_TARGET_ERROR_NOT_EXIST": "[！] Не удалось найти цель для редактирования!",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_1": "\n┌───────────[Цели поиска]───────────┐",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_2": "├┬ {name} ({url})\n│├ Ключевые слова сбора: {keyword}\n│└ Диапазон поиска: {search_start_date} ~ {search_end_date}",
        "PRINT_SEARCH_TARGET_LIST_CONTEXT_3": "└───────────[Цели поиска]───────────┘\n",
        "PRINT_MENU": "\n┌────────────────────────────────┐\n├ 1. Показать цели поиска\n├ 2. Редактировать цели поиска\n├ 3. Экспорт CSV-файла\n├ 4. Выйти из программы\n└────────────────────────────────┘",
        "SEARCH_GALLERY_THREAD_INIT": "[！] Запуск потока поиска сообщений...",
        "READ_POST_THREAD_INIT": "[！] Запуск потока чтения сообщений...",
        "EXPORT_CSV_FIELDS": ["Gallery ID","Gallery Name","Post ID","URL","Title","Author","IP","Date","Keywords Found in Title", "Keywords Found in Post", "Number of Keywords Found in Title", "Number of Keywords Found in Post", "Total Number of Keywords Found"],
        # "EXPORT_CSV_FIELDS": ["Идентификатор галереи","Название галереи","Идентификатор сообщения","URL","Заголовок","Автор","IP","Дата","Найденные ключевые слова в заголовке", "Найденные ключевые слова в сообщении", "Количество найденных ключевых слов в заголовке", "Количество найденных ключевых слов в сообщении", "Общее количество найденных ключевых слов"],
        "EXPORT_CSV_SUCCESS": "[○] CSV-файл был создан! ({filename})",
        "CONVERT_DB_TO_CSV_CONTEXT": "\n┌───────────[Экспорт CSV]───────────┐\n├ 1. Вся информация\n├ 2. Информация с хотя бы одним совпадением ключевого слова\n├ 3. Назад\n└───────────[Экспорт CSV]───────────┘",
        "CONVERT_DB_TO_CSV_QUESTION": "Какие данные вы хотите экспортировать? > ",
        "READ_SEARCH_TARGET_INIT": "[！] Загрузка целей поиска из файла ./search_target.json...",
        "READ_SEARCH_TARGET_SUCCESS": "[○] Цели поиска были зарегистрированы из файла ./search_target.json! ({gallery_id} - {name})",
        "READ_SEARCH_TARGET_FAILED": "[×] Не удалось загрузить цели поиска из файла ./search_target.json!",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_1": "[！] Пример цели поиска был добавлен! (policeofficer - Галерея полицейских)",
        "READ_SEARCH_TARGET_ADDED_EXAMPLE_2": "[！] Пример цели поиска был добавлен! (gong - Галерея текущих государственных служащих)",
        "SAVE_POST_SUCCESS": "[○] Поток записи в базу данных завершен!",
        "SEARCH_GALLERY_THREAD_SUCCESS": "[○] Поток поиска сообщений завершен!",
        "READ_POST_THREAD_SUCCESS": "[○] Поток чтения сообщений завершен!",
        "DAEMON_IS_RUNNING": "(Веб-сканер работает в фоновом режиме)",
        "MAIN_TYPE_MENU": "Пожалуйста, введите желаемое действие. > ",
        "MAIN_EXIT_PROGRAM": "[！] Безопасное завершение программы!"
	}
}

"""
    GET request function
"""
# Get post list
def getList(gallery_id, page):
    global GALLERY_ID_AND_SETTINGS
    url = "https://gall.dcinside.com/board/lists"
    if GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"]:
        url = "https://gall.dcinside.com/mini/board/lists"
    params={"id": gallery_id, "page": page }
    return getPage(url, params)

# Get post context
def getContext(gallery_id, post_id):
    global GALLERY_ID_AND_SETTINGS
    url = "https://gall.dcinside.com/board/view"
    if GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"]:
        url = "https://gall.dcinside.com/mini/board/view"
    params={"id": gallery_id, "no": post_id}
    return getPage(url, params)

# Send GET request
def getPage(url, param):
    global HEADERS
    res = requests.get(url, params=param, headers=HEADERS)
    statusCode = res.status_code
    if statusCode == 200:
        result = {"statusCode": 200, "message": "SUCCESS", "html": res.content}
        return result
    else:
        res.close()
        if statusCode == 400:
            return {"statusCode":400, "message":"BAD REQUEST", "url": url, "param": param}
        elif statusCode == 500:
            return {"statusCode":500, "message":"INTERNAL SERVER ERROR", "url": url, "param": param}
        elif statusCode == 403:
            return {"statusCode":403, "message":"NO PERMISSION", "url": url, "param": param}
        else:
            return {"statusCode":404, "message":"PAGE NOT FOUND", "url": url, "param": param}


"""
    SQLite3 management function
"""
# Create tables
def create_db():
    global GALLERY_ID_AND_SETTINGS
    global LATEST_POST_ID
    global DB_MUTEX
    global LANGUAGE
    global SELECTED_LANGUAGE
    with DB_MUTEX:
        print(LANGUAGE[SELECTED_LANGUAGE]["CREATE_DB_INIT"])
        try:
            con = sqlite3.connect('./dc_post.db')
            cur = con.cursor()
            for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
                cur.execute(f"CREATE TABLE IF NOT EXISTS dc_post_{gallery_id} (post_id INTEGER PRIMARY KEY, title TEXT, created_by TEXT, ip TEXT, created_at TEXT, match_keywords_at_title TEXT, match_keywords_at_context TEXT DEFAULT NULL, match_keywords_at_title_count INTEGER, match_keywords_at_context_count INTEGER DEFAULT 0, total_match_keywords_count INTEGER, is_context_read INTEGER DEFAULT 0)")
                cur.execute(f"SELECT post_id FROM dc_post_{gallery_id} ORDER BY post_id DESC LIMIT 1")
                result = cur.fetchall()
                if len(result) > 0:
                    LATEST_POST_ID[gallery_id] = result[0][0]
                else:
                    LATEST_POST_ID[gallery_id] = -1
                cur.execute(f"SELECT post_id FROM dc_post_{gallery_id} ORDER BY post_id LIMIT 1")
                result = cur.fetchall()
                if len(result) > 0:
                    FIRST_POST_ID[gallery_id] = result[0][0]
                else:
                    FIRST_POST_ID[gallery_id] = -1
                NEXT_PAGE[gallery_id] = 1
            cur.close()
            con.close()
            print(LANGUAGE[SELECTED_LANGUAGE]["CREATE_DB_SUCCESS"])
            return True
        except Exception as e:
            print(e)
            print(LANGUAGE[SELECTED_LANGUAGE]["CREATE_DB_FAILED"])
            return False

# Get unread post
def select_unread_post():
    global GALLERY_ID_AND_SETTINGS
    global DB_MUTEX
    results = {}
    with DB_MUTEX:
        try:
            con = sqlite3.connect('./dc_post.db')
            cur = con.cursor()
            for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
                cur.execute(f"CREATE TABLE IF NOT EXISTS dc_post_{gallery_id} (post_id INTEGER PRIMARY KEY, title TEXT, created_by TEXT, ip TEXT, created_at TEXT, match_keywords_at_title TEXT, match_keywords_at_context TEXT DEFAULT NULL, total_match_keywords TEXT, match_keywords_at_title_count INTEGER, match_keywords_at_context_count INTEGER DEFAULT 0, total_match_keywords_count INTEGER, is_context_read INTEGER DEFAULT 0)")
                cur.execute(f"SELECT post_id, match_keywords_at_title_count FROM dc_post_{gallery_id} WHERE is_context_read = 0 ORDER BY post_id DESC LIMIT 10")
                result = cur.fetchall()
                if len(result) > 0:
                    results[gallery_id] = []
                    for post_id in result:
                        results[gallery_id].append([result[0][0], result[0][1]])
            cur.close()
            con.close()
            return results
        except Exception as e:
            print(e)
            return results

# Insert post info
def insert_post(gallery_id, values):
    global DB_MUTEX
    with DB_MUTEX:
        try:
            con = sqlite3.connect('./dc_post.db')
            cur = con.cursor()
            column_targets = ','.join(values)
            cur.execute(f"INSERT OR IGNORE INTO dc_post_{gallery_id} (post_id, title, created_by, ip, created_at, match_keywords_at_title, match_keywords_at_title_count) VALUES {','.join(values)}")
            con.commit()
            cur.close()
            con.close()
            return True
        except Exception as e:
            print(e)
            print(f"INSERT OR IGNORE INTO dc_post_{gallery_id} (post_id, title, created_by, ip, created_at, match_keywords_at_title, match_keywords_at_title_count) VALUES {','.join(values)}")
            return False

# Update post info
def update_post(gallery_id, post_id, match_keywords_at_title_count, content):
    global GALLERY_ID_AND_SETTINGS
    global DB_MUTEX
    if gallery_id not in CONTEXT_BUFFER:
        CONTEXT_BUFFER[gallery_id] = []
    matched_keywords = []
    if content:
        try:
            for keyword in GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"]:
                if keyword in content:
                    matched_keywords.append(keyword)
        except Exception as e:
            print(e)
    match_keywords_at_context = ', '.join(matched_keywords)
    match_keywords_at_context_count = len(matched_keywords)
    total_match_keywords_count = match_keywords_at_title_count + match_keywords_at_context_count
    
    query = f"UPDATE dc_post_{gallery_id} SET match_keywords_at_context="
    if len(match_keywords_at_context) > 0:
        query = query + f'"{match_keywords_at_context}", '
    else:
        query = query + f'NULL, '
    query = query + f'match_keywords_at_context_count={match_keywords_at_context_count}, total_match_keywords_count={total_match_keywords_count}, is_context_read=1 WHERE post_id={post_id}'
    with DB_MUTEX:
        try:
            con = sqlite3.connect('./dc_post.db')
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            cur.close()
            con.close()
            return True
        except Exception as e:
            print(e)
            return False

# Get CSV export datas
def select_datas(gallery_id, is_mini_gallery, page, limit, is_only_matched):
    global DB_MUTEX
    with DB_MUTEX:
        try:
            con = sqlite3.connect('./dc_post.db')
            cur = con.cursor()
            query = f'SELECT "{gallery_id}" AS gallery_id, post_id, title, created_by, ip, created_at, match_keywords_at_title, match_keywords_at_context, match_keywords_at_title_count, match_keywords_at_context_count, total_match_keywords_count FROM dc_post_{gallery_id} WHERE is_context_read = 1 '
            if is_only_matched:
                query = query + 'AND total_match_keywords_count > 0 '
            query = query + f'ORDER BY post_id DESC LIMIT {page * limit}, {(page * limit) + limit}'
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            con.close()
            return result
        except Exception as e:
            print(e)
            return None


"""
    Post crawling function
"""
# Save all post list in memory
def save_post():
    global STOP_PROGRAM
    global POST_BUFFER
    global POST_MUTEX
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["SAVE_POST_INIT"])
    while STOP_PROGRAM == False:
        with POST_MUTEX:
            posts = POST_BUFFER.copy()
            for gallery_id in posts.keys():
                if posts[gallery_id] and len(posts[gallery_id]) > 0 and insert_post(gallery_id, posts[gallery_id]) == True:
                    POST_BUFFER[gallery_id] = []
        time.sleep(10)
    print(LANGUAGE[SELECTED_LANGUAGE]["SAVE_POST_EXIT"])
    with POST_MUTEX:
        posts = POST_BUFFER.copy()
        for gallery_id in posts.keys():
            if posts[gallery_id] and len(posts[gallery_id]) > 0 and insert_post(gallery_id, posts[gallery_id]) == True:
                POST_BUFFER[gallery_id] = []
    return

# Save post list to memory
def collect_post(gallery_id, post_id, title, created_by, ip, created_at):
    global POST_MUTEX
    global POST_BUFFER
    global GALLERY_ID_AND_SETTINGS
    with POST_MUTEX:
        if gallery_id not in POST_BUFFER:
            POST_BUFFER[gallery_id] = []
        matched_keywords = []
        for keyword in GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"]:
            if keyword in title:
                matched_keywords.append(keyword)
        match_keywords_at_title = ', '.join(matched_keywords)
        match_keywords_at_title_count = len(matched_keywords)
        
        query = f'({post_id}, "{title}", "{created_by}", '
        if ip != None:
            query = query + f'"{ip}", "{created_at}", '
        else:
            query = query + f'NULL, "{created_at}", '
            
        if len(match_keywords_at_title) > 0:
            query = query + f'"{match_keywords_at_title}", {match_keywords_at_title_count})'
        else:
            query = query + f'NULL, {match_keywords_at_title_count})'
        
        POST_BUFFER[gallery_id].append(query)

# Post crawler
def search_gallery_thread():
    global NEXT_PAGE
    global ROLL_BACK
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["SEARCH_GALLERY_THREAD_INIT"])
    while STOP_PROGRAM == False:
        try:
            for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
                if NEXT_PAGE[gallery_id] > 0:
                    result = getList(gallery_id, NEXT_PAGE[gallery_id])
                    if(result["statusCode"] == 200):
                        table = BeautifulSoup(result["html"], 'html.parser').find('table', class_='gall_list')
                        posts = table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_txt'})
                        posts += table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_pic'})
                        posts += table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_movie'})
                        posts += table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_recomtxt'})
                        posts += table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_recomovie'})
                        posts += table.findAll('tr', class_='ub-content us-post', attrs={'data-type': 'icon_recomimg'})
                        date_updated = False
                        for post in posts:
                            post_id = int(post.find('td', class_='gall_num').text.strip())
                            title = post.findAll('a')[0].text.strip().replace("\"", "'")
                            created_by = post.find('td', class_='gall_writer ub-writer').find('span', class_='nickname')
                            if created_by:
                                created_by = created_by.text.strip().replace("\"", "'")
                            ip = post.find('td', class_='gall_writer ub-writer').find('span', class_='ip')
                            if ip:
                                ip = ip.text.strip().replace("(", "").replace(")", "")
                            created_at = post.find('td', class_='gall_date').attrs['title'].strip()
                            
                            
                            start_y = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[0])
                            start_m = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[1])
                            start_d = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[2])
                            end_y = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[0])
                            end_m = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[1])
                            end_d = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[2])
                            created_at_y = int(created_at.split(" ")[0].split("-")[0])
                            created_at_m = int(created_at.split(" ")[0].split("-")[1])
                            created_at_d = int(created_at.split(" ")[0].split("-")[2])

                            if start_y > created_at_y:
                                NEXT_PAGE[gallery_id] = 1
                                if gallery_id not in ROLL_BACK:
                                    ROLL_BACK.append(gallery_id)
                                date_updated = True
                            elif start_y == created_at_y:
                                if start_m > created_at_m:
                                    NEXT_PAGE[gallery_id] = 1
                                    if gallery_id not in ROLL_BACK:
                                        ROLL_BACK.append(gallery_id)
                                    date_updated = True
                                elif start_m == created_at_m:
                                    if start_d > created_at_d:
                                        NEXT_PAGE[gallery_id] = 1
                                        if gallery_id not in ROLL_BACK:
                                            ROLL_BACK.append(gallery_id)
                                        date_updated = True
                            if end_y < created_at_y:
                                NEXT_PAGE[gallery_id] = -1
                                date_updated = True
                            elif end_y == created_at_y:
                                if end_m < created_at_m:
                                    NEXT_PAGE[gallery_id] = -1
                                    date_updated = True
                                elif end_m == created_at_m:
                                    if end_d < created_at_d:
                                        NEXT_PAGE[gallery_id] = -1
                                        date_updated = True

                            if gallery_id in ROLL_BACK and post_id < LATEST_POST_ID[gallery_id]:
                                NEXT_PAGE[gallery_id] = 1
                                
                            if LATEST_POST_ID[gallery_id] < post_id:
                                LATEST_POST_ID[gallery_id] = post_id
                            if FIRST_POST_ID[gallery_id] > post_id:
                                FIRST_POST_ID[gallery_id] = post_id
                                
                            collect_post(gallery_id, post_id, title, created_by, ip, created_at)
                        if date_updated == False:
                            NEXT_PAGE[gallery_id] = NEXT_PAGE[gallery_id] + 1
                    else:
                        print(result["message"])
                    time.sleep(random.randrange(5,8))
        except Exception as e:
            print(e)
            continue


"""
    Post's context crawling function
"""
# Post's context crawler
def read_post_thread():
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["READ_POST_THREAD_INIT"])
    while STOP_PROGRAM == False:
        targets = select_unread_post()
        for gallery_id in targets.keys():
            post_id = targets[gallery_id][0][0]
            match_keywords_at_title_count = targets[gallery_id][0][1]
            result = getContext(gallery_id, post_id)
            if(result["statusCode"] == 200):
                content = BeautifulSoup(result["html"], 'html.parser').find('div', class_='write_div')
                if content:
                    text = content.text.strip()
                    update_post(gallery_id, post_id, match_keywords_at_title_count, text)
                else:
                    print("NONE", BeautifulSoup(result["html"], 'html.parser'))
            elif(result["statusCode"] == 404):
                update_post(gallery_id, post_id, match_keywords_at_title_count, None)
            else:
                print(result["message"])
            time.sleep(random.randrange(3,6))


"""
    Search target management function
"""
# Add new search target dialogue
def add_new_search_target():
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    gallery_id = None
    datas = {
            "name": None,
            "url": None,
            "keyword": [],
            "is_mini_gallery": False,
            "search_start_date": "1995-05-19",
            "search_end_date": "9999-12-25"
    }
    while True:
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID"])
        gallery_id = choice.strip()
        if len(gallery_id) > 0:
            if gallery_id in GALLERY_ID_AND_SETTINGS.keys():
                print(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_ID_ERROR_ALREADY_EXIST"])
                return
            else:
                break
    while True:
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME"])
        choice = choice.strip()
        if len(choice) < 1:
            print(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_SHORT"])
        elif len(choice) > 16:
            print(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_GALLERY_NAME_ERROR_TOO_LONG"])
        else:
            datas["name"] = choice
            break
    while True:
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS"])
        choice = choice.strip()
        if choice:
            for keyword in choice.strip().split(","):
                datas["keyword"].append(keyword)
            break
        else:
            print(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_MATCH_KEYWORDS_ERROR_TOO_SHORT"])
    choice = input(LANGUAGE[SELECTED_LANGUAGE]["ADD_NEW_SEARCH_TARGET_TYPE_IS_MINI_GALLERY"])
    choice = choice.strip().lower()
    if choice == "y" or choice == "yes" or choice == "o" or choice == "네":
        datas["url"] = "https://gall.dcinside.com/mini/board/lists?id=" + gallery_id
        datas["is_mini_gallery"] = True
    else:
        datas["url"] = "https://gall.dcinside.com/board/lists?id=" + gallery_id
        datas["is_mini_gallery"] = False
    GALLERY_ID_AND_SETTINGS[gallery_id] = datas
    create_db()

# Compare start date and end date
def change_start_date_and_end_date(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    temp = GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"]
    GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"] = GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"]
    GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"] = temp
    print(LANGUAGE[SELECTED_LANGUAGE]["CHANGE_START_DATE_AND_END_DATE"])

# Change search target's collection date range
def set_gallery_search_date(gallery_id, is_start_date):
    global GALLERY_ID_AND_SETTINGS
    global NEXT_PAGE
    global LANGUAGE
    global SELECTED_LANGUAGE
    print("")
    date_string = LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_START_DATE"]
    keyword = "search_start_date"
    if not is_start_date:
        date_string = LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_END_DATE"]
        keyword = "search_end_date"
    while True:
        formatted_context = LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_TYPE_SEARCH_DATE"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']).replace("{date_string}", date_string)
        choice = input(formatted_context)
        if choice:
            choice = choice.strip().lower()
            try:
                datetime.datetime.strptime(choice, '%Y-%m-%d')
                Y = choice.split("-")[0]
                M = choice.split("-")[1]
                D = choice.split("-")[2]
                if len(M) < 2:
                    M = "0" + M
                if len(D) < 2:
                    D = "0" + D
                GALLERY_ID_AND_SETTINGS[gallery_id][keyword] = f"{Y}-{M}-{D}"
                
                start_y = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[0])
                end_y = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[0])
                if start_y > end_y:
                    change_start_date_and_end_date(gallery_id)
                elif start_y == end_y:
                    start_m = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[1])
                    end_m = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[1])
                    if start_m > end_m:
                        change_start_date_and_end_date(gallery_id)
                    elif start_m == end_m:
                        start_d = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"].split("-")[2])
                        end_d = int(GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"].split("-")[2])
                        if start_d > end_d:
                            change_start_date_and_end_date(gallery_id)
                NEXT_PAGE[gallery_id] = 1
                print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_SUCCESS"].replace("{date_string}", date_string))
                break
            except:
                print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT"].replace("{date_string}", date_string))
        else:
            print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_SEARCH_DATE_ERROR_DATE_FORMAT"].replace("{date_string}", date_string))

# Change search target's mini gallery status
def set_gallery_is_mini(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print("")
    choice = input(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_IS_MINI_TYPE_YES_OR_NO"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']))
    if choice:
        choice = choice.strip().lower()
        if choice == "n" or choice == "no" or choice == "x" or choice == "아니" or choice == "아니오" or choice == "아니요" or choice == "0":
            GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"] = False
        else:
            GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"] = True
    else:
        GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"] = True
    print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_IS_MINI_SUCCESS"])

# Change search target's keyword
def set_gallery_keyword(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    while True:
        print("")
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_KEYWORD_TYPE_KEYWORDS"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']))
        if choice:
            GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"] = []
            for keyword in choice.strip().split(","):
                GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"].append(keyword.strip())
            print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_KEYWORD_TYPE_KEYWORDS_SUCCESS"])
            break
        else:
            print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_KEYWORD_TYPE_KEYWORDS_ERROR_TOO_SHORT"])

# Change search target's url
# (Doesn't affect crawling operations)
def set_gallery_url(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print("")
    choice = input(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_URL_TYPE_URL"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']))
    if choice:
        choice = choice.strip()
        GALLERY_ID_AND_SETTINGS[gallery_id]["url"] = choice
        print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_URL_TYPE_URL_SUCCESS"])
    else:
        GALLERY_ID_AND_SETTINGS[gallery_id]["url"] = ""
        print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_URL_REMOVE_URL_SUCCESS"])

# Change search target's name
# (Doesn't affect crawling operations)
def set_gallery_name(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    while True:
        print("")
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_NAME_TYPE_NAME"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']))
        if choice:
            choice = choice.strip().lower()
            if len(choice) < 1:
                print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT"])
            elif len(choice) > 16:
                print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_LONG"])
            else:
                GALLERY_ID_AND_SETTINGS[gallery_id]["name"] = choice
                print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_NAME_TYPE_NAME_SUCCESS"])
                break
        else:
            print(LANGUAGE[SELECTED_LANGUAGE]["SET_GALLERY_NAME_TYPE_NAME_ERROR_TOO_SHORT"])

# Show search target's management items
def select_edit_parameter(gallery_id):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    while True:
        context = LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_PARAMETER_CONTEXT"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{url}", GALLERY_ID_AND_SETTINGS[gallery_id]["url"]).replace("{keyword}", ', '.join(GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"])).replace("{is_mini_gallery}", str(GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"])).replace("{search_start_date}", GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"]).replace("{search_end_date}", GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"])
        print(context)
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_PARAMETER_QUESTION"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{gallery_id}", gallery_id))
        if choice:
            choice = choice.strip().lower()
            if choice == "8" or choice == "exit" or choice == "back" or choice == "뒤로" or choice == "종료":
                break
            elif choice == "1" or choice == "이름" or choice == "name":
                set_gallery_name(gallery_id)
            elif choice == "2" or choice == "url":
                set_gallery_url(gallery_id)
            elif choice == "3" or choice == "keyword" or choice == "수집 키워드" or choice == "키워드":
                set_gallery_keyword(gallery_id)
            elif choice == "4" or choice == "mini" or choice == "미니 갤러리 여부" or choice == "미니 갤러리":
                set_gallery_is_mini(gallery_id)
            elif choice == "5" or choice == "start" or choice == "검색 시작일" or choice == "시작일":
                set_gallery_search_date(gallery_id, True)
            elif choice == "6" or choice == "end" or choice == "검색 종료일" or choice == "종료일":
                set_gallery_search_date(gallery_id, False)
            elif choice == "7" or choice == "del" or choice == "remove" or choice == "검색 대상 제거" or choice == "제거":
                remove_choice = input(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_PARAMETER_DELETE_QUESTION"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{gallery_id}", gallery_id))
                remove_choice = remove_choice.strip().lower()
                if remove_choice == "y" or remove_choice == "yes" or remove_choice == "o" or remove_choice == "네":
                    print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_PARAMETER_DELETE_SUCCESS"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{gallery_id}", gallery_id))
                    GALLERY_ID_AND_SETTINGS.pop(gallery_id)
                    break

# Show management targets
def select_edit_target():
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    while True:
        print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_CONTEXT_1"])
        index = 1
        index_per_gallery_id = {}
        for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
            index_per_gallery_id[str(index)] = gallery_id
            print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_CONTEXT_2"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{index}", str(index)).replace("{gallery_id}", gallery_id))
            index = index+1
        add_index = index
        exit_index = index+1
        print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_CONTEXT_3"].replace("{add_index}", str(add_index)).replace("{exit_index}", str(exit_index)))
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_QUESTION"])
        if choice:
            choice = choice.strip()
            try:
                if choice in GALLERY_ID_AND_SETTINGS.keys():
                    select_edit_parameter(gallery_id)
                elif choice in index_per_gallery_id.keys():
                    select_edit_parameter(index_per_gallery_id[choice])
                elif choice == str(add_index) or choice == "add" or choice == "new" or choice == "검색대상 추가" or choice == "추가":
                    add_new_search_target()
                elif choice == str(exit_index) or choice == "exit" or choice == "back" or choice == "뒤로" or choice == "종료":
                    break
                else:
                    print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_ERROR_NOT_EXIST"])
            except:
                print(LANGUAGE[SELECTED_LANGUAGE]["SELECT_EDIT_TARGET_ERROR_NOT_EXIST"])


"""
    CSV file export function
"""
# CSV file export
def export_csv(is_only_matched):
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    limit = 1000
    fields=LANGUAGE[SELECTED_LANGUAGE]["EXPORT_CSV_FIELDS"]
    filename = f'all_datas_{round(time.time() * 1000)}.csv'
    if is_only_matched:
        filename = f'matched_datas_{round(time.time() * 1000)}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
            url = "https://gall.dcinside.com/board/view"
            if GALLERY_ID_AND_SETTINGS[gallery_id]['is_mini_gallery']:
                url = "https://gall.dcinside.com/mini/board/view"
            url = url + f"?id={gallery_id}&no="
            page = 0
            while True:
                results = select_datas(gallery_id, GALLERY_ID_AND_SETTINGS[gallery_id]["is_mini_gallery"], page, limit, is_only_matched)
                if results:
                    for result in results:
                        writer.writerow([result[0],GALLERY_ID_AND_SETTINGS[gallery_id]["name"],result[1],url + str(result[1]),result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9],result[10]])
                    page = page + 1
                else:
                    break
    print(LANGUAGE[SELECTED_LANGUAGE]["EXPORT_CSV_SUCCESS"].replace("{filename}", filename))

# Show CSV export options
def convert_db_to_csv():
    global LANGUAGE
    global SELECTED_LANGUAGE
    while True:
        print(LANGUAGE[SELECTED_LANGUAGE]["CONVERT_DB_TO_CSV_CONTEXT"])
        choice = input(LANGUAGE[SELECTED_LANGUAGE]["CONVERT_DB_TO_CSV_QUESTION"])
        if choice:
            choice = choice.strip().lower()
            if choice == "3" or choice == "exit" or choice == "back" or choice == "뒤로" or choice == "종료":
                break
            elif choice == "1" or choice == "전체" or choice == "all" or choice == "전체 데이터":
                export_csv(False)
                break
            elif choice == "2" or choice == "매칭" or choice == "matched" or choice == "키워드가 1개 이상 매칭된 데이터만":
                export_csv(True)
                break


"""
    ETC
"""
# Show search target list
def print_search_target_list():
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["PRINT_SEARCH_TARGET_LIST_CONTEXT_1"])
    for gallery_id in GALLERY_ID_AND_SETTINGS.keys():
        print(LANGUAGE[SELECTED_LANGUAGE]["PRINT_SEARCH_TARGET_LIST_CONTEXT_2"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]["name"]).replace("{url}", GALLERY_ID_AND_SETTINGS[gallery_id]["url"]).replace("{keyword}", ', '.join(GALLERY_ID_AND_SETTINGS[gallery_id]["keyword"])).replace("{search_start_date}", GALLERY_ID_AND_SETTINGS[gallery_id]["search_start_date"]).replace("{search_end_date}", GALLERY_ID_AND_SETTINGS[gallery_id]["search_end_date"]))
    print(LANGUAGE[SELECTED_LANGUAGE]["PRINT_SEARCH_TARGET_LIST_CONTEXT_3"])

# Show menu
def print_menu():
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["PRINT_MENU"])

# Read search target config file
# (./search_target.json)
def read_search_target():
    global GALLERY_ID_AND_SETTINGS
    global LANGUAGE
    global SELECTED_LANGUAGE
    print(LANGUAGE[SELECTED_LANGUAGE]["READ_SEARCH_TARGET_INIT"])
    try:
        with open("./search_target.json", 'r') as f:
            lines = f.readlines()
            text = ''.join(lines)
            json_setting = json.loads(text)
            for gallery_id in json_setting.keys():
                GALLERY_ID_AND_SETTINGS[gallery_id] = {}
                GALLERY_ID_AND_SETTINGS[gallery_id]['name'] = json_setting[gallery_id]['name']
                GALLERY_ID_AND_SETTINGS[gallery_id]['url'] = json_setting[gallery_id]['url']
                GALLERY_ID_AND_SETTINGS[gallery_id]['keyword'] = json_setting[gallery_id]['keyword']
                GALLERY_ID_AND_SETTINGS[gallery_id]['is_mini_gallery'] = json_setting[gallery_id]['is_mini_gallery']
                GALLERY_ID_AND_SETTINGS[gallery_id]['search_start_date'] = json_setting[gallery_id]['search_start_date']
                GALLERY_ID_AND_SETTINGS[gallery_id]['search_end_date'] = json_setting[gallery_id]['search_end_date']
                print(LANGUAGE[SELECTED_LANGUAGE]["READ_SEARCH_TARGET_SUCCESS"].replace("{name}", GALLERY_ID_AND_SETTINGS[gallery_id]['name']).replace("{gallery_id}", gallery_id))
        return True
    except Exception as e:
        print(e)
        print(LANGUAGE[SELECTED_LANGUAGE]["READ_SEARCH_TARGET_FAILED"])
        GALLERY_ID_AND_SETTINGS = {
            "policeofficer": {
                "name": "순경 갤러리",
                "url": "https://gall.dcinside.com/board/lists?id=policeofficer",
                "keyword": ["비밀","기밀","사실"],
                "is_mini_gallery": False,
                "search_start_date": "2024-05-29",
                "search_end_date": "9999-05-30"
            },
            "gong": {
                "name": "현직 공무원 갤러리",
                "url": "https://gall.dcinside.com/mini/board/lists?id=gong",
                "keyword": ["비밀","기밀","사실"],
                "is_mini_gallery": True,
                "search_start_date": "2024-05-29",
                "search_end_date": "9999-05-30"
            }
        }
        print(LANGUAGE[SELECTED_LANGUAGE]["READ_SEARCH_TARGET_ADDED_EXAMPLE_1"])
        print(LANGUAGE[SELECTED_LANGUAGE]["READ_SEARCH_TARGET_ADDED_EXAMPLE_2"])
        return False

# Show language
def select_language():
    global SELECTED_LANGUAGE
    while True:
        print("")
        print("┌───────────[Language]───────────┐")
        print(f"├ 1. English")
        print(f"├ 2. 한국어")
        print(f"├ 3. 日本語")
        print(f"├ 4. 中文")
        print(f"├ 5. Русский")
        print("└───────────[Language]───────────┘")
        choice = input(f"Select language > ")
        if choice:
            choice = choice.strip().lower()
            if choice == "1" or choice == "en" or choice == "english":
                SELECTED_LANGUAGE = "en"
                break
            elif choice == "2" or choice == "kr" or choice == "한국어":
                SELECTED_LANGUAGE = "kr"
                break
            elif choice == "3" or choice == "jp" or choice == "日本語":
                SELECTED_LANGUAGE = "jp"
                break
            elif choice == "4" or choice == "cn" or choice == "中文":
                SELECTED_LANGUAGE = "cn"
                break
            elif choice == "5" or choice == "ru" or choice == "Русский":
                SELECTED_LANGUAGE = "ru"
                break

# Main function
if __name__ == "__main__":
    select_language()
    read_search_target()
    try:
        if create_db():
            STOP_PROGRAM = False
            save_post_thread = threading.Thread(target=save_post)
            save_post_thread.daemon = True
            save_post_thread.start()
            print(LANGUAGE[SELECTED_LANGUAGE]["SAVE_POST_SUCCESS"])
            search_gallery_thread = threading.Thread(target=search_gallery_thread)
            search_gallery_thread.daemon = True
            search_gallery_thread.start()
            print(LANGUAGE[SELECTED_LANGUAGE]["SEARCH_GALLERY_THREAD_SUCCESS"])
            read_post_thread = threading.Thread(target=read_post_thread)
            read_post_thread.daemon = True
            read_post_thread.start()
            print(LANGUAGE[SELECTED_LANGUAGE]["READ_POST_THREAD_SUCCESS"])
            print(LANGUAGE[SELECTED_LANGUAGE]["DAEMON_IS_RUNNING"])
            while STOP_PROGRAM == False:
                print_menu()
                choice = input(LANGUAGE[SELECTED_LANGUAGE]["MAIN_TYPE_MENU"])
                if choice:
                    choice = choice.strip().lower()
                    if choice == "4" or choice == "exit" or choice == "종료" or choice == "프로그램 종료" or choice == "프로그램종료":
                        print(LANGUAGE[SELECTED_LANGUAGE]["MAIN_EXIT_PROGRAM"])
                        STOP_PROGRAM = True
                        time.sleep(15)
                    elif choice == "1" or choice == "list" or choice == "검색 대상 확인":
                        print_search_target_list()
                    elif choice == "2" or choice == "edit" or choice == "검색 대상 편집":
                        select_edit_target()
                    elif choice == "3" or choice == "export" or choice == "csv" or choice == "수집된 데이터를 CSV 파일로 추출" or choice == "추출":
                        convert_db_to_csv()
        else:
            STOP_PROGRAM = True
    except KeyboardInterrupt:
        print("\n" + LANGUAGE[SELECTED_LANGUAGE]["MAIN_EXIT_PROGRAM"])
        STOP_PROGRAM = True
        time.sleep(15)