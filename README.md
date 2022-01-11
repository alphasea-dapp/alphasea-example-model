## alphasea-example-model

alphasea-example-modelは、
[alphasea-agent](https://github.com/alphasea-dapp/alphasea-agent)
に対して毎日予測を投稿するプログラムです。

Numeraiのexample modelに相当します。

## 動かし方

.envファイルを作り、ALPHASEA_MODEL_IDを設定します。
ALPHASEA_MODEL_IDはユニークである必要があります。

#### **`.env`**
```text
ALPHASEA_MODEL_ID=my_model_id
```

以下でofeliaと予測ボットを起動します。

```bash
docker-compose up -d
```

## ofelia

[ofelia](https://github.com/mcuadros/ofelia)を使って、
以下のタスクを実行しています。
ofeliaはdockerと親和性の高いcronのようなものです。

- 0:05 UTC 予測投稿

## モデル改良

```bash
docker-compose -f docker-compose-jupyter.yml up -d
```

http://localhost:8888/lab/workspaces/auto-f/tree/notebooks にアクセス
