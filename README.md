# omikuji — 作業リポジトリ

Claude との作業で作った成果物をまとめて置いてあるリポジトリです。
**この `main` ブランチに全部そろっています。** 自宅／職場どちらのパソコンから開いても、
ここを見れば今までの成果物が一覧できます。

---

## 目次

### 歯科医院（吉本歯科医院）

| 内容 | ファイル |
|---|---|
| インプラント治療専用サイト（1ページLP・SEO/AEO対策済み） | [`yoshimoto-implant/index.html`](yoshimoto-implant/index.html) ／ [説明](yoshimoto-implant/README.md) |
| インプラント手術の説明書・同意書（PDF） | [`docs/consent-form/インプラント手術の説明書・合意書.pdf`](docs/consent-form/) |
| 同上のPDF生成スクリプト | [`docs/consent-form/make_consent_pdf.py`](docs/consent-form/make_consent_pdf.py) |
| 抜歯に関する説明書兼同意書（改訂版） | [`documents/抜歯に関する説明書兼同意書_改訂版.docx`](documents/) |
| 抜歯同意書チェック用・スタッフ回覧 | [`documents/抜歯同意書確認_スタッフ回覧.docx`](documents/) |
| 抜歯の診断・説明に関する院内ルール | [`docs/抜歯の診断・説明に関する院内ルール.docx`](docs/) |
| カウンセリング申込書（A4×3ページ） | [`docs/counseling-form.html`](docs/counseling-form.html) ／ [PDF](docs/) |
| 水曜日朝の院内清掃・器具消毒についてのスタッフ回覧 | [`documents/staff-memo-wednesday-cleaning.md`](documents/staff-memo-wednesday-cleaning.md) ／ [.docx](documents/staff-memo-wednesday-cleaning.docx) |
| 熱中症予防ポスター（緊急連絡先入り） | [`posters/heatstroke-prevention-poster.html`](posters/heatstroke-prevention-poster.html) ／ [PDF](posters/heatstroke-prevention-poster.pdf) |

### 情報発信・集客

| 内容 | ファイル |
|---|---|
| 院長ブログ 週3回投稿システム（運用フロー＋投稿スクリプト） | [`blog/README.md`](blog/README.md) ／ [`blog/wp_post.sh`](blog/wp_post.sh) |
| ブログ記事：ノーコード・ブートキャンプ特別講義（2025-07-22） | [`blog/2025-07-22-nocode-bootcamp-wordpress.html`](blog/2025-07-22-nocode-bootcamp-wordpress.html) |
| MEO投稿文：抜歯後の骨について（Googleビジネスプロフィール用） | [`meo/2026-07-25-extraction-bone-meo-post.md`](meo/2026-07-25-extraction-bone-meo-post.md) |
| MEO投稿下書き3本（ブログ→MEO転用・週3回運用の見本） | [`meo/2026-07-27-blog-to-meo-drafts.md`](meo/2026-07-27-blog-to-meo-drafts.md) |
| MEO週3回投稿スケジュール（7月末〜9月末） | [`meo/2026-meo-posting-schedule.md`](meo/2026-meo-posting-schedule.md) |
| MEO投稿 全28回の投稿文＋画像（予約登録済み） | [`meo/2026-meo-posts-all-28.md`](meo/2026-meo-posts-all-28.md) ／ [`meo/images/`](meo/images/) |
| VSL型ランディングページのテンプレート | [`docs/vsl.html`](docs/vsl.html) |

### 学習教材（共通テスト「公共、倫理」）

| 内容 | ファイル |
|---|---|
| タブレット学習アプリ（8週間コース・模試付き） | [`app/kokyo-rinri-study.html`](app/kokyo-rinri-study.html) |
| 同上（GitHub Pages 公開用の同一ファイル） | [`docs/index.html`](docs/index.html) |
| 共通テスト形式のオリジナル演習問題 | [`practice/kokyo-rinri-practice.md`](practice/kokyo-rinri-practice.md) |

### 人間科学研究所

| 内容 | ファイル |
|---|---|
| 「知ったかぶり講座」収支報告書（2026-07-18） | [`accounting/2026-07-18_知ったかぶり講座_収支報告書.md`](accounting/) ／ [.docx](accounting/) |
| boseigata.com ランディングページ（母性型思考・無料タイプ診断つき） | [`boseigata/index.html`](boseigata/index.html) ／ [説明・公開前TODO](boseigata/README.md) |
| **母性型 365日メールマガジン**（毎朝配信・全回「これが母性型です」に着地） | [`boseigata/mailmagazine/`](boseigata/mailmagazine/) ／ [設計書](boseigata/mailmagazine/README.md) |
| 同上：プライバシーポリシー・特定商取引法に基づく表記 | [`boseigata/privacy.html`](boseigata/privacy.html) ／ [`boseigata/tokushoho.html`](boseigata/tokushoho.html) |

---

## 別のパソコンで作業を続けるには

この `main` ブランチが全成果物の集合場所です。次のことを守ると、どのパソコンから開いても
続きから作業できます。

1. **新しく作業を始めるときは `main` から枝分かれする**
2. **作業が終わったら `main` に取り込む**（プルリクエストを作ってマージする、など）
3. Claude に「◯◯の続きをやりたい」と伝えれば、該当ファイルを探して再開できます

> 参考：これまでは 1 セッション = 1 ブランチで作業が分かれていて、`main` に統合されていなかったため、
> 別のパソコンでセッションを開くと過去の成果物が見えない状態になっていました。
> 過去のブランチ（`claude/…`）は履歴として残してあります。

## GitHub Pages について

`docs/` フォルダを公開設定にすると、以下がブラウザから閲覧できます。

- `docs/index.html` — 公共・倫理 学習アプリ
- `docs/counseling-form.html` — カウンセリング申込書
- `docs/vsl.html` — VSL型ランディングページ

インプラントサイト（`yoshimoto-implant/`）の公開手順は
[`yoshimoto-implant/README.md`](yoshimoto-implant/README.md) を参照してください。
