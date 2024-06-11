def invertir_caracteres(cadena_de_caracteres):
    if len(cadena_de_caracteres) == 0:
        return " "
    else:
        return cadena_de_caracteres[-1] + invertir_caracteres(cadena_de_caracteres[:-1])

# Solicitar al usuario que ingrese la cadena de caracteres
cadena_usuario = input("Por favor, ingrese la cadena de caracteres que desea invertir: ")

# Invertir la cadena ingresada por el usuario
resultado = invertir_caracteres(cadena_usuario)

# Mostrar el resultado
print(resultado)
