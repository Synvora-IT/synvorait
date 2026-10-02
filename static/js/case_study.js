const CASES = JSON.parse(
    document.getElementById("cases").textContent
);


// ======================================================
// DOM ELEMENTS
// ======================================================

const track = document.querySelector("#csTrack");
const modal = document.querySelector("#csModal");


// ======================================================
// STATE
// ======================================================

let list = CASES.slice();
let current = 0;


// ======================================================
// HELPERS
// ======================================================

const $ = (selector) => {
    return document.querySelector(selector);
};


const escapeHTML = (value) => {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
};


// ======================================================
// CATEGORY / SERVICE TAG
// ======================================================

const tag = (project) => {

    return `
        <span class="cs-tag">
            ${escapeHTML(project.cat || "Uncategorized")}
        </span>
    `;
};


// ======================================================
// PROJECT IMAGE
// ======================================================

const projectCover = (project) => {

    if (project.image) {

        return `
            <div class="cs-card-cover">
                <img
                    src="${escapeHTML(project.image)}"
                    alt="${escapeHTML(project.title)}"
                    loading="lazy"
                >
            </div>
        `;

    }

    return `
        <div class="cs-card-cover cs-no-image">
            <span>No image available</span>
        </div>
    `;
};


// ======================================================
// DURATION
// ======================================================

const getDuration = (project) => {

    if (!project.start_date || !project.end_date) {
        return "—";
    }

    const start = new Date(project.start_date);
    const end = new Date(project.end_date);

    const difference =
        Math.ceil(
            (end - start) / (1000 * 60 * 60 * 24)
        );

    if (difference < 0) {
        return "—";
    }

    if (difference === 0) {
        return "1 day";
    }

    if (difference < 7) {
        return `${difference} days`;
    }

    const weeks = Math.ceil(difference / 7);

    if (weeks === 1) {
        return "1 week";
    }

    return `${weeks} weeks`;
};


// ======================================================
// TECHNOLOGIES
// ======================================================

const renderTechnologies = (project) => {

    if (!project.stack || project.stack.length === 0) {
        return `
            <span class="cs-empty">
                No technologies
            </span>
        `;
    }

    return project.stack
        .map(technology => `
            <span class="cs-tech">
                ${escapeHTML(technology)}
            </span>
        `)
        .join("");
};


// ======================================================
// BUILD FILTERS
// ======================================================

const buildFilters = () => {

    const filterContainer = $("#csFilters");

    if (!filterContainer) {
        return;
    }

    const categories = [
        ...new Set(
            CASES
                .map(project => project.cat)
                .filter(Boolean)
        )
    ];

    filterContainer.innerHTML = `
        <button
            type="button"
            class="cs-filter active"
            data-filter="all"
        >
            All
        </button>

        ${categories
            .map(category => `
                <button
                    type="button"
                    class="cs-filter"
                    data-filter="${escapeHTML(category)}"
                >
                    ${escapeHTML(category)}
                </button>
            `)
            .join("")
        }
    `;


    filterContainer
        .querySelectorAll(".cs-filter")
        .forEach(button => {

            button.addEventListener("click", () => {

                filterContainer
                    .querySelectorAll(".cs-filter")
                    .forEach(item => {
                        item.classList.remove("active");
                    });

                button.classList.add("active");

                const filter =
                    button.dataset.filter;

                if (filter === "all") {

                    list = CASES.slice();

                } else {

                    list = CASES.filter(
                        project => project.cat === filter
                    );

                }

                current = 0;

                renderCards();

                update();
            });
        });
};


// ======================================================
// RENDER CARDS
// ======================================================

const renderCards = () => {

    if (!track) {
        return;
    }


    if (list.length === 0) {

        track.innerHTML = `
            <div class="cs-empty-state">
                <h3>No projects found</h3>
                <p>
                    There are no projects in this category.
                </p>
            </div>
        `;

        return;
    }


    track.innerHTML = list
        .map((project, index) => {

            return `
                <article
                    class="cs-card"
                    data-i="${index}"
                >

                    ${projectCover(project)}

                    <div class="cs-card-body">

                        <div class="cs-card-top">

                            ${tag(project)}

                            <span class="cs-client">
                                ${escapeHTML(
                                    project.client || "Client"
                                )}
                            </span>

                        </div>


                        <h3 class="cs-card-title">
                            ${escapeHTML(project.title)}
                        </h3>


                        <p class="cs-card-summary">
                            ${escapeHTML(
                                project.summary || ""
                            )}
                        </p>


                        <div class="cs-card-meta">

                            <div class="cs-meta-item">

                                <span class="cs-meta-label">
                                    Technologies
                                </span>

                                <strong>
                                    ${
                                        project.stack
                                            ? project.stack.length
                                            : 0
                                    }
                                </strong>

                            </div>


                            <div class="cs-meta-item">

                                <span class="cs-meta-label">
                                    Duration
                                </span>

                                <strong>
                                    ${getDuration(project)}
                                </strong>

                            </div>

                        </div>


                        <button
                            type="button"
                            class="cs-preview"
                            data-preview="${index}"
                        >
                            Preview
                        </button>

                    </div>

                </article>
            `;

        })
        .join("");


    attachCardEvents();
};


