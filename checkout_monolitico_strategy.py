from abc import ABC, abstractmethod

# ==========================================================
# Interfaces de Estratégia
# ==========================================================
class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor_final):
        pass

class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular_frete(self, valor_com_desconto):
        pass

# ==========================================================
# Implementações Concretas de Pagamento
# ==========================================================
class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True

class PagamentoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via Cartão de Crédito...")
        if valor_final < 1000:
            print("   -> Pagamento com Credito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Credito REJEITADO (limite excedido).")
            return False

class PagamentoMana(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via Transferência de Mana...")
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True

# ==========================================================
# Implementações Concretas de Frete
# ==========================================================
class FreteNormal(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = valor_com_desconto * 0.05
        print(f"Frete Normal: R${custo_frete:.2f}")
        return custo_frete

class FreteExpresso(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = valor_com_desconto * 0.10 + 15.00
        print(f"Frete Expresso (com taxa): R${custo_frete:.2f}")
        return custo_frete

class FreteTeletransporte(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = 50.00
        print(f"Frete Teletransporte: R${custo_frete:.2f}")
        return custo_frete

# ==========================================================
# Classe Pedido (Contexto)
# ==========================================================
class Pedido:
    def __init__(self, itens, estrategia_pagamento, estrategia_frete, tem_embalagem_presente=False):
        self.itens = itens
        self.estrategia_pagamento = estrategia_pagamento
        self.estrategia_frete = estrategia_frete
        self.tem_embalagem_presente = tem_embalagem_presente
        self.valor_base = sum(item['valor'] for item in itens)

    def aplicar_desconto(self):
        if isinstance(self.estrategia_pagamento, PagamentoPix):
            print("Aplicando 5% de desconto PIX.")
            return self.valor_base * 0.95
        elif self.valor_base > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            return self.valor_base * 0.90
        else:
            return self.valor_base

    def finalizar_compra(self):
        print("=========================================")
        print("INICIANDO CHECKOUT COM PADRÃO STRATEGY...")

        # 1. Aplicar Descontos
        valor_apos_desconto = self.aplicar_desconto()

        # 2. Calcular Frete
        custo_frete = self.estrategia_frete.calcular_frete(valor_apos_desconto)
        valor_final = valor_apos_desconto + custo_frete

        # 3. Taxa Adicional
        if self.tem_embalagem_presente:
            taxa = 5.00
            valor_final += taxa
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 4. Processar Pagamento
        if self.estrategia_pagamento.processar_pagamento(valor_final):
            print("\nSUCESSO: Pedido finalizado e registrado no estoque.")
            print("Emitindo nota fiscal (lógica de subsistema oculta).")
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False

# ==========================================================
# USO ATUAL (CENÁRIOS DE TESTE)
# ==========================================================
if __name__ == "__main__":
    # Cenário 1: Pedido com PIX (Desconto) e Frete Normal.
    itens_p1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]
    pedido1 = Pedido(itens_p1, PagamentoPix(), FreteNormal(), tem_embalagem_presente=False)
    pedido1.finalizar_compra()

    print("\n--- Próximo Pedido ---")

    # Cenário 2: Pedido Grande (Desconto) com Cartão (Lógica de limite)
    # e Embalagem Presente (Lógica de taxa).
    itens_p2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    pedido2 = Pedido(itens_p2, PagamentoCredito(), FreteExpresso(), tem_embalagem_presente=True)
    pedido2.finalizar_compra()