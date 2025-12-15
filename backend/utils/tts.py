import logging
from elevenlabs.client import ElevenLabs
from backend.config.config import Config
import tempfile
import os
import time

# Try to import pygame, but make it optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except (ImportError, AttributeError) as e:
    PYGAME_AVAILABLE = False
    logging.warning(f"Pygame not available: {e}. Audio playback will be limited.")

logger = logging.getLogger(__name__)

class TTS:
    def __init__(self):
        if not Config.ELEVEN_LABS_API_KEY:
            logger.warning("Eleven Labs API key not configured. TTS will be unavailable.")
            self.client = None
            return
            
        self.client = ElevenLabs(api_key=Config.ELEVEN_LABS_API_KEY)
        self.voice_id = "Xb7hH8MSUJpSbSDYk0k2"  # Alice's voice ID
        self.temp_dir = tempfile.gettempdir()
        
        # Initialize pygame mixer for audio playback if available
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
            except Exception as e:
                logger.warning(f"Failed to initialize pygame mixer: {e}")
    
    def speak(self, text: str, mood: str = None) -> bool:
        """Converts text to speech and plays it without opening external player"""
        if not self.client:
            logger.warning("TTS client not initialized. Cannot speak.")
            return False
            
        if not text or not isinstance(text, str):
            logger.error("Invalid text input for TTS")
            return False

        try:
            # Generate unique filename with timestamp to avoid permission errors
            timestamp = int(time.time())
            temp_path = os.path.join(self.temp_dir, f"aura_response_{timestamp}.mp3")
            
            # Adjust voice settings based on mood
            model_id = "eleven_monolingual_v1"
            voice_settings = {}
            if mood in ["sad", "depressed", "lonely"]:
                voice_settings = {"stability": 0.7, "similarity_boost": 0.8}
            elif mood in ["happy", "excited"]:
                voice_settings = {"stability": 0.5, "similarity_boost": 0.75}
            elif mood in ["anxious", "confused"]:
                voice_settings = {"stability": 0.8, "similarity_boost": 0.7}
            else:
                voice_settings = {"stability": 0.6, "similarity_boost": 0.75}
            
            # Generate audio using the client
            audio = self.client.generate(
                text=text,
                voice=self.voice_id,
                model=model_id,
                stream=True,
                voice_settings=voice_settings
            )
            
            # Save to temp file with unique name
            with open(temp_path, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
            
            # Play audio with pygame if available
            if PYGAME_AVAILABLE:
                try:
                    pygame.mixer.music.load(temp_path)
                    pygame.mixer.music.play()
                    logger.info(f"TTS: Playing audio with voice={self.voice_id}, mood={mood}")
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                        
                except Exception as audio_err:
                    logger.error(f"Audio playback error: {str(audio_err)}")
                    # Fall back to system player if pygame fails
                    self._fallback_play(temp_path)
            else:
                # Fall back to system player if pygame is not available
                self._fallback_play(temp_path)
    
            # Clean up temp file after playback
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception as cleanup_err:
                logger.warning(f"Failed to clean up temp file: {str(cleanup_err)}")
                
            return True
            
        except Exception as e:
            logger.error(f"TTS Error: {str(e)}")
            return False
    
    def _fallback_play(self, temp_path):
        """Fallback method to play audio using system player"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(temp_path)
            elif os.name == 'posix':  # macOS/Linux
                import subprocess
                subprocess.run(['open', temp_path], check=False)  # macOS
            else:
                logger.warning("Cannot play audio: no suitable player available")
        except Exception as e:
            logger.error(f"Fallback audio playback failed: {str(e)}")
