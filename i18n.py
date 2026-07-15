import functools
import re
import streamlit as st

TRANSLATIONS = {
    "Brak zmiennej AI_JOB_COOKIE_PASSWORD. Ustaw bezpieczny klucz przed uruchomieniem aplikacji.": "AI_JOB_COOKIE_PASSWORD is missing. Set a secure key before starting the application.",
    "Baza danych jest chwilowo niedostępna. Twoje dane nie zostały utracone.": "The database is temporarily unavailable. Your data has not been lost.",
    "Spróbuj ponownie": "Try again",
    "Konto i wszystkie dane zostały trwale usunięte.": "Your account and all associated data have been permanently deleted.",
    "Logowanie": "Login", "Rejestracja": "Register", "Hasło": "Password",
    "Nie wylogowuj mnie": "Keep me signed in", "Zaloguj się": "Sign in",
    "Nieprawidłowy login lub hasło.": "Invalid username or password.",
    "Nowy login": "New username", "Nowe hasło": "New password",
    "Zapoznałem(-am) się z Polityką prywatności.": "I have read the Privacy Policy.",
    "Politykę prywatności znajdziesz w menu po zalogowaniu oraz pod adresem aplikacji w sekcji „Polityka prywatności”.": "The Privacy Policy is available from the application menu after signing in.",
    "Utwórz konto": "Create account",
    "Przed utworzeniem konta zapoznaj się z Polityką prywatności.": "Please read the Privacy Policy before creating an account.",
    "Login musi mieć co najmniej 3 znaki.": "The username must contain at least 3 characters.",
    "Hasło musi mieć co najmniej 8 znaków.": "The password must contain at least 8 characters.",
    "Konto zostało utworzone. Możesz się zalogować.": "Your account has been created. You can now sign in.",
    "Użytkownik o takiej nazwie już istnieje.": "A user with this username already exists.",
    "Konto": "Account", "Zalogowany jako:": "Signed in as:", "Menu": "Menu",
    "Analiza CV": "CV Analysis", "Historia": "History", "Plan nauki": "Learning Plan",
    "Aplikacje": "Applications", "Wersje CV": "CV Versions",
    "Przygotowanie do rozmowy": "Interview Preparation", "Profil": "Profile",
    "Polityka prywatności": "Privacy Policy", "Wyloguj się": "Sign out",
    "Nie udało się połączyć z bazą danych. Spróbuj ponownie za chwilę.": "Could not connect to the database. Please try again shortly.",
    "Dashboard": "Dashboard", "Historia analiz": "Analysis History",
    "Liczba analiz": "Number of analyses", "Średni wynik": "Average score",
    "Najlepszy wynik": "Best score", "Postęp nauki": "Learning progress",
    "Analiza postępu": "Progress analysis", "Data": "Date", "Dopasowanie CV": "CV match",
    "Najczęściej brakujące umiejętności": "Most frequently missing skills",
    "Najczęściej wykrywane umiejętności": "Most frequently detected skills",
    "Postęp roadmapy": "Roadmap progress", "Twój cel": "Your goal", "Pozostało": "Remaining",
    "Brak danych do wyświetlenia.": "No data to display.", "Brak danych.": "No data.",
    "Brak danych": "No data", "Wynik analizy": "Analysis result",
    "Wynik": "Score", "Znalezione umiejętności": "Skills found",
    "Brakujące umiejętności": "Missing skills", "Sugestie": "Suggestions",
    "Wybierz plik PDF z CV": "Choose a CV PDF file", "Oferta pracy": "Job offer",
    "Analizuj CV": "Analyze CV", "Wklej ofertę pracy.": "Paste the job offer.",
    "Wgraj CV w formacie PDF.": "Upload your CV as a PDF file.",
    "Raport ATS": "ATS Report", "Znalezione słowa kluczowe": "Keywords found",
    "Brakujące słowa kluczowe": "Missing keywords", "Raport PDF": "PDF Report",
    "Pobierz raport": "Download report", "Dodaj do Trackera aplikacji": "Add to Application Tracker",
    "Firma": "Company", "Stanowisko": "Position", "Status": "Status", "Notatki": "Notes",
    "Dodaj aplikację": "Add application", "Tracker aplikacji": "Application Tracker",
    "Podsumowanie": "Summary", "Wszystkie": "All", "Wysłane": "Sent",
    "Rozmowy": "Interviews", "Oferty": "Offers", "Skuteczność": "Effectiveness",
    "Filtrowanie": "Filters", "Szukaj": "Search", "Usuń": "Delete", "Edytuj": "Edit",
    "Zapisz": "Save", "Anuluj": "Cancel", "Plan nauki jest pusty. Wykonaj analizę CV, aby dodać brakujące umiejętności.": "Your learning plan is empty. Run a CV analysis to add missing skills.",
    "Plan jest automatycznie tworzony z brakujących umiejętności wykrytych podczas analizy CV.": "The plan is automatically created from missing skills detected during CV analysis.",
    "Cel tygodniowy": "Weekly goal", "Roadmapa": "Roadmap", "Ukończone": "Completed",
    "Do zrobienia": "To do", "Priorytet": "Priority", "Wysoki": "High",
    "Średni": "Medium", "Niski": "Low", "Przygotowanie do rozmowy rekrutacyjnej": "Interview Preparation",
    "Plan przygotowania": "Preparation plan", "Pytania techniczne": "Technical questions",
    "Pytania HR": "HR questions", "Feedback po rozmowie": "Post-interview feedback",
    "Mock Interview": "Mock Interview", "Odpowiedź": "Answer", "Następne pytanie": "Next question",
    "Zakończ rozmowę": "Finish interview", "Eksport danych": "Data export",
    "Eksportuj moje dane": "Export my data", "Zmień hasło": "Change password",
    "Obecne hasło": "Current password", "Powtórz nowe hasło": "Repeat new password",
    "Strefa niebezpieczna": "Danger zone",
    "Rozumiem, że tej operacji nie można cofnąć.": "I understand that this action cannot be undone.",
    "Potwierdź hasłem": "Confirm with your password", "Wpisz USUŃ KONTO": "Type DELETE ACCOUNT",
    "Usuń konto i wszystkie dane": "Delete account and all data", "Career Insights": "Career Insights",
}


