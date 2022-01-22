## alphasea-example-model

alphasea-example-modelは、
[alphasea-agent](https://github.com/alphasea-dapp/alphasea-agent)
に対して毎日予測を投稿するプログラムです。

Numeraiのexample modelに相当します。

## 動かし方

.envファイルを作り、ALPHASEA_MODEL_ID_PREFIXを設定します。

- Numeraiのモデル名に相当
- model_idはAlphaSea全体でユニーク
- model_idは4文字以上31文字以内の小文字のC識別子 ( \[a-z_\]\[a-z0-9_\]{3,30} )
- 実際のモデルIDは末尾に0030や0230など執行時刻を表す文字列が追加される

#### **`.env`**
```text
ALPHASEA_MODEL_ID_PREFIX=my_model_id_
```

以下で予測ボットを起動します。

```bash
docker-compose up -d
```

以下で正しく起動できたか確認します。

```bash
docker-compose logs
```

## モデル改良

```bash
docker-compose -f docker-compose-jupyter.yml up -d
```

http://localhost:8888/lab/workspaces/auto-f/tree/notebooks にアクセス

## environment variables

|name|description|
|:-:|:-:|
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
