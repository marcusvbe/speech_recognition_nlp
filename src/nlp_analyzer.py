import re
import nltk
import spacy
from typing import List, Dict
from collections import Counter

# Download necessário para NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class NLPAnalyzer:
    """Classe para analisar problemas de PLN em texto transcrito"""
    
    def __init__(self):
        # Carregar modelo do spaCy para inglês
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️ Modelo spaCy não encontrado. Execute: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Dicionário de homófonos comuns em inglês
        self.homophones = {
            'to': ['too', 'two'],
            'too': ['to', 'two'],
            'two': ['to', 'too'],
            'there': ['their', 'they\'re'],
            'their': ['there', 'they\'re'],
            'they\'re': ['there', 'their'],
            'your': ['you\'re'],
            'you\'re': ['your'],
            'its': ['it\'s'],
            'it\'s': ['its'],
            'hear': ['here'],
            'here': ['hear'],
            'write': ['right', 'rite'],
            'right': ['write', 'rite'],
            'rite': ['write', 'right'],
            'new': ['knew'],
            'knew': ['new'],
            'four': ['for', 'fore'],
            'for': ['four', 'fore'],
            'fore': ['four', 'for'],
            'eight': ['ate'],
            'ate': ['eight'],
            'one': ['won'],
            'won': ['one'],
            'sun': ['son'],
            'son': ['sun'],
            'flower': ['flour'],
            'flour': ['flower'],
            'break': ['brake'],
            'brake': ['break'],
            'pears': ['pairs'],
            'pairs': ['pears'],
            'pair': ['pear'],
            'pear': ['pair'],
            'sea': ['see'],
            'see': ['sea'],
            'meat': ['meet'],
            'meet': ['meat'],
            'peace': ['piece'],
            'piece': ['peace'],
            'no': ['know'],
            'know': ['no'],
            'by': ['buy', 'bye'],
            'buy': ['by', 'bye'],
            'bye': ['by', 'buy'],
            'read': ['red'],
            'red': ['read'],
            'tail': ['tale'],
            'tale': ['tail'],
            'mail': ['male'],
            'male': ['mail'],
            'sail': ['sale'],
            'sale': ['sail'],
            'wait': ['weight'],
            'weight': ['wait'],
            'weak': ['week'],
            'week': ['weak'],
            'steel': ['steal'],
            'steal': ['steel'],
            'bear': ['bare'],
            'bare': ['bear'],
            'fair': ['fare'],
            'fare': ['fair']
        }
        
        # Frases problemáticas conhecidas para segmentação
        self.segmentation_patterns = [
            r"let'?s eat \w+",
            r"come and eat \w+",
            r"time to eat \w+"
        ]
    
    def analyze_speech_text(self, text: str) -> Dict:
        """Analisa texto de fala para problemas de PLN"""
        problems = {
            'original_text': text,
            'homophones': self._find_homophones(text),
            'punctuation': self._check_punctuation_problems(text),
            'segmentation': self._check_segmentation(text)
        }
        return problems
    
    def display_detailed_analysis(self, problems: Dict):
        """Exibe análise detalhada dos problemas encontrados"""
        text = problems['original_text']
        
        print(f"\n{'='*60}")
        print(f"📝 TEXTO TRANSCRITO: '{text}'")
        print(f"{'='*60}")
        
        total_problems = 0
        
        # Homófonos com explicação expandida
        if problems['homophones']:
            print("\n🔄 PROBLEMA: AMBIGUIDADE LEXICAL (HOMÓFONOS)")
            print("━" * 50)
            print("📖 EXPLICAÇÃO:")
            print("   Homófonos são palavras com a mesma pronúncia, mas grafias e")
            print("   significados diferentes. O sistema de reconhecimento de fala pode")
            print("   transcrever a palavra incorreta, alterando completamente o sentido")
            print("   da frase. Este é um problema crítico para PLN pois:")
            print("   • Análise semântica fica comprometida")
            print("   • Sistemas de tradução podem falhar")
            print("   • Classificação de texto produz resultados incorretos")
            print("   • Análise de sentimento pode ser invertida")
            print()
            print("🔍 HOMÓFONOS DETECTADOS:")
            for h in problems['homophones']:
                print(f"   ⚠️  Palavra transcrita: '{h['word']}'")
                print(f"   🤔 Possíveis confusões: {', '.join(h['alternatives'])}")
                
                # Exemplos específicos baseados na palavra
                if h['word'] in ['two', 'to', 'too']:
                    print("   💡 Exemplo de confusão:")
                    print("      'I have two apples' vs 'I want to go' vs 'It's too hot'")
                elif h['word'] in ['there', 'their', 'they\'re']:
                    print("   💡 Exemplo de confusão:")
                    print("      'There is a book' vs 'Their house' vs 'They're coming'")
                elif h['word'] in ['pairs', 'pears']:
                    print("   💡 Exemplo de confusão:")
                    print("      'Two pairs of shoes' vs 'Two pears from tree'")
                print()
                total_problems += 1
        
        # Segmentação com explicação expandida
        if problems['segmentation']['has_problems']:
            print("\n📖 PROBLEMA: ERROS DE SEGMENTAÇÃO/PONTUAÇÃO")
            print("━" * 50)
            print("📖 EXPLICAÇÃO:")
            print("   Sistemas de reconhecimento de fala raramente inserem pontuação")
            print("   corretamente ou podem omitir vírgulas essenciais. Isso causa:")
            print("   • Mudança radical no significado das frases")
            print("   • Dificuldade na análise sintática (parsing)")
            print("   • Problemas na segmentação de sentenças")
            print("   • Ambiguidade na estrutura gramatical")
            print("   • Falhas em sistemas de QA (Question-Answering)")
            print()
            
            # Verifica se é o caso específico "Let's eat grandma"
            is_grandma_case = any("CASO CLÁSSICO" in issue for issue in problems['segmentation']['issues'])
            
            if is_grandma_case:
                print("🚨 CASO CLÁSSICO DE AMBIGUIDADE DETECTADO!")
                print("━" * 40)
                print("   📚 'Let's eat grandma' vs 'Let's eat, grandma'")
                print()
                print("   SEM vírgula: 'Let's eat grandma'")
                print("   ➤ Interpretação: Vamos comer a vovó (canibalismo!)")
                print()
                print("   COM vírgula: 'Let's eat, grandma'")
                print("   ➤ Interpretação: Vamos comer, vovó (chamando para comer)")
                print()
                print("   🎯 IMPACTO CRÍTICO PARA PLN:")
                print("   • Análise de dependência sintática falha completamente")
                print("   • Sistemas de tradução produzem frases incorretas/ofensivas")
                print("   • Extração de informação identifica ações erradas")
                print("   • Classificação de sentimento pode detectar violência")
                print("   • Sistemas de diálogo podem gerar respostas inadequadas")
                print()
                print("   💡 SOLUÇÕES PARA PLN:")
                print("   • Modelos neurais de pontuação automática")
                print("   • Análise de pausas e entonação no áudio original")
                print("   • Correção gramatical baseada em contexto")
                print("   • Detecção de ambiguidade sintática")
            
            print("🔍 PROBLEMAS DE SEGMENTAÇÃO DETECTADOS:")
            for issue in problems['segmentation']['issues']:
                print(f"   ⚠️  {issue}")
                total_problems += 1
            print()
        
        # Pontuação geral com explicação
        if problems['punctuation']['has_problems']:
            print("\n📝 PROBLEMA: AUSÊNCIA DE PONTUAÇÃO GERAL")
            print("━" * 50)
            print("📖 EXPLICAÇÃO:")
            print("   A falta de pontuação adequada em textos transcritos causa:")
            print("   • Dificuldade na identificação de fronteiras de sentenças")
            print("   • Problemas na análise de estrutura discursiva")
            print("   • Ambiguidade na interpretação de pausas e ênfases")
            print("   • Falhas em sistemas de sumarização automática")
            print()
            print("🔍 PROBLEMAS DETECTADOS:")
            for issue in problems['punctuation']['issues']:
                print(f"   ⚠️  {issue}")
                total_problems += 1
            print()
        
        # Resumo expandido
        print("📊 RESUMO DA ANÁLISE")
        print("━" * 30)
        if total_problems == 0:
            print("✅ NENHUM PROBLEMA CRÍTICO DETECTADO!")
            print("   O texto está adequado para processamento por sistemas de PLN.")
        else:
            print(f"⚠️  {total_problems} PROBLEMA(S) DETECTADO(S)")
            print("   ⚡ RECOMENDAÇÕES PARA PLN:")
            
            if problems['homophones']:
                print("   • Implementar correção contextual de homófonos")
                print("   • Usar modelos de linguagem para desambiguação")
                
            if problems['segmentation']['has_problems']:
                print("   • Aplicar pós-processamento para inserção de pontuação")
                print("   • Utilizar modelos neurais de pontuação automática")
                print("   • Implementar análise de pausas no áudio original")
                
                # Recomendação específica para o caso "grandma"
                if any("CASO CLÁSSICO" in issue for issue in problems['segmentation']['issues']):
                    print("   • ⚠️ CRÍTICO: Implementar detecção de ambiguidade sintática")
                    print("   • Usar análise de dependência para validar estruturas")
        
        print(f"\n{'='*60}\n")
    
    def _find_homophones(self, text: str) -> List[Dict]:
        """Detecta homófonos problemáticos"""
        words = re.findall(r'\w+', text.lower())
        found_homophones = []
        
        for word in words:
            if word in self.homophones:
                alternatives = self.homophones[word]
                found_homophones.append({
                    'word': word,
                    'alternatives': alternatives,
                    'context': text
                })
        
        return found_homophones
    
    def _check_segmentation(self, text: str) -> Dict:
        """Verifica problemas de segmentação de palavras"""
        issues = []
        text_lower = text.lower()
        
        # Detectar casos específicos famosos
        if re.search(r"let'?s eat \w+", text_lower):
            if "grandma" in text_lower or "gradma" in text_lower:
                issues.append("CASO CLÁSSICO DETECTADO: 'Let's eat grandma' - Ambiguidade crítica por vírgula ausente")
        
        # Verificar outros padrões problemáticos específicos
        for pattern in self.segmentation_patterns:
            if re.search(pattern, text_lower):
                if "eat" in text_lower and "grandma" not in text_lower:
                    issues.append("Frase ambígua detectada - vírgula ausente pode mudar sentido drasticamente")
        
        # Palavras muito longas (possível junção)
        words = text.split()
        long_words = [w for w in words if len(re.sub(r'[^\w]', '', w)) > 15]
        if long_words:
            issues.append(f"Palavras muito longas detectadas: {', '.join(long_words)} (possível junção incorreta)")
        
        return {
            'issues': issues,
            'has_problems': len(issues) > 0
        }
    
    def _check_punctuation_problems(self, text: str) -> Dict:
        """Verifica problemas gerais de pontuação"""
        issues = []
        
        # Texto sem pontuação final
        if not re.search(r'[.!?]$', text.strip()):
            issues.append("Frase sem pontuação final")
        
        # Múltiplas frases sem separação
        if len(text.split()) > 10 and not re.search(r'[.!?,;]', text):
            issues.append("Texto longo sem pontuação interna")
        
        return {
            'issues': issues,
            'has_problems': len(issues) > 0
        }