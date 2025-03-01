# Articulos generados con IA - Reflex
Proyecto Reflex que permite generar articulos con IA deepseek sin necesidad de token o apiKey perfilando un usuario como autor y basado en su edad carga ubicacion y un tema principal, este proyecto se basa en el ejemplo del template de sales by Reflex


## Instrucciones
Siga los siguientes pasos para instalar y ejecutar la aplicacion de articulos, es recomendado utilizar venv python y activar el entorno

```shell
python -m venv .venv
source .venv/bin/activate
```

## 1. Instalar Reflex y sus dependencias
Instalar reflex:

```shell
pip install reflex
```

```shell
pip install -r requirements.txt
```

## 2. Inicializar la base de datos

```shell
reflex db init
```

## 3. Configrar el entorno de IA ejemplo DeepSeek utilizando la libreria Ollama en python
ingresa a https://ollama.com/download y descarga segun tu sistema operativo
una vez instalado correctamente ejecuta el siguiente comando para instalar la version DeepSeek

```shell
ollama pull deepseek-r1:7b
```

### 4. Ejecutar la aplicación

```shell
reflex run
```
Luego puedes entrar a tu aplicacion con el navegador y la dirección por defecto

```shell
http://localhost:3000
```

### Notes
No olvides configurar IA - como OLlama con deepseek - que funcione en tu equipo

## Aplicando cambios en la base de datos

si se realizan cambios en el modelo de base de datos ejecutar el comando

```bash
reflex db makemigrations --message "Brief description of the change"
```

```bash
reflex db migrate
```
