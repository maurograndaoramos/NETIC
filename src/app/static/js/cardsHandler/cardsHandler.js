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
    document.querySelector(".userModel").classList.add("userModel_disappear")
});

function filterCards(course) {
    visibleCards = allCards.filter(card => card.course === course && !hiddenCards.includes(card));
    console.log("init  :  ", visibleCards);
    console.log(visibleCards.length);

    currentCardIndex = 0;
    updateDisplayedCard();
}

function updateDisplayedCard() {
    allCards.forEach(card => {
        card.element.style.display = "none";
    });

    if (visibleCards.length > 0 && currentCardIndex < visibleCards.length) {
        document.querySelector(".cards").style.display = "flex";
        document.querySelector(".noCards").style.display = "none";
        const cardToDisplay = visibleCards[currentCardIndex];
        cardToDisplay.element.style.display = "flex";

        // Update the modal content with the current card data
        updateModalContent(cardToDisplay);
    }else {
        document.querySelector(".cards").style.display = "none";
        document.querySelector(".noCards").style.display = "flex";
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

        // Exemplo de dados a serem enviados
        const dados = {
            userToAdd: currentCard.element.getAttribute("userId"),
            userId: currentCard.element.getAttribute("loggedUserId"),
        };  
        

        // Envio dos dados para o Django
        fetch('http://localhost:8000/receive_id/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dados)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            })
            .catch(error => console.error('Erro:', error));

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }


        currentCard.element.classList.add('slide-up');
        setTimeout(() => {
            currentCard.element.style.display = "none";
            currentCard.element.classList.remove('slide-up');
            hiddenCards.push(currentCard);
            visibleCards.shift();
            currentCardIndex = (currentCardIndex + 1) % visibleCards.length;
            updateDisplayedCard();
            if (visibleCards.length == 0) {
                document.querySelector(".cards").style.display = "none";
                document.querySelector(".noCards").style.display = "flex";
            }
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