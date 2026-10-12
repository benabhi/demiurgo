# Tipo: personaje

Individuos con nombre propio, de cualquier especie o naturaleza: desde un mendigo hasta un monarca, vivos o muertos, incluidos animales con nombre y seres artificiales con identidad. Los dioses y las entidades superiores no son de este tipo: tendrán su propio módulo.

## Identidad del tipo
- **Emoji del tipo:** 👤, al inicio del H1 de todas las fichas: `# 👤 Nombre Apellido`.
- **Emoji propio:** cada personaje tiene uno en la propiedad `emoji`, elegido según quién es (⚒️ herrero, 🗡️ asesina, 📜 escriba, 🐺 cazador…).
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Personaje.md`.
- **Módulo:** `modulo.json` (familia, emoji, rango de enlaces pendientes nuevos, carpeta según el rol y propiedad → tipo de entidad); lo usan `find_gaps.py` y `check_note.py`.
- **Tipo auxiliar:** `secreto`, solo cuando el personaje tiene uno (ver "Secretos").

## Rol y carpeta
La propiedad `rol` decide la carpeta (definida en `modulo.json`; `check_note.py` la valida):

| rol | carpeta |
|---|---|
| `protagonista` | `20_Personajes/Protagonistas` |
| `secundario` | `20_Personajes/Personajes_Secundarios` |
| `antagonista` | `20_Personajes/Antagonistas` |
| `historico` | `20_Personajes/Figuras_Historicas` |

**Cómo decidir el rol**, en este orden:
1. **Si el usuario lo dice**, se respeta ("un protagonista…", "el villano…").
2. **Si no, se deduce del concepto:**
   - **`historico`:** vivió en una era anterior al presente. Señales: "murió hace siglos", "fundador antiguo", "héroe de la guerra de…", "figura legendaria".
   - **`antagonista`:** su papel es oponerse. Señales: "villano", "enemigo de…", "el que amenaza…", "líder enemigo".
   - **`protagonista`:** el usuario lo plantea como figura central. Señales: "el héroe", "personaje principal", "nuestro protagonista".
3. **Si no hay pistas, `secundario`.**

Si el rol fue deducido, el resumen final lo dice y explica por qué. Un personaje que muere en el presente conserva su rol: solo cambia `situacion_vital`.

## Nombre
- Según la sonoridad de la Ficha del Mundo y coherente con su pueblo. Genera candidatos con `generate_names.py` (`--profile <su cultura>`, que usa el perfil `Nombres_<Cultura>` si existe, o `Generico`) y elige o adapta uno.
- Archivo `Nombre_Apellido.md` en ASCII (Guía de Nombres). H1 con la ortografía real.
- En `aliases`: el nombre real si difiere del archivo, apodos y títulos.

## Cómo rellenar la ficha
La ficha se rellena **según su relevancia**: el frontmatter, completo; las secciones, las que dice `check_note.py --depth` (ver «Profundidad» en `SKILL.md`), sin dejar campos vacíos en lo que lleva y sin inventar para llenar. Lo único sin resolver son los enlaces pendientes.
- **Concreto y específico:** colores, materiales, gestos, nombres. Nada genérico ("ojos bonitos", "es amable").
- **Resumen:** quién es y qué lo hace interesante, no solo su oficio.
- **Identidad:** la tabla completa. Si el calendario de la Ficha está por definir, la edad va en años y el nacimiento en términos relativos; si existe el calendario de referencia, el nacimiento va con su fecha («15 de Siega de 380 UE»).
- **Apariencia:** alimenta la imagen (el retrato). Describe lo visible con detalle: colores, materiales, cicatrices, prendas. El **rasgo distintivo** es lo primero que alguien recuerda, un elemento visual único.
- **Voz y presencia:** cómo suena y cómo se lo percibe. La frase característica va entre comillas.
- **Personalidad:** virtudes y defectos en tensión. El código moral y "Bajo presión" hacen al personaje predecible para escribirlo.
- **Motivaciones:**
  - el deseo es lo que persigue; la necesidad, lo que de verdad le haría bien (a menudo se oponen);
  - el "Tema que encarna" es uno de los temas centrales de la Ficha.
- **Trasfondo:**
  - Orígenes: 1 o 2 párrafos.
  - Momentos decisivos: de 3 a 6, con fecha (relativa si no hay calendario) y enlaces a los eventos.
  - El presente: qué hace ahora y por qué.
  - Un día típico: breve.
- **Vida social:** residencia, facciones (con su rango), creencias (con su grado de devoción) y reputación, cada una con su enlace.
- **Familia:**
  - Todos los parentescos relevantes, con su estado (vivo, muerto, desaparecido o desconocido).
  - Edades coherentes: los padres, mayores que los hijos, y cada edad acorde con la longevidad y la madurez de su especie si tiene ficha (el auditor lo revisa).
  - El linaje, si existe.
- **Relaciones:**
  - Vínculos variados (personas, lugares, objetos o animales): 1 o 2 con relevancia 1 o 2; al menos 4 desde la 3.
  - **Vínculo:** mentor, discípulo, rival, amigo, aliado, enemigo, amante, deudor, acreedor, protector, protegido, patrón, empleado, compañero…
  - **Actitud:** confianza, respeto, miedo, desprecio, devoción, envidia, culpa, indiferencia… Es la de **este** personaje: la del otro lado no se deduce de ella (ver «Relaciones» en `SKILL.md`).
  - **Por qué y qué cambia:** de dónde viene el vínculo y qué consecuencia concreta tiene para él (una deuda que lo ata, un miedo que lo aparta de un camino). Si no cambia nada, sobra.
- **Posesiones y recursos:** objetos notables con su significado, equipo, riqueza y contactos.
- **Habilidades y conocimientos:** los poderes respetan la regla de poderes de la Ficha y las reglas de su sistema (la magia, el don o el pacto que usa), que se enlaza en el texto y en `sistemas`; lo mismo una técnica fuera de lo común. Si no hay poderes, escribe "Ninguno".
- **Salud y afecciones:** el estado físico; las afecciones con su enlace; las cicatrices, con la historia de cada una.
- **Relación con el mundo:** su postura concreta ante el conflicto central de la Ficha y cómo le afecta en su día a día.
- **Secretos y rumores:**
  - Solo algunos personajes tienen secreto (ver "Secretos"); si lo tiene, va como nota aparte.
  - Aquí van 2 o 3 **rumores**, alguno falso, y las **señales visibles** del secreto si lo hay; si no lo hay, "Señales visibles: ninguna".
- **Ganchos:** de 2 a 4 situaciones abiertas que se puedan desarrollar.
- **Citas:** de 1 a 3 frases suyas o sobre él, atribuidas (`— alguien`).
- **Imagen:**
  - "Descripción visual": de 4 a 6 elementos clave para el retrato.
  - "Prompt": lo completa `generar-imagen`; si no se genera, escribe "pendiente".
  - Con imagen, `generar-imagen` añade el embed `![[Retrato_Nombre.jpg|300]]` bajo el resumen.
- **Mecánicas:** solo si la Ficha define un sistema de rol. Se añade `## Mecánicas (<sistema>)` antes de Imagen, compatible con ese sistema.

