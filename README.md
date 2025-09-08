# Reconhecimento de Fala em Inglês para PLN

Descrição em Alto Nível do Projeto
O sistema de reconhecimento de fala em inglês para PLN implementa um fluxo completo para capturar fala, transcrevê-la e analisar problemas comuns para processamento de linguagem natural.


Arquitetura
O projeto segue uma arquitetura modular com três componentes principais:

speech_recognizer.py: Responsável pela captura e transcrição de áudio
nlp_analyzer.py: Analisa o texto transcrito para identificar desafios de PLN


Bibliotecas Utilizadas

Reconhecimento de Fala

SpeechRecognition: Framework de alto nível para reconhecimento de fala que permite integração com várias APIs (Google, Sphinx, etc.)

PyAudio: Biblioteca para entrada e saída de áudio baseada no PortAudio, manipula a captura de áudio do microfone

keyboard: Permite detecção de teclas pressionadas para controlar início/fim da gravação


Fluxo de Funcionamento

O usuário inicia o programa via main.py

Ao escolher reconhecimento de fala:
SpeechRecognizer configura o microfone e ajusta para o ruído ambiente
O usuário pressiona SPACE para iniciar/parar a gravação
O áudio é capturado e enviado à Google Speech API para transcrição
Após a transcrição:
NLPAnalyzer examina o texto em busca de problemas comuns:
Homófonos (palavras que soam igual mas têm significados diferentes)
Falta de pontuação
Problemas de segmentação
Os resultados são exibidos, mostrando tanto a transcrição quanto os problemas identificados

## Conceitos Demonstrados

1. **Reconhecimento de Fala**  
   - Captura de áudio via microfone usando PyAudio  
   - Transcrição usando Google Speech API
   - Processamento de sinais de áudio  

2. **Problemas para PLN Identificados**  
   - **Homófonos**: to/too/two, there/their/they're  
   - **Problemas de pontuação**/**segmentação**


## Pré-requisitos

- Python 3.7+  
- Microfone
- 
## Instalação

# 1. Criar o ambiente virtual
python -m venv venv

# 2. Ativar o venv
# Windows
venv\Scripts\activate

1. Instalar as dependências Python:  
   ```bash
   pip install -r requirements.txt
   ```

2. Baixe o modelo do spaCy para inglês:  
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Execução

```bash
python main.py
```

## Estrutura do Projeto

- `main.py`  
  Interface principal do sistema.  
- `src/speech_recognizer.py`  
  Classe que faz captura de áudio e transcrição usando Google Speech API.  
- `src/nlp_analyzer.py`  
  Análise de transcrições para identificar problemas de PLN.  
- `requirements.txt`  
  Lista de dependências Python.  

## Exemplos de Uso
