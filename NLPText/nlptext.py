import spacy
from SpeechToText import speech2text

nlp = spacy.load("en_core_web_sm")

text = speech2text.speech_to_text()

TIME_WORDS = {
    "yesterday","today","tomorrow","tonight","now",
    "later","soon","morning","evening","afternoon"
}

def convert_to_sign_structure(sentence):

    doc = nlp(sentence)

    subject = None
    verb = None
    obj = None

    time = []
    location = []
    adjectives = []
    negation = None
    persons = []

    for token in doc:

        # phát hiện tên người
        if token.ent_type_ == "PERSON":
            persons.append(token.text)

        # VERB chính
        if token.dep_ == "ROOT":
            verb = token.lemma_

        # SUBJECT
        if token.dep_ in ["nsubj","csubj"]:
            subject = token.text

        # PASSIVE SUBJECT
        if token.dep_ in ["nsubjpass","csubjpass"]:
            obj = token.text

        # OBJECT
        if token.dep_ in ["dobj","iobj","attr","oprd"]:
            obj = token.text

        # ADJECTIVE COMPLEMENT
        if token.dep_ == "acomp":
            adjectives.append(token.text)

        # PREPOSITIONAL OBJECT
        if token.dep_ == "prep":
            for child in token.children:
                if child.dep_ == "pobj":
                    location.append(child.text)

        # PASSIVE AGENT
        if token.dep_ == "agent":
            for child in token.children:
                if child.dep_ == "pobj":
                    subject = child.text

        # TIME
        if token.text.lower() in TIME_WORDS:
            time.append(token.text)

        # NEGATION
        if token.dep_ == "neg":
            negation = token.text

        # NOUN MODIFIER
        if token.dep_ in ["compound","amod"]:
            adjectives.append(token.text)

    def split_name(name):
        return list(name.upper())

    output = []

    output.extend(time)
    output.extend(location)

    if subject:
        if subject in persons:
            output.extend(split_name(subject))
        else:
            output.append(subject)

    if negation:
        output.append(negation)

    if verb and verb != "be":
        output.append(verb)

    if obj:
        if obj in persons:
            output.extend(split_name(obj))
        else:
            output.append(obj)

    output.extend(adjectives)

    print("SIGN STRUCTURE:", " ".join(output))
    return output


print(convert_to_sign_structure(text))