## Frontmatter
- Cada relación es un enlace entre comillas: `residencia: "[[Forja_del_Puerto]]"`. Las listas, un valor por línea:
  ```yaml
  padres:
    - "[[Madre_de_Aldric_Voss]]"
  ```
- **Las propiedades de relación solo contienen enlaces.** Si el dato se desconoce o depende de un pilar por definir, la propiedad queda vacía (`""` o `[]`) y el cuerpo lo explica. Nunca escribas texto como `desconocido` en una propiedad de relación.
- **Frontmatter y cuerpo coinciden:** todo enlace de una propiedad aparece también en su sección del cuerpo, con contexto.
- `ultima_revision`: la fecha de hoy **sin comillas** (`ultima_revision: 2026-10-10`). La plantilla la trae entre comillas solo por compatibilidad con el plugin Plantillas de Obsidian.
- `edad`: un número o `desconocida`. `genero`: texto libre.
- `relevancia`: de 1 a 5 según la Guía de Organización. Un tabernero suele ser 1 o 2; un líder de facción, 3 o 4; una figura que cambió el mundo, 5.
- `nacimiento` y `muerte`: número de años en el calendario de la Ficha (negativos antes del año 0).
  - Si la Ficha tiene `ano_actual`, entonces `nacimiento` = año actual − edad.
