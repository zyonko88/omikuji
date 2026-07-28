# Instagram 投稿の音声文字起こしツール

Instagram の公開アカウントの投稿を取得し、リール動画の音声を文字起こしして、
テキストと PDF にまとめるための一式。

自宅の PC でも Claude Code on the web の環境でも、同じ手順で動く。

## 使い方

```bash
cd tools/instagram-transcribe
./run.sh <instagram_username>
```

作業用ファイルは `ig-work-<username>/` に作られる（リポジトリには含めない）。
途中で止めても、もう一度同じコマンドを叩けば済んだ工程はスキップして再開する。

## 出力

| 出力 | 内容 |
| --- | --- |
| `ALL_TRANSCRIPTS.md` | 全投稿の文字起こしを 1 ファイルにまとめたもの |
| `pdf/` | 投稿ごとに 1 ファイルの PDF |
| `<username>_全文字起こし.pdf` | 表紙・目次・しおりつきで全投稿を 1 冊にした PDF |

## 事前に必要なもの

```bash
pip install faster-whisper reportlab imageio-ffmpeg
```

`ffmpeg` は `imageio-ffmpeg` が同梱のバイナリを持ってくるので、別途インストールは不要。
文字起こしモデル（約 1.6GB）は初回実行時に Hugging Face から自動で落ちてくる。

### Claude Code on the web で動かす場合のネットワーク設定

環境設定の Network access を **Custom** にして、Allowed domains に以下を追加する
（「Also include default list of common package managers」にはチェックを入れておく）。

```
instagram.com
www.instagram.com
*.cdninstagram.com
huggingface.co
*.huggingface.co
*.hf.co
```

## 各スクリプトの役割

| ファイル | 役割 |
| --- | --- |
| `crawl.py` | プロフィールの全投稿のメタデータをページングで取得（`all_items.json`） |
| `extract.py` | 動画をダウンロードして 16kHz モノラルの wav を作り、動画は消す |
| `transcribe_all.py` | Whisper で文字起こし。シャード指定で並列実行する |
| `assemble.py` | 文字起こし結果を 1 つの Markdown に組み立てる |
| `makepdf.py` | 投稿ごとの PDF を作る |
| `makebook.py` | 全投稿を 1 冊の PDF にまとめる |

## 実装上の注意点

**投稿一覧の取得**: プロフィールページの HTML はログインを要求してくるので使えない。
`/api/v1/feed/user/<username>/username/` に `x-ig-app-id` ヘッダを付けて叩くと、
ログインなしで一覧が返ってくる。`next_max_id` でページングする。

**個別投稿の取得**: 通常のアクセスはエラーページになる。リンクプレビュー用のクローラーの
User-Agent で正規のリール URL を取ると、`og:description` にキャプション全文が入って返る。

**文字起こしの精度**: モデルは `large-v3-turbo` を `compute_type="float32"` で使う。
`int8` で量子化すると、このモデルは出力が壊れて意味のない文字列を吐くので使わないこと。

**並列度**: CPU 4 コアなら「2 プロセス × 2 スレッド」が最速。
4 プロセス × 1 スレッドはメモリ不足で落ちる。

**BGM の除去**: 発話のない動画に Whisper をかけると、BGM の歌詞や無意味な繰り返しを
拾ってしまう。`assemble.py` の `classify()` で、短すぎるもの・同じ文字の繰り返し・
日本語より英字が多いものを落としている。

## 出力物の扱いについて

このリポジトリは公開設定のため、取得した投稿の本文はコミットしないこと。
`.gitignore` で作業ディレクトリごと除外してある。
他人の発信内容を再公開することになるため、成果物は手元か非公開の場所に保管する。
