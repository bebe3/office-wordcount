"""Pre-compiled regex patterns for text analysis.

All patterns are compiled at module load time for optimal performance.
Uses the 'regex' library for Unicode property support (\\p{...}).
"""

from typing import Final

import regex

# Matches any whitespace characters including Unicode spaces
SPACES: Final[regex.Pattern[str]] = regex.compile(r"[\p{Zs}\t\n\r\f\v]+")

# Matches line break characters (CR, LF, or CRLF)
BREAKS: Final[regex.Pattern[str]] = regex.compile(r"[\r\n]+")

# Unicode script patterns for Asian character detection
# Includes: Chinese, Japanese (Hiragana/Katakana), Korean, and related symbols
ASIAN_PATTERN: Final[str] = "".join(
    (
        # Scripts
        r"\p{Script=Han}",  # Chinese characters (also used in Japanese Kanji)
        r"\p{Script=Hiragana}",  # Japanese Hiragana
        r"\p{Script=Katakana}",  # Japanese Katakana
        r"\p{Script=Hangul}",  # Korean characters
        r"\p{Script=Bopomofo}",  # Chinese phonetic symbols
        # Blocks - Common
        r"\p{Block=Halfwidth_and_Fullwidth_Forms}",  # Full-width punctuation/letters
        r"\p{Block=CJK_Symbols_and_Punctuation}",  # CJK punctuation
        # Note: Enclosed_Alphanumerics (①②③) excluded — Word counts them as 1 word
        r"\p{Block=Enclosed_CJK_Letters_and_Months}",  # ㈱ ㈲ ㊀ ㊁
        r"\p{Block=CJK_Compatibility}",  # ㍻ ㍼ ㍽ (era names, units)
        r"\p{Block=CJK_Compatibility_Forms}",  # Vertical punctuation
        r"\p{Block=Vertical_Forms}",  # Vertical writing symbols
        # Blocks - Radicals and extended
        r"\p{Block=Kangxi_Radicals}",  # Kangxi radicals
        r"\p{Block=CJK_Radicals_Supplement}",  # Radical supplements
        r"\p{Block=Ideographic_Symbols_and_Punctuation}",  # 〽 etc.
        r"\p{Block=Katakana_Phonetic_Extensions}",  # ㇰㇱㇲ Ainu katakana
        # Script=Common but functionally CJK (not matched by Script=Katakana)
        r"・ー",  # U+30FB Middle Dot, U+30FC Prolonged Sound Mark
    )
)

# Characters excluded from character counts (invisible/presentation modifiers)
# - U+FEFF: BOM (Byte Order Mark)
# - U+200B: ZWSP (Zero Width Space)
# - U+FE00-FE0F: Variation Selectors (VS1-16)
# - U+E0100-E01EF: Variation Selectors Supplement (VS17-256)
# Note: ZWJ (U+200D) and ZWNJ (U+200C) are NOT excluded — Word counts them
CHAR_EXCLUDES: Final[regex.Pattern[str]] = regex.compile(
    r"[\uFEFF\u200B\uFE00-\uFE0F\U000E0100-\U000E01EF]+"
)

# Unicode line/paragraph separators — Word counts each as 1 word
UNICODE_SEPARATORS: Final[regex.Pattern[str]] = regex.compile(r"[\u2028\u2029]")

# Matches one or more consecutive Asian characters
ASIANS: Final[regex.Pattern[str]] = regex.compile(rf"[{ASIAN_PATTERN}]+")

# Matches one or more consecutive non-Asian, non-whitespace characters (Western words)
NON_ASIAN_WORDS: Final[regex.Pattern[str]] = regex.compile(rf"[^{ASIAN_PATTERN}\s]+")
