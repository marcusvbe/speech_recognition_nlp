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
            'there': ['their', 'they\'re'],
            'your': ['you\'re'],
            'its': ['it\'s'],
            'hear': ['here'],
            'write': ['right', 'rite'],
            'new': ['knew'],
            'four': ['for', 'fore'],
            'eight': ['ate'],
            'one': ['won'],
            'sun': ['son'],
            'flower': ['flour'],
            'break': ['brake'],
            'pears': ['pairs'],
            'pair': ['pear'],
            'two': ['to', 'too'],
            'ate': ['eight'],
            'sea': ['see'],
            'meat': ['meet'],
            'peace': ['piece']
        }
        
        # Frases problemáticas conhecidas para segmentação
        self.segmentation_patterns = [
            # Padrão: texto sem vírgula que muda o sentido
            r"let'?s eat \w+",  # "let's eat grandma" vs "let's eat, grandma"
            r"come and eat \w+",
            r"time to eat \w+",
        ]
        
    
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