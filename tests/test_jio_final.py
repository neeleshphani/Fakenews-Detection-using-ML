import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

query = 'the ceo of jio stduios is phani'

# Typo check
effective_input = query
words = effective_input.split()
fixed_words = []
word_changed = False
for i in range(len(words)):
    w = words[i]
    if i > 0:
        _, psug = wikipedia.search(f"{words[i-1]} {w}", suggestion=True)
        if psug and psug.lower() != f"{words[i-1]} {w}".lower():
            parts = psug.split()
            if len(parts) >= 2 and parts[-1].lower() != w.lower():
                w = parts[-1]
                word_changed = True
    fixed_words.append(w)
if word_changed:
    effective_input = ' '.join(fixed_words)
    print("Auto-corrected to:", effective_input)

role_match = re.search(r'(ceo|chief executive officer|founder|owner|director|chairman|head)\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', effective_input, re.I)
if role_match:
    role = role_match.group(1).strip()
    org = role_match.group(2).strip()
    person = role_match.group(3).strip()
    res = wikipedia.search(org)
    top_org = res[0]
    summ = wikipedia.summary(top_org, sentences=2, auto_suggest=False)
    if person.lower() in summ.lower():
        print("VERDICT: REAL")
    else:
        print("VERDICT: FAKE")
        print("Real Information:", f"Live Wikipedia records state that '{person.title()}' is not the {role} of {top_org}. Real information: {summ}")
    print("Source:", f"Wikipedia Live Web API ({top_org})")
