import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer


def normalize_arabic(text):
  # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
  # Normalize letters variations
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    text = re.sub("ڤ", "ف", text)
    text = re.sub("چ", "ج", text)
    text = re.sub("پ", "ب", text)
    text = re.sub("ڜ", "ش", text)
    text = re.sub("ڪ", "ك", text)
    text = re.sub("ڧ", "ق", text)
    text = re.sub("ٱ", "ا", text)
    return text

def handle_emojis(text, mode='remove'):
    if mode == 'remove':
        return emoji.replace_emoji(text, '')
    elif mode == 'description':
        return emoji.demojize(text, language='ar')
    return text

def remove_arabic_noise(text):
    # Remove tatweel
    text = re.sub(r'\u0640', '', text)
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

all_punctuations = arabic_punctuations + english_punctuations

def remove_punctuation(text):
    return re.sub(f"[{re.escape(all_punctuations)}]", " ", text)

def correct_arabic_text(text):
    corrections = {
        'انشاء الله': 'إن شاء الله',
        'لاكن': 'لكن',
        'انشالله': 'إن شاء الله',
        'هاذا': 'هذا',
    }

    for mistake, correction in corrections.items():
        text = text.replace(mistake, correction)

    return text

def handle_numbers_and_special_chars(text, mode='remove'):
    if mode == 'remove':
        text = re.sub(r'\d+', '', text)
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
        for arabic, name in number_map.items():
            text = text.replace(arabic, name)
        return text
    
    
    def arabizi_to_arabic(text):
    # This is a simplified conversion. A complete solution would be more complex.
        conversion_dict = {
            'a': 'ا', 'b': 'ب', 't': 'ت', 'th': 'ث', 'g': 'ج', '7': 'ح', 'kh': 'خ',
            'd': 'د', 'th': 'ذ', 'r': 'ر', 'z': 'ز', 's': 'س', 'sh': 'ش', '9': 'ص',
            '6': 'ط', '3': 'ع', 'gh': 'غ', 'f': 'ف', 'q': 'ق', 'k': 'ك', 'l': 'ل',
            'm': 'م', 'n': 'ن', 'h': 'ه', 'w': 'و', 'y': 'ي'
        }

        for latin, arabic in conversion_dict.items():
            text = text.replace(latin, arabic)

        return text
    
    
def normalize_elongated_words(text):
    # Remove elongation
    text = re.sub(r'(.)\1+', r'\1\1', text)
    return text


def remove_stopwords(text):
    stop_words = set(stopwords.words('arabic'))
    text = word_tokenize(text)
    text = [word for word in text if word not in stop_words]
    return ' '.join(text)


def stem_arabic_text(text):
    stemmer = ISRIStemmer()
    text = word_tokenize(text)
    text = [stemmer.stem(word) for word in text]
    return ' '.join(text) 
    