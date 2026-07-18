#!/usr/bin/env bash
# 吉本歯科医院 院長ブログ (WordPress) 投稿スクリプト
#
# 使い方:
#   下書き作成:  ./wp_post.sh draft   "タイトル" 本文ファイル.html
#   公開:        ./wp_post.sh publish "タイトル" 本文ファイル.html
#   下書きを公開: ./wp_post.sh publish-id <投稿ID>
#
# 必要な環境変数:
#   WP_BASE      例: https://www.8181118.com/director3
#   WP_USER      WordPressのユーザー名
#   WP_APP_PASS  アプリケーションパスワード (通常のログインパスワードではなく、
#                wp-admin > ユーザー > プロフィール > アプリケーションパスワード で発行したもの)
set -euo pipefail

: "${WP_BASE:?WP_BASE を設定してください}"
: "${WP_USER:?WP_USER を設定してください}"
: "${WP_APP_PASS:?WP_APP_PASS を設定してください}"

API="$WP_BASE/wp-json/wp/v2"
AUTH="$WP_USER:$WP_APP_PASS"

cmd="${1:?draft / publish / publish-id のいずれかを指定}"

case "$cmd" in
  draft|publish)
    title="${2:?タイトルを指定してください}"
    body_file="${3:?本文ファイルを指定してください}"
    status="draft"
    [ "$cmd" = "publish" ] && status="publish"
    jq -n --arg title "$title" --rawfile content "$body_file" --arg status "$status" \
      '{title: $title, content: $content, status: $status}' \
      | curl -sS --fail-with-body -u "$AUTH" \
          -H "Content-Type: application/json" \
          -X POST "$API/posts" \
          --data @- \
      | jq '{id, status, link}'
    ;;
  publish-id)
    post_id="${2:?投稿IDを指定してください}"
    curl -sS --fail-with-body -u "$AUTH" \
      -H "Content-Type: application/json" \
      -X POST "$API/posts/$post_id" \
      --data '{"status":"publish"}' \
      | jq '{id, status, link}'
    ;;
  *)
    echo "不明なコマンド: $cmd" >&2
    exit 1
    ;;
esac
