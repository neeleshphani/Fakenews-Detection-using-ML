from fact_checker import FactChecker

def test():
    checker = FactChecker()

    cases = [
        ("India has 28 states", "SUPPORTED"),
        ("India has 29 states", "CONTRADICTED"),
        ("The prime minister of India is Narendra Modi", "SUPPORTED"),
        ("The prime minister of India is Modi", "SUPPORTED"),
        ("India prime minister is Modi", "SUPPORTED"),
        ("The India prime minister is Modi", "SUPPORTED"),
        ("Modi is the prime minister of India", "SUPPORTED"),
        ("The prime minister of India is Trump", "CONTRADICTED"),
        ("The president of India is Droupadi Murmu", "SUPPORTED"),
        ("The president of India is Trump", "CONTRADICTED"),
        ("The government announced a new railway project yesterday", "UNVERIFIED")
    ]
    
    passed = 0
    for claim, expected in cases:
        status, _, _ = checker.check_claim(claim)
        if status == expected:
            print(f"[PASS] {claim} -> {status}")
            passed += 1
        else:
            print(f"[FAIL] {claim} -> Expected {expected}, got {status}")
            
    print(f"\n{passed}/{len(cases)} tests passed.")

if __name__ == "__main__":
    test()
