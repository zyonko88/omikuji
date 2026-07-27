# -*- coding: utf-8 -*-
"""インプラント手術の説明書・合意書 → A4縦 上質PDF"""
from weasyprint import HTML

ITEMS = [
    "手術日が決定しましたら、麻酔科医・インプラント専門歯科技工士含め全てのスタッフが手術に向けて体制を整えます。また一般診療や手術のお約束をお取りしないなど予約の調整も致しますので、手術日決定からのキャンセルの場合、300,000円（税別）が必要となります。",
    "当日は健康な状態で手術に臨めるように、手術前から体調管理には充分ご注意なさってください。また、内出血が出た場合は10日〜3週間かけて消褪します。大切なイベントの直前2週間は治療を見合わせるべきです。",
    "手術前、手術後の注意事項は別紙にてお渡しいたします。必ず手術までにお読みください。注意事項に関して疑問、質問等がありましたら遠慮なくお声かけください。",
    "午前手術の場合は朝食が絶食、午後手術の場合は昼食が絶食となります。手術2時間前までの水の摂取はして頂いて結構です。（嘔吐による窒息を防ぎ、水分の取りすぎによりトイレに行きたくなるのを避けるため）",
    "お渡ししたお薬は指示通りに服用して下さい。また、当日は、術後にお薬をお飲みいただきますので、お渡ししたお薬をお持ちになってお越しください。",
    "手術中はトイレに行けませんので、トイレがご心配な方、ご不安のある方は「紙オムツ」をご使用になってください。手術中は口腔内が常に出血状態にあります。手術中トイレに行かれますと、大量出血が引き起こされたり、唾液による細菌感染が起こりやすくなります。",
    "手術は精神鎮静法（静脈内鎮静麻酔）と局所麻酔をして行ないます。術後は身体がふらつき、数センチの段差で転倒される方もいらっしゃいます。御自身で自転車、車、バイク等の運転は絶対になさらないようお願いいたします。できれば、ご家族の方の送迎もしくはタクシーがよろしいかと思います。また、公共の交通機関をご利用の場合は、なるべく歩くことが少ない方法でお帰りください。当医院では事故に遭われた場合の責任を負いかねます。遠距離の患者様には、手術前日当日の近隣ホテルへの宿泊をお勧めいたします。",
    "手術当日にご連絡させていただく方の連絡先をお書きください。<div class='fill'>（お名前・ご連絡先<span class='fill-line'>&nbsp;</span>）</div>",
    "手術部に骨がない場合は、骨造成手術を行います。骨造成とは、自分の骨が足りない部分に自家骨や人工骨を入れることです。当医院で使用する人工骨は、牛から取り出した成分を加工して作られた人工骨と、リン酸カルシウムを材料として作られた人工骨です。いずれも長期に手術応用されているもので、不具合は報告されていません。自分の骨を造る場所を提供する骨補填材です。",
    "手術前にCTデータから埋入位置、本数をシミュレーション致しますが、実際の骨の状況から予定している位置や本数が変更になったり、必要な追加手術を行うことがあります。患者様の安全を優先して術式変更や、複数回に分けて手術をさせて頂くことがあります。",
    "手術後、骨とインプラントが結合するまでの期間は流動食や柔らかいものを召しあがって下さい。術後の食事指導をお守りいただけない場合、インプラントを外さないといけなくなることがあります。",
    "個人差はありますが、手術部が腫れたり、皮下出血がみられる事があります。これは1〜4週間程度で消失していきますので、心配はありません。部位は手術部位に限らず、また皮下出血の部位が重力で首等下に下がっていきます。",
    "手術後約2週間、口の中に血がたまったような感じがしたり、唾液に混じって血が大量に出ているような感じがされる方もいらっしゃいますが、傷口から絶えず溢れ出るように出血していなければ心配はありません。傷が治るために若干の出血は必要です。",
    "手術後にしびれが生じることがあります。手術翌日にしびれが生じた場合、神経を圧迫している可能性があります。早急にご連絡ください。手術数日後からしびれが生じる場合があります。炎症による神経圧迫です。ご連絡ください。痛みがなくても、最後までお薬を飲みきってください。炎症を抑える薬を飲む必要があります。",
    "下唇に軽い感覚麻痺（触っても触った感じがしない、触ると痛い）が出る事があります。統計的に3ヶ月〜6ヶ月程度で軽くなっていくことが多いです。",
    "上顎手術の場合、自覚症状なく鼻血が出ることがあります。上顎の場所は鼻の骨と上の顎の骨が繋がっているためにおきる症状です。深呼吸をしない、鼻を強くかまない、等、鼻血がでないようにお気をつけください。洗顔やお化粧時に頬を圧迫したり叩かないようにお願い致します。",
    "手術後は、埋め込んだインプラントに力が加わることを出来るだけ避けなくてはなりません。頬や粘膜から刺激や振動が加わらないよう手術部分を安静にしてください。",
    "歯ブラシは手術後約2週間からなさってください。",
    "インプラント手術後はフッ素入りハミガキ粉、ヨード系イソジンはお控えください。フッ素やイソジンがチタンに悪い影響を及ぼすことがあると報告されています。当医院では、あえてハミガキ粉を使う必要がないと考えております。もしハミガキ粉を使用されたい場合は、フッ素が入っていない液状ハミガキ粉をご使用ください。ザラザラとした粒状のハミガキ粉は危険です。ハミガキ粉やウガイ薬に関してはスタッフにご相談ください。",
    "歯ブラシは、ソニッケア（音波電動歯ブラシ）をお使いください。インプラント周囲歯ぐきは、手動の歯ブラシではバイ菌を全く取れません。ソニッケアはブラシがあたっている2、3mm先のバイ菌を除去したり、インプラント周囲に空気を送り込む事ができます。ただし間に詰まった大きい塊は取れませんので、先にフロスや歯間ブラシをお使いください。",
    "インプラントの本数と上部の歯の本数に違いがあることがあります。",
    "最終の被せ物（本歯)は、かみ合わせや、お口の中の状況に応じて部位によって材質が決まります。部分の材質によって金額が変わることはございません。事前にご説明させて頂きますが、陶材（セラミックス）、強化プラスチック（ハイブリットセラミックスレジン）、金属などが挙げられます。材質については院長と技工士が患者さまの状態にあった材質をご提案させていただきます。適切な仮歯の期間を経て本歯に移ります。仮歯の期間が短期や長期になりすぎると、インプラントを除去しなければならないことがあります。",
    "インプラントの仮歯や本歯は清掃が適切に行える目的で、意図的に隙間を開けています。その為、物が詰まりやすく感じられたり、空気や音が漏れて発音しにくい感じがされたりいたしますが、インプラントを長期に安定して維持させるためには清掃が最も重要です。慣れるまでは違和感を感じられますが、丁寧に清掃して下さい。",
    "インプラントは、ご自身の歯のように自覚症状があらわれません。そのため、定期的な清掃が必要不可欠です。インプラント埋入部分は、清掃がしやすいように、あえて隙間を開けています。どの程度の隙間が開くのか、事前にイメージしにくい場合が多いため、ご希望の方には事前に画像をお見せすることもできます。お気軽にスタッフにお知らせください。",
    "インプラントを埋め込む位置は残存している骨の場所によって異なります。舌側に埋めた場合には舌の部屋が治療前に比べて狭く感じられたり動きにくい、発声に違和感がでるなど舌の感覚が変わることがあります。唇側に埋めた場合は頬っぺたの裏側や唇の裏側が治療前に比べて押されるような違和感を感じることがあります。個人差はありますが、慣れるまでは多少の期間がかかります。",
    "最終の被せ物（本歯）の強化プラスチック（ハイブリットセラミックス）は色が付いたり変色がおこる材質です。機能的には何も問題がありませんが、見た目を気にされることがあるかもしれません。しかし、強く磨くと一時的にはきれいになりますが、キズが入ってどんどん着色しやすくなってしまいます。着色が気になられる場合は院長、スタッフにご相談ください。",
    "インプラントの仮歯や最終被せ物（本歯）は噛む力など衝撃が加わった時に、インプラント本体やご自身の骨を守るために、過度な衝撃が加わった場合に上部が外れるように作られております。驚かれるかも知れませんが、もし外れた場合は、ご連絡頂き、外れた物をお持ちになってお越し下さい。",
    "インプラント治療中は食事制限の期間もありますので、体重が変動することがあります。体調の変化など、ご心配なことがありましたら院長、スタッフにご相談ください。",
    "治療後2年間は最もインプラントに何らかのトラブルが起こりやすい時期です。統計的にインプラントにまつわる偶発症の8割が2年以内に起こります。治療後良い状態を持続させるために、問題を早期に発見し、最小限のご負担で治療をするためにメインテナンスが不可欠です。お約束させて頂く時期に必ず受診くださいますようお願い申し上げます。ご来院いただけない場合、経過不良時の責任を負いかねます。",
    "本歯セット後2年間のメインテナンス費用につきましては、初回金額に含まれております。（消耗品を除く）",
    "本歯セット後3年目以降は個人差がありますが、数ヶ月に一度必ず受診くださいますようお願い申し上げます。",
    "本歯セット後3年目以降のメインテナンスは、費用のご負担金が発生いたします。",
    "インプラント治療後は、ご自分の歯以上に日常のプラークコントロールを徹底することが大切です。ご自分の歯でも周囲の骨が溶けるように、若干ですがインプラント周囲の骨も溶けていきます。そこで、お口の中のお手入れの状態が悪い場合は、ばい菌がたまり炎症が原因で、さらにインプラント周囲の骨が溶けていきます。そのような状態になった場合は、インプラントを除去しなければならない場合もあります。治療後は必ず定期健診にお越し下さい。",
    "インプラント治療終了後に、就寝時ご使用いただくマウスピースをお作りいたします。寝ている間は、歯を食いしばる力が加減できないため、マウスピースを入れずにお休みになると、過剰な力が加わりインプラントが故障する可能性があります。インプラントは単なるネジです。必ずマウスピースをお使いください。",
    "自己判断によって、メインテナンスを中断し、インプラントにトラブルが生じた場合については、当医院では責任を負いかねます。",
    "インプラント治療を長期安定した状態でご使用頂けるように、細心の注意をはらって治療を進めてまいりますが、トラブルが生じる可能性もあります。3年目以降のトラブルの修理費用は状況にもよりますが、ご負担金が発生いたします。",
    "主なトラブルとしては、陶材（セラミックス）や強化プラスチック（ハイブリットセラミックス）の破損（白い部分が欠ける）、インプラント体と被せ物を固定しているネジの緩みや破損、強化プラスチック（ハイブリットセラミックス）は磨り減る材質ですが磨り減りかたが異常に早くかみ合わせの高さが下がる、インプラント周囲骨の異常吸収、頭痛、噛み合う相手の歯への咬合痛などがあげられます。いずれも日常のお手入れやマウスピースで軽減できます。",
    "インプラントが入ると噛めるようになります。顎関節へ急激に力の負担がかかります。噛むときは顎関節が動きますので、以前に顎関節の症状が出ていた方も、今まで顎関節の症状が出ていない方でも、顎関節が痛い、だるい、音がするといったような症状が出ることがあります。このような場合は院長、スタッフにお伝えください。",
    "インプラント治療終了後に他医院で歯科治療をされた場合は、必ず早期にご来院ください。他の歯の状態が少しでも変わることで、インプラントにトラブルが生じることがあります。歯は常に揺れますし、一生動き続けます。インプラントは全く動きません。インプラントの噛み合わせの調整は非常に特殊です。残念ながら、インプラント経験豊富な歯科医師でなければ調整不可能です。",
    "インプラントと噛み合う相手の歯に痛みが出るなどの、何らかの症状があらわれる事があります。このような場合は、院長・スタッフにお伝え下さい。",
    "引越しなどのご事情で当医院へメインテナンスにお越しいただけない場合は、決まりしだいお知らせ下さいますようお願い申し上げます。インプラント治療はメインテナンスを受けて頂くことが最も重要ですので、国内外を問わず、実績ある医院へのご紹介などご相談させていただきたいと思います。",
    "タバコは、血行血流を悪化させますので、歯やインプラントに悪影響を及ぼし、術後にインプラントと骨がくっ付かず、インプラントの除去が必要となる場合があります。また、手術が無事にできたとしても、インプラントが長期安定しないことがあります。必ずインプラント手術一カ月前までの禁煙をお願いいたします。万が一、喫煙があった場合は、責任を負いかねます。",
    "糖尿病は、インプラントが良好に長期経過していても、状況を悪化させます。糖尿病治療をされている方、予備軍の方は血糖値を良好にコントロールし、合併症の発症、進行を予防してください。",
    "全身状態（例えば認知症とか寝たきりなど）によっては、将来除去する必要や、被せ物を作り変える必要が生じる可能性があります。",
    "現在の治療計画は、インプラント以外の他の歯や関節、全身状態が現状にあることが前提として治療が行なわれます。将来、全身状態の変化や他の歯科医院で治療を受けられた際には、必ずご連絡頂き、受診して頂きますようお願い申し上げます。",
    "ビスフォスフォネート系薬剤（飲み薬、注射）を使用される場合は、必ず使用前に担当医にインプラント治療を受けていることをお伝え、ご相談下さい。また、当医院にも必ず使用前にご相談ください。主にこの薬は、骨粗しょう症、乳癌、癌、多発性骨髄腫による骨病変、固形癌骨転移による骨病変、股関節形成術後、脊髄損傷後、骨ページェット病、悪性腫瘍による高カルシウム血症等に使用されます。非常に有効な薬のため、多くの方々に使用されています。しかし、歯科治療で顎骨に刺激が加わる治療（抜歯、歯科インプラント治療、歯周外科等）を受けるもしくは受けていると、顎骨壊死が発生する場合があることが報告されています。有効な薬のため、医科の先生の中にはそのリスクを十分に説明せず使用されることがあります。使用等につきましては、ご自身でリスク等を十分に把握されて担当医とご相談ください。",
    "企業検診や歯科医院等で歯科検診を受けられる際には、必ず、インプラント治療部位を検診者にお伝えください。",
    "噛み合わせが悪いと全身の姿勢が歪みます。全身のバランスが悪いとかみ合わせが悪くなります。姿勢の歪みには日常生活の悪い生活習慣が関係しています。全身のバランスに悪影響を与えている習慣、態癖がある方は、インプラント治療前から改善していくように努力なさってください。将来全身の姿勢が崩れると、噛む位置まで変わってきます。必ずメインテナンスにお越しください。",
    "当医院のインプラント治療費には、手術費用、麻酔科医費用、仮歯、本歯の費用など全てが含まれておりますので、最終の歯の本数や材質によって、お渡ししているお見積書の金額が変更になることはございません。材質の変更を希望されたり、追加手術が必要になる場合は、費用のご負担が必要になることがあります。",
    "上部の被せ物に開いているねじ穴部分には、外れる蓋をしています。外れてもご心配はいりません。",
    "手術中、全身的局所的変化等があった場合には、手術中止となることがあります。（例えば、異常不整脈・血圧上昇・止血困難・術中嘔吐など）",
]

