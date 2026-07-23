const mapeoProductos = {
    "Control de Temperatura": ["Termocuplas", "Controladores de temperatura"],
    "Lectoras Industriales": ["De marca", "De etiqueta", "Lectura de códigos", "Trazabilidad de empaque"],
    "Sensores de Proximidad": ["Inductivos", "Capacitivos", "Posición lineal"],
    "Sensores Fotoeléctricos": ["Barrera", "Supresión de fondo", "Reflex", "Autoreflex", "Tipo U"],
    "Relevadores": ["Estado sólido", "Electromecánicos"],
    "Conectores": ["Conectores con cable", "Conectores para armado", "Conectores M12 y M8", "Rectos", "Acodados 90 grados"],
    "Contadoras y Temporizadores": ["Contadoras digitales", "Temporizadores industriales"],
    "Fibra Óptica": ["Cable", "Amplificadores"],
    "Sensores de Nivel": ["RF y capacitivos", "Ópticos", "Nivel de agua", "Por vibración"],
    "Sensores Ópticos": ["Láser", "Infrarrojos"]
};

const marcas = [
    { src: "Imagenes/marcas/optex.png", alt: "Optex" },
    { src: "Imagenes/marcas/sick.png", alt: "Sick" },
    { src: "Imagenes/marcas/finetek.png", alt: "FineTek" },
    { src: "Imagenes/marcas/scan.png", alt: "Scan" },
    { src: "Imagenes/marcas/julong.png", alt: "Julong" },
    { src: "Imagenes/marcas/riko.png", alt: "Riko" },
    { src: "Imagenes/marcas/pepperl.png", alt: "Pepperl & Fuchs" },
    { src: "Imagenes/marcas/xecro.png", alt: "Xecro" },
    { src: "Imagenes/marcas/omrom.png", alt: "Omron" },
    { src: "Imagenes/marcas/sensopart.png", alt: "Sensopart" },
    { src: "Imagenes/marcas/ibest.png", alt: "I Best" },
    { src: "Imagenes/marcas/greegoo.png", alt: "Greegoo" }
];

function buildSlider() {
    const track = document.getElementById("slider-track");
    if (!track) return;

    [...marcas, ...marcas].forEach(({ src, alt }) => {
        const slide = document.createElement("div");
        slide.className = "slide";

        const img = document.createElement("img");
        img.src = src;
        img.alt = alt;
        img.loading = "lazy";
        img.width = 120;
        img.height = 60;

        slide.appendChild(img);
        track.appendChild(slide);
    });

    let isDragging = false;
    let startX = 0;
    let dragOffset = 0;
    let baseOffset = 0;

    const getTranslateX = () => {
        const computed = window.getComputedStyle(track).transform;
        if (!computed || computed === "none") return 0;
        return new DOMMatrix(computed).m41;
    };

    let keyframeStyleTag = document.getElementById("dynamic-slider-kf");
    if (!keyframeStyleTag) {
        keyframeStyleTag = document.createElement("style");
        keyframeStyleTag.id = "dynamic-slider-kf";
        document.head.appendChild(keyframeStyleTag);
    }

    const resumeAnimation = (fromX) => {
        const slideWidth = track.firstElementChild ? track.firstElementChild.offsetWidth : 150;
        const halfWidth = slideWidth * marcas.length;
        let startPx = fromX % halfWidth;

        if (startPx > 0) startPx -= halfWidth;
        if (startPx < -halfWidth) startPx += halfWidth;

        const endPx = startPx - halfWidth;
        const duration = window.innerWidth <= 768 ? 12 : 25;
        const fraction = Math.abs(startPx) / halfWidth;
        const remainingDuration = duration * (1 - fraction);
        const kfName = `sliderResume_${Date.now()}`;

        keyframeStyleTag.textContent = `@keyframes ${kfName} { from { transform: translateX(${startPx}px); } to { transform: translateX(${endPx}px); } }`;

        track.style.transform = "";
        track.style.animation = "none";
        void track.offsetWidth;
        track.style.animation = `${kfName} ${remainingDuration}s linear 1, scrollLateral ${duration}s linear ${remainingDuration}s infinite`;
    };

    track.addEventListener("touchstart", (event) => {
        if (event.touches.length !== 1) return;
        isDragging = true;
        startX = event.touches[0].clientX;
        baseOffset = getTranslateX();
        dragOffset = 0;
        track.style.animation = "none";
        track.style.transform = `translateX(${baseOffset}px)`;
    }, { passive: true });

    track.addEventListener("touchmove", (event) => {
        if (!isDragging || event.touches.length !== 1) return;
        dragOffset = event.touches[0].clientX - startX;
        track.style.transform = `translateX(${baseOffset + dragOffset}px)`;
    }, { passive: true });

    track.addEventListener("touchend", () => {
        if (!isDragging) return;
        isDragging = false;
        resumeAnimation(baseOffset + dragOffset);
    });
}

