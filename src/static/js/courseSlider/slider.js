let currentOptionIndex = 4;
const options = document.querySelectorAll(".option");

function updateOptionDisplay() {
    options.forEach((option, index) => {
        option.classList.remove("active"); 
        option.style.transform = `translateY(${(index - currentOptionIndex) * 100
            }%)`;
    });
    options[currentOptionIndex].classList.add("active"); 
    // console.log(`Opção selecionada: ${options[currentOptionIndex].textContent}`); 
    document.querySelector("body").dispatchEvent(new CustomEvent("changedCourse", { detail: { course: options[currentOptionIndex].textContent }}))
}

// Navegação com scroll do rato para alternar a opção selecionada
document
    .querySelector(".selector_choseCourse")
    .addEventListener("wheel", (event) => {
        if (event.deltaY > 0) {
            currentOptionIndex = (currentOptionIndex + 1) % options.length;
        } else {
            currentOptionIndex =
                (currentOptionIndex - 1 + options.length) % options.length;
        }
        updateOptionDisplay();
        event.preventDefault();
    });

document
    .querySelector(".selector_choseCourse")
    .addEventListener("keydown", (event) => {
        if (event.key === "ArrowDown") {
            currentOptionIndex = (currentOptionIndex + 1) % options.length;
        } else if (event.key === "ArrowUp") {
            currentOptionIndex =
                (currentOptionIndex - 1 + options.length) % options.length;
        }
        updateOptionDisplay();
        event.preventDefault();
    });

updateOptionDisplay();
