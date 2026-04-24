# HÉROE EMPRENDEDOR

Sitio estático de HÉROE EMPRENDEDOR, construido a partir del material aprobado de marca, arquitectura y contenidos.

Nota: esta versión se está usando para validar el flujo de cambios en GitHub.

Incluye:

- home editorial con propuesta de valor y respaldo de Grupo Vadillo
- hubs de navegación para `Empieza`, `Impuestos`, `Ayudas`, `Recursos`, `Asesoría`, `Contacto` y `Quiénes somos`
- páginas madre y piezas satélite ya estructuradas en navegación pública
- build para GitHub Pages que publica la web visual final y genera `sitemap.xml`

## Publicación

GitHub Pages se construye desde `build_site.py`.

El script copia la versión estática publicada del sitio a `_site/` y añade:

- `sitemap.xml`
- `robots.txt` con referencia al sitemap
- `.nojekyll`

## Pendiente

- incorporar los textos jurídicos definitivos cuando estén validados
- cerrar la información comercial aún marcada como pendiente de validación interna
