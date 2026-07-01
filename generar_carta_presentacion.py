#!/usr/bin/env python3
"""
Genera la Carta de Presentación en PDF para CR Sensores Industriales.
Diseño de una sola página con marca de agua y estilo moderno.
"""

from fpdf import FPDF
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WA_LINK = "https://wa.me/573138278238?text=Hola%20CR%20Sensores%2C%20quisiera%20recibir%20asesor%C3%ADa%20sobre%20sus%20soluciones."
PAGE_LINK = "https://hcerquera.github.io/pagina_crsensores/"
EMAIL = "contacto.crsensores@gmail.com"
EMAIL_LINK = f"mailto:{EMAIL}?subject=Consulta%20CR%20Sensores"


class CartaPDF(FPDF):
    GOLD = (193, 154, 81)
    GOLD_LIGHT = (220, 190, 130)
    DARK = (42, 48, 58)
    GRAY = (90, 100, 110)
    WHITE = (255, 255, 255)

    def header(self):
        pass

    def footer(self):
        self.set_y(-8)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.GRAY)
        self.cell(0, 4, "CR Sensores Industriales  |  +57 313 827 8238  |  contacto.crsensores@gmail.com",
                  align="C")

    def draw_watermark(self):
        """Logo como marca de agua centrada + 3 imagenes de productos de fondo."""
        # Logo principal grande
        logo_path = os.path.join(BASE_DIR, "Imagenes", "logo", "Logo_final.png")
        if os.path.exists(logo_path):
            with self.local_context(fill_opacity=0.15):
                self.image(logo_path, x=35, y=80, w=140)

        # 3 imagenes de productos como fondo decorativo
        productos_bg = [
            ("Imagenes/sensores/laser.png", 5, 180, 45),
            ("Imagenes/sensores/inductivo.png", 155, 60, 40),
            ("Imagenes/sensores/fotoelectrico2.png", 160, 185, 38),
        ]
        for img_rel, x, y, w in productos_bg:
            img_path = os.path.join(BASE_DIR, img_rel)
            if os.path.exists(img_path):
                with self.local_context(fill_opacity=0.10):
                    self.image(img_path, x=x, y=y, w=w)

    def draw_header_bar(self):
        """Encabezado con logo grande."""
        # Barra principal
        self.set_fill_color(*self.DARK)
        self.rect(0, 0, 210, 34, "F")
        # Linea dorada decorativa
        self.set_fill_color(*self.GOLD)
        self.rect(0, 34, 210, 1.2, "F")

        # Logo grande
        logo_path = os.path.join(BASE_DIR, "Imagenes", "logo", "Logo_final.png")
        if os.path.exists(logo_path):
            self.image(logo_path, x=8, y=2, w=30)

        # Nombre
        self.set_xy(42, 8)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*self.WHITE)
        self.cell(0, 8, "CR Sensores Industriales", new_x="LMARGIN", new_y="NEXT")

        # Tagline
        self.set_x(42)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*self.GOLD_LIGHT)
        self.cell(0, 5, "Precision Industrial, Sensado Inteligente", new_x="LMARGIN", new_y="NEXT")

    def section_title(self, title):
        self.ln(1.5)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.DARK)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GOLD)
        self.set_line_width(0.6)
        x = self.get_x()
        self.line(x, self.get_y(), x + 50, self.get_y())
        self.ln(2.5)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*self.GRAY)
        self.multi_cell(0, 4.5, text)
        self.ln(1)


