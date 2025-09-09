import time
from src.speech_recognizer import SpeechRecognizer
from src.nlp_analyzer import NLPAnalyzer

def main():
    print("=== Sistema de Reconhecimento de Fala para PLN ===")
    
    try:
        speech_recognizer = SpeechRecognizer()
        
        # Testa microfone primeiro
        print("\n🧪 Testando microfone...")
        if not speech_recognizer.test_microphone():
            print("⚠️ Problema detectado no microfone!")
            proceed = input("Continuar mesmo assim? (s/n): ")
            if proceed.lower() != 's':
                return
        
        print("\n✅ Sistema pronto!")
        
        # Menu de opções
        while True:
            print("\n" + "="*50)
            print("📋 OPÇÕES DISPONÍVEIS:")
            print("1 - Apenas transcrever fala")
            print("2 - Transcrever e analisar problemas comuns de PLN")
            print("0 - Sair")
            
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                transcribe_only_mode(speech_recognizer)
            elif choice == "2":
                transcribe_and_analyze_mode(speech_recognizer)
            else:
                print("❌ Opção inválida. Tente novamente.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Saindo do sistema...")
    except Exception as e:
        print(f"❌ Erro: {e}")

def transcribe_only_mode(speech_recognizer):
    """Modo apenas transcrição"""
    print("\n" + "="*50)
    print("🎤 MODO: APENAS TRANSCRIÇÃO")
    print("💡 Instruções:")
    print("   - Pressione e SEGURE SPACE para gravar")
    print("   - Fale enquanto segura a tecla")
    print("   - Solte SPACE para parar e processar")
    print("   - Digite 'voltar' para retornar ao menu")
    
    while True:
        print("\n🎤 Pronto para transcrever...")
        
        # Escuta e grava
        audio_data = speech_recognizer.listen_for_speech()
        
        if audio_data:
            # Transcreve
            text = speech_recognizer.transcribe_audio(audio_data)
            print(f"\n📝 Transcrito: '{text}'")
            
            if not text or "Não foi possível" in text or "Erro" in text:
                print("❌ Transcrição não foi bem-sucedida")
                print("💡 Dicas:")
                print("   - Fale mais alto e claro")
                print("   - Segure SPACE por mais tempo")
                print("   - Verifique conexão com internet")
        else:
            print("❌ Nenhum áudio capturado")
            print("💡 Dicas:")
            print("   - Fale mais alto")
            print("   - Segure SPACE por mais tempo")
            print("   - Verifique se o microfone está funcionando")
        
        # Pergunta se quer continuar
        continue_choice = input("\nContinuar transcrevendo? (s/n): ").strip().lower()
        if continue_choice != 's':
            break

def transcribe_and_analyze_mode(speech_recognizer):
    """Modo transcrição + análise"""
    nlp_analyzer = NLPAnalyzer()
    
    print("\n" + "="*50)
    print("🎤 MODO: TRANSCRIÇÃO + ANÁLISE PLN")
    print("💡 Instruções:")
    print("   - Pressione e SEGURE SPACE para gravar")
    print("   - Fale enquanto segura a tecla")
    print("   - Solte SPACE para parar e processar")
    print("\n🎯 Frases de teste sugeridas:")
    print("   - 'Let's eat grandma' (problema de vírgula)")
    print("   - 'There are two pears on the table' (homófonos)")
    
    while True:
        print("\n🎤 Pronto para gravar e analisar...")
        
        # Escuta e grava
        audio_data = speech_recognizer.listen_for_speech()
        
        if audio_data:
            # Transcreve
            text = speech_recognizer.transcribe_audio(audio_data)
            print(f"\n📝 Transcrito: '{text}'")
            
            # Analisa se transcrição foi bem-sucedida
            if text and "Não foi possível" not in text and "Erro" not in text:
                problems = nlp_analyzer.analyze_speech_text(text)
                nlp_analyzer.display_detailed_analysis(problems)
            else:
                print("❌ Transcrição não foi bem-sucedida")
                print("💡 Dicas:")
                print("   - Fale mais alto e claro")
                print("   - Segure SPACE por mais tempo")
                print("   - Verifique conexão com internet")
        else:
            print("❌ Nenhum áudio capturado")
            print("💡 Dicas:")
            print("   - Fale mais alto")
            print("   - Segure SPACE por mais tempo")
            print("   - Verifique se o microfone está funcionando")
        
        # Pergunta se quer continuar
        continue_choice = input("\nContinuar transcrevendo e analisando? (s/n): ").strip().lower()
        if continue_choice != 's':
            break

if __name__ == "__main__":
    main()