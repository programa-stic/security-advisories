
# Vulnerabilidades en Edenor 2.0 para Android


## 1. Información del reporte

**Título:** Vulnerabilidades en Edenor 2.0 para Android

**Reporte ID:** STIC-2015-0127

**Reporte URL:** [http://www.fundacionsadosky.org.ar/publicaciones-2](http://www.fundacionsadosky.org.ar/publicaciones-2)

**Fecha de publicación:** 2016-03-22

**Fecha de última actualización:** 2016-03-23

**Fabricantes contactados:** Edenor

**Modo de publicación:** Coordinado


## 2. Información de vulnerabilidades

**Clase:** [Inyección de código](http://cwe.mitre.org/data/definitions/94.html), [Implementación de mecanismo de seguridad del servidor en el cliente](http://cwe.mitre.org/data/definitions/602.html)], [Validación errónea de datos de entrada](http://cwe.mitre.org/data/definitions/20.html)], [Mecanismo de autorización ausente](http://cwe.mitre.org/data/definitions/862.html)

**Impacto:** Ejecución de código, Perdida de datos

**Remotamente explotable:** Si

**Localmente explotable:** Si

**Identificador CVE:** N/A

## 3. Descripción de vulnerabilidad

 Edenor 2.0 [1] es una aplicación para dispositivos móviles que permite a usuarios de Edenor [2], empresa de distribución eléctrica de Argentina, conocer los datos de la última factura, visualizarla e imprimirla. También permite ver online cualquier reclamo por falta de suministro, geolocalizar las oficinas comerciales y entidades de pago habilitadas, recibir notificaciones y avisos sobre cuentas predeterminadas y enviar a la empresa fotos del medidor del servicio eléctrico. A la fecha de publicación de este reporte, la aplicación tiene entre 50.000 y 100.000 instalaciones según estadísticas del mercado de apps Google Play.
    
 Se descubrieron varias vulnerabilidades en la aplicación que permiten a potenciales atacantes:
    
* Acceder localmente a todos los datos de la aplicación desde cualquier otra aplicación sin necesidad de permiso alguno
* Ejecutar código con los permisos de la aplicación Edenor 2.0 en el dispositivo móvil
* Obtener de los servidores de la aplicación todos los datos de todos los usuarios registrados de Edenor 2.0
* Realizar cualquiera de las operaciones disponibles en la aplicación Edenor 2.0 en nombre de cualquier otro usuario registrado
  
Las acciones descriptas pueden realizarse utilizando una aplicación maliciosa en el mismo dispositivo móvil en el que esté instalada la aplicación de Edenor o simplemente modificando la aplicación Edenor 2.0.
  

## 4. Paquetes vulnerables

* Dispositivos corriendo la versión 2.1 o versiones anteriores. El impacto de los problemas reportados es mayor en dispositvos corriendo Android versión 4.4.4 o menor (aproximadamente el 27% del total según datos de Google) [3]

## 5. Información y soluciones del fabricante
 
El 24 de enero de 2016 Edenor publicó en Google Play la versión 2.1 de la aplicación, corrigiendo algunas de las vulnerabilidades reportadas.
    
El 22 de marzo de 2016 Edenor publicó la version 2.2 de la aplicación. La empresa indicó que la última versión corrige la totalidad de los problemas reportados. 
    

## 6. Créditos

Las vulnerabilidades fueron descubiertas e investigadas por Joaquin Rinaudo. La publicación de este reporte fue coordinada por Programa Seguridad en TIC. 

## 7. Descripción técnica
 
Edenor 2.0 fué desarrollada usando Apache Cordova[4], un framework de código abierto, tambien conocido como Phonegap, que permite construir aplicaciones para dispositivos móviles usando la misma tecnología utilizada en aplicaciones web, evitando así utilizar herramientas de desarrollo del lenguaje nativo de cada plataforma móvil. 
     
El framework exporta la funcionalidad nativa de los dispositivos móviles a tecnologías web como JavaScript, CSS y HTML5. Para ello, Apache Cordova instancia dentro de la aplicación móvil el inteprete de estos lenguajes de un navegador web con una vista gráfica customizada a la que nos referiremos como "Webview".
   
El problema del uso de Webviews en aplicaciones móviles es que, para aumentar su usabilidad, frecuentemente se debilitan las protecciones que proveen aislamiento entre contenidos descargados de distintos dominios (Same Origin Policy) y entre dominios y el sistema operativo (sandbox), permitiendo que un script corriendo en el Webview interactúe directamente con componentes nativos del sistema.
  
El framework Apache Cordova permite que código Javascript en el Webview ejecute código Java nativo para acceder a diversas funcionalidades del dispositivo móvil como la cámara, el acelerómetro, el GPS, la agenda de contactos, etc. La funcionalidad disponible se controla mediante un archivo de configuración en el que se puede habilitar explícitamente cada una o todas de forma general usando un "comodín" (`*`). En dispositivos con versiones anteriores a Android 4.4.4, la habilitación de cualquiera de la funcionalidades disponibles permite que Javascript malicioso inyectado a la aplicación desde una fuente externa ejecute código nativo a elección del atacante. 
   
Versiones de Edenor 2.0 anteriores a 2.1 utilizan una versión desactualizada de Apache Cordova lo que la hace susceptible a ataques que exploten vulnerabilidades ya conocidas, como CVE-2014-3500, CVE-2014-3501 y CVE-2014-3502 [5]. La primera permite a una aplicación maliciosa, sin ningçún permiso, enviar un Intent que cambie la página de inicia de Edenor 2.0 a una provista por el atacante. La configuración de Apache Cordova de Edenor 2.0 es insegura y permite cargar contenido desde cualquier dominio, con lo cual un atacante podría inyectar, desde la página de inicio redirigida, contenido Javascript de su elección para:
    

* Exfiltrar datos usando la funcionalidad del framework disponible en Edenor 2.0 (cámara, geolocalización, acelerómetro, contactos, etc.)
* Exfiltrar datos privados del almacenamiento local (cookies, credenciales, etc.).
* Ejecutar código nativo en el intérprete Java o el intérprete de comandos del sistema operativo.

Por ejemplo, versiones anteriores a 2.1 de Edenor 2.0 utilizan la versión 2.9.0 de Apache Cordova, que es vulnerable a CVE-2014-3500 [5] permitiendole a otras aplicaciones cambiar la página de inicio por una con contenido malicioso a través de un Intent que lleve un parámetro extra con referencia al contenido bajo la clave `url`. Un configuración correcta del framework podría bloquear dicho ataque si en el archivo de configuración `res/xml/config.xml`. se restringen los dominios a los que la aplicación se puede conectar. Sin embargo, la configuración usada permite a la aplicación acceder a cualquier dominio dado a que se utiliza un "comodín" (`*`) para especificar los dominios permitidos.
    
Dentro de este archivo de configuración también se encuentran listados los plugins que se pueden utilizar desde la aplicación. Muchos de de ellos no son necesarios para su funcionamiento. Por ejemplo, `Media` permite reproducir y grabar audio desde Javascript.  `ContactManager`permite el manejo de los contactos del dispositivo y `Capture`permite capturar fotos y videos. Además de incluir estos plugins, la aplicación necesita pedir los permisos necesarios de Android para poder utilizar estos recursos. Dado los permisos que pide la aplicación, algunos de los plugins no pueden ser utilizados realmente e intentar hacerlo terminaría con execepciones de seguridad debido por falta de permisos, p.e en el caso del `ContactManager`. De lo anterior, se puede concluir que se optó por utilizar una configuración completamente permisiva de plugins, solo restringida por los permisos a nivel Android requeridos por la aplicación.
   
La aplicación aloja los datos de todos sus usuarios en Azure, la plataforma de servicios en la nube de Microsoft[6], y utiliza Azure Mobile Services para almacenarlos y accederlos. El componente utilizado genera las consultas a la base de datos usando una API REST donde la operación de acceso se indica con el verbo HTTP y los filtros correspondientes se pasan como parámetro del URL. Dado que el servidor no valida la semántica de los filtros recibidos, es posible modificarlos en el cliente para ejecutar cualquier consulta arbitraria a la base de datos.
  
Esto permite a un usuario autenticado obtener información acerca de lectura de medidores, datos de otros usuarios (incluyendo nombres, teléfonos, email, dirección, número de cuenta asociado), notificaciones enviadas de la aplicación, etc. Los pedidos autenticados a la infraestructura de Azure tienen la siguiente sintaxis:

    GET https://ednmobile.azure-mobile.net/tables/table_name?filtro 
  
Se pueden realizar pedidos a las siguientes tablas: _Contacto_, _Notificaciones_mobile_, _Lectura_Medidor_, _Contacto_Dispositivo_Cuenta_, _Cuenta_. Los pedidos generados por la aplicación agregan a las consultas filtros de acuerdo al input del usuario. Por ejemplo, si un usuario quiere asociar la cuenta de Edenor número 1234 con su usuario, se hará un pedido al servidor como el siguiente para validar dicha cuenta:
  
    GET https://ednmobile.azure-mobile.net/tables/Cuenta?$filter=(Acct_Id%20eq%20'1234')

Modificando el filtro por la condición _(Acct_Id%20gt%20'0')_, el servidor responderá enviando todas las filas de la tabla _Cuenta_. Esto se debe a que el servidor no válida que los filtros generados recibidos de un cliente correspondan con la semántica esperada para la operación requerida. El mismo tipo de ataque funciona para otros pedidos al resto de las tablas mencionadas. 
  
Finalmente, si bien la aplicación requiere que los usuarios se autentiquen, la API REST carece de un mecanismo de autorización de pedidos del lado del servidor, por lo cual cualquier usuario auténticado puede realizar operacioenes sobre la cuenta de cualqueir otro usuario.
  

## 8. Cronología del reporte

* **2015-12-29:** 
          Se envia mail a contacto de seguridad de Edenor.
        
* **2015-12-29:** 
          Respuesta de Edenor solicitando hacer una conferencia telefónica para conocer y analizar el reporte.
        
* **2016-01-05:** 
          Nuevo contacto de Edenor solictando un conferencia telefónica.
        
* **2016-01-09:** 
         El Programa STIC envia el reporte de vulnerabilidades, indicando que por procedimiento interno todas las comunicacioens deberán ser por email para que queden documentadas, haciendo referencia al documento de procedimiento de reporte y divulgación de vulnerabilidades[7] que utiliza el equipo, explicando que las vulnerabilidades fueron reportadas anteriormente al desarrollador de la aplicación  que fue identificado de manera fortuita y que es intención del Programa STIC publicar el reporte el 1ro de Febrero de 2016.
        
* **2016-01-11:** 
          Respuesta de Edenor indicando que analizarán el reporte y se volverán a contactar cuando tengan novedades
        
* **2016-01-13:** 
          Edenor informa que se está trabajando en solucionar las vulnerabilidades y en los próximos días proporcinará fecha estimada para la publicación de una nueva versión de la app. Solicita conferencia telefónica para acordar fecha de publicación del reporte. 
        
* **2016-01-13:** 
         Programa STIC solicita que Edenor informe en cuanto tenga arregladas las vulnerabilidades a fín de verificar su correcta resolución.
        
* **2016-01-14:** 
         Programa STIC reitera que las comunicaciones deben ser por mail para que queden documentadas. Indica que no tiene objeciones en reprogramar la publicación del reporte, en la medida que Edenor informe sobre la resolución de los problemas y dé una fecha estimada concreta para la publicación de parches o de una versión arreglada de la app.
        
* **2016-01-24:** 
          Edenor publica en Google Play la version 2.1 de Edenor 2.0.
        
* **2016-01-26:** 
          Edenor informa que enviará un informe describiendo las acciones correctivas y la fecha tentativa para su implementación.
        
* **2016-01-28:** 
          Edenor envia el reporte _RTA - Informe Fundacion Sadosky.docx_ solicitando comentarios a las correciones propuestas e indicando que estaría en condiciones de publicar la nueva versión a fin de Febrero.
        
* **2015-02-01:** 
          Programa STIC informa a Edenor que reprogarmó la publicación del reporte para el 1ro de marzo y envia comentarios al documento de propuesta de correciones recibido el 28 de enero. Manifiesta estar de acuerdo en la solución para los problemas de Apache Cordova, recomieda el uso de un mecanismo centralizado de autorización[8] e indica que la autorización po si solo noes sucifiente para resolver todos los problemas sino que es necesario, además, realizar validación sintáctica y semántica de los parámetros de los URLs.
        
* **2015-02-26:** 
          Edenor informa que la recomendaciones de program, STIC impactaron en los tiempos para desarrollar una versión nueva de la app con los problemas corregidos y podrá disponer de ella para purebas internas en la semanda del 7 de marzo. Pregunta si el Programa STIC podrñá realizar purebas en paralelo.
        
* **2015-03-02:** 
          Programa STIC responde que, en base a lo iunformado por Edenor, reprogrmó la publicación del reportar para el 9 de marzo y que no tendrá disponibilidad para verificar manualmente la correcta resolución de las vulnerabildades. Solicita un informe mas detallado par aentender de que forma se planea arreglarlas. 
        
* **2015-03-08:** 
          Edenor envia el documento _EDN200 - Seguridad - documento de arquitectura v1.0.docx_ en el que se describen los detalles y alcance de la solución a las vulnerabilidades reportadas. Indica que la nueva versión de la app estará disponible en Google Play en aproximadamente 10 días. 
        
* **2015-03-10:** 
          Programa STIC informa a Edenor que reprogarmó la publicación del reporte para el 18 de marza y que esa fecha es final. Idica que en el mejor de los caso podra realizar pruebas automatizadas del la app a partir del 16 de marzo.
        
* **2015-03-10:** 
          Edenor envia el APK de la nueva version de la app.
        
* **2015-03-22:** 
          Edenor publica en Google Play la version 2.2 de Edenor 2.0
        

## 9. Referencias

[1] Google Play
    [https://play.google.com/store/apps/details?id=com.edenor.mobile.android](https://play.google.com/store/apps/details?id=com.edenor.mobile.android)

[2] Edenor
      [http://www.edenor.com.ar/cms/subsolapa7.html](http://www.edenor.com.ar/cms/subsolapa7.html)

[3] Versiones de Android en uso
[http://developer.android.com/intl/es/about/dashboards/index.html](http://developer.android.com/intl/es/about/dashboards/index.html)

[4] Apache Cordova/Phonegap
[https://cordova.apache.org/docs/en/latest/guide/overview/index.html](https://cordova.apache.org/docs/en/latest/guide/overview/index.html)

[5] Vulnerabilidades en Phonegap
[http://www-01.ibm.com/support/docview.wss?uid=swg21681356](http://www-01.ibm.com/support/docview.wss?uid=swg21681356)

[6] Microsoft Azure [https://azure.microsoft.com/es-es/](https://azure.microsoft.com/es-es/)

[7] Fundación Dr. Manuel Sadosky - Procedimiento de reporte y difusión de vulnerabilidades
[http://www.fundacionsadosky.org.ar/wp-content/uploads/2015/07/procedimiento-de-reporte-y-de-difusion-de-vulnerabilidades.pdf](http://www.fundacionsadosky.org.ar/wp-content/uploads/2015/07/procedimiento-de-reporte-y-de-difusion-de-vulnerabilidades.pdf)

[8] Service-side authorization of users in Mobile Services 
[https://azure.microsoft.com/en-us/documentation/articles/mobile-services-javascript-backend-service-side-authorization/](https://azure.microsoft.com/en-us/documentation/articles/mobile-services-javascript-backend-service-side-authorization/)

## 10. Acerca Fundación Dr. Manuel Sadosky

La Fundación Dr. Manuel Sadosky es una institución público privada cuyo objetivo es favorecer la articulación entre el sistema científico – tecnológico y la estructura productiva en todo lo referido a la temática de las Tecnologías de la Información y la Comunicación (TIC). Creada a través del Decreto Nro. 678/09 del Poder Ejecutivo Nacional, la Fundación es presidida por el ministro de Ciencia, Tecnología e Innovación Productiva. Sus vicepresidentes son los presidentes de las cámaras más importantes del sector TIC: CESSI (Cámara de Empresas de Software y Servicios Informáticos) y CICOMRA (Cámara de Informática y Comunicaciones de la República Argentina). Para más información visitar: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Derechos de autor

El contenido de este reporte tiene copyright (c) 2014-2016 Fundación Sadosky y se publica bajo la licencia Creative Commons Attribution Non-Commercial Share-Alike 4.0: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)