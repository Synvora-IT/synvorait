document.addEventListener("DOMContentLoaded", function () {
    // ১. সঠিক আইডি "members-data" থেকে ডেটা পার্স করা
    const membersElement = document.getElementById("members-data");
    if (!membersElement) return;

    const members = JSON.parse(membersElement.textContent);
    console.log("Team Members JS Object:", members);

    const track = document.getElementById("teamTrack");
    const dotsContainer = document.getElementById("teamDots");

    const itemsPerSlide = 6;
    let currentSlide = 0;
    const totalSlides = Math.ceil(members.length / itemsPerSlide);

    // ২. মেম্বারদের ৬টি করে ভাগে ভাগ করে স্লাইড তৈরি করা
    for (let i = 0; i < totalSlides; i++) {
        const slideGroup = document.createElement("div");
        slideGroup.className = "team-slide-group";

        const sliceItems = members.slice(i * itemsPerSlide, (i + 1) * itemsPerSlide);
        sliceItems.forEach(member => {
            slideGroup.innerHTML += `
                <div class="team-card">
                  <div class="member-img-wrap">
                    <img src="${member.user__image ? `/media/${member.user__image}` : '/static/images/default-user.webp'}" alt="${member.user__first_name} ${member.user__last_name}" style="width: 100%; height: 100%; object-fit: cover;">
                  </div>
                  <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: var(--ink); margin-bottom: 4px;">${member.user__first_name} ${member.user__last_name}</h3>
                  <p style="font-size: 13px; font-weight: 600; color: var(--accent, #3F51D9); margin: 0;">${member.designation__name}</p>
                </div>
            `;
        });
        track.appendChild(slideGroup);
    }

    // ৩. যদি স্লাইড ১টির বেশি হয় তবেই ডটগুলো জেনারেট হবে
    if (totalSlides > 1) {
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement("button");
            dot.className = `dot ${i === 0 ? "active" : ""}`;
            dot.addEventListener("click", () => {
                currentSlide = i;
                updateCarousel();
            });
            dotsContainer.appendChild(dot);
        }
    }

    function updateCarousel() {
        track.style.transform = `translateX(-${currentSlide * 100}%)`;
        const dots = dotsContainer.querySelectorAll(".dot");
        dots.forEach((dot, index) => {
            dot.classList.toggle("active", index === currentSlide);
        });
    }
});