import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

def test_full_role_logic(effective_input):
    role_pattern = r'(music composer|music director|composer|director|producer|actor|actress|hero|heroine|singer|author|writer|creator|ceo|chief executive officer|founder|owner|chairman|director|head|prime minister|president|chief minister|chancellor|king|queen)\s+of\s+([a-zA-Z0-9\s]+?)\s+is\s+([a-zA-Z\s]+)'
    if re.search(role_pattern, effective_input, re.I):
        role_match = re.search(role_pattern, effective_input, re.I)
        role = role_match.group(1).strip().lower()
        work = role_match.group(2).strip()
        person = role_match.group(3).strip()
        
        res_work = wikipedia.search(work)
        if res_work:
            top_work = res_work[0]
            try:
                p = wikipedia.page(top_work, auto_suggest=False)
                content = p.content
                work_summary = p.summary
            except Exception:
                try:
                    p = wikipedia.page(top_work, auto_suggest=True)
                    content = p.content
                    work_summary = p.summary
                except Exception:
                    content = ''
                    work_summary = ''
                    
            if content:
                true_statement = None
                for line in content.split('\n'):
                    line_l = line.lower()
                    if 'music' in role or 'composer' in role:
                        if 'composed' in line_l and any(k in line_l for k in ['music', 'score', 'soundtrack']):
                            clean_l = re.sub(r'\[\d+\]', '', line).strip()
                            true_statement = clean_l.split('.')[0] + '.'
                            break
                    elif 'director' in role or 'directed' in role:
                        if 'directed by' in line_l or 'director' in line_l:
                            clean_l = re.sub(r'\[\d+\]', '', line).strip()
                            true_statement = clean_l.split('.')[0] + '.'
                            break
                    elif any(k in role for k in ['ceo', 'founder', 'head', 'owner']):
                        if any(k in line_l for k in ['ceo', 'founder', 'founded by', 'owner', 'subsidiary', 'headquartered']):
                            clean_l = re.sub(r'\[\d+\]', '', line).strip()
                            true_statement = clean_l.split('.')[0] + '.'
                            break
                            
                if not true_statement and work_summary:
                    true_statement = work_summary.split('.')[0] + '.'
                    
                if person.lower() in content.lower() and (not true_statement or person.lower() in true_statement.lower()):
                    pred = 1
                    reason = f"Live Wikipedia records confirm that '{person.title()}' is the {role} of {top_work}: {true_statement}"
                else:
                    pred = 0
                    reason = f"Live Wikipedia records state that: \"{true_statement}\" The claim asserting that '{person.title()}' is the {role} is incorrect."
                return pred, reason, top_work
    return None, None, None

cases = [
    'the music composer of kgf chapter one is anirudh',
    'the music composer of kgf chapter one is ravi basrur',
    'the ceo of jio studios is phani'
]

for c in cases:
    p, r, s = test_full_role_logic(c)
    verdict = 'REAL' if p == 1 else 'FAKE'
    print(f"[{verdict}] {c}")
    print(f" -> Reason: {r[:100]}...")
    print(f" -> Source: {s}\n")
