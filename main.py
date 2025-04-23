import json
from datetime import datetime

# Estrutura de dados inicial
dados_colheita = {
    "perdas": [],
    "total_manual": 0,
    "total_mecanica": 0
}

# Funções principais
def calcular_perdas(area, colhido, perdido, tipo):
    perda = (perdido / colhido) * 100
    return {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "area_plantada": area,
        "tipo_colheita": tipo,
        "perda_percentual": round(perda, 2)
    }

def salvar_json(dados):
    with open("dados_colheita.json", "w") as file:
        json.dump(dados, file, indent=4)

def carregar_json():
    try:
        with open("dados_colheita.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return dados_colheita

# Validação de entrada
def input_numero(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor if valor >= 0 else print("Valor não pode ser negativo!")
        except ValueError:
            print("Digite um número válido!")

# Menu interativo
def menu():
    print("\n=== MONITOR DE PERDAS NA COLHEITA ===")
    print("1. Registrar nova colheita")
    print("2. Ver relatório")
    print("3. Exportar dados")
    print("4. Sair")
    return input("Opção: ")

# Fluxo principal
if __name__ == "__main__":
    while True:
        opcao = menu()
        
        if opcao == "1":
            print("\n--- NOVO REGISTRO ---")
            area = input_numero("Área plantada (hectares): ")
            colhido = input_numero("Toneladas colhidas: ")
            perdido = input_numero("Toneladas perdidas: ")
            tipo = input("Tipo (manual/mecanica): ").lower()
            
            registro = calcular_perdas(area, colhido, perdido, tipo)
            dados = carregar_json()
            dados["perdas"].append(registro)
            
            if tipo == "manual":
                dados["total_manual"] += registro["perda_percentual"]
            else:
                dados["total_mecanica"] += registro["perda_percentual"]
                
            salvar_json(dados)
            print("✅ Dados salvos!")
            
        elif opcao == "2":
            dados = carregar_json()
            print("\n--- RELATÓRIO ---")
            for item in dados["perdas"]:
                print(f"{item['data']} | {item['area_plantada']} ha | "
                      f"{item['tipo_colheita']} | {item['perda_percentual']}%")
            
            print(f"\nTotal Manual: {dados['total_manual']}%")
            print(f"Total Mecânica: {dados['total_mecanica']}%")
            
        elif opcao == "3":
            with open("backup_dados.json", "w") as file:
                json.dump(carregar_json(), file, indent=4)
            print("📁 Backup salvo como 'backup_dados.json'")
            
        elif opcao == "4":
            print("Saindo...")
            break
            
        else:
            print("Opção inválida!")