// Mobile Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        if (hamburger) {
            hamburger.classList.remove('active');
        }
    });
});

// Form Validation and Submission
const contactForm = document.getElementById('contactForm');
const successMessage = document.getElementById('successMessage');

// Validation functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    if (!phone) return true; // Phone is optional
    const re = /^[\d\s\+\-\(\)]+$/;
    return re.test(phone);
}

function showError(input, message) {
    const formGroup = input.closest('.form-group');
    const errorMessage = formGroup.querySelector('.error-message');
    
    formGroup.classList.add('error');
    errorMessage.textContent = message;
    
    input.addEventListener('input', () => {
        formGroup.classList.remove('error');
        errorMessage.textContent = '';
    }, { once: true });
}

function validateField(input) {
    const value = input.value.trim();
    const fieldName = input.name;
    
    if (input.hasAttribute('required') && !value) {
        showError(input, 'هذا الحقل مطلوب');
        return false;
    }
    
    if (fieldName === 'email' && value && !validateEmail(value)) {
        showError(input, 'البريد الإلكتروني غير صحيح');
        return false;
    }
    
    if (fieldName === 'phone' && value && !validatePhone(value)) {
        showError(input, 'رقم الهاتف غير صحيح');
        return false;
    }
    
    if (fieldName === 'message' && value.length < 10) {
        showError(input, 'الرسالة يجب أن تحتوي على 10 أحرف على الأقل');
        return false;
    }
    
    return true;
}

// Real-time validation on blur
document.querySelectorAll('input, select, textarea').forEach(input => {
    input.addEventListener('blur', () => {
        if (input.value.trim()) {
            validateField(input);
        }
    });
});

// Form submission - laisse Django gérer, preventDefault seulement si invalide
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        const inputs = contactForm.querySelectorAll('input:not([type="checkbox"]), select, textarea');
        const consent = document.getElementById('consent');
        
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        if (!consent.checked) {
            showError(consent, 'يجب الموافقة على الشروط للمتابعة');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault(); // Bloque seulement si invalide
            const firstError = contactForm.querySelector('.form-group.error');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
        // Si valide : soumet normalement vers Django -> données sauvegardées en BDD
    });
}

// Animate info cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.info-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
    cardObserver.observe(card);
});

const formSection = document.querySelector('.form-section');
if (formSection) {
    formSection.style.opacity = '0';
    formSection.style.transform = 'translateY(30px)';
    formSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    cardObserver.observe(formSection);
}

const socialSection = document.querySelector('.social-section');
if (socialSection) {
    socialSection.style.opacity = '0';
    socialSection.style.transform = 'translateY(30px)';
    socialSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    cardObserver.observe(socialSection);
}

document.querySelectorAll('.social-link').forEach(link => {
    link.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px) scale(1.05)';
    });
    
    link.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

const messageField = document.getElementById('message');
if (messageField) {
    const charCounter = document.createElement('div');
    charCounter.style.cssText = 'text-align: left; font-size: 0.85rem; color: #999; margin-top: 0.3rem;';
    messageField.parentElement.appendChild(charCounter);
    
    messageField.addEventListener('input', () => {
        const length = messageField.value.length;
        charCounter.textContent = `${length} حرف`;
        charCounter.style.color = length < 10 ? '#e74c3c' : '#27ae60';
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

console.log('Contact page loaded successfully!');
