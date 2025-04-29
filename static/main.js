function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            const [key, value] = cookie.split("=");
            if (key === name) {
                cookieValue = decodeURIComponent(value);
                break;
            }
        }
    }
    return cookieValue;
}

function calculatePrice() {
    const durationPrices = [1000, 2700, 5000, 9000]; // Примерные цены: 1 мес, 3, 6, 12
    const breakfast = document.querySelector('select[name="select1"]').value === "0";
    const lunch = document.querySelector('select[name="select2"]').value === "0";
    const dinner = document.querySelector('select[name="select3"]').value === "0";
    const dessert = document.querySelector('select[name="select4"]').value === "0";
    const persons = parseInt(document.querySelector('select[name="select5"]').value) + 1;
    const durationIndex = document.querySelector("select[name='subscription_duration']").selectedIndex;

    let base = durationPrices[durationIndex];
    let mealCount = [breakfast, lunch, dinner, dessert].filter(Boolean).length;

    let total = base + mealCount * 300 * persons;
    document.getElementById("total-price").textContent = total + "₽";
    return total;
}

function checkFormValidity() {
    const foodTypeRadios = document.querySelectorAll('input[name="foodtype"]');
    const selected = Array.from(foodTypeRadios).some((r) => r.checked);
    const payButtons = document.querySelectorAll('button[type="submit"]');
    payButtons.forEach((btn) => (btn.disabled = !selected));
}

document.addEventListener("DOMContentLoaded", function () {
    calculatePrice();
    checkFormValidity();

    // Цены при изменении селектов
    document.querySelectorAll("select").forEach((sel) => {
        sel.addEventListener("change", calculatePrice);
    });

    // Валидация выбора типа меню
    document.querySelectorAll('input[name="foodtype"]').forEach((radio) => {
        radio.addEventListener("change", checkFormValidity);
    });

    // Отправка формы
    const form = document.getElementById("order");
    const messageBox = document.getElementById("form-message");

    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const formData = new FormData(form);

            const response = await fetch("/order/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            });

            if (response.ok) {
                messageBox.textContent = "Форма успешно отправлена! Перейдите в личный кабинет для оплаты";
                messageBox.className = "alert alert-success mt-3";
            } else {
                messageBox.textContent = "Ошибка при отправке. Попробуйте снова.";
                messageBox.className = "alert alert-danger mt-3";
            }

            messageBox.classList.remove("d-none");
        });
    }
});
