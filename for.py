#Programa que mostrará quais vogais estão na palavra inserida.

texto = input("Informe um texto: ")
VOGAIS = "AEIOU"


for letra in texto: #Letra é definida no próprio laço
    if letra.upper() in VOGAIS:
        print(letra, end=" ")

print() #Quebra de linha

print(letra[0]) #Teste do vetor letra.