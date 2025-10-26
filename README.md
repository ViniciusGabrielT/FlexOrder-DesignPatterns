# FlexOrder-DesignPatterns
Aplicar Padrões de Projeto Estruturais e Comportamentais para refatorar um código monolítico, melhorando o acoplamento, a coesão e a aderência aos princípios SOLID, especificamente o SRP (Single Responsibility Principle) e o OCP (Open/Closed Principle).

## Refatoração com o Padrão Comportamental Strategy

1. **Criação das Interfaces de Estratégia:**
- ``EstrategiaPagamento``: Define a interface para os métodos de pagamento.
- ``EstrategiaFrete``: Define a interface para os métodos de frete.

````python
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
````

2. **Implementação das Classes Concretas:**
- Pagamento: ``PagamentoPix``, ``PagamentoCredito``, ``PagamentoMana``.

````python
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
````

- **Frete:** ``FreteNormal``, ``FreteExpresso``, ``FreteTeletransporte``.

````python
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
````

3. **Criação da Classe ``Pedido``:** Atua como o Contexto, permitindo a troca de estratégias de pagamento e frete em tempo de execução.

4. **Remoção de Lógica Acoplada:** A lógica de pagamento e frete foi movida para as classes de estratégia.

### Explicação das Mudanças

1. **Desacoplamento:** A lógica de pagamento e frete foi movida para classes separadas, seguindo o padrão Strategy.

2. **Flexibilidade:** As estratégias de pagamento e frete podem ser alteradas em tempo de execução, permitindo maior reutilização e manutenção.

3. **Classe ``Pedido``:** Atua como o contexto, delegando as responsabilidades de pagamento e frete às estratégias.

4. **Testes:** Os cenários de teste foram ajustados para usar as novas classes e estratégias.

## Refatoração com o Padrão Comportamental Decorator

1. **Criação da Interface Base:** Adicionei a interface ``CustoPedido`` para definir o contrato de cálculo do valor total.

````python
# ==========================================================
# Interface Base para o Cálculo do Pedido
# ==========================================================
class CustoPedido(ABC):
    @abstractmethod
    def calcular_custo(self):
        pass
````

2. **Implementação da Classe Base:** A classe ``PedidoBase`` implementa a interface ``CustoPedido`` e representa o pedido básico.

````python
# ==========================================================
# Implementação Base do Pedido
# ==========================================================
class PedidoBase(CustoPedido):
    def __init__(self, itens):
        self.itens = itens
        self.valor_base = sum(item['valor'] for item in itens)

    def calcular_custo(self):
        return self.valor_base
````

3. **Criação dos Decorators:**

- ``DescontoPix``: Aplica o desconto de 5% para pagamentos via PIX.

````python
class DescontoPix(PedidoDecorator):
    def calcular_custo(self):
        custo_base = self.pedido.calcular_custo()
        desconto = custo_base * 0.05
        print(f"Aplicando 5% de desconto PIX: -R${desconto:.2f}")
        return custo_base - desconto
````

- ``TaxaEmbalagemPresente``: Adiciona uma taxa fixa de R$5,00 para pedidos com embalagem de presente.

````python
class TaxaEmbalagemPresente(PedidoDecorator):
    def calcular_custo(self):
        custo_base = self.pedido.calcular_custo()
        taxa = 5.00
        print(f"Adicionando taxa de embalagem de presente: +R${taxa:.2f}")
        return custo_base + taxa
````

4. **Modificação da Classe Pedido:** A lógica de cálculo de descontos e taxas foi movida para os decorators, deixando a classe Pedido mais simples e focada.

### Explicação das Mudanças

1. **Interface ``CustoPedido``:** Define o contrato para calcular o custo do pedido.

2. **Decorators:** ``DescontoPix`` e ``TaxaEmbalagemPresente`` são implementados como decorators que adicionam ou modificam o custo do pedido de forma dinâmica.

3. **Classe ``Pedido``:** Agora aceita uma lista de decorators, que são aplicados ao pedido base antes de calcular o frete e processar o pagamento.

4. **Flexibilidade:** Novos descontos ou taxas podem ser adicionados facilmente como novos decorators, sem modificar as classes existentes.

## Refatoração com o Padrão Estrutural Facade

1. **Criação de Subsistemas:**

- ``SistemaEstoque``: Gerencia a atualização do estoque após a conclusão do pedido.

````python
class SistemaEstoque:
    def atualizar_estoque(self, itens):
        print("Atualizando estoque com os itens do pedido...")
        for item in itens:
            print(f"   -> Removendo {item['nome']} do estoque.")
````

- ``GeradorNotaFiscal``: Responsável por gerar a nota fiscal.

````python
class GeradorNotaFiscal:
    def gerar_nota_fiscal(self, pedido):
        print("Gerando nota fiscal para o pedido...")
        print(f"   -> Itens: {[item['nome'] for item in pedido.itens]}")
        print("   -> Nota fiscal gerada com sucesso.")
````

2. **Implementação da Classe ``CheckoutFacade``:** A classe ``CheckoutFacade`` fornece uma interface simplificada para orquestrar o processo de checkout, delegando as responsabilidades para as estratégias e subsistemas.

````python
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
````

3. **Modificação da Classe ``Pedido``:** O método ``finalizar_compra()`` foi simplificado para utilizar a ``CheckoutFacade``.

## Explicação das Mudanças

1. **Subsistemas:** ``SistemaEstoque`` e ``GeradorNotaFiscal`` encapsulam responsabilidades específicas, como atualização de estoque e geração de nota fiscal.

2. **Fachada:** ``CheckoutFacade`` simplifica o processo de checkout, delegando tarefas para os subsistemas e estratégias.

3. **Classe ``Pedido``:** Mantém os dados do pedido, enquanto a lógica de checkout foi movida para a fachada.

4. **Flexibilidade:** A fachada permite adicionar ou modificar subsistemas sem alterar a lógica do pedido.