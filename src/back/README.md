

# Back end ALEMBIC


6. Fluxo do dia a dia
Primeira vez (ou quando o banco está vazio):
bash# Gera a migration inicial com tudo
alembic revision --autogenerate -m "initial schema"

# Aplica no banco
alembic upgrade head
Quando você alterar um model (ex: adicionar description em Product):
bash# Gera só o diff
alembic revision --autogenerate -m "add description to product"

# Aplica
alembic upgrade head
Outros comandos úteis:
bashalembic current          # qual revision está aplicada agora
alembic history          # histórico de migrations
alembic downgrade -1     # desfaz a última migration
alembic downgrade base   # desfaz tudo (banco limpo