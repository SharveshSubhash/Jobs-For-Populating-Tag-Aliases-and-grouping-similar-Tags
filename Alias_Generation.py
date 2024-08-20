import nltk
from nltk.corpus import wordnet
import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

nltk.download('wordnet')
nltk.download('omw-1.4')

nlp = spacy.load('en_core_web_sm')

def generate_synonyms(tag):
    synonyms = set()
    for syn in wordnet.synsets(tag):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return synonyms

def generate_abbreviations(tag):
    words = tag.split()
    abbreviation = ''.join([word[0].upper() for word in words])
    return {abbreviation, abbreviation.lower(), abbreviation.capitalize()}

def generate_expansions(tag):
    expansions = {
        'ai': ['Artificial Intelligence'],
        'ml': ['Machine Learning'],
    }
    lower_tag = tag.lower()
    if lower_tag in expansions:
        return set(expansions[lower_tag])
    return set()

def generate_case_variations(tag):
    return {tag.lower(), tag.upper(), tag.capitalize()}

def generate_misspellings(tag):
    misspellings = set()
    if len(tag) > 3:
        misspellings.add(tag[:-1] + tag[-1] * 2)
    return misspellings

def generate_aliases(tag):
    aliases = set()
    
    # Generate various types of aliases
    aliases.update(generate_synonyms(tag))
    aliases.update(generate_abbreviations(tag))
    aliases.update(generate_expansions(tag))
    aliases.update(generate_case_variations(tag))
    aliases.update(generate_misspellings(tag))
    
    # Removing all the exact matches
    aliases.discard(tag)
    
    #Thought of removing very similar redundant tags alone, we can remove this, if we dont want.
    filtered_aliases = {alias for alias in aliases if fuzz.ratio(tag, alias) < 85}
    
    return filtered_aliases
    

new_tag = "AI"
aliases = generate_aliases(new_tag)
print(f"Original Tag: {new_tag}")
print("Generated Aliases:")
for alias in aliases:
    print(f"- {alias}")
