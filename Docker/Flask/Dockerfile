# Pythonのイメージを指定
FROM python:3.11.3-buster
# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/codeに指定
RUN mkdir /code

WORKDIR /code
# ローカルのrequirements.txtをコンテナの/codeフォルダ直下に置く
COPY ./requirements.txt /code/
# コンテナ内でpip install -r requirements.txtを実行
RUN pip install -U pip && \
    pip install -r requirements.txt
# ソースコードをコンテナにコピー
COPY . /code/