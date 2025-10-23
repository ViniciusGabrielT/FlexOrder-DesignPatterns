# ==========================================================
# CÓDIGO SPAGHETTI DO E-COMMERCE MÁGICO (PRÉ-REFORMA)
# Problemas: Alto Acoplamento, Baixa Flexibilidade, Monolítico
# ==========================================================

class SistemaPedidoAntigo:
    """
    Classe monolítica que centraliza pedidos, pagamentos, frete e descontos.
    Um verdadeiro pesadelo de manutenção.
    """

    def __init__(self, itens, metodo_pagamento, tipo_frete, tem_embalagem_presente=False):
        """Inicializa o sistema de pedido antigo.

        Args:
            itens (list): A lista de itens do pedido.
            metodo_pagamento (str): O método de pagamento.
            tipo_frete (str): O tipo de frete.
            tem_embalagem_presente (bool, optional): Se o pedido tem embalagem para presente. Defaults to False.
        """
        self.itens = itens
        self.metodo_pagamento = metodo_pagamento
        self.tipo_frete = tipo_frete
        self.valor_base = sum(item['valor'] for item in itens)
        self.tem_embalagem_presente = tem_embalagem_presente

    def aplicar_desconto(self):
        """Lógica de descontos fixos (Hardcoded)."""
        if self.metodo_pagamento == 'Pix':
            print("Aplicando 5% de desconto PIX.")
            return self.valor_base * 0.95
        elif self.valor_base > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            return self.valor_base * 0.90
        else:
            return self.valor_base

    def calcular_frete(self, valor_com_desconto):
        """Lógica de frete complexa e acoplada."""
        custo_frete = 0.0

        if self.tipo_frete == 'Normal':
            custo_frete = valor_com_desconto * 0.05
            print(f"Frete Normal: R${custo_frete:.2f}")
        elif self.tipo_frete == 'Expresso':
            custo_frete = valor_com_desconto * 0.10 + 15.00  # Taxa extra
            print(f"Frete Expresso (com taxa): R${custo_frete:.2f}")
        elif self.tipo_frete == 'Teletransporte':
            # Frete VIP - Lógica de cálculo bizarra (precisa de lib externa)
            custo_frete = 50.00
            print(f"Frete Teletransporte: R${custo_frete:.2f}")
        else:
            print("Tipo de frete desconhecido.")
        
        return custo_frete

    def processar_pagamento(self, valor_final):
        """Lógica de pagamento acoplada e com ifs aninhados."""
        sucesso = False
        if self.metodo_pagamento == 'Credito':
            print(f"Processando R${valor_final:.2f} via Cartão de Crédito...")
            # Chamada direta e acoplada a um subsistema imaginário
            if valor_final < 1000:
                 print("   -> Pagamento com Credito APROVADO.")
                 sucesso = True
            else:
                 print("   -> Pagamento com Credito REJEITADO (limite excedido).")
        
        elif self.metodo_pagamento == 'Pix':
            print(f"Processando R${valor_final:.2f} via PIX...")
            print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
            sucesso = True
        
        elif self.metodo_pagamento == 'Mana':
            print(f"Processando R${valor_final:.2f} via Transferência de Mana...")
            print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
            sucesso = True

        else:
            print(f"Método de pagamento '{self.metodo_pagamento}' não suportado!")

        return sucesso

    # A função principal do sistema
    def finalizar_compra(self):
        """
        Método monolítico de alto nível que controla toda a transação.
        Violando o Facade, pois o cliente (o código de uso) chama isso
        e a lógica interna é inalterável e pouco clara.
        """
        print("=========================================")
        print("INICIANDO CHECKOUT MONOLÍTICO...")
        
        # 1. Aplicar Descontos
        valor_apos_desconto = self.aplicar_desconto()
        
        # 2. Calcular Frete
        custo_frete = self.calcular_frete(valor_apos_desconto)
        
        valor_final = valor_apos_desconto + custo_frete
        
        # 3. Taxa Adicional (Um IF perdido)
        if self.tem_embalagem_presente:
            taxa = 5.00
            valor_final += taxa
            print(f"Adicionando R${taxa:.2f} de Embalagem de Presente.")

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 4. Processar Pagamento
        if self.processar_pagamento(valor_final):
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
    pedido1 = SistemaPedidoAntigo(itens_p1, 'Pix', 'Normal', tem_embalagem_presente=False)
    pedido1.finalizar_compra()
    
    print("\n--- Próximo Pedido ---")
    
    # Cenário 2: Pedido Grande (Desconto) com Cartão (Lógica de limite)
    # e Embalagem Presente (Lógica de taxa).
    itens_p2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    pedido2 = SistemaPedidoAntigo(itens_p2, 'Credito', 'Expresso', tem_embalagem_presente=True)
    pedido2.finalizar_compra()