# Complete English UI coverage for labels, messages, statuses and interview content.
TRANSLATIONS.update({
    "Język / Language": "Language",
    "Polski": "Polish",
    "Tutaj możesz śledzić swoje postępy.": "Track your progress here.",
    "Porównaj swoje CV z ofertą pracy i sprawdź dopasowanie.": "Compare your CV with a job posting and check the match.",
    "Wklej ofertę pracy": "Paste the job posting", "Nazwa stanowiska lub firmy": "Job title or company",
    "Nazwa wersji CV": "CV version name", "Wybierz CV (PDF)": "Choose CV (PDF)",
    "Dodaj tę ofertę do trackera aplikacji": "Add this job posting to the application tracker",
    "Dodaj do aplikacji": "Add to applications", "Podaj nazwę firmy.": "Enter the company name.",
    "Podaj nazwę stanowiska.": "Enter the job title.", "Planowana": "Planned", "Wysłana": "Sent",
    "Rozmowa HR": "HR interview", "Rozmowa techniczna": "Technical interview", "Oferta": "Offer",
    "Odrzucona": "Rejected", "Wycofana": "Withdrawn", "Oczekuję na decyzję": "Awaiting decision",
    "Oferta została dodana do trackera aplikacji.": "The job posting has been added to the application tracker.",
    "Nie znaleziono pasujących umiejętności.": "No matching skills were found.",
    "Brak brakujących umiejętności.": "No missing skills.", "Generuj raport PDF": "Generate PDF report",
    "Raport został wygenerowany.": "The report has been generated.", "Pobierz raport PDF": "Download PDF report",
    "ważne informacje...": "important information...", "Zapisz aplikację": "Save application",
    "Aplikacja została zapisana.": "The application has been saved.", "Wersja CV": "CV version",
    "Wysłane": "Sent", "Skuteczność aplikacji": "Application effectiveness", "Średnie dopasowanie": "Average match",
    "Średnie przy rozmowie": "Average with interview", "Średnie bez rozmowy": "Average without interview",
    "Na obecnych danych wyższe dopasowanie CV nie przekłada się jeszcze na więcej rozmów.": "Based on the current data, a higher CV match does not yet lead to more interviews.",
    "Średnie dopasowanie jest obecnie takie samo.": "The average match is currently the same.",
    "Brak wystarczających danych o dopasowaniu CV. Dodawaj oferty do trackera bezpośrednio z analizy CV.": "There is not enough CV match data. Add job postings to the tracker directly from CV Analysis.",
    "Brak aplikacji spełniających wybrane kryteria.": "No applications match the selected criteria.",
    "Edytuj aplikację": "Edit application", "Zapisz zmiany": "Save changes", "Aplikacja została zaktualizowana.": "The application has been updated.",
    "Otwórz ofertę": "Open job posting", "Od wysłania aplikacji minęło co najmniej 7 dni. Warto wysłać follow-up.": "At least 7 days have passed since the application was sent. Consider sending a follow-up.",
    "Generuj wiadomość follow-up": "Generate follow-up message", "Język wiadomości": "Message language",
    "Gotowa wiadomość": "Ready-to-send message", "Termin kolejnego działania": "Next action date",
    "Zapisz termin": "Save date", "Termin został zapisany.": "The date has been saved.", "Zapisz notatki": "Save notes",
    "Notatki zostały zapisane.": "Notes have been saved.",
    "Wnioski są tworzone na podstawie historii analiz CV, planu nauki i trackera aplikacji.": "Insights are generated from your CV analysis history, learning plan, and application tracker.",
    "Brak wystarczających danych. Wykonaj analizy CV i dodaj aplikacje, aby zobaczyć wnioski.": "Not enough data yet. Run CV analyses and add applications to see insights.",
    "Analizy CV": "CV analyses", "Umiejętności w planie": "Skills in plan", "Najczęstsze braki": "Most common skill gaps",
    "Umiejętność": "Skill", "Liczba wystąpień": "Occurrences", "Wystąpienia": "Occurrences",
    "W historii nie ma zapisanych brakujących umiejętności.": "No missing skills are saved in the analysis history.",
    "Najlepiej dopasowane stanowiska": "Best-matching positions", "Brak danych o stanowiskach.": "No position data.",
    "Przejście do rozmowy": "Interview conversion", "Przejście do oferty": "Offer conversion",
    "Brak danych z trackera aplikacji.": "No data from the application tracker.", "Skuteczność wersji CV": "CV version effectiveness",
    "Brak danych o wersjach CV.": "No CV version data.", "Wnioski z rozmów": "Interview insights",
    "Trudność": "Difficulty", "Przechodzę dalej": "Moving forward", "Średnia samoocena": "Average self-rating",
    "Średnia trudność": "Average difficulty", "Przejście dalej": "Progression rate", "Wyniki według typu rozmowy": "Results by interview type",
    "Najczęstsze obszary do poprawy": "Most common areas for improvement", "Najczęściej trudne pytania": "Most difficult recurring questions",
    "Średnia samoocena jest niska. Warto częściej ćwiczyć odpowiedzi.": "The average self-rating is low. Practice answering more often.",
    "Rozmowy są oceniane jako trudne. Skup się na pytaniach technicznych i symulacjach.": "Interviews are rated as difficult. Focus on technical questions and mock sessions.",
    "Wyniki rozmów wyglądają stabilnie. Kontynuuj przygotowania i analizuj powtarzające się pytania.": "Interview results look stable. Keep preparing and review recurring questions.",
    "Brak feedbacku z rozmów. Dodaj go w module Przygotowanie do rozmowy.": "No interview feedback yet. Add it in Interview Preparation.",
    "Analiza Mock Interview": "Mock Interview analysis", "Aplikacja ID": "Application ID", "Pytanie": "Question",
    "Średnia ocena": "Average score", "Słabe odpowiedzi": "Weak answers", "Pytania wymagające ćwiczenia": "Questions to practice",
    "Wyniki sesji według aplikacji": "Session results by application", "Odpowiedzi wymagają dopracowania. Skup się na konkretach, przykładach i rezultatach.": "Your answers need refinement. Focus on specifics, examples, and results.",
    "Mock Interview wskazuje na dobre przygotowanie. Skup się teraz na płynności i naturalności odpowiedzi.": "Mock Interview indicates good preparation. Now focus on fluency and natural delivery.",
    "Brak ukończonych odpowiedzi w Mock Interview.": "No completed Mock Interview answers.", "Brak danych z Mock Interview. Wykonaj sesję, aby zobaczyć analizę.": "No Mock Interview data. Complete a session to see the analysis.",
    "Rekomendowany następny krok": "Recommended next step", "Wszystkie umiejętności w planie nauki są oznaczone jako ukończone.": "All skills in the learning plan are marked as completed.",
    "Brak analiz z zapisanymi wersjami CV.": "No analyses with saved CV versions.", "Brakujące": "Missing",
    "Porównanie wersji": "Version comparison", "Średnie dopasowanie (%)": "Average match (%)", "Najlepszy wynik": "Best score",
    "Wyniki aplikacji według wersji CV": "Application results by CV version", "Skuteczność rozmów": "Interview success rate",
    "Najbliższe wydarzenia rekrutacyjne": "Upcoming recruitment events", "Wykonaj analizę CV, aby dodać umiejętności.": "Run a CV analysis to add skills.",
    "Ogólny postęp planu": "Overall plan progress", "Następny priorytet": "Next priority", "Postęp celu": "Goal progress",
    "Cel tygodniowy został zapisany.": "Weekly goal saved.", "Cel tygodniowy osiągnięty!": "Weekly goal achieved!", "Usuń cel tygodniowy": "Delete weekly goal",
    "Porównaj dwie analizy": "Compare two analyses", "Wybierz dwie różne analizy.": "Select two different analyses.",
    "Do porównania potrzebujesz co najmniej dwóch analiz.": "You need at least two analyses to compare.", "Wspólne umiejętności": "Shared skills",
    "Nowe umiejętności": "New skills", "Utracone umiejętności": "Lost skills", "Porównanie braków": "Skill-gap comparison",
    "Uzupełnione braki": "Resolved gaps", "Nadal brakujące": "Still missing", "Zmiana braków": "Change in gaps",
    "Brak zapisanych analiz.": "No saved analyses.", "Brak analiz spełniających wybrane kryteria.": "No analyses match the selected criteria.",
    "Pobierz przefiltrowaną historię CSV": "Download filtered history CSV", "Analiza została usunięta.": "The analysis has been deleted.",
    "Szukaj po stanowisku lub umiejętności": "Search by position or skill", "Liczba kroków roadmapy": "Number of roadmap steps",
    "Postęp roadmap": "Roadmap progress", "Brak zadań spełniających wybrane kryteria.": "No tasks match the selected criteria.",
    "Wybierz aplikację, aby otrzymać plan przygotowań i zestaw pytań rekrutacyjnych.": "Select an application to receive a preparation plan and a set of interview questions.",
    "Brak aplikacji. Najpierw dodaj ofertę do trackera.": "No applications yet. Add a job posting to the tracker first.", "Wybierz aplikację": "Select application",
    "Plan przygotowania": "Preparation plan", "Postęp przygotowania": "Preparation progress", "Pytania do firmy": "Questions for the company",
    "Dodaj lub zaktualizuj feedback": "Add or update feedback", "Nie zapisano jeszcze feedbacku dla tej aplikacji.": "No feedback has been saved for this application yet.",
    "Poziom trudności": "Difficulty level", "Jak oceniasz swoją rozmowę?": "How do you rate your interview?", "Wynik rozmowy": "Interview outcome",
    "Co poszło dobrze?": "What went well?", "Co poprawić?": "What could be improved?", "Jakie pytania sprawiły największą trudność?": "Which questions were the most difficult?",
    "Zapisz feedback": "Save feedback", "Feedback został zapisany.": "Feedback has been saved.",
    "Odpowiadaj na pytania jedno po drugim. Sesja zapisuje się w bazie.": "Answer the questions one by one. Your session is saved to the database.",
    "Brak aplikacji w trackerze.": "No applications in the tracker.", "Postęp sesji": "Session progress", "Twoja odpowiedź": "Your answer",
    "Wpisz odpowiedź.": "Enter an answer.", "Zapisz i przejdź dalej": "Save and continue", "Sesja Mock Interview ukończona!": "Mock Interview session completed!",
    "Wynik sesji": "Session score", "Odpowiedź zapisana.": "Answer saved.", "Rozpocznij sesję od nowa": "Restart session",
    "Profil": "Profile", "Analizy": "Analyses", "Eksport obejmuje": "Export includes", "rekordów.": "records.",
    "Pobierz swoje analizy, plan nauki, aplikacje oraz dane przygotowania do rozmów w jednym pliku JSON.": "Download your analyses, learning plan, applications, and interview preparation data in one JSON file.",
    "Nie udało się przygotować eksportu danych.": "Could not prepare the data export.", "Strefa niebezpieczna": "Danger zone",
    "Usunięcie konta jest trwałe. Zostaną usunięte analizy CV, plan nauki, aplikacje oraz dane rozmów.": "Account deletion is permanent. CV analyses, learning plan, applications, and interview data will be deleted.",
    "Potwierdź, że rozumiesz skutki usunięcia konta.": "Confirm that you understand the consequences of deleting your account.",
    "Wpisz dokładnie: USUŃ KONTO": "Type exactly: DELETE ACCOUNT", "USUŃ KONTO": "DELETE ACCOUNT",
    "Nie udało się usunąć konta. Spróbuj ponownie później.": "Could not delete the account. Please try again later.",
    "Nieprawidłowe hasło.": "Incorrect password.", "Nowe hasła nie są takie same.": "The new passwords do not match.",
    "Nowe hasło musi mieć co najmniej 8 znaków.": "The new password must contain at least 8 characters.",
    "Hasło zostało zmienione.": "Password changed.", "Data aplikacji": "Application date", "Utworzono": "Created", "Zaktualizowano": "Updated",
    "Dopasowanie": "Match", "Termin wydarzenia": "Event date", "Typ wydarzenia": "Event type", "Etykieta": "Label",
    "Kolejność": "Order", "Postęp analiz": "Analysis progress", "Umiejętności": "Skills", "Postęp roadmapy": "Roadmap progress",
})

