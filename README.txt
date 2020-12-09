XADREZ

Instruções para o modo offline:

- Executar o ficheiro "main.py" ("python3 main.py")


Instruções para o modo multiplayer:

- Em primeiro lugar executar o ficheiro "server.py" e colocar como parametros o IP e a porta
  Ex: python3 server.py 192.168.2.10 5432

- De seguida ambos os clientes podem conectar-se ao servidor executando o ficheiro "client.py"
  Ex: python3 client.py 192.168.2.10 5432 (o IP e porta devem ser os mesmos que o do servidor)

- O cliente que tiver a mensagem "JOGADOR 1 - BRANCAS" é o primeiro a jogar 


Possíveis erros:

- O servidor e ambos os clientes devem-se encontrar na mesma rede (LAN).

- A porta especificada no script do servidor nao deve ser menor que 1024, uma vez que a propabilidade de portas abaixo deste número
  estarem a ser usadas é alta 

- O movimento de roque ainda não foi implementado

Bibliotecas requiridas:
-pygame

