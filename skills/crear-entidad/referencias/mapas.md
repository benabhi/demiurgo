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
N. **Nombre** · orientación — una línea. Conecta con 2 y 5.
```
- **Nombre:** si la zona es una entidad (un palacio, un templo, un barrio con nombre propio), va enlazada, a su nota o como enlace pendiente con su texto legible: `**[[Palacio_de_Ormal|El palacio]]**`. Si no lo es, va como texto, en minúscula y por lo que es: `**la plaza de las cenizas**`. Es la misma regla de siempre: las entidades se enlazan y los demás nombres no.
- **Orientación:** una de nueve: noroeste, norte, noreste, oeste, centro, este, suroeste, sur, sureste. En una mazmorra de varios niveles, con su nivel: `nivel 2, norte`. Tiene que cuadrar con lo que cuenta la nota («al norte del puerto»).
- **Una línea:** qué es y **lo que se ve** de ella, porque es lo que se dibuja: «sala del trono con un trono de piedra, charcos y relieves en los muros».
- **Conecta con:** las zonas a las que se pasa directamente (un pasillo, una calle, un camino, una escalera entre niveles). Las conexiones son físicas: van en las dos zonas. Solo las que la nota sostiene; no todo tiene que estar conectado.

## Reglas
- **Los números son estables:** las zonas nuevas van al final; nunca se renumera ni se reutiliza un número. Una zona que desaparece se queda, con lo que le pasó en su línea («derruida en el incendio»). Así, «la zona 7» significa lo mismo en todas las ediciones.
- **Como mucho 12 zonas por mapa.** Una mazmorra mayor se divide en niveles, con la numeración seguida (si el nivel 1 acaba en la 8, el nivel 2 empieza en la 9). Una ciudad o una región que se llena agrupa lugares en una zona con mapa propio (un barrio, una subregión).
- **Al crear un lugar dentro de otro** que tiene leyenda (su `ubicacion`, su `region`), añádelo a esa leyenda sin leerla:
  ```bash
  python <directorio de esta skill>/scripts/map_key.py <Lugar_que_lo_contiene> --add "[[Nota|Nombre]]" --position <orientación> --desc "<una línea>" [--level <n>] [--connects 2,5]
  ```
  - Si ya estaba en la leyenda (como enlace pendiente), no hace nada.
  - Si el lugar ya tiene mapa, la zona queda «sin cartografiar» hasta la edición siguiente.
  - Si sale con código 3, la leyenda está llena: no lo fuerces. Anota la pregunta con `add_entries.py --question` (qué zona con mapa propio debería agruparlo).
- `map_key.py <Nota>` muestra la leyenda, su edición y si toca dibujar la primera edición o una nueva.

## La imagen
La dibuja `generar-imagen` en modo mapa (ver su `referencias/mapas.md`), después del concept art. Una edición nueva toca cuando hay 3 zonas sin cartografiar o más, o un cuarto de las cartografiadas. Además de la leyenda, la sección `## Mapa` lleva:
- el mapa embebido (`![[Mapa_<Nota>.jpg|600]]`; en una mazmorra, uno por nivel, cada uno con su título `**Nivel 2**`);
- una línea con la edición: `*Edición 2 · 2026-10-12 · técnica: Boceto en acuarela · comprobado: 12/12 marcadores, sin repetidos*`.

En el frontmatter, `mapa` lista sus imágenes (una por nivel), `mapa_edicion` es la edición y `mapa_zonas` el último número cartografiado. Los actualiza `map_key.py <Nota> --charted` al terminar cada edición.
