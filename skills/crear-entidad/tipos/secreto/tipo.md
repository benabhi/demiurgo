# Tipo: secreto

La verdad oculta sobre una entidad o un hecho: lo que realmente es, frente a lo que se cree. Se crea sola (`/crear-entidad secreto`) o como parte de otra entidad, por ejemplo un personaje.

## Identidad del tipo
- **Emoji del tipo:** 🔒, al inicio del H1: `# 🔒 La deuda de Aldric Voss`.
- **Carpeta:** `80_Secretos`.
- **Plantilla:** `plantilla.md`, que se instala como `Plantilla_Secreto.md`.
- **Nombre del archivo:** `Secreto_<Tema>_de_<Entidad>` en ASCII. Ejemplo: `Secreto_La_Deuda_de_Aldric_Voss.md`.

## Reglas
- **Dirección de los enlaces:**
  - la nota de lore afectada **nunca enlaza** al secreto;
  - el secreto enlaza a lo que afecta (`afecta_a`) y a quienes lo conocen (`conocido_por`).
- **"Señales y pistas"** coincide con las señales visibles y los rumores de las notas afectadas: es lo que un observador atento podría descubrir.
- **`conocido_por`** puede incluir enlaces pendientes: personas que conocen el secreto y aún no tienen nota.
- **`relevancia`:** sigue a la gravedad: `menor` es 1 o 2, `grave` es 3 o 4 y `mundial` es 5.
- **`gravedad`:**
  - `menor`: afecta a la vida de una persona;
  - `grave`: afecta a una familia, un grupo o un lugar;
  - `mundial`: podría cambiar el mundo.
- Rellena todas las secciones.
  - **"La verdad":** el detalle completo.
  - **"Cómo se oculta":** quién lo encubre y cómo.
  - **"Si se revela":** las consecuencias concretas.
