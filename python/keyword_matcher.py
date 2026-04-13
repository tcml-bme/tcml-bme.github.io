SAMPLE_TITLE = """
SIMPLE: Simultaneous Multi-Plane Self-Supervised Learning for Isotropic MRI Restoration from Anisotropic Data
"""

SAMPLE_ABSTRACT = """
Magnetic resonance imaging (MRI) is crucial in diagnosing various abdominal conditions and anomalies. Traditional MRI scans often yield anisotropic data due to technical constraints, resulting in varying resolutions across spatial dimensions, which limits diagnostic accuracy and volumetric analysis. Super-resolution (SR) techniques aim to address these limitations by reconstructing isotropic high-resolution images from anisotropic data. However, current SR methods often rely on indirect mappings and limited training data, focusing mainly on two-dimensional improvements rather than achieving true three-dimensional isotropy. We introduce SIMPLE, a Simultaneous Multi-Plane Self-Supervised Learning approach for isotropic MRI restoration from anisotropic data. Our method leverages existing anisotropic clinical data acquired in different planes, bypassing the need for simulated downsampling processes. By considering the inherent three-dimensional nature of MRI data, SIMPLE ensures realistic isotropic data generation rather than solely improving through-plane slices. This approach flexibility allows it to be extended to multiple contrast types and acquisition methods commonly used in clinical settings. Our experiments show that SIMPLE outperforms state-of-the-art methods both quantitatively using the Kernel Inception Distance (KID) and semi-quantitatively through radiologist evaluations. The generated isotropic volume facilitates more accurate volumetric analysis and 3D reconstructions, promising significant improvements in clinical diagnostic capabilities.
"""


def strip_non_ascii(text):
    return text.encode('ascii', 'ignore').decode('utf-8')


from lab_keywords import KEYWORDS
import spacy
nlp = spacy.load("en_core_web_lg")


def extract_keywords(title, abstract):
    from keybert import KeyBERT

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        strip_non_ascii(title + "\n" + abstract),
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=10,
        candidates=[keyword.lower() for keyword in KEYWORDS]
    )

    kw = [item[0] for item in keywords]
    keywords_lower = [keyword.lower() for keyword in KEYWORDS]
    out = [KEYWORDS[idx] for idx in [keywords_lower.index(word) for word in kw]]

    return out

# %%
import spacy
import string
from Levenshtein import ratio


# Function to normalize a title
def normalize_title(title, lemmatize=False, remove_stopwords=False):
    # Lowercase the title
    title = title.lower()

    # Remove punctuation
    title = title.translate(str.maketrans('', '', string.punctuation))

    # Remove extra spaces
    title = " ".join(title.split())

    if lemmatize or remove_stopwords:
        doc = nlp(title)
        tokens = []
        for token in doc:
            if remove_stopwords and token.is_stop:
                continue  # Skip stop words if required
            if lemmatize:
                tokens.append(token.lemma_)
            else:
                tokens.append(token.text)
        title = " ".join(tokens)

    return title


# Function to compare two titles using Levenshtein similarity
def compare_titles(title1, title2, lemmatize=False, remove_stopwords=False):
    normalized_title1 = normalize_title(title1, lemmatize=lemmatize, remove_stopwords=remove_stopwords)
    normalized_title2 = normalize_title(title2, lemmatize=lemmatize, remove_stopwords=remove_stopwords)

    # Compute similarity using Levenshtein ratio (0 to 1)
    similarity = ratio(normalized_title1, normalized_title2)

    return similarity


if __name__ == "__main__":
    from keybert import KeyBERT

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        SAMPLE_TITLE + "\n" + SAMPLE_ABSTRACT,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=10,
        candidates=[keyword.lower() for keyword in KEYWORDS]
    )

    kw = [item[0] for item in keywords]
    keywords_lower = [keyword.lower() for keyword in KEYWORDS]
    out = [KEYWORDS[idx] for idx in [keywords_lower.index(word) for word in kw]]
    print(out)

    breakpoint()