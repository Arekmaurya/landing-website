document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation scroll effect
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Make sure header state is correct on load
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    }

    // 2. Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if(mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            header.classList.add('scrolled'); // Ensure background is solid when menu opens
        });
    }

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });

    // 3. Intersection Observer for Scroll Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });

    // 4. Helper: Get CSRF token from the cookie (set by Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 5. Form Submission — sends booking to backend, admin gets email
    const form = document.querySelector('#appointment-form');
    const formMsg = document.querySelector('#form-msg');
    const submitBtn = document.querySelector('#submit-btn');

    if(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const originalBtnText = submitBtn.innerText;
            submitBtn.innerText = 'Confirming...';
            submitBtn.disabled = true;

            // Collect form data
            const formData = {
                name: document.querySelector('#name').value.trim(),
                age: document.querySelector('#age').value.trim(),
                sex: document.querySelector('#sex').value,
                contact: document.querySelector('#contact-input').value.trim(),
            };

            try {
                const response = await fetch('/api/appointments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok) {
                    formMsg.style.display = 'block';
                    formMsg.innerText = '✅ ' + (result.message || 'Booking confirmed!');
                    formMsg.className = 'form-message success';
                    form.reset();
                } else {
                    formMsg.style.display = 'block';
                    formMsg.innerText = result.error || 'Something went wrong. Please try again.';
                    formMsg.className = 'form-message error';
                }
            } catch (error) {
                console.error('Submission error:', error);
                formMsg.style.display = 'block';
                formMsg.innerText = 'Network error. Please try again later.';
                formMsg.className = 'form-message error';
            } finally {
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;

                setTimeout(() => {
                    formMsg.style.display = 'none';
                    formMsg.className = 'form-message';
                }, 6000);
            }
        });
    }

    // 6. Lightbox for review patient images
    const lightboxOverlay = document.getElementById('lightbox-overlay');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');

    if (lightboxOverlay) {
        // Open lightbox when clicking a review image link
        document.querySelectorAll('[data-lightbox]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const imgSrc = link.getAttribute('href');
                lightboxImg.src = imgSrc;
                lightboxOverlay.classList.add('active');
                lightboxOverlay.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
            });
        });

        // Close lightbox — close button
        lightboxClose.addEventListener('click', closeLightbox);

        // Close lightbox — overlay click (not on the image itself)
        lightboxOverlay.addEventListener('click', (e) => {
            if (e.target === lightboxOverlay) {
                closeLightbox();
            }
        });

        // Close lightbox — Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightboxOverlay.classList.contains('active')) {
                closeLightbox();
            }
        });

        function closeLightbox() {
            lightboxOverlay.classList.remove('active');
            lightboxOverlay.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }
    }
});
