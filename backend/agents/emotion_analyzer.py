import logging
from transformers import pipeline
import asyncio
import torch
from functools import lru_cache

logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """
    Wraps a Hugging Face transformers pipeline for emotion classification.

    Note: This version avoids `low_cpu_mem_usage` and other options that
    require the `accelerate` package, so it works in simple deployments
    without extra dependencies.
    """

    def __init__(self):
        # Use a multi-class emotion classification model.
        # If a GPU is available, use it (device=0); otherwise, use CPU (device=-1).
        device = 0 if torch.cuda.is_available() else -1
        self.analyzer = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
            device=device,
        )

    @lru_cache(maxsize=128)
    def _analyze_sync(self, text: str):
        """Synchronous call to the pipeline. Cached for repeated requests."""
        return self.analyzer(text)

    async def analyze(self, text: str) -> dict:
        """Run the emotion analysis asynchronously and normalize the result."""
        results = await asyncio.to_thread(self._analyze_sync, text)
        if results and isinstance(results, list) and len(results) > 0:
            # 'results[0]' is a list of dictionaries with 'label' and 'score'.
            scores = results[0]
            best = max(scores, key=lambda x: x["score"])
            raw_label = best.get("label", "").lower()
            score = best.get("score", 0.0)

            # Map raw labels to friendlier terms.
            label_mapping = {
                "joy": "happy",
                "sadness": "sad",
                "anger": "upset",
                "fear": "anxious",
                "surprise": "surprised",
                "disgust": "disgusted",
                "neutral": "calm",
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

        return {"mood": "neutral", "confidence": "Not very confident"}