QUESTION_TRANSLATIONS = {
"Jaka jest różnica między listą a krotką w Pythonie?":"What is the difference between a list and a tuple in Python?",
"Jak działa obsługa wyjątków try/except?":"How does try/except exception handling work?",
"Jak działa obsługa wyjątków w Pythonie?":"How does exception handling work in Python?",
"Czym różni się metoda instancji od metody statycznej?":"What is the difference between an instance method and a static method?",
"Jak zarządzasz zależnościami i środowiskiem projektu?":"How do you manage project dependencies and environments?",
"Jak przetestowałbyś funkcję przetwarzającą dane?":"How would you test a data-processing function?",
"Jaka jest różnica między WHERE a HAVING?":"What is the difference between WHERE and HAVING?",
"Wyjaśnij INNER JOIN, LEFT JOIN i FULL JOIN.":"Explain INNER JOIN, LEFT JOIN, and FULL JOIN.",
"Wyjaśnij różnicę między INNER JOIN i LEFT JOIN.":"Explain the difference between INNER JOIN and LEFT JOIN.",
"Do czego służą funkcje okienkowe?":"What are window functions used for?",
"Jak znaleźć duplikaty w tabeli?":"How do you find duplicates in a table?",
"Jak zoptymalizować wolne zapytanie SQL?":"How do you optimize a slow SQL query?",
"Jak podszedłbyś do optymalizacji wolnego zapytania?":"How would you approach optimizing a slow query?",
"Jak przygotowujesz dane przed analizą?":"How do you prepare data before analysis?",
"Jak radzisz sobie z brakującymi wartościami?":"How do you handle missing values?",
"Jak dobierasz właściwy typ wykresu?":"How do you choose the right chart type?",
"Jak sprawdzasz jakość i poprawność danych?":"How do you check data quality and correctness?",
"Jak sprawdzasz jakość danych przed analizą?":"How do you check data quality before analysis?",
"Jak wyjaśniłbyś wynik analizy osobie nietechnicznej?":"How would you explain an analysis result to a non-technical person?",
"Jak prezentujesz wynik analizy osobie nietechnicznej?":"How do you present an analysis result to a non-technical person?",
"Jak zaprojektowałbyś REST API?":"How would you design a REST API?",
"Czym różni się autoryzacja od uwierzytelniania?":"What is the difference between authorization and authentication?",
"Jak obsłużyć błędy i walidację danych w API?":"How do you handle errors and data validation in an API?",
"Jak obsłużyć walidację i błędy w API?":"How do you handle validation and errors in an API?",
"Jak zapobiegać problemom z wydajnością bazy?":"How do you prevent database performance issues?",
"Jak monitorować aplikację produkcyjną?":"How do you monitor a production application?",
"Jak diagnozujesz problem z wydajnością backendu?":"How do you diagnose a backend performance problem?",
"Jak działa DOM?":"How does the DOM work?", "Czym różni się stan komponentu od propsów?":"What is the difference between component state and props?",
"Jak ograniczyć niepotrzebne renderowanie?":"How do you reduce unnecessary rendering?", "Jak obsłużyć błędy wywołań API?":"How do you handle API call errors?",
"Jak zapewnić responsywność interfejsu?":"How do you ensure a responsive interface?", "Jaka jest różnica między obrazem a kontenerem Docker?":"What is the difference between a Docker image and a container?",
"Jak działa pipeline CI/CD?":"How does a CI/CD pipeline work?", "Jak zarządzać sekretami w środowisku produkcyjnym?":"How do you manage secrets in a production environment?",
"Jak monitorować dostępność aplikacji?":"How do you monitor application availability?", "Jak zaplanować bezpieczny rollback wdrożenia?":"How do you plan a safe deployment rollback?",
"Opowiedz o projekcie, z którego jesteś najbardziej dumny.":"Tell me about the project you are most proud of.", "Jak rozwiązujesz trudne problemy techniczne?":"How do you solve difficult technical problems?",
"Jak uczysz się nowych technologii?":"How do you learn new technologies?", "Jak organizujesz pracę nad zadaniem?":"How do you organize your work on a task?",
"Jak reagujesz na feedback?":"How do you respond to feedback?", "Opowiedz krótko o sobie.":"Tell me briefly about yourself.",
"Dlaczego interesuje Cię to stanowisko?":"Why are you interested in this position?", "Dlaczego chcesz pracować w tej firmie?":"Why do you want to work for this company?",
"Jakie są Twoje mocne strony?":"What are your strengths?", "Nad czym obecnie pracujesz rozwojowo?":"What are you currently working on improving?",
"Opowiedz o trudnej sytuacji i sposobie jej rozwiązania.":"Tell me about a difficult situation and how you resolved it.", "Jak radzisz sobie z presją czasu?":"How do you handle time pressure?",
"Jakiego środowiska pracy szukasz?":"What kind of work environment are you looking for?", "Jakie masz oczekiwania finansowe?":"What are your salary expectations?",
"Kiedy możesz rozpocząć pracę?":"When can you start?", "Opisz trudny problem i sposób jego rozwiązania.":"Describe a difficult problem and how you solved it.",
"Jak wygląda typowy dzień na tym stanowisku?":"What does a typical day in this role look like?", "Jakie są najważniejsze cele na pierwsze 3 miesiące?":"What are the most important goals for the first three months?",
"Jak wygląda współpraca w zespole?":"What does collaboration within the team look like?", "Jak mierzone są wyniki na tym stanowisku?":"How is performance measured in this role?",
"Jakie są kolejne etapy procesu rekrutacyjnego?":"What are the next stages of the recruitment process?",
}
TRANSLATIONS.update(QUESTION_TRANSLATIONS)

