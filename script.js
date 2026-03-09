// Mobile Menu Toggle
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navMenu = document.querySelector('.nav-menu');
const navActions = document.querySelector('.nav-actions');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('active');
        
        // Toggle menu visibility
        if (navMenu.style.display === 'flex') {
            navMenu.style.display = 'none';
            navActions.style.display = 'none';
        } else {
            navMenu.style.display = 'flex';
            navMenu.style.flexDirection = 'column';
            navMenu.style.position = 'absolute';
            navMenu.style.top = '100%';
            navMenu.style.left = '0';
            navMenu.style.right = '0';
            navMenu.style.background = '#fff';
            navMenu.style.padding = '1rem';
            navMenu.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
            navMenu.style.gap = '1rem';
            
            navActions.style.display = 'flex';
            navActions.style.flexDirection = 'column';
            navActions.style.position = 'absolute';
            navActions.style.top = 'calc(100% + ' + navMenu.offsetHeight + 'px)';
            navActions.style.left = '0';
            navActions.style.right = '0';
            navActions.style.background = '#fff';
            navActions.style.padding = '1rem';
            navActions.style.gap = '0.5rem';
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to header
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
    } else {
        header.style.boxShadow = '0 2px 8px rgba(0,0,0,0.05)';
    }
    
    lastScroll = currentScroll;
});

// Newsletter form submission
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        alert(`Thank you for subscribing with: ${email}`);
        newsletterForm.reset();
    });
}

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -10px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            // Stop observing once animation has played
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Add fade-in class to cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.capability-card, .step-card, .app-card, .benefit-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(15px)';
        card.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
        observer.observe(card);
    });
});