// ======================================================
// CARD EVENTS
// ======================================================

const attachCardEvents = () => {

    track
        .querySelectorAll(".cs-card")
        .forEach(card => {

            card.addEventListener("click", (event) => {

                if (
                    event.target.closest(".cs-preview")
                ) {
                    return;
                }

                const index =
                    Number(card.dataset.i);

                openCase(index);
            });
        });


    track
        .querySelectorAll(".cs-preview")
        .forEach(button => {

            button.addEventListener("click", (event) => {

                event.stopPropagation();

                const index =
                    Number(button.dataset.preview);

                openCase(index);
            });
        });
};


// ======================================================
// CAROUSEL
// ======================================================

const prev = $("#csPrev");
const next = $("#csNext");
const bar = $("#csBar");
const count = $("#csCount");


const step = () => {

    const card =
        track?.querySelector(".cs-card");

    if (!card) {
        return 0;
    }

    return (
        card.getBoundingClientRect().width + 24
    );
};


// ======================================================
// CAROUSEL UPDATE
// ======================================================

const update = () => {

    if (!track) {
        return;
    }

    const maxScroll =
        track.scrollWidth - track.clientWidth;


    if (prev) {

        prev.disabled =
            track.scrollLeft <= 5;

    }


    if (next) {

        next.disabled =
            track.scrollLeft >= maxScroll - 5;

    }


    if (bar) {

        const percentage =
            maxScroll > 0
                ? (track.scrollLeft / maxScroll) * 100
                : 100;

        bar.style.width =
            `${percentage}%`;

    }


    if (count) {

        const total = list.length;

        const position =
            total > 0
                ? Math.min(
                    total,
                    Math.floor(
                        track.scrollLeft / step()
                    ) + 1
                )
                : 0;

        count.textContent =
            `${position} / ${total}`;

    }
};


// ======================================================
// PREVIOUS
// ======================================================

if (prev) {

    prev.addEventListener("click", () => {

        track.scrollBy({
            left: -step(),
            behavior: "smooth"
        });

    });

}


// ======================================================
// NEXT
// ======================================================

if (next) {

    next.addEventListener("click", () => {

        track.scrollBy({
            left: step(),
            behavior: "smooth"
        });

    });

}


// ======================================================
// SCROLL
// ======================================================

if (track) {

    track.addEventListener(
        "scroll",
        update,
        { passive: true }
    );

}


// ======================================================
// RESIZE
// ======================================================

window.addEventListener(
    "resize",
    update
);


// ======================================================
// KEYBOARD
// ======================================================

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "ArrowLeft" &&
            prev
        ) {
            prev.click();
        }


        if (
            event.key === "ArrowRight" &&
            next
        ) {
            next.click();
        }

    }
);


// ======================================================
// MOUSE DRAG SCROLL
// ======================================================

let down = false;
let startX = 0;
let scrollLeft = 0;
let moved = false;


if (track) {

    track.addEventListener(
        "pointerdown",
        (event) => {

            down = true;
            moved = false;

            startX =
                event.clientX;

            scrollLeft =
                track.scrollLeft;

            track.setPointerCapture(
                event.pointerId
            );

            track.classList.add("dragging");

        }
    );


    track.addEventListener(
        "pointermove",
        (event) => {

            if (!down) {
                return;
            }

            const distance =
                event.clientX - startX;

            if (Math.abs(distance) > 5) {
                moved = true;
            }

            track.scrollLeft =
                scrollLeft - distance;

        }
    );


    const stopDragging = () => {

        if (!down) {
            return;
        }

        down = false;

        track.classList.remove(
            "dragging"
        );


        if (moved) {

            const position =
                Math.round(
                    track.scrollLeft / step()
                );

            track.scrollTo({
                left: position * step(),
                behavior: "smooth"
            });

        }

    };


    track.addEventListener(
        "pointerup",
        stopDragging
    );


    track.addEventListener(
        "pointercancel",
        stopDragging
    );


    track.addEventListener(
        "pointerleave",
        () => {

            if (down) {
                stopDragging();
            }

        }
    );

}


