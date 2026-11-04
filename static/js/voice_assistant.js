/**
 * KrishiMitra - Voice Assistant Engine
 * Utilizes Web Speech API (SpeechRecognition) & SpeechSynthesis
 * Supports English (en-IN) and Telugu (te-IN) for farmers.
 */

class KrishiVoiceAssistant {
  constructor() {
    this.recognition = null;
    this.isListening = false;
    this.currentLanguage = 'en-IN'; // or 'te-IN'
    this.lastInputWasVoice = false;
    this.synth = window.speechSynthesis || null;

    // UI Elements
    this.floatingMicBtn = document.getElementById('kmVoiceFloatBtn');
    this.modalEl = document.getElementById('kmVoiceModal');
    this.modal = null;
    this.modalMicBtn = document.getElementById('kmVoiceModalMicBtn');
    this.statusText = document.getElementById('kmVoiceStatusText');
    this.transcriptText = document.getElementById('kmVoiceTranscript');
    this.wavesContainer = document.getElementById('kmVoiceWaves');
    this.langSelect = document.getElementById('kmVoiceLangSelect');

    this.setupSpeechRecognition();
    this.bindEvents();
  }

  setupSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Speech Recognition API is not supported by this browser.");
      if (this.statusText) {
        this.statusText.innerText = "Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.";
      }
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.lang = this.currentLanguage;

    this.recognition.onstart = () => {
      this.isListening = true;
      this.updateUIListening(true);
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("Voice recognized:", transcript);
      if (this.transcriptText) {
        this.transcriptText.innerText = `"${transcript}"`;
      }
      this.handleVoiceCommand(transcript);
    };