PREP_TRANSLATIONS = {
"Przeczytaj ponownie ofertę i zaznacz 5 najważniejszych wymagań.":"Review the job posting and identify the five most important requirements.",
"Przygotuj 60-sekundowe przedstawienie swojego doświadczenia.":"Prepare a 60-second introduction to your experience.",
"Wybierz 2 projekty, które najlepiej pasują do stanowiska.":"Choose two projects that best match the role.",
"Przygotuj odpowiedzi metodą STAR do 3 sytuacji zawodowych.":"Prepare STAR-method answers for three professional situations.",
"Przećwicz pytania techniczne i zapisz krótkie odpowiedzi.":"Practice technical questions and write down short answers.",
"Przygotuj 4 pytania do rekrutera lub zespołu.":"Prepare four questions for the recruiter or team.",
"Sprawdź informacje o firmie, produkcie i kulturze organizacyjnej.":"Research the company, product, and organizational culture.",
"Przygotuj środowisko, sprzęt i dokumenty przed rozmową.":"Prepare your environment, equipment, and documents before the interview.",
"Skup się na brakach względem oferty i przygotuj przykłady szybkiej nauki.":"Focus on gaps relative to the job posting and prepare examples of learning quickly.",
"Podkreśl mocne dopasowanie i przygotuj konkretne dowody osiągnięć.":"Emphasize your strong match and prepare concrete evidence of achievements.",
}
TRANSLATIONS.update(PREP_TRANSLATIONS)
TRANSLATIONS.update({
"Nie udało się pewnie wykryć stanowiska. Wpisz je ręcznie.":"The position could not be detected reliably. Enter it manually.",
"Kontakt do rekrutera, termin rozmowy, ważne informacje...":"Recruiter contact, interview date, important information...",
"Aplikacje zakończone rozmową mają średnio o":"Applications that reached an interview have an average",
"Najwyższe średnie dopasowanie masz do stanowiska **":"Your highest average match is for the position **",
"** ze średnim dopasowaniem":"** with an average match of",
"Średnia_samoocena":"Average_self_rating", "Średnia_trudność":"Average_difficulty",
"Najlepszy kolejny krok: rozpocznij lub kontynuuj naukę **":"Best next step: start or continue learning **",
"Średnie dopasowanie CV dla aplikacji zakończonych rozmową wynosi **":"The average CV match for applications that reached an interview is **",
"Na obecnych danych wyższe dopasowanie CV nie daje jeszcze wyraźnie większej szansy na rozmowę.":"Based on the current data, a higher CV match does not yet clearly increase the chance of an interview.",
"Aplikacje z rozmową mają średnio o **":"Applications that reached an interview have an average **",
"Średnie_dopasowanie":"Average_match", "Średnie_dopasowanie:Q":"Average_match:Q",
"** — średnie dopasowanie":"** — average match",
"Plan nauki jest pusty. Wykonaj analizę CV, aby dodać umiejętności.":"The learning plan is empty. Run a CV analysis to add skills.",
"Ogólny postęp planu:":"Overall plan progress:", "Następny priorytet:":"Next priority:",
"### 🧩 Porównanie znalezionych umiejętności":"### 🧩 Comparison of found skills", "Liczba braków:":"Number of gaps:",
"Umiejętności:":"Skills:", "Brakujące:":"Missing:", "Notatki przed rozmową":"Pre-interview notes",
"Najważniejsze informacje, które chcesz zapamiętać":"Key information you want to remember", "Zapisz odpowiedź":"Save answer",
"Mocne odpowiedzi, przykłady, komunikacja...":"Strong answers, examples, communication...", "Braki techniczne, zbyt ogólne odpowiedzi...":"Technical gaps, overly general answers...",
"**Co poszło dobrze:**":"**What went well:**", "**Co poprawić:**":"**What could be improved:**",
"Wyjaśnij różnicę między listą a krotką w Pythonie.":"Explain the difference between a list and a tuple in Python.",
"Odpowiedzi są krótkie lub mało konkretne. Dodawaj przykłady i rezultaty.":"Answers are short or lack specifics. Add examples and results.",
"Przygotowanie wygląda dobrze. Warto dopracować konkretne przykłady.":"Your preparation looks good. Refine your concrete examples.",
"Odpowiedzi są rozbudowane i konkretne.":"Answers are detailed and specific.",
})


