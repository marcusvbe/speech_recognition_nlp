from src.nlp_analyzer import NLPAnalyzer

def demonstrate_problematic_cases():
    """Demonstra casos problemáticos específicos para PLN"""
    
    analyzer = NLPAnalyzer()
    
    print("\n=== CASOS PROBLEMÁTICOS PARA PLN ===\n")
    
    # Caso 1: Homófonos
    print("📌 CASO 1: HOMÓFONOS")
    print("Problema: Palavras que soam igual mas têm significados diferentes")
    
    test_cases_homophones = [
        "i want to go to the store",  # 'to' pode ser 'too' ou 'two'
        "there house is over their",  # 'there' vs 'their'
        "its a beautiful day",        # 'its' vs "it's"
        "i can hear you from here"    # 'hear' vs 'here'
    ]
    
    for text in test_cases_homophones:
        print(f"\n   Texto: '{text}'")
        problems = analyzer.identify_problems(text)
        for problem in problems:
            if "Homófonos" in problem:
                print(f"   ⚠️  {problem}")
        print(f"   💡 Solução: Usar contexto semântico e modelos de linguagem")
    
    # Caso 2: Ausência de pontuação e hesitações
    print("\n" + "="*60)
    print("📌 CASO 2: FALA NATURAL SEM ESTRUTURA")
    print("Problema: Hesitações, repetições e falta de pontuação")
    
    test_cases_speech = [
        "um i think that we should uh maybe go to the store you know",
        "the the meeting is tomorrow and and we need to prepare",
        "basically like we need to finish this project before the deadline"
    ]
    
    for text in test_cases_speech:
        print(f"\n   Texto: '{text}'")
        problems = analyzer.identify_problems(text)
        for problem in problems:
            print(f"   ⚠️  {problem}")
        print(f"   💡 Solução: Pré-processamento para remoção de hesitações")
    
    # Caso 3: Análise comparativa
    print("\n" + "="*60)
    print("📌 ANÁLISE COMPARATIVA")
    
    original_speech = "um i think that we should go to the store and buy to apples"
    cleaned_text = "I think that we should go to the store and buy two apples."
    
    print(f"\n   Fala transcrita: '{original_speech}'")
    problems_original = analyzer.identify_problems(original_speech)
    print("   Problemas encontrados:")
    for problem in problems_original:
        print(f"     - {problem}")
    
    print(f"\n   Texto limpo: '{cleaned_text}'")
    problems_cleaned = analyzer.identify_problems(cleaned_text)
    if problems_cleaned:
        print("   Problemas encontrados:")
        for problem in problems_cleaned:
            print(f"     - {problem}")
    else:
        print("   ✅ Nenhum problema identificado")
    
    print("\n" + "="*60)
    print("📋 RESUMO DOS PRINCIPAIS PROBLEMAS PARA PLN:")
    print("1. Homófonos causam ambiguidade semântica")
    print("2. Hesitações adicionam ruído aos dados")
    print("3. Falta de pontuação dificulta análise sintática")
    print("4. Repetições criam redundância desnecessária")
    print("5. Contrações precisam ser expandidas")
    print("6. Números vs palavras causam confusão")

if __name__ == "__main__":
    demonstrate_problematic_cases()