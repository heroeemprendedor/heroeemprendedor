from __future__ import annotations

import html
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = Path(os.environ.get("BUILD_OUTPUT", ROOT))


def page_path(route: str) -> Path:
    if route == "/":
        return OUTPUT / "index.html"
    return OUTPUT / route.strip("/") / "index.html"


def write_page(route: str, body: str) -> None:
    target = page_path(route)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")


def nav(current: str) -> str:
    items = [
        ("Inicio", "/"),
        ("Empieza", "/empieza/"),
        ("Impuestos", "/impuestos/"),
        ("Ayudas", "/ayudas/"),
        ("Recursos", "/recursos/"),
        ("Asesoria", "/asesoria/"),
        ("Contacto", "/contacto/"),
    ]
    links = []
    for label, href in items:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
    return "\n".join(links)


def layout(title: str, description: str, route: str, main: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}" />
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="header-inner">
        <a class="brand-lockup" href="/">
          <span class="brand-mark">HE</span>
          <span>
            <span class="brand-title">HEROE EMPRENDEDOR</span>
            <span class="brand-tag">Asesoria para emprender en Vitoria-Gasteiz y Alava</span>
          </span>
        </a>
        <button class="menu-toggle" type="button" aria-expanded="false" data-menu-toggle>Menu</button>
        <nav class="site-nav" data-site-nav>
          {nav(route)}
        </nav>
        <a class="header-cta" href="/contacto/">Quiero contaros mi caso</a>
      </div>
    </header>
    <main>
      {main}
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-top">
          <div>
            <div class="footer-closing">Claridad para empezar. Criterio para construir.</div>
            <div class="footer-meta">Respaldado por Grupo Vadillo · Vitoria-Gasteiz · Alava · Euskadi</div>
          </div>
          <a class="text-link" href="https://www.grupovadillo.com/" target="_blank" rel="noreferrer">Ver Grupo Vadillo</a>
        </div>
        <ul class="footer-links">
          <li><a href="/empieza/">Empieza</a></li>
          <li><a href="/impuestos/">Impuestos</a></li>
          <li><a href="/ayudas/">Ayudas</a></li>
          <li><a href="/recursos/">Recursos</a></li>
          <li><a href="/asesoria/">Asesoria</a></li>
          <li><a href="/quienes-somos/">Quienes somos</a></li>
        </ul>
      </div>
    </footer>
    <script src="/main.js"></script>
  </body>
