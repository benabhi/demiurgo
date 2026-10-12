# Catálogo de técnicas artísticas

La **técnica** dice cómo está hecha la imagen: óleo, acuarela, cómic, lápiz… Es independiente de la **ambientación**, que la marca el mundo (ver `estilos.md`). Así un mismo mundo de fantasía oscura puede verse como un óleo, un boceto en acuarela o una página de cómic sin dejar de parecer el mismo.

Cada técnica tiene:
- un **id** (para pedirla: `/generar-imagen Aldric_Voss acuarela`);
- **TÉCNICA** y **ACABADO**: los bloques en inglés que van al prompt;
- **Color**, que dice qué hacer con la paleta del mundo:
  - `mundo`: se usa la paleta del mundo;
  - `acento`: monocromo con un solo color de acento, tomado de la paleta del mundo;
  - `monocromo`: se ignora la paleta (la técnica ya define sus tonos);
- 📄 si es una técnica **sobre papel o pergamino**: el fondo se funde con el soporte en vez de ser un fondo oscuro;
- a veces, **restricciones extra** que se suman a las de la Guía Visual.

## Índice
Es el texto que ve el usuario cada vez que elige técnica o pregunta cuáles hay: **cópialo tal cual**, como lista y con el total (sin meterlo en un bloque de código), para que sepa todo lo que puede elegir. Cada técnica se puede pedir por su nombre o por su id (el de su sección, más abajo).

27 técnicas disponibles:
- Pintura (7): Óleo clásico · Boceto en acuarela · Tinta y acuarela · Gouache de cuento · Impresionista · Concept art digital · RPG clásico
- Dibujo (6): Lápiz a mano alzada · Carboncillo · Plumilla · Tinta y aguada · Pastel · Boceto de diseñador
- Cómic y gráfico (5): Cómic · Línea clara · Anime y manga · Portada pulp retro · Art nouveau
- Grabados y artes antiguas (6): Xilografía · Lámina de códice · Manuscrito iluminado · Estampa japonesa · Vitral · Tapiz medieval
- Digital y cine (3): Fotograma de cine · Pixel art · Render 3D estilizado
- Además: «Variada» (cada imagen sortea una de varias) o una técnica propia, descrita con tus palabras.

Al añadir una técnica, ponla en su familia y actualiza los dos totales: el de su familia y el general.

## Recomendadas por género
Punto de partida para proponer tres técnicas al crear la Guía Visual; el tono y la premisa pueden cambiar el orden.

| Género | Técnicas |
|---|---|
| Fantasía oscura | `oleo`, `rpg_clasico`, `tinta_aguada` |
| Fantasía épica o heroica | `pintura_digital`, `oleo`, `acuarela` |
| Fantasía ligera o de cuento | `gouache`, `acuarela`, `linea_clara` |
| Ciencia ficción | `cinematico`, `pintura_digital`, `pulp` |
| Cyberpunk | `cinematico`, `comic`, `manga` |
| Post-apocalíptico | `pintura_digital`, `comic`, `carboncillo` |
| Horror | `carboncillo`, `grabado`, `oleo` |
| Steampunk | `tinta_acuarela`, `oleo`, `art_nouveau` |
| Histórico o mitológico | `oleo`, `manuscrito`, `tapiz` |

## Pintura

### `oleo` — Óleo clásico
Pintura de museo: veladuras, empastes y luz dramática. **Color:** mundo. **Ideal para:** retratos, deidades, escenas solemnes.
- TÉCNICA: `classical oil painting on canvas, rich layered glazes, visible impasto brushstrokes, dramatic chiaroscuro lighting, old-master color harmony`
- ACABADO: `museum-quality fine art oil painting`

### `acuarela` — Boceto en acuarela 📄
Suelta y luminosa, con el lápiz y el papel a la vista. **Color:** mundo. **Ideal para:** paisajes, regiones, flora, viajes.
- TÉCNICA: `loose watercolor sketch over a light pencil underdrawing, soft wet-on-wet color bleeds, pigment granulation, white paper left for the highlights, visible cold-press paper texture`
- ACABADO: `airy, expressive sketchbook watercolor with loose unfinished edges`

### `tinta_acuarela` — Tinta y acuarela 📄
Línea fina de tinta con aguadas de color, como un cuaderno de viaje. **Color:** mundo. **Ideal para:** asentamientos, lugares, objetos.
- TÉCNICA: `pen and ink drawing with transparent watercolor washes, fine confident linework, light hatching, delicate color tints on textured paper`
- ACABADO: `elegant travel-journal illustration`

### `gouache` — Gouache de cuento
Manchas planas y opacas de textura mate, formas simplificadas. **Color:** mundo. **Ideal para:** tonos esperanzadores, culturas, costumbres.
- TÉCNICA: `gouache illustration with flat opaque shapes of color, matte chalky texture, simplified forms, soft painterly edges`
- ACABADO: `charming storybook illustration`

