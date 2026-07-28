#!/bin/bash
# Instagram の公開アカウントの投稿を取得し、動画音声を文字起こしして PDF にまとめる。
#
#   ./run.sh <instagram_username>
#
# 各ステップは途中から再開できる。出力済みのファイルがあればスキップされるので、
# 止まったところでもう一度同じコマンドを叩けばよい。
set -euo pipefail

USER_NAME="${1:-${IG_USER:-}}"
if [ -z "$USER_NAME" ]; then
  echo "usage: ./run.sh <instagram_username>" >&2
  exit 1
fi
export IG_USER="$USER_NAME"

HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK_DIR:-$PWD/ig-work-$USER_NAME}"
mkdir -p "$WORK"
cd "$WORK"
echo "作業ディレクトリ: $WORK"

step() { echo; echo "=== $1 ==="; }

step "1/5 投稿一覧の取得"
[ -f all_items.json ] || python3 "$HERE/crawl.py" "$USER_NAME"

step "2/5 音声の抽出"
[ -d wav ] || python3 "$HERE/extract.py"

step "3/5 文字起こし（2プロセス並列 / CPU 4コア想定）"
if [ ! -f .transcribed ]; then
  python3 "$HERE/transcribe_all.py" 0 2 &
  python3 "$HERE/transcribe_all.py" 1 2 &
  wait
  touch .transcribed
fi

step "4/5 テキストの組み立て"
python3 "$HERE/assemble.py"

step "5/5 PDF の作成"
python3 "$HERE/makepdf.py"    # 投稿ごとに 1 ファイル -> pdf/
python3 "$HERE/makebook.py"   # 全投稿を 1 冊に -> <user>_全文字起こし.pdf

echo
echo "完了。出力:"
echo "  $WORK/ALL_TRANSCRIPTS.md"
echo "  $WORK/pdf/"
echo "  $WORK/${USER_NAME}_全文字起こし.pdf"
