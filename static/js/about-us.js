
document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // HERO SLIDER
    // ==========================================

    const slider = document.getElementById('heroSlider');
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.slider-dot');

    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');

    const currentSlideEl = document.getElementById('currentSlide');
    const counterLine = document.getElementById('counterLine');

    const totalSlides = slides.length;

    let currentIndex = 0;
    let autoplayInterval = null;
    const autoplayDelay = 6000;
    let isPaused = false;

    function updateSlide(index) {
        if (totalSlides === 0) return;

        // Remove active class from current slide
        slides[currentIndex]?.classList.remove('active');

        dots[currentIndex]?.classList.remove('active');
        dots[currentIndex]?.setAttribute('aria-selected', 'false');

        // Calculate next slide index
        currentIndex = (index + totalSlides) % totalSlides;

        // Activate new slide
        slides[currentIndex]?.classList.add('active');

        dots[currentIndex]?.classList.add('active');
        dots[currentIndex]?.setAttribute('aria-selected', 'true');

        // Update slide number
        if (currentSlideEl) {
            currentSlideEl.textContent = String(currentIndex + 1).padStart(2, '0');
        }

        // Restart progress indicator
        if (counterLine) {
            counterLine.style.transition = 'none';
            counterLine.style.height = '0%';

            void counterLine.offsetHeight;

            counterLine.style.transition = `height ${autoplayDelay}ms linear`;
            counterLine.style.height = '100%';
        }
    }

    function goToSlide(index) {
        if (totalSlides === 0) return;

        updateSlide(index);
        resetAutoplay();
    }

    function nextSlide() {
        goToSlide(currentIndex + 1);
    }

    function prevSlide() {
        goToSlide(currentIndex - 1);
    }

    // Start automatic sliding
    function startAutoplay() {
        clearInterval(autoplayInterval);

        if (totalSlides > 1) {
            autoplayInterval = setInterval(() => {
                if (!isPaused) {
                    updateSlide(currentIndex + 1);
                }
            }, autoplayDelay);
        }
    }

    // Reset timer after manual navigation
    function resetAutoplay() {
        startAutoplay();
    }

    // Left button
    if (prevBtn) {
        prevBtn.addEventListener('click', (event) => {
            event.preventDefault();
            prevSlide();
        });
    }

    // Right button
    if (nextBtn) {
        nextBtn.addEventListener('click', (event) => {
            event.preventDefault();
            nextSlide();
        });
    }

    // Slider dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', (event) => {
            event.preventDefault();
            goToSlide(index);
        });
    });

    // Pause autoplay while hovering over the slider
    if (slider) {
        slider.addEventListener('mouseenter', () => {
            isPaused = true;
        });

        slider.addEventListener('mouseleave', () => {
            isPaused = false;
        });

        // Touch swipe support
        let touchStartX = 0;
        let touchEndX = 0;

        slider.addEventListener('touchstart', (event) => {
            touchStartX = event.changedTouches[0].screenX;
            isPaused = true;
        }, { passive: true });

        slider.addEventListener('touchend', (event) => {
            touchEndX = event.changedTouches[0].screenX;

            const difference = touchStartX - touchEndX;

            if (Math.abs(difference) > 50) {
                if (difference > 0) {
                    nextSlide();
                } else {
                    prevSlide();
                }
            }

            isPaused = false;
        }, { passive: true });
    }

    // Keyboard navigation
    document.addEventListener('keydown', (event) => {
        const target = event.target;

        // Do not change slides while typing in form fields
        if (
            target instanceof HTMLInputElement ||
            target instanceof HTMLTextAreaElement ||
            target instanceof HTMLSelectElement ||
            target.isContentEditable
        ) {
            return;
        }

        if (event.key === 'ArrowLeft') {
            prevSlide();
        }

        if (event.key === 'ArrowRight') {
            nextSlide();
        }
    });

    // Initialize slider
    if (totalSlides > 0) {
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === 0);
        });

        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === 0);
            dot.setAttribute(
                'aria-selected',
                index === 0 ? 'true' : 'false'
            );
        });

        currentIndex = 0;

        if (currentSlideEl) {
            currentSlideEl.textContent = String(1).padStart(2, '0');
        }

        if (counterLine) {
            counterLine.style.height = '0%';
            counterLine.style.transition = `height ${autoplayDelay}ms linear`;

            requestAnimationFrame(() => {
                counterLine.style.height = '100%';
            });
        }

        startAutoplay();
    }


    // ==========================================
    // NAVBAR
    // Works even if the About page uses base.html navbar
    // ==========================================

    const navbar = document.getElementById('navbar');

    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 20);
        }, { passive: true });
    }


    // ==========================================
    // MOBILE MENU
    // ==========================================

    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (navToggle && mobileMenu) {
        navToggle.addEventListener('click', () => {
            const isOpen = mobileMenu.classList.toggle('open');

            navToggle.classList.toggle('open', isOpen);
            navToggle.setAttribute('aria-expanded', String(isOpen));
        });

        mobileMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('open');
                navToggle.classList.remove('open');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }


    // ==========================================
    // SCROLL REVEAL
    // ==========================================

    const prefersReducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
    ).matches;

    const revealElements = document.querySelectorAll('.reveal');

    if (prefersReducedMotion) {
        revealElements.forEach((element) => {
            element.classList.add('visible');
        });
    } else if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -60px 0px'
        });

        revealElements.forEach((element) => {
            revealObserver.observe(element);
        });
    } else {
        revealElements.forEach((element) => {
            element.classList.add('visible');
        });
    }


    // ==========================================
    // COUNTER ANIMATION
    // ==========================================

    const countElements = document.querySelectorAll('.count-up');

    function setCounterValue(element, value) {
        element.textContent = value.toLocaleString();
    }

    function animateCounter(element) {
        const target = Number.parseInt(
            element.getAttribute('data-target'),
            10
        );

        if (!Number.isFinite(target)) return;

        const duration = 2000;
        const startTime = performance.now();

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = 1 - Math.pow(1 - progress, 3);

            setCounterValue(
                element,
                Math.floor(easedProgress * target)
            );

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                setCounterValue(element, target);
            }
        }

        requestAnimationFrame(updateCounter);
    }

    if (prefersReducedMotion) {
        countElements.forEach((element) => {
            const target = Number.parseInt(
                element.getAttribute('data-target'),
                10
            );

            if (Number.isFinite(target)) {
                setCounterValue(element, target);
            }
        });
    } else if ('IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });

        countElements.forEach((element) => {
            counterObserver.observe(element);
        });
    } else {
        countElements.forEach(animateCounter);
    }


    // ==========================================
    // SMOOTH SCROLL
    // ==========================================

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (event) => {
            const href = anchor.getAttribute('href');

            if (!href || href === '#') return;

            let target;

            try {
                target = document.querySelector(href);
            } catch {
                return;
            }

            if (!target) return;

            event.preventDefault();

            const navbarHeight = navbar
                ? navbar.offsetHeight
                : 0;

            const offset = navbarHeight + 20;

            const top =
                target.getBoundingClientRect().top +
                window.scrollY -
                offset;

            window.scrollTo({
                top,
                behavior: prefersReducedMotion ? 'auto' : 'smooth'
            });
        });
    });

});