window.toggleSubmenu = function toggleSubmenu(card) {
    const isOpen = card.classList.toggle("card-open");
    card.setAttribute("aria-expanded", String(isOpen));
};

window.handleCardKey = function handleCardKey(event, card) {
    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        window.toggleSubmenu(card);
    }
};

window.actualizarSubcategorias = function actualizarSubcategorias() {
    const catSelect = document.getElementById("categoria-select");
    const subSelect = document.getElementById("subcategoria-select");
    const categoria = catSelect.value;

    subSelect.innerHTML = '<option value="" disabled selected>-- Seleccione tecnología --</option>';

    if (mapeoProductos[categoria]) {
        subSelect.disabled = false;
        subSelect.removeAttribute("aria-disabled");
        mapeoProductos[categoria].forEach((sub) => {
            const option = document.createElement("option");
            option.value = sub;
            option.textContent = sub;
            subSelect.appendChild(option);
        });
        return;
    }

    subSelect.disabled = true;
    subSelect.setAttribute("aria-disabled", "true");
};

window.enviarCotizacionAvanzada = function enviarCotizacionAvanzada() {
    const nombre = document.getElementById("nombre-contacto").value.trim();
    const empresa = document.getElementById("empresa-contacto").value.trim();
    const aplicacion = document.getElementById("aplicacion-contacto").value.trim();
    const categoria = document.getElementById("categoria-select").value;
    const subcategoria = document.getElementById("subcategoria-select").value;
    const telefono = "573232723632";

    if (!categoria || !subcategoria) {
        alert("Por favor selecciona la familia de producto y la tecnología para procesar tu solicitud.");
        return;
    }

    const mensaje = [
        "Hola CR Sensores, solicito asesoría comercial y técnica para la siguiente necesidad:",
        nombre ? `Nombre: ${nombre}` : null,
        empresa ? `Empresa: ${empresa}` : null,
        `Familia de producto: ${categoria}`,
        `Tecnología: ${subcategoria}`,
        aplicacion ? `Aplicación: ${aplicacion}` : "Aplicación: Pendiente de ampliar en conversación"
    ].filter(Boolean).join("\n");

    window.open(`https://wa.me/${telefono}?text=${encodeURIComponent(mensaje)}`, "_blank", "noopener,noreferrer");
};

document.addEventListener("DOMContentLoaded", () => {
    buildSlider();

    const btn = document.getElementById("btn-ver-mas");
    const extraSensors = document.querySelectorAll(".galeria-grid .sensor-item:nth-child(n+9)");
    const hidden = "none";
    const visible = "flex";

    extraSensors.forEach((sensor) => {
        sensor.style.display = hidden;
    });

    if (btn) {
        btn.addEventListener("click", () => {
            const isHidden = extraSensors.length > 0 && extraSensors[0].style.display === hidden;

            extraSensors.forEach((sensor, index) => {
                if (isHidden) {
                    sensor.style.display = visible;
                    sensor.style.animation = `reveal 0.4s ease forwards ${index * 0.05}s`;
                } else {
                    sensor.style.display = hidden;
                    sensor.style.animation = "";
                }
            });

            btn.textContent = isHidden ? "MOSTRAR MENOS" : "MOSTRAR MÁS SENSORES";
            btn.setAttribute("aria-expanded", String(isHidden));
            btn.classList.toggle("btn-ver-mas-active", isHidden);

            if (!isHidden) {
                document.querySelector(".galeria-sensores").scrollIntoView({ behavior: "smooth" });
            }
        });
    }

    const toggle = document.getElementById("menu-toggle");
    const nav = document.getElementById("nav-menu");
    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            const expanded = toggle.getAttribute("aria-expanded") === "true";
            toggle.setAttribute("aria-expanded", String(!expanded));
            nav.classList.toggle("nav-open");
        });
    }
});