    this.recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      this.isListening = false;
      this.updateUIListening(false);
      if (this.statusText) {
        if (event.error === 'not-allowed') {
          this.statusText.innerText = "Microphone access blocked. Please allow microphone permission.";
        } else if (event.error === 'no-speech') {
          this.statusText.innerText = "No voice heard. Tap the microphone and try again.";
        } else {
          this.statusText.innerText = `Error: ${event.error}. Please try again.`;
        }
      }
    };

    this.recognition.onend = () => {
      this.isListening = false;
      this.updateUIListening(false);
    };
  }

  bindEvents() {
    if (this.modalEl && window.bootstrap) {
      this.modal = new bootstrap.Modal(this.modalEl);
    }

    if (this.floatingMicBtn) {
      this.floatingMicBtn.addEventListener('click', () => {
        if (this.modal) {
          this.modal.show();
        }
        this.startListening();
      });
    }

    if (this.modalMicBtn) {
      this.modalMicBtn.addEventListener('click', () => {
        if (this.isListening) {
          this.stopListening();
        } else {
          this.startListening();
        }
      });
    }

    if (this.langSelect) {
      this.langSelect.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
      });
    }
  }

  setLanguage(langCode) {
    this.currentLanguage = langCode;
    if (this.recognition) {
      this.recognition.lang = langCode;
    }
    const welcome = langCode === 'te-IN' 
      ? "తెలుగు వాయిస్ సిద్ధంగా ఉంది. 'వాతావరణం', 'మార్కెట్ ధరలు', లేదా పంట సందేహం మాట్లాడండి." 
      : "English voice ready. Say 'Check weather', 'Mandi prices', or ask any crop query.";
    if (this.statusText) {
      this.statusText.innerText = welcome;
    }
  }

  startListening() {
    if (!this.recognition) {
      alert("Speech recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
      return;
    }

    // Stop speaking if currently speaking
    if (this.synth && this.synth.speaking) {
      this.synth.cancel();
    }

    try {
      this.recognition.lang = this.currentLanguage;
      this.recognition.start();
      this.lastInputWasVoice = true;
    } catch (e) {
      console.warn("Recognition already started or error:", e);
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
    }
  }

  updateUIListening(listening) {
    if (this.floatingMicBtn) {
      if (listening) {
        this.floatingMicBtn.classList.add('listening');
      } else {
        this.floatingMicBtn.classList.remove('listening');
      }
    }

    if (this.modalMicBtn) {
      if (listening) {
        this.modalMicBtn.classList.remove('btn-success');
        this.modalMicBtn.classList.add('btn-danger', 'pulse-anim');
        this.modalMicBtn.innerHTML = '<i class="bi bi-mic-fill fs-2"></i>';
      } else {
        this.modalMicBtn.classList.remove('btn-danger', 'pulse-anim');
        this.modalMicBtn.classList.add('btn-success');
        this.modalMicBtn.innerHTML = '<i class="bi bi-mic fs-2"></i>';
      }
    }

    if (this.wavesContainer) {
      if (listening) {
        this.wavesContainer.classList.add('active');
      } else {
        this.wavesContainer.classList.remove('active');
      }
    }

    if (this.statusText) {
      if (listening) {
        this.statusText.innerText = this.currentLanguage === 'te-IN' 
          ? "వినబడుతోంది... మాట్లాడండి (Listening in Telugu...)" 
          : "Listening... Speak your agricultural question.";
      }
    }
  }

  handleVoiceCommand(transcript) {
    if (this.statusText) {
      this.statusText.innerText = "Processing query...";
    }

    fetch('/api/voice-command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ transcript: transcript })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'redirect') {
          if (this.statusText) {
            this.statusText.innerText = data.message;
          }
          this.speak(data.voice_text || data.message, this.currentLanguage.startsWith('te') ? 'te' : 'en');
          setTimeout(() => {
            window.location.href = data.url;
          }, 1200);
        } else {
          // Open chatbot with answer
          if (this.statusText) {
            this.statusText.innerText = "Response ready:";
          }
          if (this.transcriptText) {
            this.transcriptText.innerText = data.voice_text || data.response_text;
          }

          // Speak back
          this.speak(data.voice_text || data.response_text, data.language || 'en');

          // Also populate into Chatbot if available
          if (window.krishiChat) {
            window.krishiChat.openChat();
            window.krishiChat.appendUserMessage(transcript);
            window.krishiChat.appendBotMessage(data);
          }
        }
      })
      .catch(err => {
        console.error("Voice command processing error:", err);
        if (this.statusText) {
          this.statusText.innerText = "Could not process request. Please try again.";
        }
      });
  }

  speak(text, lang = 'en') {
    if (!this.synth) {
      console.warn("Speech Synthesis is not supported in this browser.");
      return;
    }

    // Cancel ongoing speech
    this.synth.cancel();

    // Clean markdown characters or asterisks from spoken text
    const cleanText = text.replace(/[*#_~`]/g, '').trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.95; // Slightly slower, clear cadence for farmers
    utterance.pitch = 1.0;

    // Language selection
    if (lang === 'te' || lang.startsWith('te')) {
      utterance.lang = 'te-IN';
    } else {
      utterance.lang = 'en-IN';
    }

    // Attempt to match an Indian accent or Telugu voice if available
    const voices = this.synth.getVoices();
    if (voices && voices.length > 0) {
      let targetVoice = null;
      if (lang === 'te' || lang.startsWith('te')) {
        targetVoice = voices.find(v => v.lang.includes('te') || v.name.toLowerCase().includes('telugu'));
      }
      if (!targetVoice) {
        targetVoice = voices.find(v => v.lang.includes('en-IN') || v.name.toLowerCase().includes('india'));
      }
      if (targetVoice) {
        utterance.voice = targetVoice;
      }
    }

    this.synth.speak(utterance);
  }
}

// Global Voice Assistant Instance
document.addEventListener('DOMContentLoaded', () => {
  window.krishiVoice = new KrishiVoiceAssistant();

  // Load voices cache if available
  if (window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.getVoices();
    };
  }
});
