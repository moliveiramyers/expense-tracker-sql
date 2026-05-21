function updateExpense(id) {
    fetch("/update/" + id, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: document.getElementById("title-" + id).value,
            amount: parseFloat(document.getElementById("amount-" + id).value),
            category: document.getElementById("category-" + id).value,
            date: document.getElementById("date-" + id).value
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log("updated:", data);

            // pega a linha atual
            const row = document.getElementById("row-" + id);

            row.style.backgroundColor = "#e7ffe7";

            setTimeout(() => {
                row.style.backgroundColor = "white";
            }, 500);
        })
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".save-expense").forEach((button) => {
        button.addEventListener("click", () => {
            updateExpense(button.dataset.expenseId);
        });
    });
});