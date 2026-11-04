/**
 * KrishiMitra - AI Chatbot Component
 * Handles rule-based farmer chat, quick suggestion chips, and text-to-speech.
 */

class KrishiChatbot {
  constructor() {
    this.chatBox = document.getElementById('kmChatBox');
    this.chatBody = document.getElementById('kmChatBody');
    this.chatInput = document.getElementById('kmChatInput');
    this.chatSendBtn = document.getElementById('kmChatSendBtn');
    this.toggleBtn = document.getElementById('kmChatToggleBtn');
    this.closeBtn = document.getElementById('kmChatCloseBtn');
    this.clearBtn = document.getElementById('kmChatClearBtn');
    this.voiceToggleBtn = document.getElementById('kmChatVoiceToggleBtn');
    
    this.voiceEnabled = true;
    this.isOpen = false;
    
    this.init();
  }

  init() {
    if (!this.chatBox && !document.getElementById('fullPageChatBody')) return;

    // Use full-page chat body if on dedicated chatbot page
    if (document.getElementById('fullPageChatBody')) {
      this.chatBody = document.getElementById('fullPageChatBody');
      this.chatInput = document.getElementById('fullPageChatInput');
      this.chatSendBtn = document.getElementById('fullPageChatSendBtn');
      this.clearBtn = document.getElementById('fullPageChatClearBtn');
    }

    if (this.toggleBtn) {
      this.toggleBtn.addEventListener('click', () => this.toggleChat());
    }

    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.closeChat());
    }

    if (this.clearBtn) {
      this.clearBtn.addEventListener('click', () => this.clearChat());
    }

    if (this.chatSendBtn) {
      this.chatSendBtn.addEventListener('click', () => this.sendMessage());
    }

    if (this.chatInput) {
      this.chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    if (this.voiceToggleBtn) {
      this.voiceToggleBtn.addEventListener('click', () => {
        this.voiceEnabled = !this.voiceEnabled;
        this.voiceToggleBtn.innerHTML = this.voiceEnabled
          ? '<i class="bi bi-volume-up-fill text-success"></i>'
          : '<i class="bi bi-volume-mute-fill text-muted"></i>';
      });
    }

    // Delegate chip pill clicks
    document.addEventListener('click', (e) => {
      if (e.target && e.target.classList.contains('chat-chip-pill')) {
        const queryText = e.target.getAttribute('data-query') || e.target.innerText.trim();
        if (this.chatInput) {
          this.chatInput.value = queryText;
          this.sendMessage();
        }
      }
    });
  }

  toggleChat() {
    if (this.isOpen) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }

  openChat() {
    if (this.chatBox) {
      this.chatBox.style.display = 'flex';
      this.isOpen = true;
      if (this.chatInput) this.chatInput.focus();
      this.scrollToBottom();
    }
  }

  closeChat() {
    if (this.chatBox) {
      this.chatBox.style.display = 'none';
      this.isOpen = false;
    }
  }

  clearChat() {
    if (this.chatBody) {
      this.chatBody.innerHTML = `
        <div class="chat-bubble chat-bubble-bot">
          <strong>KrishiMitra Assistant / కృషిమిత్ర:</strong><br>
          Chat history cleared. How can I assist you with your crops, weather, or mandi prices today?<br>
          <div class="mt-2">
            <span class="chip-pill chat-chip-pill" data-query="Paddy Blast Remedy">Paddy Blast</span>
            <span class="chip-pill chat-chip-pill" data-query="Cotton Mandi Price">Cotton Price</span>
            <span class="chip-pill chat-chip-pill" data-query="PM-KISAN Scheme">PM-KISAN</span>
            <span class="chip-pill chat-chip-pill" data-query="వరి తెగుళ్లు">వరి తెగుళ్లు</span>
          </div>
        </div>
      `;
    }
  }

  appendUserMessage(text) {
    if (!this.chatBody) return;
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble chat-bubble-user';
    bubble.innerText = text;
    this.chatBody.appendChild(bubble);
    this.scrollToBottom();
  }

  appendTypingIndicator() {
    if (!this.chatBody) return null;
    const indicator = document.createElement('div');
    indicator.id = 'chatTypingIndicator';
    indicator.className = 'chat-bubble chat-bubble-bot text-muted';
    indicator.innerHTML = '<i class="bi bi-three-dots"></i> <em>KrishiMitra is finding advice...</em>';
    this.chatBody.appendChild(indicator);
    this.scrollToBottom();
    return indicator;
  }

  removeTypingIndicator() {
    const el = document.getElementById('chatTypingIndicator');
    if (el) el.remove();
  }

  appendBotMessage(data) {
    if (!this.chatBody) return;
    this.removeTypingIndicator();

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble chat-bubble-bot';

    // Format line breaks
    const formattedText = data.response_text.replace(/\n/g, '<br>');

    let chipsHtml = '';
    if (data.suggested_chips && data.suggested_chips.length > 0) {
      chipsHtml = '<div class="mt-2 d-flex flex-wrap gap-1">';
      data.suggested_chips.forEach(chip => {
        chipsHtml += `<button type="button" class="btn btn-sm btn-outline-success rounded-pill chat-chip-pill py-0 px-2" style="font-size: 0.78rem;" data-query="${chip}">${chip}</button>`;
      });
      chipsHtml += '</div>';
    }

    let actionBtnHtml = '';
    if (data.action_url) {
      actionBtnHtml = `<div class="mt-2"><a href="${data.action_url}" class="btn btn-sm btn-km-primary py-0 px-2" style="font-size: 0.8rem;"><i class="bi bi-box-arrow-up-right me-1"></i>Open Related Section</a></div>`;
    }

    bubble.innerHTML = `
      <div>${formattedText}</div>
      ${actionBtnHtml}
      ${chipsHtml}
      <div class="mt-1 text-end" style="font-size: 0.75rem;">
        <button class="btn btn-link p-0 text-muted btn-speak-msg" title="Listen spoken response">
          <i class="bi bi-volume-up"></i> Listen
        </button>
      </div>
    `;

    // Attach speak button handler
    const speakBtn = bubble.querySelector('.btn-speak-msg');
    if (speakBtn) {
      speakBtn.addEventListener('click', () => {
        if (window.krishiVoice) {
          window.krishiVoice.speak(data.voice_text || data.response_text, data.language || 'en');
        }
      });
    }

    this.chatBody.appendChild(bubble);
    this.scrollToBottom();

    // Auto speak if enabled and requested via voice
    if (this.voiceEnabled && window.krishiVoice && data.voice_text && window.krishiVoice.lastInputWasVoice) {
      window.krishiVoice.speak(data.voice_text, data.language || 'en');
      window.krishiVoice.lastInputWasVoice = false;
    }
  }

  sendMessage() {
    if (!this.chatInput) return;
    const query = this.chatInput.value.trim();
    if (!query) return;

    this.appendUserMessage(query);
    this.chatInput.value = '';
    this.appendTypingIndicator();

    fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: query })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          this.appendBotMessage(data);
        } else {
          this.removeTypingIndicator();
          this.appendBotMessage({
            response_text: data.response_text || "I encountered an error. Please try again.",
            language: 'en'
          });
        }
      })
      .catch(err => {
        console.error("Chat error:", err);
        this.removeTypingIndicator();
        this.appendBotMessage({
          response_text: "Could not connect to KrishiMitra service. Please check your connection.",
          language: 'en'
        });
      });
  }

  scrollToBottom() {
    if (this.chatBody) {
      this.chatBody.scrollTop = this.chatBody.scrollHeight;
    }
  }
}

// Global instance
document.addEventListener('DOMContentLoaded', () => {
  window.krishiChat = new KrishiChatbot();
});
