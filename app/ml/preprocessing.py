import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)


# ─────────────────────────────────────────────
# 1. Normalization
# ─────────────────────────────────────────────

def normalize_arabic(text):
    # Remove diacritics (fixed: consistent 4-space indent)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Normalize letter variations
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('ى', 'ي', text)
    text = re.sub('ؤ', 'ء', text)
    text = re.sub('ئ', 'ء', text)
    text = re.sub('ة', 'ه', text)
    text = re.sub('گ', 'ك', text)
    text = re.sub('ڤ', 'ف', text)
    text = re.sub('چ', 'ج', text)
    text = re.sub('پ', 'ب', text)
    text = re.sub('ڜ', 'ش', text)
    text = re.sub('ڪ', 'ك', text)
    text = re.sub('ڧ', 'ق', text)
    text = re.sub('ٱ', 'ا', text)
    return text


# ─────────────────────────────────────────────
# 2. Noise Removal
# ─────────────────────────────────────────────

def remove_arabic_noise(text):
    """Remove tatweel, HTML tags, and extra whitespace."""
    text = re.sub(r'\u0640', '', text)       # tatweel
    text = re.sub(r'<.*?>', '', text)         # HTML tags
    text = re.sub(r'\s+', ' ', text).strip()  # extra whitespace
    return text


def remove_urls_mentions_hashtags(text):
    """Remove Twitter-specific noise: URLs, @mentions, #hashtags."""
    text = re.sub(r'http\S+|www\S+', '', text)   # URLs
    text = re.sub(r'@\w+', '', text)              # mentions
    text = re.sub(r'#(\w+)', r'\1', text)         # keep hashtag word, remove #
    return text


arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!"…"–ـ'''
english_punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
all_punctuations = arabic_punctuations + english_punctuations

def remove_punctuation(text):
    return re.sub(f"[{re.escape(all_punctuations)}]", " ", text)


# ─────────────────────────────────────────────
# 3. Emoji Handling
# ─────────────────────────────────────────────

def handle_emojis(text, mode='remove'):
    if mode == 'remove':
        return emoji.replace_emoji(text, '')
    elif mode == 'description':
        return emoji.demojize(text, language='ar')
    return text


# ─────────────────────────────────────────────
# 4. Numbers & Special Characters
# ─────────────────────────────────────────────

def handle_numbers_and_special_chars(text, mode='remove'):
    if mode == 'remove':
        text = re.sub(r'[\d٠-٩]+', '', text)
        return text
    elif mode == 'normalize':
        number_map = {
                      '٠': 'صفر',
                      '١': 'واحد',
                      '٢': 'اثنان',
                      '٣': 'ثلاثة',
                      '٤': 'أربعة',
                      '٥': 'خمسة',
                      '٦': 'ستة',
                      '٧': 'سبعة',
                      '٨': 'ثمانية',
                      '٩': 'تسعة',
                      '0': 'صفر',
                      '1': 'واحد',
                      '2': 'اثنان',
                      '3': 'ثلاثة',
                      '4': 'أربعة',
                      '5': 'خمسة',
                      '6': 'ستة',
                      '7': 'سبعة',
                      '8': 'ثمانية',
                      '9': 'تسعة'
        }
        for digit, name in number_map.items():
            text = text.replace(digit, f' {name} ')
        return text
    return text


# ─────────────────────────────────────────────
# 5. Arabizi → Arabic
# ─────────────────────────────────────────────

def arabizi_to_arabic(text):
    conversion_dict = {
        'th': 'ث', 
        'kh': 'خ',
        'sh': 'ش',
        'gh': 'غ',
        '2': 'ء',
        '3': 'ع',
        '5': 'خ',
        '6': 'ط',
        '7': 'ح',
        '8': 'غ',
        '9': 'ص',
        'a': 'ا',
        'b': 'ب',
        't': 'ت',
        'j': 'ج',
        'd': 'د',
        'r': 'ر',
        'z': 'ز',
        's': 'س',
        'f': 'ف',
        'q': 'ق',
        'k': 'ك',
        'l': 'ل',
        'm': 'م',
        'n': 'ن',
        'h': 'ه',
        'w': 'و',
        'y': 'ي',
    }

    arabic_pattern = re.compile(r'[\u0600-\u06FF]')

    def convert_token(token):
        # Skip tokens that already contain Arabic characters
        if arabic_pattern.search(token):
            return token
        result = token.lower()
        # Multi-char mappings first, then single-char
        for latin, arabic in conversion_dict.items():
            result = result.replace(latin, arabic)
        return result

    return ' '.join(convert_token(tok) for tok in text.split())


# ─────────────────────────────────────────────
# 6. Elongation
# ─────────────────────────────────────────────

def normalize_elongated_words(text):
    return re.sub(r'(.)\1{2,}', r'\1\1', text)


# ─────────────────────────────────────────────
# 7. Spelling Corrections
# ─────────────────────────────────────────────

# Word-boundary pattern for Arabic (space or start/end of string)
_WB = r'(?<![^\s]){}(?![^\s])'

_CORRECTIONS = {
    'انشاء الله': 'إن شاء الله',
    'انشالله':    'إن شاء الله',
    'لاكن':       'لكن',
    'هاذا':       'هذا',
    'هاذه':       'هذه',
}

def correct_arabic_text(text):
    """Apply common spelling corrections with word-boundary awareness."""
    for mistake, correction in _CORRECTIONS.items():
        # Use space/boundary-safe replacement
        pattern = r'(?<!\S)' + re.escape(mistake) + r'(?!\S)'
        text = re.sub(pattern, correction, text)
    return text


# ─────────────────────────────────────────────
# 8. Stopwords & Stemming
# ─────────────────────────────────────────────

def remove_stopwords(text):
    stop_words = set(stopwords.words('arabic'))
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(tokens)


def stem_arabic_text(text):
    stemmer = ISRIStemmer()
    tokens = word_tokenize(text)
    tokens = [stemmer.stem(w) for w in tokens]
    return ' '.join(tokens)


# ─────────────────────────────────────────────
# 9. Master Pipeline  (NEW)
# ─────────────────────────────────────────────

def preprocess_text(
    text,
    emoji_mode='description',
    number_mode='normalize',
    remove_stops=True,
    stem=False,
    convert_arabizi=True,
):
    """
    Full preprocessing pipeline in the correct order.

    Steps:
        1. Remove URLs, mentions, hashtags
        2. Handle emojis
        3. Correct common spelling mistakes
        4. Normalize Arabic letters & diacritics
        5. Remove Arabic noise (tatweel, HTML, whitespace)
        6. Handle numbers
        7. Remove punctuation
        8. Normalize elongated words
        9. (Optional) Convert Arabizi tokens
       10. (Optional) Remove stopwords
       11. (Optional) Stem
    """
    if not isinstance(text, str) or not text.strip():
        return ''

    text = remove_urls_mentions_hashtags(text)
    text = handle_emojis(text, mode=emoji_mode)
    text = correct_arabic_text(text)
    text = normalize_arabic(text)
    text = remove_arabic_noise(text)
    text = handle_numbers_and_special_chars(text, mode=number_mode)
    text = remove_punctuation(text)
    text = normalize_elongated_words(text)

    if convert_arabizi:
        text = arabizi_to_arabic(text)

    if remove_stops:
        text = remove_stopwords(text)

    if stem:
        text = stem_arabic_text(text)

    # Final whitespace cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    return text