### `impresionista` — Impresionista
Pincelada corta y suelta, luz natural vibrante. **Color:** mundo. **Ideal para:** paisajes, escenas cotidianas, mercados.
- TÉCNICA: `impressionist oil painting, broken color applied in short visible brushstrokes, vibrant natural light, soft atmospheric edges`
- ACABADO: `luminous plein-air painting`

### `pintura_digital` — Concept art digital
El estándar de la industria: pincelada digital y composición de cine. **Color:** mundo. **Ideal para:** cualquier tipo.
- TÉCNICA: `digital concept art painting, confident painterly brushwork, strong value structure, cinematic composition`
- ACABADO: `highly detailed production concept art`

### `rpg_clasico` — RPG clásico
Pintura digital al estilo de los juegos de rol clásicos del género, con las referencias de juego de `estilos.md`. **Color:** mundo. **Ideal para:** cualquier tipo; era la técnica por defecto.
- TÉCNICA: `classic {GENERO} RPG art style, reminiscent of {REFERENCIAS}, digital painting with visible painterly brushstrokes`
- ACABADO: `highly detailed {GENERO} concept art`

## Dibujo

### `lapiz` — Lápiz a mano alzada 📄
Boceto de cuaderno con las líneas de construcción a la vista. **Color:** monocromo. **Ideal para:** personajes, estudios rápidos.
- TÉCNICA: `freehand graphite pencil sketch on off-white sketchbook paper, loose gestural lines, visible construction lines, cross-hatched shading, softly smudged tones`
- ACABADO: `artist's sketchbook study`

### `carboncillo` — Carboncillo 📄
Negros profundos y difuminados, trazo enérgico. **Color:** monocromo. **Ideal para:** horror, retratos duros, ruinas.
- TÉCNICA: `expressive charcoal drawing on textured paper, deep smudged blacks, eraser-lifted highlights, bold sweeping strokes`
- ACABADO: `dramatic fine-art charcoal study`

### `plumilla` — Plumilla 📄
Tinta negra con tramas cruzadas y punteado. **Color:** monocromo. **Ideal para:** objetos, criaturas, bestiarios.
- TÉCNICA: `detailed pen and ink illustration, dense cross-hatching and stippling, crisp black ink lines on white paper`
- ACABADO: `meticulous antique book illustration`

### `tinta_aguada` — Tinta y aguada 📄
Pincel con tinta diluida, salpicaduras y mucho espacio vacío. **Color:** acento. **Ideal para:** paisajes brumosos, espíritus, mitos.
- TÉCNICA: `ink wash painting, expressive brush strokes, diluted grey ink gradients, scattered ink splatters, generous empty space`
- ACABADO: `atmospheric ink painting`

### `pastel` — Pastel 📄
Color de tiza difuminado sobre papel tintado. **Color:** mundo. **Ideal para:** retratos íntimos, tonos suaves.
- TÉCNICA: `soft pastel drawing on toned paper, chalky blended colors, visible paper grain, gentle highlights`
- ACABADO: `delicate pastel artwork`

### `boceto_concepto` — Boceto de diseñador 📄
Lápiz y rotulador gris con pocos acentos de color, rápido y enérgico. **Color:** acento. **Ideal para:** objetos, vehículos, tecnología, criaturas.
- TÉCNICA: `rough concept design sketch, loose pencil lines over grey marker tones, a few bold accents of color, quick energetic strokes`
- ACABADO: `fast professional concept sketch`

## Cómic y gráfico

### `comic` — Cómic
Entintado negro con manchas, colores planos y trama de puntos. **Color:** mundo. **Ideal para:** acción, personajes, ciencia ficción.
- TÉCNICA: `comic book illustration, bold black ink outlines, dynamic inking with spotted blacks, flat cel colors, halftone dot shading`
- ACABADO: `polished graphic novel art`
- Restricciones extra: `no speech bubbles, no captions, no panel borders`

### `linea_clara` — Línea clara
Contornos limpios y uniformes, colores planos y fondos muy detallados. **Color:** mundo. **Ideal para:** aventura, ciudades, viajes.
- TÉCNICA: `ligne claire comic illustration, clean uniform black outlines, flat bright colors without hatching, richly detailed backgrounds`
- ACABADO: `classic European comic album art`
- Restricciones extra: `no speech bubbles, no captions, no panel borders`

### `manga` — Anime y manga
Línea fina, sombreado por zonas y colores vivos. **Color:** mundo. **Ideal para:** personajes, tonos luminosos.
- TÉCNICA: `anime cel-shaded illustration, clean thin lineart, soft gradient shading, expressive eyes, vibrant colors`
- ACABADO: `high-quality anime key visual`
- Restricciones extra: `no speech bubbles, no logo`