</html>
"""


def hero(eyebrow: str, title: str, text: str, primary: tuple[str, str], secondary: tuple[str, str] | None = None) -> str:
    secondary_html = ""
    if secondary:
        secondary_html = f'<a class="button button-secondary" href="{secondary[1]}">{secondary[0]}</a>'
    return f"""
    <section class="hero-home">
      <div class="section-inner hero-shell">
        <div class="hero-copy reveal">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p class="lead">{text}</p>
          <div class="actions">
            <a class="button" href="{primary[1]}">{primary[0]}</a>
            {secondary_html}
          </div>
        </div>
      </div>
    </section>
    """


def section(title: str, paragraphs: list[str], eyebrow: str = "") -> str:
    eyebrow_html = f'<p class="eyebrow eyebrow-ink">{eyebrow}</p>' if eyebrow else ""
    body = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f"""
    <section class="section">
      <div class="section-inner split-intro">
        <div class="reveal">
          {eyebrow_html}
          <h2>{title}</h2>
        </div>
        <div class="text-block reveal">
          {body}
        </div>
      </div>
    </section>
    """


def cards(title: str, items: list[tuple[str, str, str, str]]) -> str:
    articles = []
    for label, heading, text, href in items:
        articles.append(
            f"""
            <article class="guide-card reveal">
              <span class="guide-index">{label}</span>
              <h3>{heading}</h3>
              <p>{text}</p>
              <a class="text-link" href="{href}">Abrir</a>
            </article>
            """
        )
    return f"""
    <section class="section section-soft">
      <div class="section-inner">
        <div class="section-heading reveal">
          <h2>{title}</h2>
        </div>
        <div class="cards-grid cards-grid-home">
          {''.join(articles)}
        </div>
      </div>
    </section>
    """


def article(title: str, description: str, route: str, eyebrow: str, intro: str, paragraphs: list[str]) -> str:
    prose = "".join(f"<p>{p}</p>" for p in paragraphs)
    return layout(
        title,
        description,
        route,
        f"""
        {hero(eyebrow, title, intro, ("Quiero contaros mi caso", "/contacto/"), ("Volver al inicio", "/"))}
        <section class="section">
          <div class="section-inner">
            <article class="prose-panel reveal">
              {prose}
            </article>
          </div>
        </section>
        """,
    )


def build_pages() -> None:
    write_page(
        "/",
        layout(
            "HEROE EMPRENDEDOR | Asesoria para emprender en Vitoria-Gasteiz y Alava",
            "Lo que nadie te explica cuando empiezas. Guias claras, recursos utiles y asesoria para emprender con criterio en Vitoria-Gasteiz y Alava.",
            "/",
            hero(
                "HEROE EMPRENDEDOR · by Grupo Vadillo",
                "Lo que nadie te explica cuando empiezas",
                "Te ayudamos a entender que tienes que hacer, en que orden conviene hacerlo y que errores merece la pena evitar si quieres emprender con criterio en Vitoria-Gasteiz y Alava.",
                ("Quiero entender por donde empezar", "/empieza/"),
                ("Ver como podeis acompanarme", "/asesoria/"),
            )
            + section(
                "Tener una idea no suele ser lo mas dificil.",
                [
                    "Lo dificil es empezar sin que nadie te traduzca la realidad.",
                    "Te hablan de darte de alta, de IVA, de IRPF, de ayudas, de TicketBAI, de modelos, de certificados y de obligaciones.",
                    "La informacion existe, pero casi nadie te la ordena ni te la aterriza cuando solo estas intentando empezar bien.",
                ],
                "Problema real",
            )
            + cards(
                "Empieza por la duda que mas te pesa ahora mismo",
                [
                    ("Empieza", "Quiero emprender, pero no se por donde empezar", "Primeros pasos, orden logico y decisiones basicas para no avanzar a ciegas.", "/empieza/"),
                    ("Impuestos", "Quiero hacerme autonomo y no meter la pata", "Alta, impuestos, obligaciones y errores frecuentes explicados desde cero.", "/impuestos/"),
                    ("Ayudas", "Quiero entender ayudas y subvenciones sin perderme", "Que puedes revisar y como prepararte para no llegar tarde.", "/ayudas/"),
                    ("Recursos", "Quiero una base clara para no improvisar", "Guias y piezas utiles para empezar con criterio.", "/recursos/"),
                ],
            )
            + section(
                "Y cuando dejar de hacerlo solo tenga sentido, podemos acompanarte.",
                [
                    "Si ya has decidido empezar, te ayudamos con la parte fiscal, contable, laboral, administrativa y de seguimiento para que no avances a base de dudas sueltas, retrasos y decisiones improvisadas.",
                    "La pregunta importante no es solo si puedes hacerlo por tu cuenta. La pregunta importante es si te compensa hacerlo bien, a tiempo y sin quitarle foco al negocio que quieres construir.",
                    "El primer ano de cuota mensual estara becado al 100%, segun las condiciones comerciales definidas por la marca.",
                ],
                "Acompanamiento",
            ),
        ),
    )

    write_page(
        "/empieza/",
        layout(
            "Empieza | HEROE EMPRENDEDOR",
            "Guias para empezar a emprender con criterio en Vitoria-Gasteiz y Alava.",
            "/empieza/",
            hero(
                "Empieza",
                "Una base clara para no empezar a ciegas",
                "Aqui reunimos las guias base para entender el arranque, el alta, la forma juridica y las primeras decisiones que mas pesan cuando todavia estas intentando ordenar el comienzo.",
                ("Hablar con vosotros", "/contacto/"),
            )
            + cards(
                "Guias base de arranque",
                [
                    ("Guia base", "Como empezar a emprender en Vitoria-Gasteiz", "El orden correcto, las decisiones que importan y lo que nadie te dice cuando todavia estas pensando si lanzarte.", "/empieza/como-empezar-a-emprender-en-vitoria-gasteiz/"),
                    ("Autonomos", "Como hacerse autonomo en Alava", "Que necesitas antes del alta y como empezar con mas criterio.", "/empieza/como-hacerse-autonomo-en-alava/"),
                    ("Decision", "Autonomo o SL: que te conviene de verdad", "Que cambia, cuando compensa y que suele entenderse mal.", "/empieza/autonomo-o-sl-que-te-conviene-de-verdad/"),
                ],
            ),
        ),
    )

    write_page(
        "/impuestos/",
        layout(
            "Impuestos | HEROE EMPRENDEDOR",
            "Fiscalidad basica para autonomos y pequenos negocios explicada sin jerga.",
            "/impuestos/",
            hero(
                "Impuestos",
                "Fiscalidad explicada sin niebla innecesaria",
                "IVA, IRPF, TicketBAI y obligaciones basicas para que entiendas que te aplica, cuando te aplica y que no conviene improvisar.",
                ("Quiero resolver mi caso", "/contacto/"),
            )
            + cards(
                "Piezas clave",
                [
                    ("Impuestos", "Que impuestos paga un autonomo cuando empieza", "La fotografia basica del arranque.", "/impuestos/que-impuestos-paga-un-autonomo-cuando-empieza/"),
                    ("IVA", "IVA para principiantes", "Que es y cuando te afecta de verdad.", "/impuestos/iva-para-principiantes-que-es-y-cuando-te-afecta/"),
                    ("IRPF", "IRPF para autonomos explicado sin jerga", "Una base clara para no mezclar conceptos.", "/impuestos/irpf-para-autonomos-explicado-sin-jerga/"),
                ],
            ),
        ),
    )

    write_page(
        "/ayudas/",
        layout(
            "Ayudas | HEROE EMPRENDEDOR",
            "Ayudas y subvenciones para emprender con una base mas ordenada.",
            "/ayudas/",
            hero(
                "Ayudas",
                "Ayudas y subvenciones sin perderte en la superficie",
                "No se trata solo de encontrar una ayuda. Se trata de entender si encaja contigo, si llegas a tiempo y si estas preparando bien lo que te van a pedir.",
                ("Quiero ver mi caso", "/contacto/"),
            )
            + cards(
                "Empieza por aqui",
                [
                    ("Ayudas", "Ayudas para emprender en Vitoria-Gasteiz y Alava", "Las principales lineas y como orientarte.", "/ayudas/ayudas-para-emprender-en-vitoria-gasteiz-y-alava/"),
                ],
            ),
        ),
    )

    write_page(
        "/recursos/",
        layout(
            "Recursos | HEROE EMPRENDEDOR",
            "Recursos utiles para empezar con una base mas clara.",
            "/recursos/",
            hero(
                "Recursos",
                "Recursos utiles para empezar con criterio",
                "Contenido pensado para ayudarte incluso si todavia no contratas nada. La prioridad aqui es reducir incertidumbre real.",
                ("Quiero una orientacion directa", "/contacto/"),
            )
            + cards(
                "Recursos destacados",
                [
                    ("Checklist", "Checklist para empezar sin ir a ciegas", "Una pieza accionable para ordenar el arranque.", "/recursos/checklist-para-empezar-sin-ir-a-ciegas/"),
                ],
            ),
        ),
    )

    write_page(
        "/asesoria/",
        layout(
            "Asesoria | HEROE EMPRENDEDOR",
            "Acompanamiento para emprender, arrancar o corregir la base del negocio.",
            "/asesoria/",
            hero(
                "Asesoria",
                "Acompanamiento para emprender con mas claridad y menos ruido",
                "Si ya has decidido empezar o si tu negocio ya ha arrancado pero la parte de atras empieza a pesarte demasiado, aqui tienes una vista clara de como podemos ayudarte.",
                ("Quiero contaros mi caso", "/contacto/"),
            )
            + section(
                "No se trata solo de presentar impuestos.",
                [
                    "Te ayudamos con alta y puesta en marcha, fiscalidad, contabilidad, gestion laboral, apoyo administrativo, orientacion sobre ayudas y consultas juridicas con nuestro equipo.",
                    "La idea no es empujarte a contratar antes de tiempo. Primero claridad, luego confianza, despues contratacion.",
                    "Si empiezas con nosotros desde el dia cero, puedes acceder a una beca del 100% de la cuota mensual de asesoria durante el primer ano, segun las condiciones definidas por la marca.",
                ],
                "Que resolvemos",
            ),
        ),
    )

    write_page(
        "/contacto/",
        layout(
            "Contacto | HEROE EMPRENDEDOR",
            "Cuentanos en que punto estas y te ayudamos a ordenar el siguiente paso.",
            "/contacto/",
            hero(
                "Contacto",
                "Cuentanos en que punto estas y te ayudamos a ordenar el siguiente paso",
                "No hace falta que vengas con todo resuelto. Nos basta con entender si estas en fase idea, arranque o ya en marcha para ver si tiene sentido ayudarte.",
                ("Escribir por email", "mailto:info@grupovadillo.com"),
                ("WhatsApp", "https://wa.me/34689014530"),
            )
            + section(
                "Formas de contacto",
                [
                    "WhatsApp: 689 014 530. Contestamos en un plazo maximo de 24 horas salvo fines de semana y festivos.",
                    "Telefono: 945 222 762.",
                    "Email: info@grupovadillo.com.",
                    "Oficinas: Pintor Diaz de Olano, 18 y Paduleta 55 en Vitoria-Gasteiz; Virgen Blanca, 11 en Oyon; Travesia Paganos, 45 en Laguardia.",
                ],
            ),
        ),
    )

    write_page(
        "/quienes-somos/",
        article(
            "Quienes somos",
            "El enfoque de HEROE EMPRENDEDOR y la experiencia real de Grupo Vadillo detras del proyecto.",
            "/quienes-somos/",
            "Quienes somos",
            "No venimos de estudiar empresas desde fuera. Venimos de acompanarlas desde dentro.",
            [
                "Detras de este proyecto esta Grupo Vadillo Asesores, una empresa familiar creada en 1949 que ha evolucionado desde la mediacion aseguradora hacia la gestoria, la asesoria y la consultoria.",
                "Eso importa porque una cosa es saber teoria empresarial y otra muy distinta es haber acompanado empresas reales, pequenos negocios y autonomos durante anos.",
                "No hemos creado HEROE EMPRENDEDOR para sonar epicos. Lo hemos creado porque al emprendedor se le exige mucho antes de que nadie le aclare bien el terreno.",
            ],
        ),
    )

    write_page(
        "/empieza/como-empezar-a-emprender-en-vitoria-gasteiz/",
        article(
            "Como empezar a emprender en Vitoria-Gasteiz",
            "Guia base para empezar a emprender con mas claridad.",
            "/empieza/como-empezar-a-emprender-en-vitoria-gasteiz/",
            "Guia base",
            "La primera necesidad rara vez es abrir papeles deprisa. La primera necesidad suele ser ordenar bien el comienzo.",
            [
                "Antes de darte de alta conviene aclarar que vas a vender, a quien, en que formato y con que estructura minima.",
                "Tambien conviene entender si vas a empezar como autonomo, si tiene sentido pensar en una sociedad o si todavia estas en una fase demasiado temprana para tomar ciertas decisiones.",
                "Empezar bien no es hacerlo todo a la vez. Es hacerlo en un orden que reduzca errores evitables.",
            ],
        ),
    )

    write_page(
        "/empieza/como-hacerse-autonomo-en-alava/",
        article(
            "Como hacerse autonomo en Alava",
            "Guia practica para entender el alta y los primeros pasos.",
            "/empieza/como-hacerse-autonomo-en-alava/",
            "Autonomos",
            "Darte de alta no es lo primero que conviene entender. Conviene entender primero que implica y que vas a necesitar sostener despues.",
            [
                "Antes del alta, necesitas revisar actividad, facturacion, obligacion de emitir facturas, certificado digital y una base minima de calendario.",
                "Despues llegan IVA, IRPF, TicketBAI y la necesidad de mantener cierto orden desde el principio.",
                "El problema no suele ser el formulario. El problema suele ser empezar sin saber que viene justo despues.",
            ],
        ),
    )

    write_page(
        "/empieza/autonomo-o-sl-que-te-conviene-de-verdad/",
        article(
            "Autonomo o SL: que te conviene de verdad",
            "Comparativa base para elegir forma juridica con mas criterio.",
            "/empieza/autonomo-o-sl-que-te-conviene-de-verdad/",
            "Decision clave",
            "La respuesta no es universal. Depende de ingresos, riesgo, estructura y de si realmente necesitas ya una sociedad o no.",
            [
                "Ser autonomo suele ser la opcion mas simple para empezar cuando la actividad aun esta arrancando y la estructura es ligera.",
                "La sociedad puede tener sentido cuando hay mas complejidad, mas volumen, socios o una necesidad real de separar mejor determinadas capas.",
                "El error frecuente es abrir una sociedad demasiado pronto o descartarla demasiado deprisa sin entender que cambia de verdad.",
            ],
        ),
    )

    write_page(
        "/impuestos/que-impuestos-paga-un-autonomo-cuando-empieza/",
        article(
            "Que impuestos paga un autonomo cuando empieza",
            "Base fiscal para entender IVA, IRPF y obligaciones iniciales.",
            "/impuestos/que-impuestos-paga-un-autonomo-cuando-empieza/",
            "Impuestos",
            "Cuando alguien empieza, suele mezclar demasiadas cosas a la vez. Conviene separar conceptos.",
            [
                "Una cosa es la cuota de autonomos. Otra son impuestos como IVA e IRPF. Y otra distinta son sistemas y obligaciones operativas como TicketBAI.",
                "No todas las actividades funcionan igual ni todos los escenarios implican lo mismo, pero casi todo mejora cuando entiendes cada capa por separado.",
                "La calma no viene de memorizar modelos. Viene de entender que te aplica a ti y en que momento.",
            ],
        ),
    )

    write_page(
        "/impuestos/iva-para-principiantes-que-es-y-cuando-te-afecta/",
        article(
            "IVA para principiantes",
            "Explicacion clara para entender que es el IVA y cuando te afecta.",
            "/impuestos/iva-para-principiantes-que-es-y-cuando-te-afecta/",
            "IVA",
            "El IVA suele parecer mas oscuro de lo que es cuando nadie te explica bien la logica.",
            [
                "No se trata solo de sumar un porcentaje en una factura. Se trata de entender cuando repercutes, cuando soportas y como se ordena eso despues.",
                "El error habitual es intentar aprenderlo deprisa cuando ya estas facturando sin una base minima.",
                "Conviene entenderlo pronto para que la facturacion no te empiece a pesar mas de la cuenta.",
            ],
        ),
    )

    write_page(
        "/impuestos/irpf-para-autonomos-explicado-sin-jerga/",
        article(
            "IRPF para autonomos explicado sin jerga",
            "Base clara para entender como entra el IRPF en el arranque.",
            "/impuestos/irpf-para-autonomos-explicado-sin-jerga/",
            "IRPF",
            "El IRPF no necesita jerga para entenderse mejor. Necesita una explicacion ordenada.",
            [
                "Conviene distinguir entre ingresos, gastos, beneficio y pagos a cuenta para no mezclar ideas desde el principio.",
                "Cuando no entiendes la logica, cada trimestre parece una sorpresa.",
                "Cuando si la entiendes, empiezas a ver el IRPF como una parte mas del sistema y no como una amenaza abstracta.",
            ],
        ),
    )

    write_page(
        "/ayudas/ayudas-para-emprender-en-vitoria-gasteiz-y-alava/",
        article(
            "Ayudas para emprender en Vitoria-Gasteiz y Alava",
            "Orientacion base para revisar ayudas y prepararte mejor.",
            "/ayudas/ayudas-para-emprender-en-vitoria-gasteiz-y-alava/",
            "Ayudas",
            "Buscar ayudas sin preparar bien la base suele hacer perder mas tiempo del que parece.",
            [
                "Conviene revisar plazos, requisitos, actividad, documentacion y punto real del proyecto antes de contar con una ayuda como si ya estuviera asegurada.",
                "Las ayudas pueden ayudar, pero no sustituyen una base bien montada.",
                "Prepararte mejor suele ahorrar mas energia que lanzarte a pedir todo sin criterio.",
            ],
        ),
    )

    write_page(
        "/recursos/checklist-para-empezar-sin-ir-a-ciegas/",
        article(
            "Checklist para empezar sin ir a ciegas",
            "Recurso base para ordenar el comienzo y reducir errores evitables.",
            "/recursos/checklist-para-empezar-sin-ir-a-ciegas/",
            "Checklist",
            "Antes de correr, conviene tener una lista corta y util de lo que realmente necesitas aclarar.",
            [
                "Que vas a vender y a quien.",
                "Si tiene sentido empezar ya o necesitas ordenar mejor la propuesta.",
                "Que forma de arranque encaja mas contigo, que obligaciones te esperan y que documentos conviene resolver cuanto antes.",
                "La checklist no sustituye el criterio, pero ayuda a no empezar totalmente a oscuras.",
            ],
        ),
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_pages()
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    shutil.copyfile(ROOT / "styles.css", OUTPUT / "styles.css")
    shutil.copyfile(ROOT / "main.js", OUTPUT / "main.js")


if __name__ == "__main__":
    main()
