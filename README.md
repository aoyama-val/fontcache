# AWS Lambdaでカスタムフォントを使う

参考

- https://qiita.com/komeda-shinji/items/e049edd1389579059c53
- https://stackoverflow.com/questions/46486261/include-custom-fonts-in-aws-lambda

中身

- fontcache.py
    - fc-cacheを実行するLambda関数
- index.js
    - フォントを使ってhtmlをPDFに変換するLambda関数


## セットアップ

この作業はAmazon Linux上で行う。

```
npm i
./build
aws s3 fontcache.zip s3://
```
