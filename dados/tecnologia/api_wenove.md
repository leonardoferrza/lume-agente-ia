# Documentação Técnica - API WeNove (v1.0)

Esta documentação é voltada para a equipe de desenvolvimento e detalha os endpoints principais do marketplace de moda circular WeNove.

## Autenticação
Todas as requisições para a API exigem um token Bearer no cabeçalho (Header).
`Authorization: Bearer <SEU_TOKEN>`

## Endpoints de Produtos (Peças)

### 1. Listar Peças Disponíveis
- **Rota:** `GET /api/v1/produtos`
- **Descrição:** Retorna a lista de todas as peças de roupa ativas no marketplace.
- **Filtros suportados:** `categoria`, `tamanho`, `condicao` (ex: vintage, seminovo).

### 2. Cadastrar Nova Peça
- **Rota:** `POST /api/v1/produtos`
- **Descrição:** Cria o anúncio de uma nova peça na plataforma.
- **Corpo da Requisição (JSON obrigatório):**
  - `titulo`: String (ex: "Calça Wide Leg Cintura Alta")
  - `descricao`: String detalhando o estado da peça.
  - `preco`: Float (valor em Reais).
  - `marca`: String.

### 3. Atualizar Status de Venda
- **Rota:** `PATCH /api/v1/produtos/{id}/status`
- **Descrição:** Altera o status da peça (ex: de "disponível" para "vendido"). Apenas administradores e o próprio vendedor têm permissão.