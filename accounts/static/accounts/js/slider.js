
document.addEventListener("DOMContentLoaded", function () {

    const slider = document.getElementById("ccSlider");

    if (!slider) return;

    const slides = slider.querySelectorAll(".cc-slide");
    const prevButton = slider.querySelector(".cc-prev");
    const nextButton = slider.querySelector(".cc-next");
    const dots = slider.querySelectorAll(".cc-dot");

    if (slides.length === 0) return;

    let currentIndex = 0;
    let autoSlide;

    function showSlide(index) {
        currentIndex = (index + slides.length) % slides.length;

        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === currentIndex);
        });

        dots.forEach((dot, i) => {
            dot.classList.toggle("active", i === currentIndex);
        });
    }

    function startAutoSlide() {
        clearInterval(autoSlide);

        autoSlide = setInterval(() => {
            showSlide(currentIndex + 1);
        }, 5000);
    }

    if (nextButton) {
        nextButton.addEventListener("click", () => {
            showSlide(currentIndex + 1);
            startAutoSlide();
        });
    }

    if (prevButton) {
        prevButton.addEventListener("click", () => {
            showSlide(currentIndex - 1);
            startAutoSlide();
        });
    }

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showSlide(index);
            startAutoSlide();
        });
    });

    showSlide(0);
    startAutoSlide();

});
