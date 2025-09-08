import time
from src.speech_recognizer import SpeechRecognizer
from src.nlp_analyzer import NLPAnalyzer

def main():
    print("=== Sistema de Reconhecimento de Fala para PLN ===")
    
    try:
        speech_recognizer = SpeechRecognizer()
        nlp_analyzer = NLPAnalyzer()
        
        # Testa microfone primeiro
        print("\n🧪 Testando microfone...")
        if not speech_recognizer.test_microphone():
            print("⚠️ Problema detectado no microfone!")
            proceed = input("Continuar mesmo assim? (s/n): ")
            if proceed.lower() != 's':
                return
        
        print("\n✅ Sistema pronto!")
        print("💡 Instruções:")
        print("   - Pressione e SEGURE SPACE para gravar")
        print("   - Fale enquanto segura a tecla")
        print("   - Solte SPACE para parar e processar")
        print("   - Pressione Ctrl+C para sair")
        print("\n🎯 Frases de teste sugeridas:")
        print("   - 'Let's eat grandma' (problema de vírgula)")
        print("   - 'There are two pears on the table' (homófonos)")
        
        while True:
            print("\n" + "="*50)
            
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
            
            # Volta automaticamente para capturar próxima frase
            print("\n🎤 Pronto para próxima frase...")
                
    except KeyboardInterrupt:
        print("\n\n👋 Saindo do sistema...")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()