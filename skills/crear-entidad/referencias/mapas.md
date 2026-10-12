# La leyenda del mapa

Además de su imagen principal (el concept art, que sigue siendo obligatorio y la primera imagen de la nota), los lugares que lo merecen tienen **mapa**. El mapa no es la imagen: es la **leyenda numerada** de la sección `## Mapa`. La imagen la dibuja `generar-imagen` y es una *edición* de esa leyenda. El mundo crece en la leyenda; el dibujo se rehace cuando ha cambiado bastante.

## Qué lugares la llevan
La regla `mapa` del `modulo.json` de cada tipo dice qué categorías llevan mapa, de qué clase y desde qué relevancia. `check_note.py --depth <tipo>:<relevancia>:<categoría>` dice si a una nota le toca. Hay cuatro clases:
- **interior:** el plano de un edificio, unas ruinas o una mazmorra, por niveles;
- **urbano:** el plano de un asentamiento;
- **paraje:** el mapa de una isla, un bosque, una montaña o un paraje;
- **territorio:** el mapa de una región. La leyenda se escribe desde que le toca, pero la imagen espera a que tenga las zonas mínimas de su regla (`zonas_minimas`): un territorio con dos lugares sería un mapa pobre.

## Qué entra en la leyenda
Cada mapa muestra **solo su nivel directo**:
- **interior:** las salas o zonas, en el orden en que se recorren (la entrada es la 1): las de su Recorrido y, en una mazmorra, las salas menores que le dan sentido (un almacén, unas celdas, un pozo). Esas salas menores son detalles inventados: lístalos en el informe.
- **urbano:** sus barrios y zonas, sus lugares notables y lo que da forma al plano (las puertas, el puerto, la plaza mayor). No los locales de cada barrio: esos irán en el mapa del barrio, si llega a ser un lugar propio.
- **paraje:** sus partes (un claro, una cumbre, una orilla) y sus lugares notables.
- **territorio:** su capital (primero), sus asentamientos y lugares notables, y los accidentes con nombre que cuenta su Geografía (un río, una cordillera). No los lugares que están dentro de sus asentamientos.

La leyenda solo indexa lo que la nota cuenta: si una zona importa, la nota también la describe en su sección.

## Formato de cada zona
```
- **N.** **Nombre** · orientación — una línea. Conecta con 2 y 5.
```
Es una viñeta con el número en negrita, no una lista numerada: Obsidian renumera las listas al leerlas, y una leyenda que crece (1, 2, 3, 9) se vería 1, 2, 3, 4.
- **Nombre:** si la zona es una entidad (un palacio, un templo, un barrio con nombre propio), va enlazada, a su nota o como enlace pendiente con su texto legible: `**[[Palacio_de_Ormal|El palacio]]**`. Si no lo es, va como texto, en minúscula y por lo que es: `**la plaza de las cenizas**`. Es la misma regla de siempre: las entidades se enlazan y los demás nombres no.
- **Orientación:** una de nueve: noroeste, norte, noreste, oeste, centro, este, suroeste, sur, sureste. En un lugar de varios niveles (los pisos de una torre o un edificio, los niveles de una mazmorra), con su nivel: `nivel 2, norte`. El nivel 1 es el de la entrada; los demás siguen el orden en que se recorren, hacia arriba o hacia abajo, y la conexión lo dice («una escalera que baja al nivel 2»). Tiene que cuadrar con lo que cuenta la nota («al norte del puerto»).
- **Una línea:** qué es y **lo que se ve** de ella, porque es lo que se dibuja: «sala del trono con un trono de piedra, charcos y relieves en los muros».
- **Conecta con:** las zonas a las que se pasa directamente (un pasillo, una calle, un camino, una escalera entre niveles). Las conexiones son físicas: van en las dos zonas. Solo las que la nota sostiene; no todo tiene que estar conectado.
- **Lo escondido que se conoce,** si lo hay, al final de la línea:
  - `Paso oculto a 7.` (o `Pasos ocultos a 7 y 9.`): una puerta disimulada, un pasadizo, una trampilla hacia esa zona. Va en las dos zonas, como las conexiones.
  - `Trampa: <una línea>.` (una losa que se hunde y suelta la reja de la escalera): una por zona como mucho.

  En el dibujo, el paso oculto es una línea de puntos que atraviesa el muro, y la trampa, un pequeño triángulo (los símbolos de la Guía Visual).

**Lo que se sabe frente a lo que es:** la leyenda y el mapa están en la nota, que cuenta lo que se sabe. Solo llevan los pasos ocultos y las trampas que la nota conoce (sus Accesos y sus Peligros: alguien los usa, alguien los sufrió). Un paso del que se habla pero nadie sabe dónde está va en el texto, no en la leyenda. Lo que nadie conoce es un **secreto**: va en `80_Secretos` y nunca en la leyenda ni en el mapa.

