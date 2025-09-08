from src.speech_recognizer import SpeechRecognizer
from src.nlp_analyzer import NLPAnalyzer
from examples.problematic_cases import demonstrate_problematic_cases

def main():
    print("=== Sistema de Reconhecimento de Fala em Inglês ===")
    
    # Inicializar componentes
    recognizer = SpeechRecognizer()
    nlp_analyzer = NLPAnalyzer()
    
    while True:
        print("\nOpções:")
        print("1. Reconhecimento de fala com análise de transcrição problemática para PLN")
        print("2. Sair")
        
        choice = input("\nEscolha uma opção (1-2): ")
        
        if choice == "1":
            live_recognition(recognizer, nlp_analyzer)
        elif choice == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

def live_recognition(recognizer, nlp_analyzer):
    print("\n--- Reconhecimento de Fala ---")
    print("Fale algo em inglês após o prompt.")
    print("\nPressione Ctrl+C para parar...")
    
    try:
        while True:
            # Capturar e transcrever áudio
            text = recognizer.listen_and_transcribe()
            
            if text:
                print(f"\n📝 Transcrição: '{text}'")
                
                # Analisar problemas para PLN
                problems = nlp_analyzer.identify_problems(text)
                
                if problems:
                    print("⚠️  Problemas identificados para PLN:")
                    for problem in problems:
                        print(f"   - {problem}")
                print("-" * 50)
            else:
                print("❌ Não foi possível reconhecer. Tente novamente.")
                
    except KeyboardInterrupt:
        print("\nParando reconhecimento...")

if __name__ == "__main__":
    main()