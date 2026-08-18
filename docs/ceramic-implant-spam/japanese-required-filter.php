<?php
/**
 * ceramic-implant.jp お問い合わせフォーム スパムフィルタ
 *
 * Contact Form 7 の wpcf7_spam フィルタを使って、
 * 「日本語が1文字も含まれていない送信」をスパム扱いにする。
 * スパム判定された送信は、管理者宛メールも自動返信メールも一切送られない。
 *
 * 設置場所：WPCode などのコードスニペットプラグイン（PHP Snippet）
 *           ※この1行目の <?php は貼り付けない
 *
 * 注意：英語だけで書かれた正当なお問い合わせも弾く。
 *       海外からの英語の問い合わせを受ける可能性がある場合は使わないこと。
 *
 * 対象フォームID：149（ceramic-implant.jp のお問い合わせフォーム）
 */

add_filter( 'wpcf7_spam', 'yoshimoto_ci_japanese_required', 10, 2 );

function yoshimoto_ci_japanese_required( $spam, $submission ) {
	// すでに他のフィルタ（Turnstile など）がスパム判定していればそのまま
	if ( $spam ) {
		return $spam;
	}

	// 対象フォームを限定する（他のフォームには影響させない）
	$contact_form = $submission->get_contact_form();

	if ( ! $contact_form || 149 !== (int) $contact_form->id() ) {
		return $spam;
	}

	$data = $submission->get_posted_data();

	// 入力値を文字列として取り出す（チェックボックス等の配列にも対応）
	$get = static function ( $key ) use ( $data ) {
		if ( ! isset( $data[ $key ] ) ) {
			return '';
		}

		$value = $data[ $key ];

		return is_array( $value )
			? implode( ' ', $value )
			: (string) $value;
	};

	// ひらがな・カタカナ・漢字のいずれかを含むか
	$has_japanese = static function ( $text ) {
		return (bool) preg_match(
			'/[\x{3040}-\x{309F}\x{30A0}-\x{30FF}\x{4E00}-\x{9FFF}]/u',
			$text
		);
	};

	$name    = trim( $get( 'your-name' ) );
	$message = trim( $get( 'your-message1' ) . ' ' . $get( 'your-message2' ) );

	$reasons = array();

	// 1. お名前に日本語が無い
	if ( '' !== $name && ! $has_japanese( $name ) ) {
		$reasons[] = 'お名前に日本語が含まれていない';
	}

	// 2. 内容記入欄に日本語が無い
	if ( '' !== $message && ! $has_japanese( $message ) ) {
		$reasons[] = '内容記入欄に日本語が含まれていない';
	}

	// 3. 本文中に URL が2件以上（宣伝目的のスパム対策）
	if ( preg_match_all( '#https?://#i', $message ) >= 2 ) {
		$reasons[] = '本文に URL が2件以上含まれている';
	}

	if ( ! empty( $reasons ) ) {
		// Flamingo の「スパム」タブで理由が確認できるよう記録する
		$submission->add_spam_log( array(
			'agent'  => 'yoshimoto_japanese_required',
			'reason' => implode( ' / ', $reasons ),
		) );

		return true;
	}

	return $spam;
}
