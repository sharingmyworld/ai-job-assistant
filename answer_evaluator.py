import re


QUESTION_CONCEPTS = {
    "lista a krotka": {
        "list": ["lista", "list", "mutowal", "zmien"],
        "tuple": ["krotk", "tuple", "niemutowal"],
        "use": ["zastos", "uży", "wydajno", "hash"]
    },
    "where a having": {
        "where": ["where", "przed grupow", "wiersz"],
        "having": ["having", "po grupow", "agreg"],
        "example": ["group by", "count", "sum", "avg"]
    },
    "inner join": {
        "inner": ["inner join", "wspól", "dopas"],
        "left": ["left join", "lewej", "null"],
        "example": ["tabela", "klucz", "rekord"]
    },
    "rest api": {
        "http": ["http", "get", "post", "put", "delete"],
        "resources": ["zasób", "endpoint", "url"],
        "quality": ["status", "walid", "auth", "wersjon"]
    },
    "wyjątk": {
        "syntax": ["try", "except"],
        "specific": ["konkretn", "typ wyjątku", "exception"],
        "cleanup": ["finally", "else", "log"]
    },
}


def _normalize(text):
    return re.sub(
        r"\s+",
        " ",
        str(text).lower()
    ).strip()


def _concept_groups(question):
    normalized = _normalize(question)

    for phrase, groups in QUESTION_CONCEPTS.items():
        if phrase in normalized:
            return groups

    return {}


def evaluate_answer(question, answer):
    clean_answer = _normalize(answer)
    words = clean_answer.split()
    word_count = len(words)

    if not clean_answer:
        return 0, "Brak odpowiedzi."

    score = 1
    feedback = []

    # Konkretność i rozwinięcie
    if word_count >= 25:
        score += 1
    else:
        feedback.append(
            "Rozwiń odpowiedź do co najmniej 25 słów."
        )

    # Trafność względem pytania
    question_words = {
        word
        for word in re.findall(
            r"[a-ząćęłńóśźż0-9]+",
            _normalize(question)
        )
        if len(word) >= 4
    }

    overlap = sum(
        1
        for word in question_words
        if word in clean_answer
    )

    if overlap >= 2:
        score += 1
    else:
        feedback.append(
            "Odnieś się bardziej bezpośrednio do treści pytania."
        )

    # Pojęcia kluczowe dla znanych pytań
    concept_groups = _concept_groups(question)

    if concept_groups:
        covered_groups = 0

        for keywords in concept_groups.values():
            if any(
                keyword in clean_answer
                for keyword in keywords
            ):
                covered_groups += 1

        coverage = (
            covered_groups / len(concept_groups)
        )

        if coverage >= 0.66:
            score += 1
        else:
            missing_count = (
                len(concept_groups) - covered_groups
            )
            feedback.append(
                f"Brakuje około {missing_count} kluczowych "
                "elementów technicznych."
            )
    elif word_count >= 50:
        score += 1

    # Przykład / STAR / rezultat
    evidence_markers = (
        "na przykład",
        "przykład",
        "w projekcie",
        "sytuacja",
        "zadanie",
        "działanie",
        "rezultat",
        "wynik",
        "dzięki temu",
        "wdrożyłem",
        "zrobiłem"
    )

    if any(
        marker in clean_answer
        for marker in evidence_markers
    ):
        score += 1
    else:
        feedback.append(
            "Dodaj konkretny przykład, działanie i rezultat."
        )

    score = min(score, 5)

    if score >= 5:
        summary = (
            "Bardzo dobra odpowiedź: trafna, konkretna "
            "i poparta przykładem."
        )
    elif score >= 4:
        summary = (
            "Dobra odpowiedź. Drobne uzupełnienie zwiększy "
            "jej siłę."
        )
    elif score >= 3:
        summary = (
            "Odpowiedź jest poprawna, ale wymaga większej "
            "konkretności."
        )
    else:
        summary = (
            "Odpowiedź wymaga rozwinięcia i lepszego "
            "powiązania z pytaniem."
        )

    if feedback:
        summary += " " + " ".join(feedback[:3])

    return score, summary
