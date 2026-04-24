const menuToggle = document.querySelector("[data-menu-toggle]");
const siteNav = document.querySelector("[data-site-nav]");

if (menuToggle && siteNav) {
  menuToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

const reveals = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    },
    {
      threshold: 0.12,
    }
  );

  reveals.forEach((element) => revealObserver.observe(element));
} else {
  reveals.forEach((element) => element.classList.add("is-visible"));
}

const mailForms = document.querySelectorAll("[data-mail-form]");

mailForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const bodyLines = [
      `Nombre: ${formData.get("nombre") || ""}`,
      `Contacto: ${formData.get("contacto") || ""}`,
      `Fase: ${formData.get("fase") || ""}`,
      "",
      "Mensaje:",
      `${formData.get("mensaje") || ""}`,
    ];

    const subject = encodeURIComponent("Consulta desde HÉROE EMPRENDEDOR");
    const body = encodeURIComponent(bodyLines.join("\n"));
    window.location.href = `mailto:info@grupovadillo.com?subject=${subject}&body=${body}`;
  });
});
