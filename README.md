## alphasea-example-model

alphasea-example-modelは、
[alphasea-agent](https://github.com/alphasea-dapp/alphasea-agent)
に対して毎ラウンド、予測を投稿するプログラムです。

Numeraiのexample modelに相当します。

## 準備

alphasea-example-modelの動作には、
[alphasea-agent](https://github.com/alphasea-dapp/alphasea-agent)
が必要です。リンク先の手順に従ってセットアップしてください。

## インストール

alphasea-example-modelリポジトリをクローンします。

```bash
git clone https://github.com/alphasea-dapp/alphasea-example-model.git
```

以降の作業はクローンしたディレクトリ内で行います。

## 動かし方

### .envファイル作成

以下のような内容の.envファイルをalphasea-example-modelディレクトリ直下に作ります。

#### **`.env`**
```text
ALPHASEA_AGENT_BASE_URL=http://[alphasea-agentのIPアドレス]:8070
ALPHASEA_MODEL_ID=my_model_id
ALPHASEA_MODEL_PATH=data/example_model_rank.xz
```

ALPHASEA_AGENT_BASE_URLにはalphasea-agentのURLを指定します。

ALPHASEA_MODEL_IDには好きなモデルIDを設定します。
NumeraiのモデルIDに相当します。

モデルIDの制約

- AlphaSea全体でユニーク
- 4文字以上31文字以内
- 小文字のアルファベットと数字とアンダースコア(_)を使用可能
- 先頭は小文字のアルファベットかアンダースコア(_)のみ

ALPHASEA_MODEL_PATHには学習したモデルファイルのパスをリポジトリルートからの相対パスで指定します。
data/example_model_rank.xzは学習済みモデルです。
学習の仕方はnotebooks内を見てください。

### 起動

以下のコマンドを実行し、example-modelを起動します。

```bash
docker-compose up -d
```

以下のコマンドで、example-modelのログを確認できます。

```bash
docker-compose logs -f
```

以上で、セットアップは完了です。

## モデル改良

モデルを改良する方法を説明します。
以下のコマンドを実行し、jupyterを起動します。

```bash
docker-compose -f docker-compose-jupyter.yml up -d
```

以下のURLにアクセスしjupyterをブラウザで開きます。
モデル学習notebookをいくつか用意したので、それらを参考にして、改良してください。

http://localhost:8888/lab/workspaces/auto-f/tree/notebooks

## environment variables

|name|description|
|:-:|:-:|
|ALPHASEA_AGENT_BASE_URL|alphasea-agentのbase URL|
|ALPHASEA_MODEL_ID|モデルID|
|ALPHASEA_MODEL_PATH|モデルファイルパス|
|ALPHASEA_SYMBOLS|学習に使うシンボル。本番ではモデルファイルに記録した学習時のシンボルを使うのでこの設定は使いません。|
|ALPHASEA_POSITION_NOISE|提出するポジションにノイズを加える(デバッグ用)|

## Development

### test

alphasea-agentに依存。

```bash
docker-compose run --rm model bash scripts/test.sh
```

### predict

```bash
docker-compose run --rm model python src/predict.py
```
