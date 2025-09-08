import speech_recognition as sr
import pyaudio
import keyboard
import time
import threading

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        self.audio_data = None
        
        # Configurações mais sensíveis
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        # Ajusta para ruído ambiente
        print("Ajustando para ruído ambiente...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print(f"✅ Reconhecedor inicializado. Energia: {self.recognizer.energy_threshold}")
    
    def listen_for_speech(self):
        """Método simplificado para captura"""
        print("Pressione e SEGURE SPACE para gravar...")
        
        # Espera pressionar SPACE
        while not keyboard.is_pressed('space'):
            time.sleep(0.1)
        
        print("🔴 GRAVANDO... (solte SPACE para parar)")
        
        # Grava enquanto SPACE está pressionado
        self.is_recording = True
        self.audio_data = None
        
        # Inicia gravação em thread
        record_thread = threading.Thread(target=self._continuous_record)
        record_thread.start()
        
        # Espera soltar SPACE
        while keyboard.is_pressed('space'):
            time.sleep(0.1)
        
        print("⏹️ Parando gravação...")
        self.is_recording = False
        
        # Espera thread terminar
        record_thread.join(timeout=3)
        
        return self.audio_data
    
    def _continuous_record(self):
        """Grava continuamente enquanto is_recording for True"""
        try:
            with self.microphone as source:
                print("🎤 Microfone ativo...")
                
                # Inicia gravação
                audio_frames = []
                
                while self.is_recording:
                    try:
                        # Grava pequenos chunks
                        audio_chunk = self.recognizer.listen(
                            source, 
                            timeout=0.5, 
                            phrase_time_limit=0.5
                        )
                        audio_frames.append(audio_chunk.frame_data)
                        
                    except sr.WaitTimeoutError:
                        # Timeout é normal, continua gravando
                        continue
                    except Exception as e:
                        print(f"Erro durante gravação: {e}")
                        break
                
                # Junta todos os chunks de áudio
                if audio_frames:
                    print(f"✅ Capturados {len(audio_frames)} chunks de áudio")
                    
                    # Combina todos os frames
                    combined_audio = b''.join(audio_frames)
                    
                    # Cria AudioData com os frames combinados
                    self.audio_data = sr.AudioData(
                        combined_audio, 
                        source.SAMPLE_RATE, 
                        source.SAMPLE_WIDTH
                    )
                else:
                    print("❌ Nenhum áudio capturado")
                    
        except Exception as e:
            print(f"❌ Erro na captura de áudio: {e}")
    
    def transcribe_audio(self, audio_data, language="en-US"):
        """Transcreve áudio usando Google Speech Recognition"""
        if audio_data is None:
            return "Nenhum áudio para transcrever."
        
        try:
            print("🌐 Transcrevendo áudio...")
            text = self.recognizer.recognize_google(audio_data, language=language)
            print("✅ Transcrição concluída!")
            return text
        
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio."
        except sr.RequestError as e:
            return f"Erro no serviço de reconhecimento: {e}"
        except Exception as e:
            return f"Erro na transcrição: {e}"
    
    def save_audio_to_file(self, audio_data, filename):
        """Salva áudio em arquivo WAV"""
        if audio_data is None:
            return False
        
        try:
            with open(filename, "wb") as f:
                f.write(audio_data.get_wav_data())
            print(f"💾 Áudio salvo em: {filename}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar áudio: {e}")
            return False
    
    def test_microphone(self):
        """Testa se o microfone está funcionando"""
        try:
            print("🧪 Testando microfone (2 segundos)...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)
                print("✅ Microfone capturou áudio!")
                return True
        except sr.WaitTimeoutError:
            print("⚠️ Timeout - microfone pode estar sem entrada")
            return False
        except Exception as e:
            print(f"❌ Erro no teste do microfone: {e}")
            return False