## Reglas
- **Los números son estables:** las zonas nuevas van al final; nunca se renumera ni se reutiliza un número. Una zona que desaparece se queda, con lo que le pasó en su línea («derruida en el incendio»). Así, «la zona 7» significa lo mismo en todas las ediciones.
- **Las zonas y los niveles son los que pida el lugar,** sin un número fijo: una cripta pequeña puede tener 3 salas en un nivel y una fortaleza, 30 en cuatro pisos. **Como mucho 12 zonas por mapa** (es lo que un generador de imágenes dibuja bien): un lugar mayor se divide en niveles o pisos, cada uno con su mapa, con la numeración seguida (si el nivel 1 acaba en la 8, el nivel 2 empieza en la 9). Una ciudad o una región que se llena agrupa lugares en una zona con mapa propio (un barrio, una subregión).
- **Al crear un lugar dentro de otro** que tiene leyenda (su `ubicacion`, su `region`), añádelo a esa leyenda sin leerla:
  ```bash
  python <directorio de esta skill>/scripts/map_key.py <Lugar_que_lo_contiene> --add "[[Nota|Nombre]]" --position <orientación> --desc "<una línea>" [--level <n>] [--connects 2,5]
  ```
  - Si ya estaba en la leyenda (como enlace pendiente), no hace nada.
  - Si el lugar ya tiene mapa, la zona queda «sin cartografiar» hasta la edición siguiente.
  - Si sale con código 3, la leyenda está llena: no lo fuerces. Anota la pregunta con `add_entries.py --question` (qué zona con mapa propio debería agruparlo).
- `map_key.py <Nota>` muestra la leyenda, su edición y si toca dibujar la primera edición o una nueva.

## Variedad: las tablas de mapas
Los modelos repiten patrones: sin azar, todas las mazmorras tendrían la misma planta y todas las ciudades los mismos barrios. Antes de escribir la leyenda, tira en las tablas de mapas (`<expandir-mundo>/assets/Tablas/Mapas.md`, o la versión del mundo en `06_Generacion/Tablas`) con `roll_tables.py`, que da azar real; `--count` da varios resultados distintos entre sí:
- **interior:**
  ```bash
  python <expandir-mundo>/scripts/roll_tables.py --file Mapas --table "Interior: planta" --table "Interior: tamaño" --table "Interior: niveles" --table "Interior: estado"
  python <expandir-mundo>/scripts/roll_tables.py --file Mapas --table "Interior: salas" --count <zonas>
  python <expandir-mundo>/scripts/roll_tables.py --file Mapas --table "Interior: rasgo de una sala" --count <3 a 5>
  python <expandir-mundo>/scripts/roll_tables.py --file Mapas --table "Interior: conexiones" --count 3
  ```
- **urbano:** `Urbano: forma`, `Urbano: hito` y `Urbano: bordes`, y `Urbano: barrios` con `--count <zonas>`;
- **paraje:** `Paraje: partes` con `--count <zonas>`;
- **territorio:** `Territorio: dónde vive la gente` y `Territorio: caminos`, y `Territorio: accidentes` con `--count <3 a 5>`.

**Lo oculto:** tira `Interior: lo oculto`. Por cada trampa, tira juntas sus cuatro tablas: `Trampa: mecanismo`, `Trampa: disparador`, `Trampa: efecto` y `Trampa: quién la puso y para qué`. Por cada paso oculto, `Paso oculto: forma` y `Paso oculto: quién lo conoce`. Son categorías, no trampas hechas: combínalas en una sola, concreta, que encaje con el lugar y con su historia. Quién la puso y para qué es lo que la hace única. Nunca repitas una trampa en un mismo lugar, ni copies la de otro: cada una sale de su propia tirada.

Las tiradas son una **semilla, no una orden**:
- Manda lo que cuenta la nota y lo que pidió el usuario: si la nota dice que la cripta tiene cinco cámaras, el tamaño no la cambia. La entrada es siempre la zona 1 y la sala principal la pone el concepto; las tiradas varían el resto.
- El tamaño se ajusta a la relevancia: con relevancia 2, como mucho mediano.
- Cada resultado se adapta al mundo, a su género y a su tecnología («establos o hangar»). Si uno choca con el canon, vuelve a tirar solo esa tabla.
- Anota las tiradas en el informe («Tiradas»).

## La imagen
La dibuja `generar-imagen` en modo mapa (ver su `referencias/mapas.md`), después del concept art. Una edición nueva toca cuando hay 3 zonas sin cartografiar o más, o un cuarto de las cartografiadas. Además de la leyenda, la sección `## Mapa` lleva:
- una línea con la edición, al principio: `*Edición 2 · 2026-10-12 · técnica: Boceto en acuarela · comprobado: 12/12 marcadores, sin repetidos*`;
- si la leyenda tiene pasos ocultos o trampas, debajo, la línea que explica sus símbolos (los de la Guía Visual): `*En el mapa, la línea de puntos que atraviesa un muro es un paso oculto, y el triángulo, una trampa.*`;
- el mapa embebido (`![[Mapa_<Nota>.jpg|600]]`) encima de sus zonas. Con varios niveles, cada nivel lleva su título (`**Nivel 2**`), su mapa y debajo sus zonas; `map_key.py --add` pone cada zona nueva con las de su nivel.

En el frontmatter, `mapa` lista sus imágenes (una por nivel), `mapa_edicion` es la edición y `mapa_zonas` el último número cartografiado. Los actualiza `map_key.py <Nota> --charted` al terminar cada edición.
