# Guía de Organización — {{MUNDO}}

## Principio de ubicación única
Cada nota vive en **una sola carpeta**, según **qué es**, no según con qué se relaciona. Las relaciones se expresan con enlaces `[[...]]` y propiedades; nunca se duplica una nota.

## Mapa de la bóveda
| Sección | Contenido |
|---|---|
{{MAPA_SECCIONES}}

El `README.md` de cada carpeta detalla qué va y qué no.

## Desempates frecuentes
- **Especie o pueblo:** la biología va en `Especies_Inteligentes`; la cultura, en `Pueblos_y_Culturas`.
- **Acontecimiento o guerra:** un hecho puntual va en `Acontecimientos`; un conflicto prolongado, en `Guerras_y_Conflictos`.
- **Entidad o creencia:** el ser va en `Deidades_y_Entidades`; su culto o ideología, en `Creencias_y_Religiones`.
- **Artefacto o fenómeno:** un objeto concreto va en `Artefactos_y_Reliquias`; una fuerza o anomalía, en `Fenomenos_Extraordinarios`.
- **Fenómeno o afección:** la fuerza va en `Fenomenos_Extraordinarios`; lo que provoca en los seres vivos (enfermedad, mutación), en `Enfermedades_y_Afecciones`.
- **Material natural o procesado:** en bruto, en `50_Naturaleza`; transformado, en `Materiales_Procesados`.
- **Astro:** si se visita o habita, es un lugar (`Grandes_Regiones`); si solo se observa desde el mundo, va en `Cosmos_y_Astros`.
- **Lugar o ruina:** en uso, `Lugares_y_Estructuras`; abandonado o peligroso, `Ruinas_y_Zonas_Peligrosas`.
- **Mito, arte o secreto:** lo que el mundo cuenta va en `Mitos_y_Leyendas`; las obras y textos, en `Arte_y_Expresion`; la verdad detrás, en `80_Secretos`.
- **Sistema o ejemplo:** la regla general va en `70_Sistemas_y_Cosmologia`; cada ejemplo concreto, en su carpeta natural.

## Frontmatter base
Toda nota de lore empieza con estas propiedades. Las plantillas de cada tipo pueden añadir más, nunca quitar.

```yaml
---
tipo:            # un tipo registrado (ver tabla), en minúsculas y singular
estado: borrador # borrador | canon | archivado
aliases: []      # nombre real con su ortografía, apodos, traducciones
tags: []
origen: manual   # opcional: manual | procedural (si falta, se asume manual)
relevancia: 3    # de 1 a 5 (ver "Relevancia")
ultima_revision: # fecha real AAAA-MM-DD
---
```

- Propiedades recomendadas: `region`, `era`, `fuentes`.
- Nombres de propiedades en `snake_case`, sin tildes. Tags en minúsculas, sin tildes, con guiones.
- Los enlaces dentro de propiedades van entre comillas (`"[[Nota]]"`); en las listas, un valor por línea precedido de `- `. Obsidian 1.9+ solo reconoce `aliases`, `tags` y `cssclasses` (no `alias`, `tag` ni `cssclass`).

### Relevancia
Cuánto importa la entidad al mundo. Decide qué se desarrolla primero, cuánto se enlaza y **cuánto desarrollo lleva su nota**: el frontmatter y el núcleo van siempre; las secciones de profundidad (citas, ganchos, un día típico…), solo desde cierta relevancia. Una entidad que gana peso se profundiza después.

| Valor | Significado |
|---|---|
| 1 | Anecdótica: un detalle de color. |
| 2 | Local menor: conocida en su entorno inmediato. |
| 3 | Local importante: pesa en su ciudad, su gremio o su comarca. |
| 4 | Regional: la conoce o la nota toda una región. |
| 5 | Mundial: define o cambia el mundo. |

### Fechas del mundo
- Las fechas del mundo se guardan como **número de años** en el eje del calendario de la Ficha: el año 0 es el hecho que marca la Ficha y lo anterior es negativo (`nacimiento: -42`).
- Las propiedades de fecha de cada tipo (por ejemplo `nacimiento` y `muerte`) solo admiten un número entero o quedar vacías.
- Si el calendario está por definir, quedan vacías y el cuerpo usa fechas relativas ("hace veinte años").
- Si existe un **calendario de referencia** (una nota de tipo `calendario` con `referencia: true`, en `40_Historia/Eras_y_Periodos`), sus meses y su forma de escribir los años dan las fechas del texto, y el día exacto va en `fecha_exacta` («15 de Siega de 412 UE») en los tipos que la tienen.

## Tipos registrados
Punto de extensión del proyecto: cada skill que cree un tipo de nota añade aquí su fila. El sistema de generación procedural usará esta tabla para saber qué skill invocar según el tipo obtenido.

| tipo | carpeta | plantilla | skill |
|---|---|---|---|
| ficha_mundo | `00_Sistema` | — | inicializar-mundo |
| moc | raíz de cada sección | — | inicializar-mundo |
| meta | `00_Sistema` | — | inicializar-mundo |

## Espacios reservados
- `00_Sistema/06_` en adelante: herramientas que añadan otras skills (por ejemplo, tablas de generación procedural).
- `90_` en adelante: módulos de uso del mundo (narrativa, juego…).
- Toda skill que añada carpetas les crea su `README.md` y las registra en la tabla "Carpetas añadidas por skills".

## Carpetas añadidas por skills
Carpetas que las skills crean al usarse por primera vez (cada una con su `README.md`).

| Carpeta | Contenido | skill |
|---|---|---|

## Estados
`borrador` → `canon` → `archivado`. Ver [[Guia_de_Canon]].

## Flujo
1. Las ideas sin clasificar entran en `05_Bandeja_de_Entrada`.
2. La nota se crea en su carpeta, con la plantilla de su tipo si existe.
3. Los MOC de cada sección se actualizan solos (Obsidian Bases).
4. Lo obsoleto pasa a `03_Archivados`; nunca se borra.