### `pulp` — Portada pulp retro
Pintura de revista de aventuras de mediados del siglo XX. **Color:** mundo. **Ideal para:** ciencia ficción retro, aventura, horror.
- TÉCNICA: `vintage pulp magazine cover painting, dramatic lighting, saturated retro colors, mid-century illustration style, visible gouache texture`
- ACABADO: `classic retro adventure illustration`
- Restricciones extra: `no title, no logo, no lettering`

### `art_nouveau` — Art nouveau
Líneas orgánicas, motivos florales y figuras estilizadas, con dorados. **Color:** mundo. **Ideal para:** deidades, nobleza, culturas.
- TÉCNICA: `art nouveau illustration, flowing organic linework, decorative floral motifs, elegant stylized figures, muted tones with gold accents`
- ACABADO: `ornate decorative art print`
- Restricciones extra: `no lettering`

## Grabados y artes antiguas

### `grabado` — Xilografía 📄
Tallas gruesas, alto contraste, tinta sobre papel envejecido. **Color:** monocromo. **Ideal para:** mitos, crónicas, bestiarios, horror.
- TÉCNICA: `woodcut print, bold carved lines, high-contrast black ink on aged paper, rough hand-printed texture`
- ACABADO: `antique woodblock print`

### `codice` — Lámina de códice 📄
Lámina de naturalista: tinta fina y aguadas sobre pergamino. **Color:** mundo. **Ideal para:** flora, criaturas, afecciones, materiales.
- TÉCNICA: `antique naturalist codex plate, fine ink linework, delicate watercolor tints, aged parchment background, specimen-style composition`
- ACABADO: `scientific illustration plate`
- Restricciones extra: `no labels, no handwriting`

### `manuscrito` — Manuscrito iluminado
Miniatura medieval con pan de oro y perspectiva plana. **Color:** mundo. **Ideal para:** mitos, acontecimientos históricos, deidades.
- TÉCNICA: `illuminated manuscript miniature, tempera and gold leaf on vellum, flat medieval perspective, ornate patterning`
- ACABADO: `medieval book of hours illumination`
- Restricciones extra: `no lettering`

### `ukiyoe` — Estampa japonesa 📄
Grabado en madera con planos de color y contornos marcados. **Color:** mundo. **Ideal para:** paisajes, mares, tormentas.
- TÉCNICA: `ukiyo-e woodblock print style, flat areas of color, bold contour lines, stylized waves and clouds, washi paper texture`
- ACABADO: `traditional Japanese woodblock print`
- Restricciones extra: `no lettering, no seal stamps`

### `vitral` — Vitral
Plomos oscuros y vidrio luminoso en tonos joya. **Color:** mundo. **Ideal para:** deidades, creencias, héroes legendarios.
- TÉCNICA: `stained glass window artwork, bold dark lead lines, luminous jewel-toned glass, backlit glow`
- ACABADO: `cathedral stained glass panel`

### `tapiz` — Tapiz medieval
Lana tejida, figuras planas y tintes naturales. **Color:** mundo. **Ideal para:** mitos, batallas, linajes.
- TÉCNICA: `medieval tapestry, woven wool texture, flat stylized figures, muted natural dyes`
- ACABADO: `museum-preserved tapestry`

## Digital y cine

### `cinematico` — Fotograma de cine
Fotorrealista, como una película: lente anamórfica, grano y profundidad de campo. **Color:** mundo. **Ideal para:** ciencia ficción, cyberpunk, histórico.
- TÉCNICA: `photorealistic cinematic film still, anamorphic lens, shallow depth of field, natural film grain, motivated practical lighting`
- ACABADO: `high-budget film production still`

### `pixel` — Pixel art
Píxeles nítidos de 16 bits y paleta limitada. **Color:** mundo. **Ideal para:** homenajes a los juegos retro.
- TÉCNICA: `detailed 16-bit pixel art, limited color palette, crisp hard-edged pixels, subtle dithering`
- ACABADO: `classic 16-bit era game art`

### `render_3d` — Render 3D estilizado
Formas esculpidas, materiales táctiles y luz suave. **Color:** mundo. **Ideal para:** tonos ligeros, criaturas, objetos.
- TÉCNICA: `stylized 3D render, sculpted forms, soft global illumination, subsurface scattering, tactile materials`
- ACABADO: `polished animated feature film still`

## Técnica propia
Si el usuario describe una técnica que no está aquí ("como un mapa antiguo", "acrílico con espátula"), escribe tú sus bloques en inglés con la misma forma: TÉCNICA (soporte, trazo, color, bordes, luz), ACABADO, Color y, si hace falta, 📄 y restricciones extra. Nunca nombres de personas reales, tampoco de artistas.
