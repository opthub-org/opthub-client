[English Version](https://github.com/opthub-org/opthub-client) 👈

# OptHub Client

![Skills](https://skillicons.dev/icons?i=py,graphql,docker,vscode,github)

Opthub Clientは、以下の機能を提供するPythonパッケージです。

- OptHubのコンペに解を送信する機能
- OptHubのコンペに送信した解の履歴やステータスを確認する機能

ここでは、Opthub Clientのインストール方法やチュートリアルを説明しています。より詳しい説明は、[OptHub Client 利用ガイド](https://opthub.notion.site/OptHub-Client-1fec52032bca4cdda14d5a28c0028952?pvs=4)をご確認ください。

## インストール

事前に、Python 3.10以上をインストールして、パッケージマネージャーとしてpipを使えるように設定してください。その後、以下のコマンドを実行して、PyPIからopthub-clientをインストールします。

```bash
$ pip install opthub-client
```

## チュートリアル

チュートリアルでは、参加しているコンペティションの競技の解を送信する方法や送信した解の履歴を確認する方法を説明します。

解を送信するためには、事前にアカウントを作成し、コンペに参加する必要があります。

👉 [アカウントの作成方法とコンペの参加方法](https://opthub.notion.site/1b96e2f4e9424db0934f297ee0351403?pvs=4)

### ログイン

`opt login`を実行し、ユーザー名、パスワードを入力します。

```bash
$ opt login
Username: [username] # 自分のユーザー名
Password: [password]   # 自分のパスワード
Hello [username]. Successfully logged in.
```

⚠ 事前にアカウントを作成し、メールアドレスを確認する必要があります。

### コンペ・競技の選択

`opt select`を実行し、コンペと競技を選択します。
```bash
$ opt select
? Select a competition: [competition_id] # ↑↓キーでコンペを選択
? Select a match: [match_id] # ↑↓キーで競技を選択
You have selected [competition_id]/[match_id]
```
⚠ 事前にコンペに参加する必要があります。

### 解の送信

`opt submit`を実行し、競技の入出力の規定に沿って解を入力します。

```bash
$ opt submit
? Write the solution: [your_solution] #解を入力
Submitting to [competition_id]/[match_id]... # 送信中
...Submitted # 送信完了
```

👉 [ファイルで解を送信する方法](https://opthub.notion.site/submit-8a6268ea5fb64dacb8fbcd57cf33f21a?pvs=4)
👉 [プログラム経由で解を送信する方法](https://opthub.notion.site/OptHub-API-e35cc47419054d6b8723180b27405c49?pvs=4)


### 解の確認

`opt show trials`を実行し、送信した解が表示されます。`n`キーで次の20件の解を表示、`e`キーで確認を終了できます。

```bash
$ opt show trials # デフォルトで20件ずつ降順で表示される
Trial No: 30, status: success, Score: 0.0001
Trial No: 29, status: scoring
Trial No: 28, status: evaluating
・・・
n: next solutions, e: exit
# nキーで次の20件の解を表示、eキーで確認をやめる
```

### 解のダウンロード

`opt download`で試行番号の範囲を指定してダウンロードすることができます。

```bash
$ opt download -s 10 -e 30 # 試行番号10から30をダウンロード
Downloading trials  [####################################]  100%
Trials have been written to trials_match1.json
```

👉 [出力されるJSONファイルの形式](https://opthub.notion.site/download-11519960ee914c9e91983f899cbfdbfa?pvs=4)

## 開発者の方へ
1. 本リポジトリをclone
2. Poetryの設定
3. `poetry install`を実行
4. 推奨されたVS Codeの拡張機能をダウンロード
5. 他のパッケージとの競合を避けるため、以下のVS Codeの拡張機能を無効にする
    - ms-python.pylint
    - ms-python.black-formatter
    - ms-python.flake8
    - ms-python.isort

上記のセットアップ完了後、プロジェクトのrootディレクトリで`opt`コマンドが使用可能になります。

## 連絡先 <a id="Contact"></a>

ご質問やご不明な点がございましたら、お気軽にお問い合わせください (Email: dev@opthub.ai)。

<img src="https://opthub.ai/assets/images/logo.svg" width="200">