# Remaining UI strings found during the English-mode visual audit.
TRANSLATIONS.update({
    "Porównanie znalezionych umiejętności": "Comparison of found skills",
    "Znalezione umiejętności": "Skills found", "Generuj wiadomość follow-up": "Generate follow-up message",
    "Dodaj tę ofertę do trackera aplikacji": "Add this job posting to the application tracker",
    "Skuteczność aplikacji": "Application effectiveness", "Wyniki aplikacji według wersji CV": "Application results by CV version",
    "Zapisz i przejdź dalej": "Save and continue", "Sesja Mock Interview ukończona!": "Mock Interview session completed!",
    "Rozpocznij sesję od nowa": "Restart session", "Postęp roadmap": "Roadmap progress",
    "Kontakt w sprawach prywatności:": "Privacy contact:",
    "Administrator aplikacji nie uzupełnił jeszcze adresu kontaktowego.": "The application administrator has not provided a contact email address yet.",
    "Skills": "Skills",
    "Do nauki": "To learn", "W trakcie": "In progress",
    "Ogólny postęp planu: 0%": "Overall plan progress: 0%",
    "Wykryj stanowisko": "Detect job title",
    "np. Junior Python Developer — ABC Tech": "e.g. Junior Python Developer — ABC Tech",
    "np. Python Developer v2": "e.g. Python Developer v2",
    "Porównaj dwie analizy": "Compare two analyses", "Analiza A": "Analysis A", "Analiza B": "Analysis B",
    "Zmiana jest liczona od analizy A do analizy B.": "The change is calculated from analysis A to analysis B.",
    "Wynik A": "Score A", "Wynik B": "Score B", "Zmiana wyniku": "Score change",
    "Braki A": "Gaps A", "Braki B": "Gaps B", "Zmiana braków": "Change in gaps",
    "Nowe umiejętności": "New skills", "Utracone umiejętności": "Lost skills", "Wspólne umiejętności": "Shared skills",
    "Porównanie braków": "Skill-gap comparison", "Uzupełnione braki": "Resolved gaps", "Nowe braki": "New gaps", "Nadal brakujące": "Still missing",
    "Filtrowanie": "Filters", "Szukaj po stanowisku lub umiejętności": "Search by position or skill",
    "np. Python, SQL, Data Analyst": "e.g. Python, SQL, Data Analyst", "Zakres wyniku": "Score range", "Zakres dat": "Date range",
    "Pobierz przefiltrowaną historię CSV": "Download filtered history CSV", "Bez nazwy stanowiska": "Untitled position",
    "Analiza została usunięta.": "Analysis deleted.", "Brak daty": "No date",
    "Dodano": "Added", "Ostatnia zmiana": "Last updated",
    "Składnia, zmienne i typy danych": "Syntax, variables and data types",
    "Instrukcje warunkowe i pętle": "Conditionals and loops", "Funkcje i moduły": "Functions and modules",
    "Listy, słowniki, zbiory i krotki": "Lists, dictionaries, sets and tuples", "Obsługa plików i wyjątków": "File and exception handling",
    "Programowanie obiektowe": "Object-oriented programming", "Testy jednostkowe": "Unit testing",
    "Projekt praktyczny w Pythonie": "Practical Python project",
    "Odpowiedzi": "Responses", "Odrzucenia": "Rejections", "Szukaj firmy lub stanowiska": "Search by company or position",
    "Filtr statusu": "Status filter", "Znaleziono aplikacji": "Applications found", "Data aplikacji": "Application date",
    "Link do oferty": "Job posting link", "Status procesu": "Process status",
    "Najlepszy kolejny krok: rozpocznij lub kontynuuj naukę python (priorytet: Wysoki).": "Best next step: start or continue learning Python (priority: High).",
    "Bez nazwy wersji": "Untitled version", "Bez nazwy": "Untitled",
    "Average_match": "Average match", "Best_score": "Best score", "Number_of_analyses": "Number of analyses",
    "Średnie dopasowanie": "Average match",
    "Przeczytaj ponownie ofertę i zaznacz 5 najważniejszych wymagań.": "Review the job posting and identify the five most important requirements.",
    "Przygotuj 60-sekundowe przedstawienie swojego doświadczenia.": "Prepare a 60-second introduction to your experience.",
    "Wybierz 2 projekty, które najlepiej pasują do stanowiska.": "Choose two projects that best match the role.",
    "Przygotuj odpowiedzi metodą STAR do 3 sytuacji zawodowych.": "Prepare STAR-method answers for three professional situations.",
    "Przećwicz pytania techniczne i zapisz krótkie odpowiedzi.": "Practice technical questions and write down short answers.",
    "Przygotuj 4 pytania do rekrutera lub zespołu.": "Prepare four questions for the recruiter or team.",
    "Sprawdź informacje o firmie, produkcie i kulturze organizacyjnej.": "Research the company, product, and organizational culture.",
    "Przygotuj środowisko, sprzęt i dokumenty przed rozmową.": "Prepare your environment, equipment, and documents before the interview.",
})


