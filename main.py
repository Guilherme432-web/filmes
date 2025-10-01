from importfilmes create_user_profile, get_user_profile, update_user_profile, delete_user_profile

def menu():
    print("\nCRUD User Profiles")
    print("1 - Criar perfil")
    print("2 - Ler perfil")
    print("3 - Atualizar perfil")
    print("4 - Deletar perfil")
    print("0 - Sair")

def main():
    while True:
        menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            user_id = input("ID do usuário: ")
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            item = create_user_profile(user_id, nome, idade)
            print("Perfil criado:", item)

        elif escolha == '2':
            user_id = input("ID do usuário: ")
            item = get_user_profile(user_id)
            if item:
                print("Perfil encontrado:", item)
            else:
                print("Perfil não encontrado.")

        elif escolha == '3':
            user_id = input("ID do usuário: ")
            nome = input("Novo nome (deixe vazio para não alterar): ")
            idade_input = input("Nova idade (deixe vazio para não alterar): ")

            nome = nome if nome.strip() != '' else None
            idade = int(idade_input) if idade_input.strip() != '' else None

            updated = update_user_profile(user_id, nome, idade)
            if updated:
                print("Perfil atualizado:", updated)
            else:
                print("Nada foi atualizado ou perfil não encontrado.")

        elif escolha == '4':
            user_id = input("ID do usuário: ")
            delete_user_profile(user_id)
            print("Perfil deletado (se existia).")

        elif escolha == '0':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if _name_ == '_main_':
    main()
