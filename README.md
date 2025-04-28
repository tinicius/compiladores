# Trabalho de Compiladores
Este projeto consiste na implementação em Python de um interpretador para uma variação da linguagem Pascal. 

## Analisador Léxico 

O analisador é responsável por analisar o código-fonte da linguagem e converter o texto em uma sequência de tokens identificados. Os tokens são unidades básicas de código, como palavras-chave, operadores e identificadores. Este analisador atua como a primeira etapa do processo de compilação, onde o código-fonte é dividido em partes menores que facilitam a análise e a interpretação.


## Como executar

Para executar o programa e obter a lista de tokens, considere as seguintes instruções:

- Os códigos Pascal devem ser inseridos no diretório `/examples`.
- Execute o comando:

  ```bash
  python3 main.py examples/<nome_arquivo.pas>
  ```

- Exemplo:

  ```bash
  python3 main.py examples/hello_world.pas
  ```
