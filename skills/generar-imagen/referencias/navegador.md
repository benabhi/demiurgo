# Alternativa: Gemini en el navegador

El flujo normal genera con Puter (Paso 3 de `SKILL.md`). Esta alternativa genera con Gemini en el Chrome del usuario y **solo se usa si la pide** (`/generar-imagen <nota> navegador`, "hazla con Gemini"). Sustituye al Paso 3; los pasos 1, 2, 4 y 5 son los mismos, con las diferencias del final.

El pedido del usuario cubre enviar el prompt a Gemini, descargar la imagen y moverla a la bóveda, sin preguntar.

## Generar en Chrome
1. Si las herramientas de Claude in Chrome (`mcp__claude-in-chrome__*`) no están cargadas, cárgalas con ToolSearch en una sola llamada. Si existe la skill `anthropic-skills:chrome-browser`, léela antes.
2. Si Chrome no está disponible, ve a "Si algo falla" de `SKILL.md`.
3. Abre una **pestaña nueva** y navega a `https://gemini.google.com/app`.
4. Comprueba la sesión. Si aparece "Iniciar sesión" o "Sign in", pide al usuario que inicie sesión por su cuenta y espera. **Nunca introduzcas credenciales.** Si aparece un aviso de términos, de cookies o de novedades, pide al usuario que lo resuelva por su cuenta: no aceptes acuerdos en su nombre.
5. Escribe en el cuadro de la petición `Generate an image: <prompt>` y envíalo.
6. **Espera la imagen.** Gemini a veces termina de generar pero deja el **recuadro gris** hasta que se refresca la página; la conversación se conserva al refrescar.
   1. Comprueba cada 10 segundos, con una captura o buscando el botón (`find`: "Descargar" / "Download"), si ya aparece el **icono de la flechita de descarga** sobre la respuesta. Es la señal de que la imagen está generada.
   2. Cuando aparezca, si la imagen se ve, sigue con "Descargar y guardar".
   3. Si sigue el recuadro gris, **refresca la página** y espera 10 segundos.
   4. Si tras el primer refresco sigue gris, **refresca una segunda vez** y espera 15 segundos.
   5. Si aun así no se ve pero el icono de descarga está, intenta descargarla igualmente: la descarga suele funcionar aunque la vista previa falle.
   6. Si en 3 minutos no aparece ni la imagen ni el icono, ve a "Si algo falla" de `SKILL.md`.
7. **Si Gemini rechaza la petición o responde solo con texto,** suaviza el prompt (más sugerido, menos explícito) y reintenta una vez en el mismo chat.
8. **Acepta la primera imagen válida.** Si el usuario quiere otra, la pedirá después (se guardará como `_v2`).

## Descargar y guardar
1. Ejecuta `python <directorio de la skill>/scripts/fetch_download.py mark` y guarda la marca que imprime.
2. Pulsa el botón de descarga de la imagen ("Descargar imagen en tamaño completo" / "Download full size image"; aparece al pasar el ratón sobre la imagen).
3. Ejecuta:
   ```bash
   python <directorio de la skill>/scripts/fetch_download.py fetch --since <marca> --dest "<bóveda>/00_Sistema/02_Activos/<Carpeta>" --name <Prefijo><Nombre_de_la_nota>
   ```
   El script imprime el nombre final, el tamaño y el nombre original de la descarga. Si ya existía un archivo con ese nombre, usa `_v2`, `_v3`…
4. Si el script no encuentra la imagen (la descarga no arrancó), pulsa de nuevo el botón y repite el paso 3.
5. Si Chrome abre un diálogo para elegir dónde guardar, la extensión no puede manejarlo. Pide al usuario que guarde en su carpeta de Descargas, o que desactive en Chrome "Preguntar dónde se guardará cada archivo", y repite el paso 3.

## Diferencias en la nota y el informe
- En la nota, el prompt se guarda **sin** la orden `Generate an image:`, que es para Gemini, y el modelo es `Gemini (navegador)`.
- En el informe, el nombre original de la descarga y las incidencias del navegador (refrescos por el recuadro gris, reintentos).
- La primera vez, avisa de que las imágenes de Gemini llevan una marca de agua visible y SynthID.