# Strings returned by report/insight generators and persisted Polish values.
TRANSLATIONS.update({
    "Wynik ATS": "ATS score",
    "CV wymaga większej optymalizacji pod tę ofertę.": "The CV needs more optimization for this job posting.",
    "CV ma dobre podstawy, ale wymaga kilku poprawek.": "The CV has a good foundation but needs a few improvements.",
    "CV jest dobrze dopasowane do systemów ATS.": "The CV is well optimized for ATS systems.",
    "Wykryte sekcje CV:": "Detected CV sections:", "Brakujące sekcje:": "Missing sections:",
    "doświadczenie": "experience", "umiejętności": "skills", "wykształcenie": "education", "języki": "languages",
    "Nie znaleziono brakujących kluczowych umiejętności.": "No missing key skills were found.",
    "Wskazówka ATS: używaj słów kluczowych dokładnie tak, jak pojawiają się w ogłoszeniu.": "ATS tip: use keywords exactly as they appear in the job posting.",
    "Umiejętności, które warto mocniej podkreślić:": "Skills worth emphasizing more:",
    "Rozwiń doświadczenie związane z:": "Expand on your experience related to:",
    "Porównanie umiejętności": "Skills comparison", "Znalezione": "Found", "Brakujące": "Missing", "Liczba": "Count",
    "Najtrudniejsze pytania": "Most difficult questions", "Typ rozmowy": "Interview type",
    "Bez nazwy wersji": "Untitled version", "Bez nazwy": "Untitled", "Planowana": "Planned", "Brak danych": "No data",
    "Najlepszy kolejny krok: rozpocznij lub kontynuuj naukę python (priorytet: Wysoki).": "Best next step: start or continue learning Python (priority: High).",
    "Jakie są Your strengths?": "What are your strengths?",
})

