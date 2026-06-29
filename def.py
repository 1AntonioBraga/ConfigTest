def verificador_ano_bissexto(ano):
    # Converte para número logo no início
    ano = int(ano) 
    
    resultbissexto = "NÃO" 

    # Lógica Matemática
    if not ano % 4 == 0:
        resultbissexto = "NÃO"
    if ano % 4 == 0:
        if ano % 100 != 0:
            resultbissexto = "SIM"
    if ano % 400 == 0:
        resultbissexto = "SIM"
            
    return resultbissexto

# O uso da função 
entrada_usuario = input()
resultado = verificador_ano_bissexto(entrada_usuario)
print(resultado)