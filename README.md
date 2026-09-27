Fenwick Tree

Este proyecto explica el funcionamiento de un Fenwick Tree mediante un video animado. La estructura está implementada en C++ y las animaciones se generan con Python y Manim.

Software requerido

Python 3.13 de 64 bits y conexión a Internet para instalar las dependencias. Puedes usar Visual Studio Code para abrir la carpeta y ejecutar los comandos desde su terminal. El archivo requirements.txt incluye Manim y el compilador C++ Zig.

Pasos para ejecutar en Windows

Abre una terminal en la carpeta del proyecto y ejecuta los siguientes comandos, uno por uno.

1. Crear el entorno:

python -m venv .venv

2. Instalar las dependencias:

.venv/Scripts/python.exe -m pip install -r requirements.txt

3. Compilar el código C++ y generar el video:

.venv/Scripts/python.exe renderizar.py

El programa compila y ejecuta fenwick.cpp automáticamente. Luego utiliza los resultados para generar las animaciones y guarda el video en Fenwick_Tree.mp4.

Para generar una vista previa rápida:

.venv/Scripts/python.exe renderizar.py --preview

Para compilar y comprobar el C++ sin generar el video:

.venv/Scripts/python.exe renderizar.py --solo-datos
