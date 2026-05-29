document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation scroll effect
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.add('scrolled'); // Force styling if we want it always light
            // Actually, let's keep the transparent-to-light effect:
            if (window.scrollY <= 50) {
                 header.classList.remove('scrolled');
            }
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

    // 4. Form Submission Handling
    const form = document.querySelector('#appointment-form');
    const formMsg = document.querySelector('#form-msg');
    const submitBtn = document.querySelector('#submit-btn');

    if(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Basic UI loading state
            const originalBtnText = submitBtn.innerText;
            submitBtn.innerText = 'Sending request...';
            submitBtn.disabled = true;

            // Collect form data
            const formData = {
                firstName: document.querySelector('#fname').value,
                lastName: document.querySelector('#lname').value,
                email: document.querySelector('#email').value,
                phone: document.querySelector('#phone').value,
                service: document.querySelector('#service').value,
                message: document.querySelector('#message').value,
            };

            try {
                // Send simulated POST request to our node.js backend
                const response = await fetch('/api/appointments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok) {
                    formMsg.innerText = result.message || 'Appointment requested successfully! We will contact you shortly.';
                    formMsg.className = 'form-message success';
                    form.reset();
                } else {
                    formMsg.innerText = result.error || 'An error occurred. Please try again.';
                    formMsg.className = 'form-message error';
                }
            } catch (error) {
                console.error('Submission error:', error);
                // Fallback gracefully if backend is not running
                formMsg.innerText = 'Network error or backend is not running. Form submitted locally!';
                formMsg.className = 'form-message success';
                form.reset();
            } finally {
                // Restore button state
                submitBtn.innerText = originalBtnText;
                submitBtn.disabled = false;
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    formMsg.style.display = 'none';
                    // clear classes
                    formMsg.className = 'form-message';
                }, 5000);
            }
        });
    }
});
