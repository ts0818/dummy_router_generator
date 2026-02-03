# dummy_router_generator

**dummy_router_generator** は、CSV ファイルからルータ構成情報を生成し、  
一意な連番を付与したコロン区切り形式の `router.db` を出力する Python CLI ツールです。

このツールは、「Ruby」製のライブラリ「Oxidized」の「model」の動作確認のためのダミーの `router.db` を生成します。
```
■■■ Oxidizedがサポートしているmodelの一覧 ■■■
https://github.com/ytti/oxidized/tree/master/lib/oxidized/model

■■■ OxidizedがサポートしているOSの一覧 ■■■
https://github.com/ytti/oxidized/blob/master/docs/Supported-OS-Types.md
```
---

## 📌 概要

- CSV を読み込み、行ごとに機器に対する接続情報を処理
- 各行に対して **モデル内連番 + グローバル連番** を付与（両方 5 桁ゼロ埋め）
- 出力は `router.db` に追記され、複数回の実行でも連番が継続
- バリデーションは **pydantic** で実施
- テストは **pytest** で実装済み

---

## 🚀 特徴

- 一度生成した `router.db` に対して複数回追記可能
- モデル数ごとの番号 + `router.db` 全体で一意な通し番号を付与
- CLI 形式で実行可能
- Python で簡単に拡張可能

---

## 🧾 必須入力 CSV フォーマット

CSV ヘッダーは以下のとおりです（順序・名称ともに厳密一致）：
```
prefix,count,ip,model,user,password,enable
```
各フィールドの意味：

| 項目         | 説明 |
|--------------|------|
| prefix       | ホスト名の接頭辞 |
| count        | 同一 prefix のレコード数 ※1|
| ip           | IPv4 アドレス |
| model        | oxidizedのmodel名 |
| user         | ユーザー名 |
| password     | パスワード |
| enable       | enable パスワード（任意） |

※1 同一のIPアドレスで模擬的に複数のホストと見立てたい場合に数を調整します。接続対象のネットワーク機器の同時接続数が関係して来るため、
実際に「Oxidized」の「model」の動作確認をする際の「Oxidized」の「Configuration」の`threads`と`use_max_threads`の設定を考慮する必要があります。
```
■■■ OxidizedのConfiguration ■■■
https://github.com/ytti/oxidized/blob/master/docs/Configuration.md
```

---

### 📄 CSV 入力例
```
prefix,count,ip,model,user,password,enable
Catalyst-2960-L,8,192.168.1.10,ios,admin,secret,enablePass
RTX830,8,10.0.0.1,yamaha,root,passwd,
```
## 📤 出力形式

出力は `router.db` というファイルに追記され、各行は次のような形式になります：
```
{prefix}-{modelLocal}-{globalUnique}:ip:model:user:password:enable
```
- **modelLocal**：CSV 内の count に基づく連番（同一 prefix 内）
- **globalUnique**：router.db 全体の通し番号

例：

【入力】`input.csv`
```
prefix,count,ip,model,user,password,enable
Catalyst-2960-L,8,192.168.1.10,ios,admin,secret,enablePass
RTX830,8,10.0.0.1,yamaha,root,passwd,
```
【出力】`router.db`
```
Catalyst-2960-L-00001-00017:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00002-00018:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00003-00019:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00004-00020:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00005-00021:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00006-00022:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00007-00023:192.168.1.10:ios:admin:secret:enablePass
Catalyst-2960-L-00008-00024:192.168.1.10:ios:admin:secret:enablePass
RTX830-00001-00025:10.0.0.1:yamaha:root:passwd
RTX830-00002-00026:10.0.0.1:yamaha:root:passwd
RTX830-00003-00027:10.0.0.1:yamaha:root:passwd
RTX830-00004-00028:10.0.0.1:yamaha:root:passwd
RTX830-00005-00029:10.0.0.1:yamaha:root:passwd
RTX830-00006-00030:10.0.0.1:yamaha:root:passwd
RTX830-00007-00031:10.0.0.1:yamaha:root:passwd
RTX830-00008-00032:10.0.0.1:yamaha:root:passwd
```

---
## ✅ 動作確認
以下のバージョンのPythonで動作確認済み
```
Python 3.13.3
```
---

## 🛠 インストール方法
シェルを起動し、以下を実行します。

1. リポジトリをクローン
2. 仮想環境を作成・有効化
3. 依存関係をインストール

```bash
# 1. リポジトリをクローン
git clone <リポジトリURL>
# 2. 仮想環境を作成・有効化
# プロジェクトルートに移動
cd dummy_router_generator
python -m venv .venv
# Windows 環境の場合
.venv\Scripts\activate
# macOS / Linux 環境の場合
source .venv/bin/activate
# 3. 依存関係をインストール
pip install -r requirements.txt
```

## 📦 実行方法

プロジェクトルートで次のように実行します：

※ 予め、input.csv の中身は設定しておきます。
```
python -m src.main input.csv
```

複数回実行する場合でも、`router.db` は追記され、グローバル連番は連続したまま継続されます。

とは言え、事前に、検証したいシナリオ向けの`input.csv` を用意し、毎回、`router.db` を空にしてから実行するのをお勧めします。

## 🧪 テスト

このプロジェクトでは pytest を使って単体テストを実装しています。
テストは tests/ 以下に配置されており、以下のコマンドで実行できます：
```
pytest
```

テストは自動で検出され、バリデーションや番号生成の一貫性をチェックします。

## 📁 ディレクトリ構成
```
dummy_router_generator/
    ├── docs/
    ├── src/
    │   ├──main.py
    │   ├── app/
    │   │   └── router_app.py
    │   ├── models/
    │   │   └── row_model.py
    │   ├── services/
    │   │   └── generator.py
    │   └── utils/
    │       └── csv_utils.py
    ├── tests/
    │   ├── app/
    │   │   └── test_router_app.py
    │   ├── models/
    │   │   └── test_row_model.py
    │   ├── services/
    │   │   └── test_generator.py
    │   └── utils/
    │       └── test_csv_utils.py
    ├── input.csv
    ├── router.db
    ├── requirements.txt
    ├── pyproject.toml
    ├── README.md
    └── .gitignore
```





