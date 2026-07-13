import re


GENERIC_TITLES = {
    "oferta pracy",
    "job offer",
    "ogłoszenie",
    "praca",
    "stanowisko",
    "about the job",
    "opis stanowiska",
    "job description",
    "kariera",
    "career",
    "dołącz do nas",
    "join us",
}


BLOCKED_PHRASES = (
    "zakres obowiązków",
    "twoje obowiązki",
    "obowiązki",
    "wymagania",
    "mile widziane",
    "oferujemy",
    "benefity",
    "responsibilities",
    "requirements",
    "what we offer",
    "about us",
    "o nas",
    "lokalizacja",
    "location",
    "wynagrodzenie",
    "salary",
    "opis stanowiska",
    "job description",
)


TITLE_KEYWORDS = (
    "developer",
    "engineer",
    "programista",
    "analityk",
    "analyst",
    "specjalista",
    "specialist",
    "manager",
    "kierownik",
    "consultant",
    "konsultant",
    "designer",
    "administrator",
    "architect",
    "architekt",
    "tester",
    "qa",
    "rekruter",
    "recruiter",
    "accountant",
    "księgowy",
    "devops",
    "product owner",
    "project manager",
    "scrum master",
    "support",
    "sales",
    "marketing",
    "intern",
    "stażysta",
    "staż",
    "assistant",
    "asystent",
    "coordinator",
    "koordynator",
    "technician",
    "technik",
    "operator",
    "doradca",
    "advisor",
    "lider",
    "lead",
    "head",
    "director",
    "dyrektor",
)


SENIORITY_WORDS = (
    "junior",
    "mid",
    "middle",
    "senior",
    "lead",
    "principal",
    "intern",
    "stażysta",
    "młodszy",
    "starszy",
)


def _clean_line(line):
    line = re.sub(
        r"^[\s\-–—•|:>#*]+",
        "",
        line
    )
    line = re.sub(
        r"[\s\-–—•|:]+$",
        "",
        line
    )
    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


def _normalize_candidate(text):
    candidate = _clean_line(text)

    candidate = re.split(
        r"[.!?;]",
        candidate,
        maxsplit=1
    )[0].strip()

    candidate = re.sub(
        r"(?i)^(?:na stanowisko|stanowisko|position|role|rola)\s*[:\-–—]?\s*",
        "",
        candidate
    )

    return candidate.strip()


def _score_candidate(line, index):
    if not line:
        return -100

    lowered = line.lower()

    if lowered in GENERIC_TITLES:
        return -100

    if any(
        phrase in lowered
        for phrase in BLOCKED_PHRASES
    ):
        return -100

    words = line.split()

    if len(line) < 3 or len(line) > 100:
        return -100

    if len(words) > 12:
        return -100

    score = 0

    if index < 3:
        score += 4
    elif index < 8:
        score += 2

    if any(
        keyword in lowered
        for keyword in TITLE_KEYWORDS
    ):
        score += 6

    if any(
        word in lowered
        for word in SENIORITY_WORDS
    ):
        score += 2

    letters = [
        char
        for char in line
        if char.isalpha()
    ]

    if letters:
        uppercase_ratio = (
            sum(char.isupper() for char in letters)
            / len(letters)
        )

        if uppercase_ratio > 0.65:
            score += 3

    if 2 <= len(words) <= 7:
        score += 2

    if ":" in line:
        score -= 1

    if line.endswith((".", "!", "?", ";")):
        score -= 2

    return score


def detect_job_title(job_offer):
    if not job_offer or not job_offer.strip():
        return ""

    text = job_offer.strip()

    patterns = (
        r"(?im)^\s*(?:stanowisko|position|job title|rola|role)\s*[:\-–—]\s*(.+)$",
        r"(?im)^\s*(?:poszukujemy|szukamy|we are looking for|looking for)\s+(?:osoby na stanowisko\s+|na stanowisko\s+|an?\s+)?(.+)$",
        r"(?im)^\s*(?:dołącz do nas jako|join us as)\s+(.+)$",
        r"(?im)^\s*(?:rekrutujemy na stanowisko|recruiting for)\s+(.+)$",
    )

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            candidate = _normalize_candidate(
                match.group(1)
            )

            if (
                candidate
                and 3 <= len(candidate) <= 100
            ):
                return candidate

    lines = [
        _clean_line(line)
        for line in text.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    best_candidate = ""
    best_score = -100

    for index, line in enumerate(lines[:20]):
        candidate = _normalize_candidate(line)
        score = _score_candidate(
            candidate,
            index
        )

        if score > best_score:
            best_candidate = candidate
            best_score = score

    if best_score >= 5:
        return best_candidate

    return ""
