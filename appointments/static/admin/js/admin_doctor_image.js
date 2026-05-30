document.addEventListener('DOMContentLoaded', function () {
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
    const MAX_SIZE_MB = 2;
    const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

    // Find the doctor_image file input
    const fileInput = document.querySelector('input[name="doctor_image"]');
    if (!fileInput) return;

    // Create preview + error elements
    const previewWrapper = document.createElement('div');
    previewWrapper.id = 'doctor-image-live-preview';

    const previewImg = document.createElement('img');
    previewImg.id = 'doctor-image-new-preview';
    previewImg.style.display = 'none';

    const errorMsg = document.createElement('div');
    errorMsg.id = 'doctor-image-error';

    const previewLabel = document.createElement('div');
    previewLabel.id = 'doctor-image-preview-label';
    previewLabel.textContent = 'New image preview:';
    previewLabel.style.display = 'none';

    previewWrapper.appendChild(previewLabel);
    previewWrapper.appendChild(previewImg);
    previewWrapper.appendChild(errorMsg);

    // Insert after the file input's parent
    const targetEl = fileInput.closest('.flex-container, .related-widget-wrapper, p, div');
    if (targetEl) {
        targetEl.after(previewWrapper);
    } else {
        fileInput.parentNode.appendChild(previewWrapper);
    }

    fileInput.addEventListener('change', function () {
        // Reset
        previewImg.style.display = 'none';
        previewLabel.style.display = 'none';
        errorMsg.textContent = '';
        errorMsg.className = '';

        const file = this.files[0];
        if (!file) return;

        // Validate type (check MIME type and file extension as fallback)
        const fileName = file.name.toLowerCase();
        const hasValidExt = fileName.endsWith('.jpg') || fileName.endsWith('.jpeg') ||
                            fileName.endsWith('.png') || fileName.endsWith('.webp');

        if (!ALLOWED_TYPES.includes(file.type) && !hasValidExt) {
            errorMsg.textContent =
                '❌ Unsupported format. Accepted: .jpg, .jpeg, .png, .webp';
            errorMsg.className = 'doctor-image-error-msg';
            this.value = '';
            return;
        }

        // Validate size
        if (file.size > MAX_SIZE_BYTES) {
            const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
            errorMsg.textContent =
                `❌ File too large (${sizeMB} MB). Maximum is ${MAX_SIZE_MB} MB.`;
            errorMsg.className = 'doctor-image-error-msg';
            this.value = '';
            return;
        }

        // Show live preview
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
            previewLabel.style.display = 'block';
        };
        reader.readAsDataURL(file);
    });

    // Toast notification on successful save (Django messages)
    const djangoMessages = document.querySelector('.messagelist');
    if (djangoMessages && djangoMessages.querySelector('.success')) {
        showToast('✅ Changes saved successfully!');
    }

    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'doctor-image-toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        // Trigger animation
        requestAnimationFrame(() => {
            toast.classList.add('visible');
        });

        setTimeout(() => {
            toast.classList.remove('visible');
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }
});