def main():
    pdf = CartaPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # Marca de agua
    pdf.draw_watermark()

    # Encabezado
    pdf.draw_header_bar()

    # ─── QUIENES SOMOS ─────────────────────────────────────────────────────────
    pdf.set_y(39)
    pdf.section_title("Quienes Somos")
    pdf.body_text(
        "En CR Sensores Industriales optimizamos la eficiencia operativa de cada "
        "cliente mediante la distribucion especializada de soluciones de deteccion "
        "y sensado inteligente. Integramos tecnologia de alto desempeno con asesoria "
        "tecnica experta, garantizando disponibilidad y continuidad operativa en "
        "entornos industriales exigentes."
    )
    pdf.ln(1)

    # ─── PORTAFOLIO DE PRODUCTOS (listado vertical) ────────────────────────────
    pdf.section_title("Portafolio de Productos")
    productos = [
        ("Temperatura", "Termocuplas y monitoreo termico de precision"),
        ("Lectoras", "De marca, etiqueta, inductivos, capacitivos, fotoelectricos"),
        ("Relevadores", "Estado solido y electromecanicos"),
        ("Conectores", "M12, M8, con cable, armado, rectos y acodados"),
        ("Fibra Optica", "Cable y amplificadores para espacios reducidos"),
        ("Sensores de Nivel", "RFA, opticos, agua, vibracion (SC28/SC24)"),
        ("Sensores Opticos", "Laser e infrarrojos, deteccion sin contacto"),
        ("Contadoras", "Conteo preciso para control de produccion"),
    ]
    for name, desc in productos:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*CartaPDF.GOLD)
        pdf.cell(4, 4.8, ">")
        pdf.set_text_color(*CartaPDF.DARK)
        pdf.cell(38, 4.8, name)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*CartaPDF.GRAY)
        pdf.cell(0, 4.8, desc, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2.5)

    # ─── ALIADOS ESTRATEGICOS (logos 4x3 mas grandes) ────────────────────────
    pdf.section_title("Aliados Estrategicos")

    marcas_dir = os.path.join(BASE_DIR, "Imagenes", "marcas")
    if os.path.isdir(marcas_dir):
        logos = sorted([f for f in os.listdir(marcas_dir) if f.endswith(".png")])
        # Mover ibest y julong al final
        move_to_end = ["ibest.png", "julong.png"]
        logos = [l for l in logos if l not in move_to_end] + [l for l in move_to_end if l in logos]
        cols = 4
        logo_w = 35
        total_width = 190
        spacing_x = total_width / cols
        x_start = 10 + (spacing_x - logo_w) / 2
        y = pdf.get_y() + 1
        spacing_y = 18

        for i, logo in enumerate(logos):
            col = i % cols
            row = i // cols
            x = x_start + col * spacing_x
            y_pos = y + row * spacing_y
            path = os.path.join(marcas_dir, logo)
            pdf.image(path, x=x, y=y_pos, w=logo_w)

        total_rows = (len(logos) + cols - 1) // cols
        pdf.set_y(y + total_rows * spacing_y + 3)

    # ─── POR QUE ELEGIRNOS (listado vertical) ─────────────────────────────────
    pdf.section_title("Por Que Elegirnos")
    ventajas = [
        "Asesoria tecnica personalizada para cada proyecto",
        "Amplio inventario con disponibilidad inmediata",
        "Marcas lideres a nivel mundial en automatizacion",
        "Atencion directa via WhatsApp para agilizar su operacion",
        "Experiencia en entornos industriales exigentes",
    ]
    for v in ventajas:
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*CartaPDF.GOLD)
        pdf.cell(4, 5.5, "-")
        pdf.set_text_color(*CartaPDF.GRAY)
        pdf.cell(0, 5.5, " " + v, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ─── CONTACTO ──────────────────────────────────────────────────────────────
    # Linea separadora
    pdf.set_draw_color(*CartaPDF.GOLD)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    contact_y = pdf.get_y()

    # Titulo contacto
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*CartaPDF.DARK)
    pdf.cell(0, 5, "Contacto", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.5)

    # WhatsApp
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*CartaPDF.DARK)
    pdf.cell(60, 5, "+57 313 827 8238  (WhatsApp)", link=WA_LINK,
             new_x="LMARGIN", new_y="NEXT")

    # Correo
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*CartaPDF.GRAY)
    pdf.cell(60, 5, EMAIL, link=EMAIL_LINK, new_x="LMARGIN", new_y="NEXT")

    # Texto invitacion
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*CartaPDF.GOLD)
    pdf.cell(60, 4, "Escribenos para asesoria sin compromiso", link=WA_LINK,
             new_x="LMARGIN", new_y="NEXT")

    # QR a la derecha
    qr_path = os.path.join(BASE_DIR, "Imagenes", "qr", "qr_git.png")
    if os.path.exists(qr_path):
        qr_size = 22
        qr_x = 168
        qr_y = contact_y + 3
        pdf.image(qr_path, x=qr_x, y=qr_y, w=qr_size, link=PAGE_LINK)
        pdf.set_xy(qr_x - 3, qr_y + qr_size + 1)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*CartaPDF.GRAY)
        pdf.cell(qr_size + 6, 3, "Visita nuestra web", align="C", link=PAGE_LINK)

    # ─── GUARDAR ───────────────────────────────────────────────────────────────
    output_path = os.path.join(BASE_DIR, "CR_Sensores_Carta_Presentacion.pdf")
    pdf.output(output_path)
    print(f"PDF generado exitosamente: {output_path}")


if __name__ == "__main__":
    main()
