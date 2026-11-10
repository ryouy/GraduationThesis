# LLMは抑制された概念を本当に忘れることができるのか？

**Can Large Language Models Truly Forget a Suppressed Concept?**  
*Investigating Concept Persistence and Reactivation in Internal Representations*

- 区分：卒論テーマ候補 A（2026-10-15）
- 領域：LLM / Mechanistic Interpretability / Concept Suppression

## 1. 背景と着眼点

「白熊を考えるな」と言われると、かえって白熊を意識することがある。LLMについても、禁止対象を**出力しない**ことと、その情報が**モデル内部から消えている**ことは区別する必要がある。

この研究は、推論時の文脈の中で概念表現が残るか・弱まるか・再活性化するかを調べるものであり、モデルの重みから知識を除去する *machine unlearning* の研究ではない。

## 2. Research Question

> When an LLM is instructed to suppress a concept, does the concept persist in its internal representations, and can it re-emerge after intervening context?

**日本語：** LLMにある概念を考えないよう指示したとき、その概念は内部表現に残るのか。また、別の文脈を経た後に再び表現が強まるのか？

## 3. 仮説（いずれも未検証）

- **H1 — 残存：** 禁止対象Xが出力されない場合でも、Hidden StateからXの情報を読み取れる場合がある。
- **H2 — 減衰：** 指示後に無関係な文章を追加すると、Xの読み取り可能性が変化する。単調減少するかどうかも実験で確かめる。
- **H3 — 置換：** 単純な抑制（Don't think of X）と置換（Think of Y instead of X）では、Xの残存パターンが異なる。

## 4. 実験案

### 実験1：概念の残存

同じ概念Xで `Neutral / Affirm / Suppression / Replacement` を比較する。出力上のXの出現率と、共通の測定位置での層別概念スコアをそれぞれ測る。

### 実験2：文脈を経た変化

指示の後に無関係な文章を、0・短・中・長の複数条件で挿入する。各条件の末尾に共通の測定プロンプトを置き、Xの表現スコアを比較する。入力長とトークン位置による交絡を統制する。

### 実験3：再活性化（追加実験）

その後、Xを直接書かずに連想させる質問を与え、無関係な質問の場合と比較する。「出力にはXがないが内部には残る」という事例を探る。ただし、出力の有無で事後的に抽出した結果には選択バイアスがある。

## 5. 測定方法と解析

- **行動指標：** 禁止語の自由生成における出現率、共通の回答位置におけるXの条件付き対数確率。
- **内部指標：** 層別Hidden Stateから、事前に用意した概念方向や線形ProbeでXの情報を読み出す。Logit Lensは補助的な観察に留める。
- **比較：** 同じ概念・同じ測定位置を使う対応あり比較。概念ごとの効果と不確実性も表示する。
- **頑健性：** 概念数・プロンプトの言い換え・モデル規模を拡張して検証する。

## 6. 留意点

1. 「Don't think of banana」という指示には最初からbananaという単語が含まれる。入力語の残響を再活性化と混同しない。
2. 「忘却」は知識の削除ではなく、**指定位置における概念情報の読み出し可能性の変化**として定義する。
3. トークン位置、文脈長、対象語の頻度・分割、置換先Yとの関連性を可能な限り統制する。
4. Probeの精度や出力確率だけでは内部機構の因果関係を証明できない。必要ならActivation Patchingなどを追加する。

## 7. 卒論の到達目標

まず「抑制対象の概念情報が残るか」を確認し、次に文脈経過と置換指示の効果を検証する。時間があれば再活性化の条件を調べる。**研究上の主張は観測できた範囲に限定する。**

## 8. 先行研究と新規性の位置づけ（暫定）

- Mann et al. (2025), *Don't Think of the White Bear*: https://arxiv.org/abs/2511.12381
- Zhou et al. (2026), *How Language Models Process Negation*: https://proceedings.mlr.press/v306/zhou26bq.html

禁止概念や否定の内部処理には先行研究がある。本案では**文脈経過を通じた概念の持続と、抑制・置換の違い**を中心に据える。ただし、この組合せが新規かどうかは追加調査を要する。
