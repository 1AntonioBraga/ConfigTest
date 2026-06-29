#Strings - Métodos

curso = " pYthon "

print(curso.upper()) #PYTHON
print(curso.lower()) #python    
print(curso.rstrip()) #Remove espaços à direita
print(curso.lstrip()) #Remove espaços à esquerda


print(curso.center(10,"#")) #Centraliza a string e preenche com o caractere especificado

print (".".join(curso)) #Coloca o caractere especificado entre cada caractere da string

print (".".join(curso.upper())) #Coloca o caractere especificado entre cada caractere da string, mas em maiúsculo



print("""

=================== Wellcome ===================
      1 - Transfer
      2 - Delete
      3 - Exit

      
=================================================
      
      Thank you!


""")