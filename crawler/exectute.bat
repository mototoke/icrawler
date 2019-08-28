@echo off

REM 変数設定
SET PYTHON_INTERPRETER=..\python-3.7.4-embed-amd64\python.exe
SET EXE_PYTHON_FILE=crawler.py
SET ARG_KEYWORD=-k "検索したいもの"
REM ['noncommercial', 'commercial', 'noncommercial,modify', 'commercial,modify']のどれかを指定
SET ARG_LICENSE=-l commercial
SET ARG_DIR=-d images
SET ARG_MAX_NUM=-m 1

REM カレントディレクトリに移動 ※絶対パスで指定する場合は不要
cd /d %~dp0

%PYTHON_INTERPRETER% %EXE_PYTHON_FILE% %ARG_KEYWORD% %ARG_LICENSE% %ARG_DIR% %ARG_MAX_NUM% 

pause