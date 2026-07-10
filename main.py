from cv_reader import read_cv
from analyzer import analyze_cv
from ai_analyzer import ai_analysis


cv = read_cv("cv.pdf")

job_offer = input("Wklej ofertę pracy:\n")


score, skills = analyze_cv(cv, job_offer)


print("\n--- Wynik analizy ---")
print(f"Dopasowanie: {score:.0f}%")

print("\nZnalezione umiejętności:")

for skill in skills:
    print("-", skill)


result = ai_analysis(cv, job_offer)

print("\n--- Analiza AI ---")
print(result)



