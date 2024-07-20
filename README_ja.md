[English Version](https://github.com/opthub-org/opthub-client) 👈

# OptHub Client

![Skills](https://skillicons.dev/icons?i=py,graphql,docker,vscode,github)

Opthub Clientは、以下の機能を提供するPythonパッケージです。

- OptHubのコンペに解を送信する機能
- OptHubのコンペに送信した解の履歴やステータスを確認する機能

このリポジトリでは、Opthub Clientのインストール方法やOptHubのコンペに解を送信する方法を説明しています。

## インストール

事前に、Python 3.10以上をインストールして、パッケージマネージャーとしてpipを使えるように設定してください。その後、以下のコマンドを実行して、PyPIからopthub-clientをインストールします。

```bash
pip install opthub-client
```

## チュートリアル

<!-- TODO: @tkumamoto -->
<!-- アカウントを作成して、ログインして、コンペを選んで参加して、ターミナルでコンペを選択して、解を送信して確認するところまでを一通り説明する。詳しいコマンドの使い方はNotionを誘導する。 -->
<!-- ここを変更する際にはnotionのチュートリアルも変更する必要あり -->
ターミナル操作を行う前に、アカウントを作成し、コンペに参加してください。アカウントの作成方法やコンペの参加方法は[こちら](https://opthub.notion.site/1b96e2f4e9424db0934f297ee0351403?pvs=4)を確認してください。
ターミナル操作によってログインからコンペを選択、解を送信、解の確認までの流れを説明します。各コマンドの詳細は[こちら](https://opthub.notion.site/OptHub-Client-1fec52032bca4cdda14d5a28c0028952?pvs=4)を確認してください。
<!-- TODO: URLを挿入 -->
1. `opt login`でログインをします。アカウント作成が完了していることを前提としています
    ```bash
    $ opt login
    ```
2. ユーザー名、パスワードを入力します
    ```bash
    $ opt login
    Username: user_name # 自分のユーザー名
    Password: *******   # 自分のパスワード
    ```
3. 成功したメッセージが表示されればログイン完了です
    ```bash
    $ opt login
    Username: user_name
    Password: *******
    Hello user_name. Successfully logged in.
    ```
4. `opt select`で解を送信するコンペ、競技を選択します
    ```bash
    $ opt select
    ```
5. 自分が参加しているコンペティションが表示されるので、コンペティションを選びます。
    ```bash
    $ opt select
    ? Select a competition:
    > competition1 # ↑↓キーで選択、Enterで決定します
      competition2 
    ```
6. コンペティションを選択したら、次は競技を選択します
    ```bash
    $ opt select
    ? Select a competition: competition1
    ? Select a match:
    > match1 # ↑↓キーで選択、Enterで決定します
      match2
    ```
7. `You have selected competition1 - match1`と表示されれば競技の選択完了です
   ```bash
    $ opt select
    ? Select a competition: competition1
    ? Select a match:
    You have selected competition1 - match1 # competition1、match1にはそれぞれコンペ名、競技名が入る
    ```
8.  `opt submit`で解を送信します
    ```bash
    # selectによって選んだ競技に解を送信する 
    $ opt submit
    ```
9. 解を入力します
    ```bash
    $ opt submit
    ? Write the solution: 3 #ここでは「3」という解を入力 
    ```
10. 解を送信中というメッセージが表示され、`Submitted`という表示がでれば送信完了です
     ```bash
    $ opt submit
    ? Write the solution: 3
    Submitting to competition1/match1... # 送信中 competition1、match1にはコンペ名、競技名が表示されている
    ...Submitted # 送信完了
    ```
11. `opt show trials`でターミナル上で解を確認します。
    ```bash
    # selectによって選んだ競技に送信した解を確認する 
    $ opt show trials
    ```
12. 解が表示される
     ```bash
    $ opt show trials # デフォルトで20件ずつ表示される
    Trial No: 1, status: evaluating # 解の番号とステータスが表示
    n: next solutions, e: exit # nキーで次の20件の解を表示、eキーで確認をやめる
    ```
13. 解の情報をファイルで確認したい場合は`opt download`で確認できる
    ```bash
    # selectによって選んだ競技に送信した解をダウンロードする
    # デフォルトでは解No1からNo50までをダウンロードする
    $ opt download
    ```
14. 解をダウンロードし終わったら、表示されているjsonファイルを確認する
    ```
    $ opt download
    Downloading trials  [####################################]  100%
    # ダウンロードの進捗が表示
    Trials have been written to trials_match1.json # trials_マッチ名.jsonファイルがダウンロードされる
    ```
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

