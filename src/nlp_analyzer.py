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
            # Padrão: texto sem vírgula que muda o sentido
            r"let'?s eat \w+",  # "let's eat grandma" vs "let's eat, grandma"
            r"come and eat \w+",
            r"time to eat \w+",
        ]
    
    def analyze_speech_text(self, text: str) -> Dict:
        """
        Analisa texto de fala para problemas de PLN
        
        Args:
            text: Texto transcrito do reconhecimento de fala
            
        Returns:
            Dicionário com análise dos problemas encontrados
        """
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
        
        # Homófonos
        if problems['homophones']:
            print("\n🔄 HOMÓFONOS DETECTADOS:")
            for h in problems['homophones']:
                print(f"   ⚠️  Palavra: '{h['word']}'")
                print(f"   🤔 Pode ser confundida com: {', '.join(h['alternatives'])}")
                total_problems += 1
        
        # Segmentação (vírgulas)
        if problems['segmentation']['has_problems']:
            print("\n📖 PROBLEMAS DE SEGMENTAÇÃO:")
            for issue in problems['segmentation']['issues']:
                print(f"   ⚠️  {issue}")
                total_problems += 1
        
        # Pontuação geral
        if problems['punctuation']['has_problems']:
            print("\n📝 OUTROS PROBLEMAS DE PONTUAÇÃO:")
            for issue in problems['punctuation']['issues']:
                print(f"   ⚠️  {issue}")
                total_problems += 1
        
        # Resumo
        if total_problems == 0:
            print("\n✅ NENHUM PROBLEMA DETECTADO!")
        else:
            print(f"\n📊 RESUMO: {total_problems} problema(s) detectado(s)")
        
        print(f"{'='*60}\n")
    
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
        
        # Verificar padrões problemáticos específicos
        for pattern in self.segmentation_patterns:
            if re.search(pattern, text_lower):
                if "eat" in text_lower:
                    issues.append("Frase ambígua detectada - vírgula ausente pode mudar sentido (ex: 'eat grandma' vs 'eat, grandma')")
        
        # Palavras muito longas (possível junção)
        words = text.split()
        long_words = [w for w in words if len(re.sub(r'[^\w]', '', w)) > 15]
        if long_words:
            issues.append(f"Palavras muito longas: {', '.join(long_words)}")
        
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
    
    # Mantém métodos originais para compatibilidade
    def identify_problems(self, text: str) -> List[str]:
        """
        Identifica problemas potenciais para PLN no texto transcrito
        
        Args:
            text: Texto transcrito do reconhecimento de fala
            
        Returns:
            Lista de problemas identificados
        """
        problems = []
        
        # 1. HOMÓFONOS - Verificar ambiguidade lexical
        homophones_found = self._find_potential_homophones(text)
        if homophones_found:
            problems.append(f"🔤 AMBIGUIDADE LEXICAL: Homófonos detectados: {', '.join(homophones_found)} (podem ter significados diferentes)")
        
        # 2. SEGMENTAÇÃO - Verificar problemas de pontuação críticos
        segmentation_issues = self._find_segmentation_problems(text)
        if segmentation_issues:
            problems.append(f"📝 ERRO DE SEGMENTAÇÃO: {segmentation_issues}")
        
        # 3. Verificar ausência geral de pontuação
        if self._lacks_punctuation(text):
            problems.append("⚠️ PONTUAÇÃO AUSENTE: Falta de pontuação pode alterar significado")
        
        return problems
    
    def _find_segmentation_problems(self, text: str) -> str:
        """Identifica problemas específicos de segmentação que mudam o sentido"""
        text_lower = text.lower()
        
        # Verificar padrões problemáticos específicos
        for pattern in self.segmentation_patterns:
            if re.search(pattern, text_lower):
                if "eat" in text_lower:
                    return "Frase ambígua detectada - vírgula ausente pode mudar sentido (ex: 'eat grandma' vs 'eat, grandma')"
        
        # Verificar frases longas sem pontuação
        words = text.split()
        if len(words) > 8 and not re.search(r'[,.!?;:]', text):
            return "Frase longa sem pontuação - dificulta análise sintática"
        
        return None
    
    def _lacks_punctuation(self, text: str) -> bool:
        """Verifica se o texto carece de pontuação adequada"""
        # Textos longos sem pontuação são problemáticos
        words = text.split()
        punctuation_marks = ['.', '!', '?', ',', ';', ':']
        
        if len(words) > 10:  # Frases com mais de 10 palavras
            has_punctuation = any(mark in text for mark in punctuation_marks)
            return not has_punctuation
        
        return False
    
    def _find_potential_homophones(self, text: str) -> List[str]:
        """Encontra homófonos potenciais no texto"""
        words = text.lower().split()
        found_homophones = []
        
        for word in words:
            # Remove pontuação
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in self.homophones:
                found_homophones.append(clean_word)
        
        return list(set(found_homophones))
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """Retorna análise detalhada do texto"""
        if not self.nlp:
            return {"error": "spaCy model not available"}
        
        doc = self.nlp(text)
        
        analysis = {
            "tokens": [token.text for token in doc],
            "pos_tags": [(token.text, token.pos_) for token in doc],
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "sentences": [sent.text for sent in doc.sents]
        }
        
        return analysis