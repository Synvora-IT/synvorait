document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".service-card-ref");
    const dotsContainer = document.querySelector(".carousel-dots");

    if (!cards.length || !dotsContainer) {
        return;
    }

    let cardsPerSlide = 3;
    let currentSlide = 0;

    // কত মিলিসেকেন্ড পরপর slide পরিবর্তন হবে
    const autoSlideInterval = 5000;

    let autoSlideTimer;

    function getCardsPerSlide() {

        if (window.innerWidth <= 640) {
            return 1;
        }

        if (window.innerWidth <= 1024) {
            return 2;
        }

        return 3;
    }

    function getTotalSlides() {
        return Math.ceil(cards.length / cardsPerSlide);
    }

    function createDots() {

        dotsContainer.innerHTML = "";

        const totalSlides = getTotalSlides();

        for (let i = 0; i < totalSlides; i++) {

            const dot = document.createElement("button");

            dot.type = "button";
            dot.classList.add("dot");

            if (i === currentSlide) {
                dot.classList.add("active");
            }

            dot.setAttribute(
                "aria-label",
                `Go to service slide ${i + 1}`
            );

            dot.addEventListener("click", function () {

                currentSlide = i;

                showSlide();

                // Dot click করার পর timer আবার শুরু হবে
                startAutoSlide();
            });

            dotsContainer.appendChild(dot);
        }
    }

    function showSlide() {

        const start = currentSlide * cardsPerSlide;
        const end = start + cardsPerSlide;

        cards.forEach((card, index) => {

            if (index >= start && index < end) {
                card.classList.remove("carousel-hidden");
            } else {
                card.classList.add("carousel-hidden");
            }

        });

        const dots = dotsContainer.querySelectorAll(".dot");

        dots.forEach((dot, index) => {

            dot.classList.toggle(
                "active",
                index === currentSlide
            );

        });
    }

    function nextSlide() {

        const totalSlides = getTotalSlides();

        currentSlide++;

        // শেষ slide-এর পর আবার প্রথম slide
        if (currentSlide >= totalSlides) {
            currentSlide = 0;
        }

        showSlide();
    }

    function startAutoSlide() {

        // আগের timer বন্ধ করি
        clearInterval(autoSlideTimer);

        // প্রতি ৫ সেকেন্ডে next slide
        autoSlideTimer = setInterval(
            nextSlide,
            autoSlideInterval
        );
    }

    function initializeCarousel() {

        cardsPerSlide = getCardsPerSlide();

        const totalSlides = getTotalSlides();

        if (currentSlide >= totalSlides) {
            currentSlide = 0;
        }

        createDots();
        showSlide();

        // Auto slide চালু
        startAutoSlide();
    }

    let resizeTimer;

    window.addEventListener("resize", function () {

        clearTimeout(resizeTimer);

        resizeTimer = setTimeout(function () {
            initializeCarousel();
        }, 150);

    });

    initializeCarousel();

});