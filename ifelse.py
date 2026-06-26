age = int(input("Digite sua idade: ")) # Atenção a entrada de dados. Foi configurado para receber tipo inteiro

if age >= 18:
    print(f"Você pode entrar pois tem {age} anos!!!")

elif age < 18:
    print(f"Você não pode entrar pois tem {age} anos!!!")   

    if age == 17:
        print(f"Após o seu próximo aniversário você poderá entrar !! Pois terá {age+1} anos") 