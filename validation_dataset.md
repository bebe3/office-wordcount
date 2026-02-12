# Word Count Validation Dataset

Copy each "Text" to Microsoft Word and compare the word count results.

## How to check in Word
1. Paste the text into Word
2. Select all (Ctrl+A)
3. Check status bar or Review > Word Count

---

## Basic Tests

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 01 | English only | `Hello World` | words=2, chars=10 | ✅ |
| 02 | Japanese hiragana | `こんにちは` | words=5, chars=5 | ✅ |
| 03 | Japanese katakana | `カタカナ` | words=4, chars=4 | ✅ |
| 04 | Japanese kanji | `日本語` | words=3, chars=3 | ✅ |
| 05 | Korean | `안녕하세요` | words=5, chars=5 | ✅ |
| 06 | Chinese | `中文测试` | words=4, chars=4 | ✅ |

## Mixed Language Tests

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 07 | English + Japanese | `Hello 世界` | words=3, chars=7 | ✅ |
| 08 | English + Japanese sentence | `This is テスト` | words=5, chars=9 | ✅ |
| 09 | Japanese + numbers | `東京2024オリンピック` | words=9, chars=12 | ✅ |

## Special Characters

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 10 | Corporation symbols | `㈱テスト㈲` | words=5, chars=5 | ✅ |
| 11 | Era names | `㍻㍼㍽㍾` | words=4, chars=4 | ✅ |
| 12 | Circled numbers | `①②③④⑤` | words=1, chars=5 | ✅ |
| 13 | Fullwidth letters | `ＡＢＣＤＥ` | words=5, chars=5 | ✅ |
| 14 | Fullwidth numbers | `１２３４５` | words=5, chars=5 | ✅ |

## Radicals and Extensions

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 15 | Kangxi radicals | `⼀⼆⼃` | words=3, chars=3 | ✅ |
| 16 | Ainu katakana | `ㇰㇱㇲ` | words=3, chars=3 | ✅ |

## Punctuation Tests

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 17 | Japanese punctuation | `「こんにちは」` | words=7, chars=7 | ✅ |
| 18 | Mixed punctuation | `Hello、World。` | words=4, chars=12 | ✅ |
| 19 | CJK symbols | `〽々〆` | words=3, chars=3 | ✅ |

## Emoji Tests

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 20 | Simple emoji | `👍` | words=1, chars=1 | ✅ |
| 21 | Multiple emoji | `👍👎👏` | words=1, chars=3 | ✅ |
| 22 | Family emoji (ZWJ) | `👨‍👩‍👧‍👦` | words=1, chars=7 | ✅ |
| 23 | Skin tone emoji | `👍🏻` | words=1, chars=2 | ✅ |
| 24 | Flag emoji | `🇯🇵` | words=1, chars=2 | ✅ |
| 25 | Emoji + text EN | `Hello👍World` | words=1, chars=11 | ✅ |
| 26 | Emoji + text JP | `こんにちは👋` | words=6, chars=6 | ✅ |
| 27 | Emoji between words | `hello 🙂 world` | words=3, chars=11 | ✅ |
| 28 | Keycap emoji | `1️⃣2️⃣3️⃣` | words=1, chars=6 | ✅ |

**Note**: If Word counts emoji like 👨‍👩‍👧‍👦 as 1 character, we need to implement grapheme-based counting.

## Zero-Width Characters and BOM

These invisible characters can affect word/character counts.

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 29 | BOM + text | `\ufeff` + `Hello` | words=1, chars_no_sp=5, chars_w_sp=5 | ✅ |
| 30 | ZWSP between words | `foo` + `\u200B` + `bar` | words=1, chars_no_sp=6, chars_w_sp=6 | ✅ |
| 31 | ZWJ between words | `foo` + `\u200D` + `bar` | words=1, chars_no_sp=7, chars_w_sp=7 | ✅ |
| 32 | ZWNJ between words | `foo` + `\u200C` + `bar` | words=1, chars_no_sp=7, chars_w_sp=7 | ✅ |

**How to test**: These characters are not easily pasted. Use Word's Insert > Symbol (Unicode) or create a .txt file programmatically.

```python
# Generate test files:
from pathlib import Path
Path("test_bom.txt").write_bytes(b"\xef\xbb\xbfHello")  # BOM + Hello
Path("test_zwsp.txt").write_text("foo\u200Bbar")          # ZWSP
Path("test_zwj.txt").write_text("foo\u200Dbar")           # ZWJ
Path("test_zwnj.txt").write_text("foo\u200Cbar")          # ZWNJ
```

## Unicode Line Separators

U+2028 (Line Separator) and U+2029 (Paragraph Separator) are Unicode-specific break characters.

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 33 | Line separator | `a` + `\u2028` + `b` | words=3, chars_no_sp=3, chars_w_sp=3 | ✅ |
| 34 | Paragraph separator | `a` + `\u2029` + `b` | words=3, chars_no_sp=3, chars_w_sp=3 | ✅ |
| 35 | Mixed with CRLF | `Hello\u2028World\u2029Test` | words=5, chars_no_sp=16, chars_w_sp=16 | ✅ |

```python
Path("test_lsep.txt").write_text("a\u2028b")
Path("test_psep.txt").write_text("a\u2029b")
Path("test_mixed_sep.txt").write_text("Hello\u2028World\u2029Test")
```

## Southeast Asian Scripts (No Space Between Words)

These languages typically don't use spaces between words. Office uses dictionary-based word breaking.

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 36 | Thai sentence | `สวัสดีครับ` | words=1, chars=10 | ✅ |
| 37 | Thai + English | `Hello สวัสดี` | words=2, chars_no_sp=11, chars_w_sp=12 | ✅ |
| 38 | Lao text | `ສະບາຍດີ` | words=1, chars=7 | ✅ |
| 39 | Khmer text | `សួស្តី` | words=1, chars=6 | ✅ |
| 40 | Myanmar text | `မင်္ဂလာပါ` | words=1, chars=9 | ✅ |

**Note**: Our tool treats these as 1 non-Asian word per whitespace chunk. If Office does character-based or dictionary-based counting, the results will differ significantly.

## Arabic and Indic Scripts

Space-separated scripts that should work like English word counting.

| # | Name | Text | Our Tool | Word |
|---|------|------|----------|------|
| 41 | Arabic (2 words) | `مرحبا بالعالم` | words=2, chars_no_sp=12, chars_w_sp=13 | ✅ |
| 42 | Hindi (2 words) | `नमस्ते दुनिया` | words=2, chars_no_sp=12, chars_w_sp=13 | ✅ |

---

## Copy-Paste Texts

### Basic / Mixed / Special (01-19)
```
Hello World
こんにちは
カタカナ
日本語
안녕하세요
中文测试
Hello 世界
This is テスト
東京2024オリンピック
㈱テスト㈲
㍻㍼㍽㍾
①②③④⑤
ＡＢＣＤＥ
１２３４５
⼀⼆⼃
ㇰㇱㇲ
「こんにちは」
Hello、World。
〽々〆
```

### Emoji (20-28)
```
👍
👍👎👏
👨‍👩‍👧‍👦
👍🏻
🇯🇵
Hello👍World
こんにちは👋
hello 🙂 world
1️⃣2️⃣3️⃣
```

### Southeast Asian / Arabic / Indic (36-42)
```
สวัสดีครับ
Hello สวัสดี
ສະບາຍດີ
សួស្តី
မင်္ဂလာပါ
مرحبا بالعالم
नमस्ते दुनिया
```
