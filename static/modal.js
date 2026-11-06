document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeBtn = document.querySelector(".close-btn");

    document.querySelectorAll(".click_row").forEach(row => {
        row.addEventListener("click", async () => {
            const id = row.getAttribute("data-id");
            modalImg.src = `/image-path?${id}`;
            modal.style.display = "flex";
        });
    });

    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
        modalImg.src = "";
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
            modalImg.src = "";
        }
    });
});