REPLACEMENTS = [
    ("Znaleziono analiz:", "Analyses found:"), ("Znaleziono aplikacji:", "Applications found:"),
    ("Ogólny postęp planu:", "Overall plan progress:"), ("Następny priorytet:", "Next priority:"),
    ("Dodano:", "Added:"), ("Ostatnia zmiana:", "Last updated:"),
    ("Dopasowanie:", "Match:"), ("Liczba braków:", "Number of gaps:"), ("Umiejętności:", "Skills:"), ("Brakujące:", "Missing:"),
    ("Najlepsza wersja:", "Best version:"), ("Bez nazwy wersji", "Untitled version"),
    ("Zalogowany jako", "Signed in as"), ("Witaj ", "Welcome "),
    ("Brakujące kompetencje", "Missing skills"), ("Znalezione kompetencje", "Skills found"),
    ("Znalezione słowa kluczowe", "Keywords found"), ("Brakujące słowa kluczowe", "Missing keywords"),
    ("Najczęściej brakujące", "Most frequently missing"), ("Najczęściej wykrywane", "Most frequently detected"),
    ("Dopasowanie CV", "CV match"), ("Liczba analiz", "Number of analyses"),
    ("Średni wynik", "Average score"), ("Najlepszy wynik", "Best score"),
    ("Postęp nauki", "Learning progress"), ("Postęp roadmapy", "Roadmap progress"),
    ("Plan nauki", "Learning Plan"), ("Historia analiz", "Analysis History"),
    ("Przygotowanie do rozmowy", "Interview Preparation"), ("Pytania techniczne", "Technical questions"),
    ("Pytania HR", "HR questions"), ("Feedback po rozmowie", "Post-interview feedback"),
    ("Wersje CV", "CV Versions"), ("Polityka prywatności", "Privacy Policy"),
    ("Twoje mocne strony", "Your strengths"), ("Warto rozważyć dodanie", "Consider adding"),
    ("Przykładowy profil zawodowy", "Example professional profile"),
    ("Przykładowa zmiana opisu doświadczenia", "Example experience-description improvement"),
    ("Pozostało", "Remaining"), ("kroków", "steps"), ("kroki", "steps"), ("krok", "step"),
    ("dni", "days"), ("dzień", "day"),
    ("Najlepsza wersja", "Best version"), ("ze średnim dopasowaniem", "with an average match of"),
    ("Najlepsza wersja CV to", "The best CV version is"), ("Najwyższe średnie dopasowanie masz do stanowiska", "Your highest average match is for the position"),
    ("Najczęściej brakującą umiejętnością jest", "The most frequently missing skill is"), ("pojawiła się w", "it appeared in"),
    ("Najlepszy kolejny krok: rozpocznij lub kontynuuj naukę", "Best next step: start or continue learning"),
    ("Najczęściej powtarzający się obszar do poprawy", "Most frequently recurring area for improvement"),
    ("Najpierw przećwicz odpowiedź na pytanie", "First, practice answering the question"),
    ("Średnie dopasowanie CV dla aplikacji zakończonych rozmową wynosi", "The average CV match for applications that reached an interview is"),
    ("Aplikacje z rozmową mają średnio o", "Applications that reached an interview have an average"),
    ("Aplikacje zakończone rozmową mają średnio o", "Applications that reached an interview have an average"),
    ("wyższe dopasowanie CV", "higher CV match"), ("Liczba braków spadła o", "The number of gaps decreased by"),
    ("Liczba braków wzrosła o", "The number of gaps increased by"), ("Liczba brakujących umiejętności nie zmieniła się", "The number of missing skills has not changed"),
    ("Do celu pozostało", "Remaining to reach the goal"), ("Postęp planu", "Plan progress"), ("Postęp przygotowania", "Preparation progress"),
    ("Postęp sesji", "Session progress"), ("Brak daty", "No date"), ("Brak nowych braków", "No new gaps"),
    ("Brak nowych umiejętności", "No new skills"), ("Brak utraconych umiejętności", "No lost skills"),
    ("Brak uzupełnionych braków", "No resolved gaps"), ("Brak wspólnych braków", "No shared gaps"), ("Brak wspólnych umiejętności", "No shared skills"),
]

