# Programa que descobre a taxa de juros de um financiamento
# funcionando como o "Atingir Meta" do Excel: ele vai testando taxas
# até que o Valor Presente calculado fique igual ao valor financiado.
#
# Fórmula: VP = P * (1 - (1 + i)^-n) / i
 
 
def valor_presente(parcela, taxa, n):
    """Calcula o VP de uma série de parcelas iguais."""
    if taxa == 0:
        return parcela * n
    return parcela * (1 - (1 + taxa) ** -n) / taxa
 
 
def atingir_meta(vp_desejado, parcela, n, precisao=1e-10, max_iteracoes=1000):
    """Procura a taxa i que faz valor_presente(parcela, i, n) == vp_desejado.
 
    Usa o método da bisseção: começa com um intervalo de taxas
    [0%, 100%] e vai cortando ao meio, ficando sempre com a metade
    onde está a resposta.
    """
    taxa_min = 0.0
    taxa_max = 1.0  # 100% ao período
 
    # Se 100% ainda não for suficiente, aumenta o limite
    while valor_presente(parcela, taxa_max, n) > vp_desejado:
        taxa_max *= 2
 
    for iteracao in range(1, max_iteracoes + 1):
        taxa_meio = (taxa_min + taxa_max) / 2
        vp_calculado = valor_presente(parcela, taxa_meio, n)
 
        # Quanto MAIOR a taxa, MENOR o VP.
        if vp_calculado > vp_desejado:
            taxa_min = taxa_meio   # taxa ainda baixa -> sobe
        else:
            taxa_max = taxa_meio   # taxa alta demais -> desce
 
        if abs(vp_calculado - vp_desejado) < precisao:
            break
 
    return taxa_meio, iteracao
 
 
def main():
    print("=== Cálculo da Taxa de Juros (Atingir Meta) ===\n")
 
    financiamento = float(input("Valor do financiamento (R$): ").replace(",", "."))
    parcela = float(input("Valor da parcela (R$): ").replace(",", "."))
    n = int(input("Quantidade de parcelas: "))
 
    if financiamento <= 0 or parcela <= 0 or n <= 0:
        print("\nErro: todos os valores devem ser maiores que zero.")
        return
 
    total_pago = parcela * n
 
    if abs(total_pago - financiamento) < 1e-9:
        print("\nO total pago é igual ao financiado: taxa de juros = 0%.")
        return
    if total_pago < financiamento:
        print("\nErro: o total das parcelas (R$ {:.2f}) é menor que o valor "
              "financiado. Não existe taxa de juros positiva.".format(total_pago))
        return
 
    taxa, iteracoes = atingir_meta(financiamento, parcela, n)
 
    taxa_anual = (1 + taxa) ** 12 - 1
 
    print("\n--- Resultado ---")
    print(f"Taxa de juros por período: {taxa * 100:.4f}%")
    print(f"Taxa anual equivalente (se mensal): {taxa_anual * 100:.4f}%")
    print(f"Total pago: R$ {total_pago:.2f}")
    print(f"Total de juros: R$ {total_pago - financiamento:.2f}")
    print(f"Iterações necessárias: {iteracoes}")
    print(f"Conferência: VP com essa taxa = R$ "
          f"{valor_presente(parcela, taxa, n):.2f}")
 
 
if __name__ == "__main__":
    main()