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
### アカウント作成
アカウント作成の流れを説明します。
1. ブラウザから下記URLにアクセスします
<!-- TODO: 本番環境URL挿入 -->
1. アカウント作成ボタンを押します
2. ユーザーネーム、メールアドレス、パスワードを入力し、メールアドレス宛に届いたメールのURLをクリックします。ここでパスワードは大文字と小文字を含む英数字8文字以上にする必要があります
3. Your registration has been confirmed!と出れば成功です

### ログイン・コンペの参加
ログインからコンペの参加までの流れを説明します。
1. ブラウザから下記URLにアクセスします
<!-- TODO: 本番環境URL挿入 -->
2. ログインボタンを押します
3. 作成したアカウントでログインします
4. 左上のメニューから「コンペ」を選択します
5. 「すべてのコンペ」から参加したい開催中のコンペを選択します
6. 右上の「コンペに参加します」ボタンを押します

### CLI操作
CLI操作によってログインからコンペを選択、解を送信、解の確認までの流れを説明します。各コマンドの詳細は[こちら]()を確認ください。
<!-- TODO: URLを挿入 -->
1. `opt login`でログインをします
2. `opt select`で解を送信するコンペ、競技を選択します
3. `opt submit`で解を送信します
4. `opt show trials`でコマンドライン上で解を確認します。ファイルにダウンロードしたい場合は`opt download`でダウンロードしたファイルを確認してください


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

