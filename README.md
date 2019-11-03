# Photozou-scraping

フォト蔵から指定したタグの付いた画像を各タグごとにディレクトリにダウンロードする。複数のタグが付与された画像は複数回ダウンロードされる。

## ログイン情報

ユーザーIDとクッキーを `login_info.json` に書き込む。

```json
{
    "userid": 1111111,
    "cookie": {"sid": "dummy_cookie"}
}
```

Cookie は、Chromium 系の browser であればフォト蔵にログインしてから
<chrome://settings/cookies/detail?site=photozou.jp&search=cookie>
にアクセスし、 sid を探す。

## Prerequisite

- BeautifulSoup4
- requests

## Rerefence

- [Pythonでスクレイピング　基本 - メモ](https://imabari.hateblo.jp/entry/2016/08/20/101006)

### アルバムごとの一括ダウンロード

以下のようにアルバムごとのダウンロードであればいくつか見つかった。今回はタグを機械学習のラベルとして使用したかったため、自分で作った。

- [irasally/photozousan: オンラインアルバム「フォト蔵」から自分のアルバム写真を一括ダウンロードするgem](https://github.com/irasally/photozousan)
- [フォト蔵のアルバム一括ダウンロードツール『採る蔵』を作りますた！ - JJworkshop.com](https://jjworkshop.com/blog/archives/2012/08/post_968.html)
  - [【レビュー】“フォト蔵”に公開されているアルバムを一括ダウンロードできる「採る蔵」 - 窓の杜](https://forest.watch.impress.co.jp/docs/review/556118.html)
