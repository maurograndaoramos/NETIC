let allCards = [];
let visibleCards = [];
let hiddenCards = [];

function initializeCards() {
    const cards = document.querySelectorAll('.card');
    if (cards.length == 0 ) {
        const noCards = document.querySelector(".no-more-cards")
        if (noCards){
            noCards.style.display="flex"
        }                      
    }
    allCards = Array.from(cards).map(card => {
        card.querySelector(".seemore button").onclick = () => {
            document.querySelector(".userModel").style.display = "flex";
            document.querySelector(".userModel").classList.add("userModel_appear");

            const cardData = {
                element: card,
                image: (card.querySelector('.image img')?.src || "").trim(),
                name: (card.querySelector('.name h3')?.textContent || "").trim(),
                course: (card.querySelector('.course p')?.textContent || "").trim(),
                description: (card.querySelector('.description p')?.textContent || "").trim(),
                bigDiscription: (card.querySelector('.bigDiscription p')?.textContent || "").trim(),
                insta: (card.querySelector('.media .insta')?.textContent || "").trim(),
                github: (card.querySelector('.media .github')?.textContent || "").trim(),
                linkedin: (card.querySelector('.media .linkedin')?.textContent || "").trim(),
                web: (card.querySelector('.media .web')?.textContent || "").trim(),
            };
            updateModalContent(cardData);
        };

        card.querySelector(".add-to-network .add").onclick = () => {
            addToNetwork(card);
        };

        card.querySelector(".add-to-network .remove").onclick = () => {
            removeFromNetwork(card);
        };

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


function filterCards(course) {
    visibleCards = allCards.filter(card => card.course === course && !hiddenCards.includes(card));
    updateDisplayedCards();
}

function updateDisplayedCards() {
    allCards.forEach(card => {
        card.element.style.display = "none";
    });

    if (visibleCards.length > 0) {
        document.querySelector(".cards").style.display = "flex";
        document.querySelector(".noCards").style.display = "none";

        visibleCards.forEach(card => {
            card.element.style.display = "flex";
        });
    } else {
        document.querySelector(".cards").style.display = "none";
        document.querySelector(".noCards").style.display = "flex";
    }
}

function removeFromNetwork(cardElement) {
    const userId = cardElement.getAttribute("userId");
    const loggedUserId = cardElement.getAttribute("loggedUserId");

    const data = {
        userToRemove: userId,
        userId: loggedUserId
    };

    
    // Adiciona a animação "slide-down" ao card
    cardElement.classList.add('slide-down');
    setTimeout(() => {
        cardElement.style.display = "none";
        cardElement.classList.remove('slide-down');
        
        cardElement.parentElement.remove()
        cardElement.remove()
        
        const cards = document.querySelectorAll('.card');
        console.log(cards.length);
        
        if (cards.length == 0) {
            const noCards = document.querySelector(".no-more-cards")
            if (noCards) {
                noCards.style.display = "flex"
            }
        }
    }, 500); // Tempo para animação de 500ms

    

    // Envio da requisição ao servidor
    fetch('http://localhost:8000/remove_id/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Usuário removido da rede com sucesso:', data);
    })
    .catch(error => console.error('Erro ao remover usuário da rede:', error));
}

function addToNetwork(cardElement) {
    const userId = cardElement.getAttribute("userId");
    const loggedUserId = cardElement.getAttribute("loggedUserId");

    const data = {
        userToAdd: userId,
        userId: loggedUserId
    };

    // Adiciona a animação "slide-up" ao card
    cardElement.classList.add('slide-up');
    setTimeout(() => {
        // Após a animação, remove o card da lista visível
        cardElement.style.display = "none";
        cardElement.classList.remove('slide-up');

        // Atualiza as listas
        hiddenCards.push(visibleCards.find(card => card.element === cardElement));
        visibleCards = visibleCards.filter(card => card.element !== cardElement);
        updateDisplayedCards();
        cardElement.remove()
    }, 500); // Tempo para animação de 500ms

    // Envio da requisição ao servidor
    fetch('http://localhost:8000/receive_id/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {})
        .catch(error => console.error('Erro:', error));
}

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

function updateModalContent(card) {
    const modal = document.querySelector('.userModel');
    
    
    if (modal) {
        modal.querySelector('.userModel_card_topInfo_image img').src = card.image;
        modal.querySelector('.userModel_card_topInfo_info h3').textContent = card.name;
        modal.querySelector('.userModel_card_topInfo_info p').textContent = card.course;
        modal.querySelector('.userModel_card_descriptions .sinopse').textContent = card.description;
        modal.querySelector('.userModel_card_descriptions .description').textContent = card.bigDiscription;
        modal.querySelector('.userModel_card_links .github').setAttribute("href", card.github)
        modal.querySelector('.userModel_card_links .linkedIn').setAttribute("href", card.linkedin)
        modal.querySelector('.userModel_card_links .insta').setAttribute("href", card.insta)
        modal.querySelector('.userModel_card_links .web').setAttribute("href", card.web) 
    }
    
    modal.querySelector(".gochat").onclick = () => {
        const user_id = card.element.getAttribute("loggedUserId")
        const contact_id = card.element.getAttribute("userId")
        
        console.log(user_id);
        console.log(contact_id);
        const data = {
            user_id: user_id,
            contact_id: contact_id
        };

        // Envio da requisição ao servidor
        fetch('http://localhost:8000/get_db_id/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                
            })
            .catch(error => console.error('Erro:', error));
    }


}

document.querySelector(".userModel_card_close-bt").addEventListener("click", () => {
    document.querySelector(".userModel").style.display = "none";
    document.querySelector(".userModel").classList.remove("userModel_appear");
});

document.querySelector("body").addEventListener("changedCourse", function (event) {
    const selectedCourse = event.detail.course.trim();
    filterCards(selectedCourse);
});

document.addEventListener("DOMContentLoaded", initializeCards);