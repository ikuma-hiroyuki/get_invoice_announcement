# 適格請求書発行事業者公表システムWeb-API機能からデータ取得



[適格請求書発行事業者公表システムWeb-API機能｜国税庁インボイス制度適格請求書発行事業者公表サイト (nta.go.jp)](https://www.invoice-kohyo.nta.go.jp/web-api/index.html)



## 取得手順

1. <code>registration_numbers.csv</code>に登録番号を入力
2. <code>get_invoice_announcement.py</code>を実行する
3. 同階層に<code>invoice.csv</code>が作られる



## invoice.csvに書き込むデータ

- 登録番号
- 会社名
- 住所