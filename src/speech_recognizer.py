import speech_recognition as sr

from typing import Optional
import json
import keyboard

class SpeechRecognizer:
    """Classe para reconhecimento de fala em inglês usando Google Speech API"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurações otimizadas
        self.recognizer.energy_threshold = 4000  # Aumentado para reduzir ruído
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0    # Mais tempo para pausas
        self.recognizer.phrase_threshold = 0.3   # Sensibilidade de frase
        self.recognizer.non_speaking_duration = 0.8  # Tempo de silêncio
        
        # Ajustar para ruído ambiente
        print("Ajustando para ruído ambiente...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Pronto para reconhecimento!")
    
    def listen_and_transcribe(self, timeout=10) -> Optional[str]:
        """
        Escuta áudio do microfone e transcreve para texto usando Google Speech
        """
        try:
            print("🎤 Pressione SPACE para iniciar gravação...")
            keyboard.wait('space')
            
            print("🔴 Gravando... (pressione SPACE novamente para parar)")
            
            with self.microphone as source:
                audio_data = []
                
                while True:
                    try:
                        # Grava em pequenos chunks
                        audio_chunk = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                        audio_data.append(audio_chunk)
                        
                        # Verifica se SPACE foi pressionado novamente
                        if keyboard.is_pressed('space'):
                            break
                            
                    except sr.WaitTimeoutError:
                        # Continua gravando se não há timeout crítico
                        if keyboard.is_pressed('space'):
                            break
                        continue
            
            print("⏹️ Gravação finalizada. Processando...")
            
            # Combina os chunks de áudio (usando o último chunk por simplicidade)
            if audio_data:
                audio = audio_data[-1] if len(audio_data) == 1 else audio_data[0]
                
                # Usar Google Speech Recognition
                text = self.recognizer.recognize_google(audio, language='en-US')
                
                if text:
                    print("✅ Reconhecimento concluído via Google Speech")
                    return text.lower()
                else:
                    print("❌ Google Speech não conseguiu reconhecer")
                    return None
            else:
                print("❌ Nenhum áudio capturado")
                return None
                
        except sr.RequestError as e:
            print(f"❌ Erro na requisição ao Google Speech: {e}")
            return None
        except sr.UnknownValueError:
            print("❌ Google Speech não conseguiu entender o áudio")
            return None
        except Exception as e:
            print(f"❌ Erro na captura de áudio: {e}")
            return None
    
    def transcribe_from_file(self, audio_file_path: str) -> Optional[str]:
        """Transcreve áudio de um arquivo usando Google Speech"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            print("🔄 Transcrevendo arquivo com Google Speech...")
            text = self.recognizer.recognize_google(audio, language='en-US')
            
            if text:
                print("✅ Transcrição concluída via Google Speech")
                return text.lower()
            else:
                return None
            
        except sr.RequestError as e:
            print(f"❌ Erro na requisição ao Google Speech: {e}")
            return None
        except sr.UnknownValueError:
            print("❌ Google Speech não conseguiu entender o áudio do arquivo")
            return None
        except Exception as e:
            print(f"❌ Erro ao transcrever arquivo: {e}")
            return None
    
    def get_available_microphones(self):
        """Lista microfones disponíveis"""
        print("Microfones disponíveis:")
        for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{i}: {mic_name}")
    
    def test_microphone(self):
        """Testa o microfone"""
        print("Teste de microfone - diga algo:")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            print("✅ Áudio capturado com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro no teste do microfone: {e}")
            return False