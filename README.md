# 研究室入退出管理システム

研究室メンバーの入退出情報と累計滞在時間を管理・表示するための Web アプリケーションです。

自分や他のメンバーの出席状況をオープンにすることで、研究のモチベーションアップを図りましょう！

## 機能

- メンバーの入退出記録
- 各メンバーの現在の在室状況表示
- メンバーごとの累計滞在時間表示
- 月別の滞在時間統計グラフ
- 月別の累計滞在時間ランキング
- メンバーごとの過去の在室状況統計検索

## サーバーの起動
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver <ip>:<port>
```

## 使用方法

### Web インターフェース

ブラウザで `http://<ip>:<port>` にアクセスすると、メンバーの在室状況と累計滞在時間を確認できます。

### API エンドポイント

入退出情報を記録するための API エンドポイントが用意されています。

- エンドポイント: `/post/info/`
- メソッド: POST
- データ形式: JSON

例:
```json
{
 "name": "Tanaka Taro",
 "inout": "in", 
 "time": "2024-01-01 09:30:00"
}
```
※inout: "in" or "out"


## 入退出情報の可視化

### 現在の研究室の滞在状況や、累計滞在時間などを可視化できます

現在の滞在状況の可視化
![image_cleanup](https://github.com/user-attachments/assets/00f0d6d7-2ba9-4361-85dc-0c5c3f215f05)

今月の出席日数・平均滞在時間の可視化
![graf](https://github.com/user-attachments/assets/f0e5c1bd-f658-47af-8da8-6986be2c74cf)