rows = "\n".join(
    f"""<tr>
      <td class="num"><span class="numchip">{i}</span></td>
      <td class="body">{t}</td>
      <td class="chk"><span class="box"></span></td>
      <td class="chk"><span class="box"></span></td>
    </tr>"""
    for i, t in enumerate(ITEMS, 1)
)

html = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><style>
@page {{
  size: A4 portrait;
  margin: 16mm 15mm 18mm 15mm;
  @bottom-center {{
    content: "— " counter(page) " / " counter(pages) " —";
    font-family: "Noto Serif CJK JP", serif;
    font-size: 7.5pt; color: #8a8a8a; letter-spacing: .15em;
  }}
  @top-right {{
    content: "インプラント手術の説明書・合意書";
    font-family: "Noto Serif CJK JP", serif;
    font-size: 7pt; color: #9b8548; letter-spacing: .25em;
  }}
}}
@page :first {{ @top-right {{ content: none; }} }}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: "Noto Serif CJK JP", "IPAPMincho", serif;
  font-size: 8.8pt; line-height: 1.62; color: #23282e;
}}

/* ---------- 表紙ヘッダー ---------- */
.masthead {{ text-align: center; margin-bottom: 5.5mm; }}
.clinic {{
  font-size: 8.5pt; letter-spacing: .55em; color: #9b8548;
  margin-bottom: 2.2mm; text-indent: .55em;
}}
h1 {{
  font-size: 17.5pt; font-weight: 700; letter-spacing: .3em; text-indent: .3em;
  color: #1d2b45; margin-bottom: 2.8mm;
}}
.rule {{
  width: 58mm; height: 0; margin: 0 auto 2.8mm auto;
  border-top: 1.6pt solid #1d2b45;
  position: relative;
}}
.rule-gold {{
  width: 34mm; margin: -1.1mm auto 3mm auto;
  border-top: .6pt solid #b3944a;
}}
.lead {{
  font-size: 8.2pt; color: #4a5058; letter-spacing: .08em;
  max-width: 150mm; margin: 0 auto;
}}

