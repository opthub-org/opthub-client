[English Version](https://github.com/opthub-org/opthub-client) 👈

# OptHub Client

![Skills](https://skillicons.dev/icons?i=py,graphql,docker,vscode,github)

Opthub Clientは、以下の機能を提供するPythonパッケージです。

- OptHubのコンペに解を送信する機能
- OptHubのコンペに送信した解の履歴やステータスを確認する機能

このリポジトリでは、Opthub Clientのインストール方法やOptHubのコンペに解を送信する方法を説明しています。

## インストール

事前に、Python 3.10以上をインストールして、pipを使えるように設定してください。その後、以下のコマンドを実行して、PyPIからopthub-clientをインストールします。

```bash
pip install opthub-client
```

## チュートリアル

<!-- TODO: @tkumamoto -->
<!-- アカウントを作成して、ログインして、コンペを選んで参加して、ターミナルでコンペを選択して、解を送信して確認するところまでを一通り説明する。詳しいコマンドの使い方はNotionを誘導する。 -->

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

