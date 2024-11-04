
let allCards = [];
let visibleCards = [];
let hiddenCards = [];
let currentCardIndex = 0;

function initializeCards() {
    const cards = document.querySelectorAll('.card');
    allCards = Array.from(cards).map(card => {
        card.querySelector(".seemore button").onclick = () => {
            document.querySelector(".userModel").style.display ="flex"
            document.querySelector(".userModel").classList.add("userModel_appear")
            
            const JustToChangeModel = {
                element: card,
                image: (card.querySelector('.image img')?.src || "").trim(),
                name: (card.querySelector('.name h3')?.textContent || "").trim(),
                course: (card.querySelector('.course p')?.textContent || "").trim(),
                description: (card.querySelector('.description p')?.textContent || "").trim(),
                bigDiscription: (card.querySelector('.bigDiscription p')?.textContent || "").trim()
            };
            updateModalContent(JustToChangeModel)
        }

        return {
            element: card,
            image: (card.querySelector('.image img')?.src || "").trim(),
            name: (card.querySelector('.name h3')?.textContent || "").trim(),
            course: (card.querySelector('.course p')?.textContent || "").trim(),
            description: (card.querySelector('.description p')?.textContent || "").trim(),
            bigDiscription: (card.querySelector('.bigDiscription p')?.textContent || "").trim()
        };
    });



    if (window.initialCourse) {
        filterCards(window.initialCourse);
    }
}

document.querySelector(".userModel_card_close-bt").addEventListener("click", () => {
    document.querySelector(".userModel").style.display ="none"
    document.querySelector(".userModel").classList.add("userModel_appear")
});

function filterCards(course) {
    visibleCards = allCards.filter(card => card.course === course && !hiddenCards.includes(card));
    console.log("init  :  ", visibleCards);
    currentCardIndex = 0;
    updateDisplayedCard();
}

function updateDisplayedCard() {
    allCards.forEach(card => {
        card.element.style.display = "none";
    });

    if (visibleCards.length > 0 && currentCardIndex < visibleCards.length) {
        const cardToDisplay = visibleCards[currentCardIndex];
        cardToDisplay.element.style.display = "flex";

        // Update the modal content with the current card data
        updateModalContent(cardToDisplay);
    }
}

function updateModalContent(card) {
    const modal = document.querySelector('.userModel');
    if (modal) {
        modal.querySelector('.userModel_card_topInfo_image img').src = card.image;
        modal.querySelector('.userModel_card_topInfo_info h3').textContent = card.name;
        modal.querySelector('.userModel_card_topInfo_info p').textContent = card.course;
        modal.querySelector('.userModel_card_descriptions .sinopse').textContent = card.description;
        modal.querySelector('.userModel_card_descriptions .description').textContent = card.bigDiscription;
    }
}

function animateAndReplaceCardUp() {
    if (visibleCards.length === 0) return;
    const currentCard = visibleCards[currentCardIndex];
    if (currentCard) {
        currentCard.element.classList.add('slide-up');
        setTimeout(() => {
            currentCard.element.style.display = "none";
            currentCard.element.classList.remove('slide-up');
            hiddenCards.push(currentCard);
            visibleCards.shift();
            currentCardIndex = (currentCardIndex + 1) % visibleCards.length;
            updateDisplayedCard();
        }, 500);
    }
}

function animateAndReplaceCardDown() {
    if (visibleCards.length === 0) return;
    const currentCard = visibleCards[currentCardIndex];
    if (currentCard) {
        currentCard.element.classList.add('slide-down');
        setTimeout(() => {
            currentCard.element.style.display = "none";
            currentCard.element.classList.remove('slide-down');
            hiddenCards.push(currentCard);
            visibleCards.shift();
            currentCardIndex = (currentCardIndex - 1 + visibleCards.length) % visibleCards.length;
            updateDisplayedCard();
        }, 500);
    }
}

document.querySelector("body").addEventListener("changedCourse", function (event) {
    const selectedCourse = event.detail.course.trim();
    console.log(selectedCourse);
    filterCards(selectedCourse);
});

document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowUp") {
        animateAndReplaceCardUp();
    } else if (event.key === "ArrowDown") {
        animateAndReplaceCardDown();
    }
});

document.addEventListener("DOMContentLoaded", initializeCards);