// ======================================================
// OPEN MODAL
// ======================================================

const openCase = (index) => {

    if (!modal || list.length === 0) {
        return;
    }


    current =
        (index + list.length) %
        list.length;


    const project =
        list[current];


    modal.innerHTML = `

        <div class="cs-modal-backdrop">

            <div
                class="cs-modal-content"
                role="dialog"
                aria-modal="true"
            >

                <button
                    type="button"
                    class="cs-modal-close"
                    aria-label="Close"
                >
                    ×
                </button>


                <div class="cs-modal-image">

                    ${
                        project.image
                            ? `
                                <img
                                    src="${escapeHTML(
                                        project.image
                                    )}"
                                    alt="${escapeHTML(
                                        project.title
                                    )}"
                                >
                              `
                            : `
                                <div class="cs-no-image">
                                    No image available
                                </div>
                              `
                    }

                </div>


                <div class="cs-modal-body">

                    <div class="cs-modal-top">

                        ${tag(project)}

                        <span class="cs-client">
                            ${escapeHTML(
                                project.client || "Client"
                            )}
                        </span>

                    </div>


                    <h2>
                        ${escapeHTML(project.title)}
                    </h2>


                    <p class="cs-modal-summary">
                        ${escapeHTML(
                            project.summary || ""
                        )}
                    </p>


                    <div class="cs-modal-facts">

                        <div>
                            <span>
                                Service
                            </span>

                            <strong>
                                ${escapeHTML(
                                    project.cat ||
                                    "Uncategorized"
                                )}
                            </strong>
                        </div>


                        <div>
                            <span>
                                Duration
                            </span>

                            <strong>
                                ${getDuration(project)}
                            </strong>
                        </div>


                        <div>
                            <span>
                                Technologies
                            </span>

                            <strong>
                                ${
                                    project.stack
                                        ? project.stack.length
                                        : 0
                                }
                            </strong>
                        </div>

                    </div>


                    ${
                        project.description
                            ? `
                                <section class="cs-modal-section">

                                    <h3>
                                        Description
                                    </h3>

                                    <div class="cs-description">
                                        ${project.description}
                                    </div>

                                </section>
                              `
                            : ""
                    }


                    <section class="cs-modal-section">

                        <h3>
                            Technologies
                        </h3>

                        <div class="cs-tech-list">
                            ${renderTechnologies(project)}
                        </div>

                    </section>


                    <div class="cs-modal-actions">

                        <button
                            type="button"
                            class="cs-modal-prev"
                        >
                            Previous
                        </button>


                        <button
                            type="button"
                            class="cs-modal-next"
                        >
                            Next
                        </button>

                    </div>

                </div>

            </div>

        </div>

    `;


    modal.classList.add("open");

    document.body.style.overflow =
        "hidden";


    const closeButton =
        modal.querySelector(
            ".cs-modal-close"
        );


    const backdrop =
        modal.querySelector(
            ".cs-modal-backdrop"
        );


    closeButton.addEventListener(
        "click",
        closeModal
    );


    backdrop.addEventListener(
        "click",
        (event) => {

            if (
                event.target === backdrop
            ) {
                closeModal();
            }

        }
    );


    modal
        .querySelector(".cs-modal-prev")
        .addEventListener(
            "click",
            () => {

                openCase(current - 1);

            }
        );


    modal
        .querySelector(".cs-modal-next")
        .addEventListener(
            "click",
            () => {

                openCase(current + 1);

            }
        );

};


// ======================================================
// CLOSE MODAL
// ======================================================

const closeModal = () => {

    if (!modal) {
        return;
    }

    modal.classList.remove("open");

    modal.innerHTML = "";

    document.body.style.overflow = "";

};


// ======================================================
// MODAL KEYBOARD
// ======================================================

document.addEventListener(
    "keydown",
    (event) => {

        if (
            !modal ||
            !modal.classList.contains("open")
        ) {
            return;
        }


        if (event.key === "Escape") {

            closeModal();

        }


        if (event.key === "ArrowLeft") {

            openCase(current - 1);

        }


        if (event.key === "ArrowRight") {

            openCase(current + 1);

        }

    }
);


// ======================================================
// INITIALIZE
// ======================================================

buildFilters();

renderCards();

update();