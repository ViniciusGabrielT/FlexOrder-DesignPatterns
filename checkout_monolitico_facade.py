from abc import ABC, abstractmethod

# ==========================================================
# Interface Base para o Cálculo do Pedido
# ==========================================================
class CustoPedido(ABC):
    @abstractmethod
    def calcular_custo(self):
        pass

# ==========================================================
# Implementação Base do Pedido
# ==========================================================
class PedidoBase(CustoPedido):
    def __init__(self, itens):
        self.itens = itens
        self.valor_base = sum(item['valor'] for item in itens)

    def calcular_custo(self):
        return self.valor_base

# ==========================================================
# Decorators para Modificar o Custo do Pedido
# ==========================================================
class PedidoDecorator(CustoPedido):
    def __init__(self, pedido):
        self.pedido = pedido

    @abstractmethod
    def calcular_custo(self):
        pass

class DescontoPix(PedidoDecorator):
    def calcular_custo(self):
        custo_base = self.pedido.calcular_custo()
        desconto = custo_base * 0.05
        print(f"Aplicando 5% de desconto PIX: -R${desconto:.2f}")
        return custo_base - desconto

class TaxaEmbalagemPresente(PedidoDecorator):
    def calcular_custo(self):
        custo_base = self.pedido.calcular_custo()
        taxa = 5.00
        print(f"Adicionando taxa de embalagem de presente: +R${taxa:.2f}")
        return custo_base + taxa

# ==========================================================
# Estratégias de Frete
# ==========================================================
class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular_frete(self, valor_com_desconto):
        pass

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

# ==========================================================
# Estratégias de Pagamento
# ==========================================================
class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar_pagamento(self, valor_final):
        pass

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

# ==========================================================
# Subsistemas
# ==========================================================
class SistemaEstoque:
    def atualizar_estoque(self, itens):
        print("Atualizando estoque com os itens do pedido...")
        for item in itens:
            print(f"   -> Removendo {item['nome']} do estoque.")

class GeradorNotaFiscal:
    def gerar_nota_fiscal(self, pedido):
        print("Gerando nota fiscal para o pedido...")
        print(f"   -> Itens: {[item['nome'] for item in pedido.itens]}")
        print("   -> Nota fiscal gerada com sucesso.")

# ==========================================================
# Classe CheckoutFacade
# ==========================================================
class CheckoutFacade:
    def __init__(self, sistema_estoque, gerador_nota_fiscal):
        self.sistema_estoque = sistema_estoque
        self.gerador_nota_fiscal = gerador_nota_fiscal

    def concluir_transacao(self, pedido):
        print("=========================================")
        print("INICIANDO CHECKOUT COM PADRÃO FACADE...")

        # 1. Calcular o custo base com os decorators
        pedido_base = PedidoBase(pedido.itens)
        for decorator in pedido.decorators:
            pedido_base = decorator(pedido_base)

        valor_com_desconto = pedido_base.calcular_custo()

        # 2. Calcular Frete
        custo_frete = pedido.estrategia_frete.calcular_frete(valor_com_desconto)
        valor_final = valor_com_desconto + custo_frete

        print(f"\nValor a Pagar: R${valor_final:.2f}")

        # 3. Processar Pagamento
        if pedido.estrategia_pagamento.processar_pagamento(valor_final):
            # 4. Atualizar Estoque
            self.sistema_estoque.atualizar_estoque(pedido.itens)

            # 5. Gerar Nota Fiscal
            self.gerador_nota_fiscal.gerar_nota_fiscal(pedido)

            print("\nSUCESSO: Pedido finalizado e registrado no sistema.")
            return True
        else:
            print("\nFALHA: Transação abortada.")
            return False

# ==========================================================
# Classe Pedido (Contexto)
# ==========================================================
class Pedido:
    def __init__(self, itens, estrategia_pagamento, estrategia_frete, decorators=[]):
        self.itens = itens
        self.estrategia_pagamento = estrategia_pagamento
        self.estrategia_frete = estrategia_frete
        self.decorators = decorators

# ==========================================================
# USO ATUAL (CENÁRIOS DE TESTE)
# ==========================================================
if __name__ == "__main__":
    # Instanciar subsistemas
    sistema_estoque = SistemaEstoque()
    gerador_nota_fiscal = GeradorNotaFiscal()

    # Instanciar a fachada
    checkout_facade = CheckoutFacade(sistema_estoque, gerador_nota_fiscal)

    # Cenário 1: Pedido com PIX (Desconto) e Frete Normal.
    itens_p1 = [
        {'nome': 'Capa da Invisibilidade', 'valor': 150.0},
        {'nome': 'Poção de Voo', 'valor': 80.0}
    ]
    pedido1 = Pedido(itens_p1, PagamentoPix(), FreteNormal(), decorators=[DescontoPix])
    checkout_facade.concluir_transacao(pedido1)

    print("\n--- Próximo Pedido ---")

    # Cenário 2: Pedido Grande com Embalagem Presente e Frete Expresso.
    itens_p2 = [
        {'nome': 'Cristal Mágico', 'valor': 600.0}
    ]
    pedido2 = Pedido(itens_p2, PagamentoCredito(), FreteExpresso(), decorators=[TaxaEmbalagemPresente])
    checkout_facade.concluir_transacao(pedido2)