def get_language():
    return st.session_state.get("language", "pl")

def tr(value):
    if get_language() != "en" or not isinstance(value, str):
        return value
    leading = value[:len(value)-len(value.lstrip())]
    trailing = value[len(value.rstrip()):]
    body = value.strip()
    m = re.match(r"^([\W_]*)(.*)$", body, re.UNICODE)
    prefix, text = (m.group(1), m.group(2)) if m else ("", body)
    result = TRANSLATIONS.get(text, text)
    if result == text:
        # Translate embedded/numbered/generated Polish fragments as well as exact labels.
        # Longest keys first prevents shorter phrases from breaking a longer match.
        for source in sorted(TRANSLATIONS, key=len, reverse=True):
            if source in result:
                result = result.replace(source, TRANSLATIONS[source])
        for source, target in REPLACEMENTS:
            result = result.replace(source, target)
    return f"{leading}{prefix}{result}{trailing}"

def _value(value):
    if isinstance(value, str): return tr(value)
    if isinstance(value, list): return [_value(v) for v in value]
    if isinstance(value, tuple): return tuple(_value(v) for v in value)
    if isinstance(value, dict): return {tr(k) if isinstance(k, str) else k: _value(v) for k, v in value.items()}
    return value

def _wrap(obj, name):
    original = getattr(obj, name)
    @functools.wraps(original)
    def wrapped(*args, **kwargs):
        args = [_value(arg) for arg in args]
        for key in ("label", "help", "placeholder", "value"):
            if key in kwargs and isinstance(kwargs[key], str):
                kwargs[key] = tr(kwargs[key])
        return original(*args, **kwargs)
    setattr(obj, name, wrapped)

def _wrap_choice(obj, name):
    original = getattr(obj, name)
    @functools.wraps(original)
    def wrapped(label, options, *args, **kwargs):
        format_func = kwargs.get("format_func", str)
        kwargs["format_func"] = lambda option: tr(str(format_func(option)))
        return original(tr(label), options, *args, **kwargs)
    setattr(obj, name, wrapped)

def install_i18n():
    if st.session_state.get("_i18n_installed"): return
    methods = (
        "title","header","subheader","caption","write","markdown","success","warning","error","info",
        "button","checkbox","text_input","text_area","file_uploader","download_button","metric",
        "slider","date_input","number_input","expander","toggle"
    )
    try:
        from streamlit.delta_generator import DeltaGenerator
        objects = (st, st.sidebar, DeltaGenerator)
    except Exception:
        objects = (st, st.sidebar)
    for obj in objects:
        for name in methods:
            if hasattr(obj, name): _wrap(obj, name)
        for name in ("radio","selectbox","multiselect"):
            if hasattr(obj, name): _wrap_choice(obj, name)
    original_tabs = st.tabs
    st.tabs = lambda tabs, *a, **k: original_tabs([tr(x) for x in tabs], *a, **k)

    # Translate table content on display without mutating application data.
    for name in ("dataframe", "data_editor", "table"):
        if hasattr(st, name):
            original = getattr(st, name)
            def make_table_wrapper(fn):
                @functools.wraps(fn)
                def wrapped(data=None, *args, **kwargs):
                    try:
                        import pandas as pd
                        if get_language() == "en" and isinstance(data, pd.DataFrame):
                            data = data.copy()
                            data.columns = [tr(str(c)) for c in data.columns]
                            for col in data.columns:
                                if data[col].dtype == object:
                                    data[col] = data[col].map(lambda x: tr(x) if isinstance(x, str) else x)
                    except Exception:
                        pass
                    return fn(data, *args, **kwargs)
                return wrapped
            setattr(st, name, make_table_wrapper(original))

    if hasattr(st, "bar_chart"):
        original_bar_chart = st.bar_chart
        @functools.wraps(original_bar_chart)
        def translated_bar_chart(data=None, *args, **kwargs):
            try:
                import pandas as pd
                if get_language() == "en" and isinstance(data, (pd.DataFrame, pd.Series)):
                    data = data.copy()
                    if isinstance(data, pd.DataFrame):
                        data.columns = [tr(str(c)) for c in data.columns]
                        for col in data.columns:
                            if data[col].dtype == object:
                                data[col] = data[col].map(lambda x: tr(x) if isinstance(x, str) else x)
                    if getattr(data, "index", None) is not None:
                        data.index = [tr(x) if isinstance(x, str) else x for x in data.index]
                        if data.index.name:
                            data.index.name = tr(str(data.index.name))
            except Exception:
                pass
            return original_bar_chart(data, *args, **kwargs)
        st.bar_chart = translated_bar_chart

    if hasattr(st, "altair_chart"):
        original_altair_chart = st.altair_chart
        @functools.wraps(original_altair_chart)
        def translated_altair_chart(chart, *args, **kwargs):
            if get_language() == "en":
                try:
                    import altair as alt
                    spec = _value(chart.to_dict())
                    chart = alt.Chart.from_dict(spec)
                except Exception:
                    pass
            return original_altair_chart(chart, *args, **kwargs)
        st.altair_chart = translated_altair_chart

    st.session_state._i18n_installed = True
