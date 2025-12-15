import logging
from transformers import pipeline
import asyncio
import torch
from functools import lru_cache

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    def __init__(self):
        # Use a multi-class emotion classification model.
        # If a GPU is available, use it (device=0); otherwise, use CPU (device=-1).
        device = 0 if torch.cuda.is_available() else -1
        # Optimize for memory: use smaller batch size and enable model offloading
        self.analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
            device=device,
            model_kwargs={"low_cpu_mem_usage": True}
        )
    
    @lru_cache(maxsize=128)
    def _analyze_sync(self, text: str):
        # Ensure analyzer is initialized
        self._ensure_initialized()
        
        if self.analyzer is None:
            # Fallback to simple keyword-based analysis
            return self._fallback_analysis(text)
        
        # Synchronous call to the pipeline. This result is cached to speed up repeated requests.
        return self.analyzer(text)
    
    def _fallback_analysis(self, text: str):
        """Simple keyword-based emotion analysis when model is unavailable"""
        text_lower = text.lower()
        emotions = {
            'happy': ['happy', 'joy', 'glad', 'excited', 'great', 'wonderful', 'amazing'],
            'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable', 'terrible'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'scared', 'afraid'],
            'neutral': []
        }
        
        scores = []
        for emotion, keywords in emotions.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            score = min(count / max(len(keywords), 1), 1.0) if emotion != 'neutral' else 0.3
            scores.append({'label': emotion, 'score': score})
        
        # Normalize scores
        total = sum(s['score'] for s in scores)
        if total > 0:
            scores = [{'label': s['label'], 'score': s['score'] / total} for s in scores]
        
        return [scores]
    
    async def analyze(self, text: str) -> dict:
        # Run the cached synchronous inference in a non-blocking way.
        results = await asyncio.to_thread(self._analyze_sync, text)
        if results and isinstance(results, list) and len(results) > 0:
            # 'results[0]' is a list of dictionaries with 'label' and 'score'.
            scores = results[0]
            best = max(scores, key=lambda x: x['score'])
            raw_label = best.get('label', '').lower()
            score = best.get('score', 0.0)
            
            # Map raw labels to friendly terms.
            label_mapping = {
                "joy": "happy",
                "sadness": "sad",
                "anger": "upset",
                "fear": "anxious",
                "surprise": "surprised",
                "disgust": "disgusted",
                "neutral": "calm"
            }
            mood = label_mapping.get(raw_label, raw_label)
            
            # Convert the numeric score to friendly text.
            if score >= 0.95:
                confidence_text = "Extremely confident"
            elif score >= 0.8:
                confidence_text = "Very confident"
            elif score >= 0.65:
                confidence_text = "Moderately confident"
            else:
                confidence_text = "Not very confident"
            
            return {"mood": mood, "confidence": confidence_text}
        else:
            return {"mood": "neutral", "confidence": "Not very confident"}
