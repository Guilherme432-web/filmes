from filmes import (
    create_user_profile,
    get_user_profile,
    update_user_profile,
    delete_user_profile,
    create_table_if_not_exists
)

import boto3

sts = boto3.client('sts')
identity = sts.get_caller_identity()

def menu():
    print("\n" + "="*30)
    print("CRUD User Profiles (DynamoDB)")
    print("="*30)
    print("1 - Criar perfil")
    print("2 - Ler perfil")
    print("3 - Atualizar perfil")
    print("4 - Deletar perfil")
    print("0 - Sair")

def main():
    create_table_if_not_exists()

    while True:
        menu()
        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == '1':
            user_id = input("ID do usuário: ").strip()
            nome = input("Nome: ").strip()
            try:
                idade = int(input("Idade: ").strip())
            except ValueError:
                print("Idade inválida. Use um número inteiro.")
                continue
            item = create_user_profile(user_id, nome, idade)
            print("\nPerfil criado:", item)

        elif escolha == '2':
            user_id = input("ID do usuário: ").strip()
            item = get_user_profile(user_id)
            if item:
                print("\nPerfil encontrado:")
                print(f"  Nome: {item['nome']}")
                print(f"  Idade: {item['idade']}")
            else:
                print("\nPerfil não encontrado.")

        elif escolha == '3':
            user_id = input("ID do usuário: ").strip()
            nome = input("Novo nome (deixe vazio para não alterar): ").strip()
            idade_input = input("Nova idade (deixe vazio para não alterar): ").strip()

            nome = nome if nome != '' else None
            idade = int(idade_input) if idade_input != '' else None

            if nome is None and idade is None:
                print("Nada para atualizar.")
                continue

            updated = update_user_profile(user_id, nome, idade)
            if updated:
                print("\nPerfil atualizado:", updated)
            else:
                print("\nPerfil não encontrado ou nada foi alterado.")

        elif escolha == '4':
            user_id = input("ID do usuário: ").strip()
            delete_user_profile(user_id)
            print("\n Perfil deletado (se existia).")

        elif escolha == '0':
            print("\n Saindo...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")

if _name_ == '_main_':
    main()
