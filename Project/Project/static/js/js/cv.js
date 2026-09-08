/* ============================================
   CV - JavaScript Interactions
   ============================================ */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ========== MOBILE MENU TOGGLE ========== 
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
            
            // Animate hamburger lines
            const spans = hamburger.querySelectorAll('span');
            if (hamburger.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }
    
    // ========== SMOOTH SCROLL FOR ANCHOR LINKS ========== 
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && targetId.length > 1) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ========== NAVBAR SCROLL EFFECT ========== 
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Add shadow on scroll
        if (currentScroll > 50) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
    
    // ========== ANIMATE SECTIONS ON SCROLL ========== 
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe all sections
    const sections = document.querySelectorAll('.cv-section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
    
    // ========== ANIMATE SKILL BARS ========== 
    const skillBars = document.querySelectorAll('.skill-progress');
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
                skillObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => {
        skillObserver.observe(bar);
    });
    
    // ========== TIMELINE ANIMATION ========== 
    const timelineItems = document.querySelectorAll('.timeline-item');
    const timelineObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, index * 150);
                timelineObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    timelineItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-30px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        timelineObserver.observe(item);
    });
    
    // ========== EDUCATION/PROJECT CARDS ANIMATION ========== 
    const educationItems = document.querySelectorAll('.education-item');
    const educationObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0) scale(1)';
                }, index * 100);
                educationObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    educationItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px) scale(0.95)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        educationObserver.observe(item);
    });
    
    // ========== LANGUAGE DOTS ANIMATION ========== 
    const languageItems = document.querySelectorAll('.language-item');
    const languageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const dots = entry.target.querySelectorAll('.dot.filled');
                dots.forEach((dot, index) => {
                    setTimeout(() => {
                        dot.style.transform = 'scale(1)';
                        dot.style.opacity = '1';
                    }, index * 100);
                });
                languageObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    languageItems.forEach(item => {
        const dots = item.querySelectorAll('.dot.filled');
        dots.forEach(dot => {
            dot.style.transform = 'scale(0)';
            dot.style.opacity = '0';
            dot.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        });
        languageObserver.observe(item);
    });
    
    // ========== CERTIFICATION ITEMS ANIMATION ========== 
    const certItems = document.querySelectorAll('.cert-item');
    const certObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, index * 100);
                certObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    
    certItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-30px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        certObserver.observe(item);
    });
    
    // ========== PARALLAX EFFECT FOR HEADER ========== 
    const cvHeader = document.querySelector('.cv-header');
    if (cvHeader) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.3;
            cvHeader.style.transform = `translateY(${parallax}px)`;
        });
    }
    
    // ========== CURSOR GLOW EFFECT (Optional Enhancement) ========== 
    const createCursorGlow = () => {
        const cursorGlow = document.createElement('div');
        cursorGlow.classList.add('cursor-glow');
        document.body.appendChild(cursorGlow);
        
        document.addEventListener('mousemove', function(e) {
            cursorGlow.style.left = e.clientX + 'px';
            cursorGlow.style.top = e.clientY + 'px';
        });
    };
    
    // Add cursor glow CSS
    const style = document.createElement('style');
    style.textContent = `
        .cursor-glow {
            position: fixed;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(100, 255, 218, 0.15) 0%, transparent 70%);
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 9999;
            transition: opacity 0.3s ease;
        }
        
        @media (max-width: 768px) {
            .cursor-glow {
                display: none;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Initialize cursor glow on desktop only
    if (window.innerWidth > 768) {
        createCursorGlow();
    }
    
    // ========== PRINT FUNCTIONALITY ========== 
    window.addEventListener('beforeprint', function() {
        // Hide navigation and adjust layout for printing
        navbar.style.display = 'none';
        document.querySelector('.footer').style.display = 'none';
    });
    
    window.addEventListener('afterprint', function() {
        // Restore navigation after printing
        navbar.style.display = 'block';
        document.querySelector('.footer').style.display = 'block';
    });
    
    // ========== COPY EMAIL FUNCTIONALITY (Optional) ========== 
    const emailElements = document.querySelectorAll('.info-item');
    emailElements.forEach(item => {
        if (item.textContent.includes('@')) {
            item.style.cursor = 'pointer';
            item.addEventListener('click', function() {
                const email = this.textContent.trim().split('\n').pop();
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(email).then(() => {
                        // Show temporary tooltip
                        const tooltip = document.createElement('span');
                        tooltip.textContent = 'Copié!';
                        tooltip.style.cssText = `
                            position: absolute;
                            background: var(--accent-cyan);
                            color: var(--primary-color);
                            padding: 0.5rem 1rem;
                            border-radius: 4px;
                            font-size: 0.85rem;
                            font-weight: 600;
                            top: -40px;
                            left: 50%;
                            transform: translateX(-50%);
                            opacity: 0;
                            transition: opacity 0.3s ease;
                        `;
                        this.style.position = 'relative';
                        this.appendChild(tooltip);
                        
                        setTimeout(() => tooltip.style.opacity = '1', 10);
                        setTimeout(() => {
                            tooltip.style.opacity = '0';
                            setTimeout(() => tooltip.remove(), 300);
                        }, 2000);
                    });
                }
            });
        }
    });
    
    // ========== KEYBOARD NAVIGATION ========== 
    document.addEventListener('keydown', function(e) {
        // Press 'P' to print
        if (e.key === 'p' && e.ctrlKey) {
            e.preventDefault();
            window.print();
        }
    });
    
    console.log('CV Interactive features loaded successfully! 🚀');
});