- `fecha_exacta`: el día de nacimiento con los nombres del calendario de referencia («15 de Siega de 380 UE»), del mismo año que `nacimiento`. Vacía si no existe ese calendario (ver `tipos/calendario/tipo.md`).
  - Si el calendario está por definir, quedan vacías y el cuerpo usa fechas relativas.
  - `muerte` queda vacía mientras viva.
- `especie` y `pueblo` enlazan a su especie y su cultura. Respeta la regla de especies de la Ficha: no crees especies nuevas si no está permitido.
- `vinculos`: personajes con los que tiene una relación fuera de la familia. Los lugares y objetos significativos van en la tabla Relaciones y en su propiedad (`residencia`, `posesiones`…).
- `sistemas`: los sistemas que usa o domina (una magia, un don, un pacto, una técnica fuera de lo común). Si es uno de sus practicantes notables y el sistema ya existe, añádelo también a sus `practicantes`.
- `imagen`: vacío hasta que `generar-imagen` lo complete.

## Enlaces pendientes
Sigue `referencias/huecos.md`: toda entidad que nombra la ficha va enlazada, y las que aún no existen quedan como enlaces pendientes, cada una con su tipo. **Entre 3 y 8 nuevos** con relevancia 4 o 5 (los que solo nombra esta nota), de al menos dos tipos si son varios; con menos relevancia, menos: el rango lo da `check_note.py --depth`. Buenos candidatos:
- un familiar (`padres`, `hermanos`, `pareja`, `hijos`);
- un vínculo (`vinculos`: un mentor, un rival, un amor perdido);
- un lugar (`lugar_nacimiento`, `residencia`: su casa, su taller);
- una facción o una creencia;
- una posesión notable;
- el sistema de su poder, si lo tiene y aún no existe (`sistemas`).

## Secretos
- **No todos los personajes tienen secreto: solo cada tanto, y solo desde relevancia 3.** Decídelo con una tirada real, nunca imaginada: `python <directorio de la skill>/scripts/roll_dice.py 1d4`. Con un **4**, el personaje tiene un secreto. Con relevancia 1 o 2 no se tira: no lleva secreto.
- Sin tirar, tiene secreto si el concepto lo implica o el usuario lo pide; y no lo tiene si el usuario lo descarta.
- Cada secreto se crea con el tipo `secreto` (`tipos/secreto/tipo.md`) y enlaza al personaje en `afecta_a`.
- La ficha del personaje **nunca enlaza** a su secreto: en "Secretos y rumores" solo van las señales visibles y los rumores.

## Comprobaciones antes de escribir
- [ ] El nombre es único en la bóveda y en el Glosario.
- [ ] El rol sigue la regla de "Rol y carpeta" y la nota está en su carpeta.
- [ ] Es coherente con la Ficha: especies, tecnología, poderes, tono, crudeza y vetos.
- [ ] Las edades familiares son coherentes, y `nacimiento`/`muerte` son números que cuadran con la edad (o están vacías si no hay calendario).
- [ ] La `relevancia` va del 1 al 5 y es proporcional a su peso en el mundo.
- [ ] No queda ningún campo del cuerpo vacío, toda entidad nombrada lleva enlace y los enlaces pendientes nuevos están en el rango de su relevancia (`check_note.py --depth`), todos con tipo.
- [ ] Las propiedades de relación contienen solo enlaces (o están vacías) y `ultima_revision` va sin comillas.
- [ ] El frontmatter y el cuerpo coinciden.
- [ ] Si tiene secreto, la ficha no menciona ni enlaza su verdad.
