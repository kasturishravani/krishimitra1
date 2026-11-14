/**
 * KrishiMitra - AI Pest & Crop Disease Camera Scanner
 * Handles live browser camera capture, image uploads, preview,
 * and integration with the backend identification model.
 */

(function () {
  'use strict';

  // State
  let cameraStream = null;
  let currentFacingMode = 'environment'; // 'environment' (rear) or 'user' (front)
  let capturedDataUrl = null;
  let selectedImageDataUrl = null;
  let selectedImageSource = ''; // 'camera' or 'upload'

  // DOM Elements
  let cameraModal = null;
  let modalEl = null;
  let videoEl = null;
  let snapshotEl = null;
  let captureCanvas = null;
  let btnCapture = null;
  let btnRetake = null;
  let btnUsePhoto = null;
  let btnSwitchCam = null;
  let cameraErrorAlert = null;
  let cameraViewContainer = null;
  let cameraCapturedContainer = null;

  // Page Elements
  let fileInput = null;
  let btnTriggerUpload = null;
  let btnTriggerCamera = null;
  let dropzoneEl = null;
  let previewSection = null;
  let previewImageEl = null;
  let previewSourceLabel = null;
  let btnRemoveImage = null;
  let btnAnalyze = null;
  let cropSelector = null;
  let resultSection = null;
  let errorAlert = null;

  document.addEventListener('DOMContentLoaded', initPestScanner);

  function initPestScanner() {
    // Modal Elements
    modalEl = document.getElementById('pestCameraModal');
    if (modalEl && window.bootstrap) {
      cameraModal = new bootstrap.Modal(modalEl, { backdrop: 'static', keyboard: false });
    }

    videoEl = document.getElementById('pestCameraVideo');
    snapshotEl = document.getElementById('capturedPhotoSnapshot');
    captureCanvas = document.getElementById('pestCaptureCanvas');
    btnCapture = document.getElementById('btnCapturePhoto');
    btnRetake = document.getElementById('btnRetakePhoto');
    btnUsePhoto = document.getElementById('btnUsePhoto');
    btnSwitchCam = document.getElementById('btnSwitchCamera');
    cameraErrorAlert = document.getElementById('cameraErrorAlert');
    cameraViewContainer = document.getElementById('cameraViewContainer');
    cameraCapturedContainer = document.getElementById('cameraCapturedContainer');

    // Page Elements
    fileInput = document.getElementById('pestImageFileInput');
    btnTriggerUpload = document.getElementById('btnTriggerUpload');
    btnTriggerCamera = document.getElementById('btnTriggerCamera');
    dropzoneEl = document.getElementById('pestUploadDropzone');
    previewSection = document.getElementById('pestImagePreviewSection');
    previewImageEl = document.getElementById('pestPreviewImg');
    previewSourceLabel = document.getElementById('pestPreviewSourceLabel');
    btnRemoveImage = document.getElementById('btnRemovePestImage');
    btnAnalyze = document.getElementById('btnAnalyzeCropImage');
    cropSelector = document.getElementById('pestCropSelector');
    resultSection = document.getElementById('pestAnalysisResultSection');
    errorAlert = document.getElementById('pestScannerErrorAlert');

    bindEvents();
  }

  function bindEvents() {
    // 1. Open Camera button
    if (btnTriggerCamera) {
      btnTriggerCamera.addEventListener('click', () => {
        openCameraInterface();
      });
    }

    // 2. Upload file button
    if (btnTriggerUpload && fileInput) {
      btnTriggerUpload.addEventListener('click', () => {
        fileInput.click();
      });
    }

    // 3. File Input Change
    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (file) {
          handleSelectedFile(file);
        }
      });
    }

    // 4. Drag & drop on dropzone
    if (dropzoneEl) {
      ['dragenter', 'dragover'].forEach(eventName => {
        dropzoneEl.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneEl.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach(eventName => {
        dropzoneEl.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzoneEl.classList.remove('dragover');
        });
      });

      dropzoneEl.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
          handleSelectedFile(files[0]);
        }
      });
    }

    // 5. Camera Capture Button
    if (btnCapture) {
      btnCapture.addEventListener('click', captureFrame);
    }

    // 6. Camera Retake Button
    if (btnRetake) {
      btnRetake.addEventListener('click', retakePhoto);
    }

    // 7. Camera Use Photo Button
    if (btnUsePhoto) {
      btnUsePhoto.addEventListener('click', useCapturedPhoto);
    }

    // 8. Switch Camera (Front/Rear)
    if (btnSwitchCam) {
      btnSwitchCam.addEventListener('click', switchCameraFacing);
    }

    // 9. Stop camera when modal is closed
    if (modalEl) {
      modalEl.addEventListener('hidden.bs.modal', () => {
        stopCameraStream();
      });
    }

    // 10. Always stop camera on page leave / unload
    window.addEventListener('beforeunload', stopCameraStream);
    window.addEventListener('pagehide', stopCameraStream);

    // 11. Remove Image Button
    if (btnRemoveImage) {
      btnRemoveImage.addEventListener('click', removeSelectedImage);
    }

    // 12. Analyze Button
    if (btnAnalyze) {
      btnAnalyze.addEventListener('click', analyzeSelectedImage);
    }
  }

  // ==========================================
  // CAMERA STREAM MANAGEMENT
  // ==========================================

  function openCameraInterface() {
    clearCameraErrors();
    resetCameraModalState();

    if (cameraModal) {
      cameraModal.show();
    }

    startCameraStream();
  }

  function startCameraStream() {
    // Check HTTPS or Localhost requirement
    const isLocal = Boolean(
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1' ||
      window.location.hostname === '[::1]'
    );
    const isSecure = window.location.protocol === 'https:';

    if (!isSecure && !isLocal) {
      showCameraError(
        "Camera access requires a secure connection (HTTPS) or localhost. " +
        "Please browse via HTTPS or use the 'Upload Image' option."
      );
      return;
    }

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showCameraError(
        "Browser camera access is not supported by your current browser. " +
        "Please use modern Chrome, Edge, or Safari, or use the 'Upload Image' option."
      );
      return;
    }

    stopCameraStream();

    const constraints = {
      video: {
        facingMode: { ideal: currentFacingMode },
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    };

    navigator.mediaDevices.getUserMedia(constraints)
      .then(stream => {
        cameraStream = stream;
        if (videoEl) {
          videoEl.srcObject = stream;
          videoEl.play().catch(err => {
            console.warn("Autoplay was prevented:", err);
          });
        }
      })
      .catch(err => {
        console.error("Camera access error:", err);
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          showCameraError(
            "Camera permission was denied. Please allow camera permissions in your browser address bar to capture crop photos, or use 'Upload Image'."
          );
        } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
          showCameraError(
            "No camera hardware detected on this device. Please use the 'Upload Image' option."
          );
        } else {
          showCameraError(`Camera initialization error (${err.name}). Please use the 'Upload Image' option.`);
        }
      });
  }

  function stopCameraStream() {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => {
        try {
          track.stop();
        } catch (e) {
          console.warn("Error stopping track:", e);
        }
      });
      cameraStream = null;
    }

    if (videoEl) {
      videoEl.srcObject = null;
    }
  }

  function switchCameraFacing() {
    currentFacingMode = (currentFacingMode === 'environment') ? 'user' : 'environment';
    startCameraStream();
  }

  function captureFrame() {
    if (!videoEl || !captureCanvas) return;

    const width = videoEl.videoWidth || 640;
    const height = videoEl.videoHeight || 480;

    captureCanvas.width = width;
    captureCanvas.height = height;

    const ctx = captureCanvas.getContext('2d');
    ctx.drawImage(videoEl, 0, 0, width, height);

    capturedDataUrl = captureCanvas.toDataURL('image/jpeg', 0.92);

    if (snapshotEl) {
      snapshotEl.src = capturedDataUrl;
    }

    // Switch view to captured state
    if (cameraViewContainer) cameraViewContainer.classList.add('d-none');
    if (cameraCapturedContainer) cameraCapturedContainer.classList.remove('d-none');
  }

  function retakePhoto() {
    capturedDataUrl = null;
    if (snapshotEl) snapshotEl.src = '';

    if (cameraCapturedContainer) cameraCapturedContainer.classList.add('d-none');
    if (cameraViewContainer) cameraViewContainer.classList.remove('d-none');
  }

  function useCapturedPhoto() {
    if (!capturedDataUrl) return;

    selectedImageDataUrl = capturedDataUrl;
    selectedImageSource = 'camera';

    stopCameraStream();

    if (cameraModal) {
      cameraModal.hide();
    }

    displayImagePreview(selectedImageDataUrl, 'Live Camera Capture (లైవ్ ఫోటో)');
  }

  function resetCameraModalState() {
    capturedDataUrl = null;
    if (snapshotEl) snapshotEl.src = '';
    if (cameraViewContainer) cameraViewContainer.classList.remove('d-none');
    if (cameraCapturedContainer) cameraCapturedContainer.classList.add('d-none');
  }

  function showCameraError(msg) {
    if (cameraErrorAlert) {
      cameraErrorAlert.innerText = msg;
      cameraErrorAlert.classList.remove('d-none');
    }
  }

  function clearCameraErrors() {
    if (cameraErrorAlert) {
      cameraErrorAlert.classList.add('d-none');
      cameraErrorAlert.innerText = '';
    }
  }

  // ==========================================
  // IMAGE PREVIEW & UPLOAD HANDLING
  // ==========================================

  function handleSelectedFile(file) {
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      showPageError("Please select a valid image file (.jpg, .jpeg, .png, or .webp).");
      return;
    }

    // Size limit check (15 MB)
    if (file.size > 15 * 1024 * 1024) {
      showPageError("Image size exceeds 15 MB. Please select or capture a smaller image.");
      return;
    }

    clearPageError();

    const reader = new FileReader();
    reader.onload = function (e) {
      selectedImageDataUrl = e.target.result;
      selectedImageSource = 'upload';
      displayImagePreview(selectedImageDataUrl, `Uploaded: ${file.name}`);
    };
    reader.onerror = function () {
      showPageError("Failed to read the selected file. Please try another image.");
    };
    reader.readAsDataURL(file);
  }

  function displayImagePreview(dataUrl, sourceLabel) {
    if (previewImageEl) {
      previewImageEl.src = dataUrl;
    }
    if (previewSourceLabel) {
      previewSourceLabel.innerText = sourceLabel || 'Selected Image';
    }
    if (previewSection) {
      previewSection.classList.remove('d-none');
    }

    // Hide any previous result when a new image is selected
    if (resultSection) {
      resultSection.classList.add('d-none');
    }

    // Smooth scroll to preview
    if (previewSection) {
      previewSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  function removeSelectedImage() {
    selectedImageDataUrl = null;
    selectedImageSource = '';

    if (fileInput) fileInput.value = '';
    if (previewImageEl) previewImageEl.src = '';
    if (previewSection) previewSection.classList.add('d-none');
    if (resultSection) resultSection.classList.add('d-none');
    clearPageError();
  }

  // ==========================================
  // AI IDENTIFICATION CALL & DISPLAY
  // ==========================================

  function analyzeSelectedImage() {
    if (!selectedImageDataUrl) {
      showPageError("No image available to analyze. Please take a picture or upload an image.");
      return;
    }

    clearPageError();

    // Show loading state on analyze button
    const originalBtnText = btnAnalyze ? btnAnalyze.innerHTML : '';
    if (btnAnalyze) {
      btnAnalyze.disabled = true;
      btnAnalyze.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing Leaf Symptoms...';
    }

    const cropHint = cropSelector ? cropSelector.value : '';

    fetch('/api/identify-pest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: selectedImageDataUrl,
        crop: cropHint
      })
    })
      .then(res => res.json())
      .then(data => {
        if (btnAnalyze) {
          btnAnalyze.disabled = false;
          btnAnalyze.innerHTML = originalBtnText;
        }

        if (data.status === 'success') {
          renderAnalysisResult(data);
        } else {
          showPageError(data.message || "Pest identification could not recognize the symptom. Please try capturing a clearer, well-lit photo of the affected area.");
        }
      })
      .catch(err => {
        console.error("Analysis API error:", err);
        if (btnAnalyze) {
          btnAnalyze.disabled = false;
          btnAnalyze.innerHTML = originalBtnText;
        }
        showPageError("Connection failed while communicating with the KrishiMitra AI engine. Please check your network and try again.");
      });
  }

  function renderAnalysisResult(data) {
    if (!resultSection) return;

    // Disease Name & Telugu Name
    const titleEl = document.getElementById('resDiseaseName');
    if (titleEl) titleEl.innerText = data.disease_name;

    const teTitleEl = document.getElementById('resTeDiseaseName');
    if (teTitleEl) teTitleEl.innerText = data.te_name || '';

    // Crop & Pathogen Type
    const cropBadge = document.getElementById('resCropBadge');
    if (cropBadge) cropBadge.innerText = data.crop;

    const typeBadge = document.getElementById('resTypeBadge');
    if (typeBadge) typeBadge.innerText = data.type;

    // Confidence Score & Meter
    const scoreText = document.getElementById('resConfidenceScore');
    if (scoreText) scoreText.innerText = `${data.confidence_score}%`;

    const scoreMeter = document.getElementById('resConfidenceMeterFill');
    if (scoreMeter) scoreMeter.style.width = `${data.confidence_score}%`;

    // Severity Badge
    const severityBadge = document.getElementById('resSeverityBadge');
    if (severityBadge) {
      severityBadge.className = `badge bg-${data.badge}-subtle text-${data.badge} border border-${data.badge}-subtle px-2 py-1`;
      severityBadge.innerText = `${data.severity} Risk`;
    }

    // Symptoms
    const symptomsEl = document.getElementById('resSymptoms');
    if (symptomsEl) symptomsEl.innerText = data.symptoms;

    // Organic Remedy
    const organicEl = document.getElementById('resOrganicRemedy');
    if (organicEl) organicEl.innerText = data.organic_remedy;

    // Chemical Remedy
    const chemicalEl = document.getElementById('resChemicalRemedy');
    if (chemicalEl) chemicalEl.innerText = data.chemical_remedy;

    // Prevention
    const preventionEl = document.getElementById('resPrevention');
    if (preventionEl) preventionEl.innerText = data.prevention;

    // Detail Protocol Link
    const detailBtn = document.getElementById('resDetailBtn');
    if (detailBtn && data.detail_url) {
      detailBtn.href = data.detail_url;
    }

    // Voice Speak Result Button
    const voiceBtn = document.getElementById('resSpeakBtn');
    if (voiceBtn) {
      voiceBtn.onclick = function () {
        if (window.krishiVoice) {
          const speechText = `Identified: ${data.disease_name} on ${data.crop}. Organic treatment: ${data.organic_remedy}. Chemical spray: ${data.chemical_remedy}`;
          window.krishiVoice.speak(speechText, 'en');
        }
      };
    }

    // Chatbot query button
    const chatBtn = document.getElementById('resChatBtn');
    if (chatBtn) {
      chatBtn.onclick = function () {
        if (window.krishiChat) {
          window.krishiChat.openChat();
          const chatInput = document.getElementById('kmChatInput');
          if (chatInput) {
            chatInput.value = `Tell me more about treatment for ${data.disease_name}`;
            window.krishiChat.sendMessage();
          }
        }
      };
    }

    // Show result card
    resultSection.classList.remove('d-none');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function showPageError(msg) {
    if (errorAlert) {
      errorAlert.innerText = msg;
      errorAlert.classList.remove('d-none');
      errorAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
      alert(msg);
    }
  }

  function clearPageError() {
    if (errorAlert) {
      errorAlert.classList.add('d-none');
      errorAlert.innerText = '';
    }
  }

})();