/* ---------- 患者名・日付欄 ---------- */
.idline {{
  display: table; width: 100%; margin: 4.5mm 0 4mm 0;
  border: .8pt solid #1d2b45; border-left: 2.4pt solid #1d2b45;
  padding: 2.6mm 4mm; background: #fbfaf7;
}}
.idline .cell {{ display: table-cell; vertical-align: bottom; }}
.label-sm {{
  font-size: 7.6pt; color: #8a7434; letter-spacing: .2em; margin-right: 2.5mm;
}}
.wline {{
  display: inline-block; border-bottom: .6pt solid #23282e;
  min-width: 62mm; vertical-align: bottom;
}}
.dateline {{ text-align: right; font-size: 9.5pt; letter-spacing: .1em; }}

/* ---------- 項目表 ---------- */
table.items {{
  width: 100%; border-collapse: collapse;
}}
thead th {{
  font-size: 7.8pt; font-weight: 700; color: #fdfcf9;
  background: #1d2b45;
  padding: 1.6mm 1mm; letter-spacing: .3em; text-indent: .3em;
  border-bottom: 1.2pt solid #b3944a;
}}
thead th.h-num {{ width: 8mm; }}
thead th.h-body {{ text-align: left; text-indent: 0; letter-spacing: .25em; padding-left: 3mm; }}
thead th.h-chk {{ width: 12.5mm; letter-spacing: .05em; text-indent: 0; white-space: nowrap; }}
tbody td {{
  border-bottom: .5pt solid #d8d4ca;
  padding: 2.1mm 1.5mm 2.1mm 1mm;
  vertical-align: top;
}}
tbody tr {{ page-break-inside: avoid; }}
td.num {{ text-align: center; padding-top: 2.3mm; }}
.numchip {{
  display: inline-block; width: 5.6mm; height: 5.6mm; line-height: 5.6mm;
  border: .7pt solid #b3944a; border-radius: 50%;
  font-size: 7.6pt; color: #8a7434; text-align: center;
  font-family: "Noto Serif CJK JP", serif;
}}
td.body {{ text-align: justify; padding-right: 3mm; }}
td.chk {{ text-align: center; padding-top: 2.5mm; }}
.box {{
  display: inline-block; width: 3.6mm; height: 3.6mm;
  border: .7pt solid #55595e; border-radius: .4mm; background: #fff;
}}
.fill {{ margin-top: 1.2mm; color: #4a5058; }}
.fill-line {{
  display: inline-block; min-width: 78mm;
  border-bottom: .5pt dotted #55595e;
}}

/* ---------- 同意・署名欄 ---------- */
.consent {{
  page-break-inside: avoid;
  margin-top: 6mm;
  border: 1pt solid #1d2b45;
  padding: 5.5mm 6mm 6mm 6mm;
  background: #fbfaf7;
  position: relative;
}}
.consent::before {{
  content: ""; display: block;
  border-top: .6pt solid #b3944a;
  position: absolute; top: 1.1mm; left: 1.1mm; right: 1.1mm; bottom: 1.1mm;
  border: .6pt solid #b3944a; pointer-events: none;
}}
.consent-title {{
  text-align: center; font-size: 10.5pt; font-weight: 700;
  letter-spacing: .5em; text-indent: .5em; color: #1d2b45; margin-bottom: 3mm;
}}
.consent p.decl {{ font-size: 9pt; text-align: justify; margin-bottom: 3.5mm; }}
.agree-row {{ text-align: center; margin-bottom: 4.5mm; font-size: 10pt; }}
.agree-opt {{ display: inline-block; margin: 0 8mm; letter-spacing: .12em; }}
.agree-opt .box {{ width: 4.2mm; height: 4.2mm; margin-right: 2.2mm; vertical-align: -0.7mm; }}
.sig-head {{
  display: table; width: 100%; margin-bottom: 4mm; font-size: 9.5pt;
}}
.sig-head .to {{ display: table-cell; letter-spacing: .1em; }}
.sig-head .dt {{ display: table-cell; text-align: right; letter-spacing: .1em; }}
.sigrow {{ display: table; width: 100%; margin-top: 2.8mm; }}
.sigrow .c {{ display: table-cell; vertical-align: bottom; }}
.sig-label {{ font-size: 8.2pt; color: #8a7434; letter-spacing: .25em; padding-right: 3mm; white-space: nowrap; }}
.sigline {{
  display: inline-block; width: 100%; border-bottom: .7pt solid #23282e; height: 6.5mm;
}}
.seal {{
  display: inline-block; width: 8.5mm; height: 8.5mm; line-height: 8.5mm;
  border: .6pt dashed #b3944a; border-radius: 50%;
  font-size: 7.5pt; color: #b3944a; text-align: center;
  margin-left: 3.5mm; vertical-align: bottom;
}}
</style></head>
<body>

<div class="masthead">
  <div class="clinic">吉本歯科医院</div>
  <h1>インプラント手術の説明書・合意書</h1>
  <div class="rule"></div>
  <div class="rule-gold"></div>
  <p class="lead">本書は、インプラント手術および術後の管理に関する大切な説明事項をまとめたものでございます。<br>
  各項目をご確認のうえ、「はい」「いいえ」いずれかの欄にチェックをご記入ください。</p>
</div>

<div class="idline">
  <div class="cell"><span class="label-sm">患 者 様 名</span><span class="wline">&nbsp;</span><span style="margin-left:2mm;">様</span></div>
  <div class="cell dateline">記入日　　　　年　　　月　　　日</div>
</div>

<table class="items">
  <thead>
    <tr>
      <th class="h-num">№</th>
      <th class="h-body">説明事項</th>
      <th class="h-chk">はい</th>
      <th class="h-chk">いいえ</th>
    </tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>

<div class="consent">
  <div class="consent-title">同　意　欄</div>
  <p class="decl">以上の説明により、インプラント治療の内容について理解し、インプラント治療を受けることに</p>
  <div class="agree-row">
    <span class="agree-opt"><span class="box"></span>同意します</span>
    <span class="agree-opt"><span class="box"></span>同意しません</span>
  </div>
  <div class="sig-head">
    <span class="to">吉本歯科医院長　殿</span>
    <span class="dt">　　　　年　　　　月　　　　日</span>
  </div>
  <div class="sigrow">
    <div class="c sig-label">患 者 様 名</div>
    <div class="c" style="width:62%;"><span class="sigline">&nbsp;</span></div>
    <div class="c" style="width:14mm; text-align:right;"><span class="seal">印</span></div>
  </div>
  <div class="sigrow">
    <div class="c sig-label">説 明 者 名</div>
    <div class="c" style="width:62%;"><span class="sigline">&nbsp;</span></div>
    <div class="c" style="width:14mm;">&nbsp;</div>
  </div>
</div>

</body></html>"""

out = "/tmp/claude-0/-home-user-omikuji/08f47ad9-024e-5bc8-804d-d2d80214ff5e/scratchpad/インプラント手術の説明書・合意書.pdf"
HTML(string=html).write_pdf(out)
print("OK", out)
