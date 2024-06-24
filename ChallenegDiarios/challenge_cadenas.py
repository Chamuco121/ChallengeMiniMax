{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def invertir_caracteres(cadena_de_caracteres):\n",
    "    if len(cadena_de_caracteres) == 0:\n",
    "        return \" \"\n",
    "    else:\n",
    "        return cadena_de_caracteres[-1] + invertir_caracteres(cadena_de_caracteres[:-1])\n",
    "\n",
    "# Solicitar al usuario que ingrese la cadena de caracteres\n",
    "cadena_usuario = input(\"Por favor, ingrese la cadena de caracteres que desea invertir: \")\n",
    "\n",
    "# Invertir la cadena ingresada por el usuario\n",
    "resultado = invertir_caracteres(cadena_usuario)\n",
    "\n",
    "# Mostrar el resultado\n",
    "print(resultado)\n"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
