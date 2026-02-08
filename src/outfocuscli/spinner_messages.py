import random

SPINNER_MESSAGES = [
    "Escolhendo o melhor modelo de linguagem para voce...",
    "Consultando os oraculos da inteligencia artificial...",
    "Perguntando ao ChatGPT se ele conhece o n8n...",
    "Debugando a matrix...",
    "Compilando pensamentos em linguagem natural...",
    "Fazendo um git push no universo paralelo...",
    "Rodando um SELECT * FROM cerebro WHERE resposta IS NOT NULL...",
    "Calculando a resposta para a vida, o universo e tudo mais... (e 42)",
    "Treinando uma rede neural com memes brasileiros...",
    "Importando bibliotecas do futuro...",
    "Perguntando pro Stack Overflow se isso e duplicata...",
    "Refatorando a resposta pela terceira vez...",
    "Esperando o deploy terminar... como sempre...",
    "Convertendo cafe em codigo...",
    "Resolvendo conflitos de merge com a realidade...",
    "Processando... nao e um bug, e uma feature...",
    "Aquecendo os GPUs...",
    "Fazendo pair programming com a IA...",
    "Otimizando a resposta com O(1) de esperanca...",
    "Lendo a documentacao (sim, alguem faz isso)...",
    "Inicializando os neuronios artificiais...",
    "Rodando os testes... todos os 0 testes passaram!",
    "Buscando a resposta no cache do universo...",
    "Executando workflow com carinho artesanal...",
]


def get_random_message() -> str:
    return random.choice(SPINNER_MESSAGES)
