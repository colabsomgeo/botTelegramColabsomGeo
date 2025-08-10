# ColabSomGeo

Este projeto é um sistema de colaboração geográfica com integração via Telegram Bot, desenvolvido em Python. A aplicação permite receber e armazenar dados enviados por usuários diretamente pelo Telegram, utilizando MongoDB como base de dados.

## 📦 Estrutura do Projeto

```
ColabSomGeo/
├── botTelegram/        # Código relacionado ao bot do Telegram
│   ├── __init__.py
│   └── bot.py
├── mongDB/             # Módulo de integração com MongoDB
│   └── __init__.py
├── main/               # Arquivos principais da aplicação
│   └── main.py
├── main.py             # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
└── LICENSE             # Licença do projeto
```

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- MongoDB
- Telegram Bot API
- Bibliotecas adicionais listadas em `requirements.txt`

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Sannyer3232/Colab_Som_Geo.git
cd Colab_Som_Geo
```

2. Crie um ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## ⚙️ Execução

Certifique-se de configurar as variáveis de ambiente necessárias, como a chave do bot do Telegram e as credenciais de acesso ao MongoDB.

Para iniciar a aplicação:

```bash
python main.py
```

## 📌 Contribuição

Sinta-se à vontade para contribuir! Faça um fork, crie uma branch com sua feature (`git checkout -b feature/nova-feature`) e depois envie um pull request.

## Autores

   * [Sergio Augusto Coelho Bezerra](sergio.bezerra@ifam.edu.br) - Professor Orientador
   * [Fani Tamires de Souza Batista](https://github.com/fanitsouza) - Aluno Desenvolvedor 
   * [Sannyer Cadoso Carvalho Nery](https://github.com/Sannyer3232) - Aluno Desenvolvedor
## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
