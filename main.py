# Biblioteca de inteligencia artificial pronta para assistentes virtuais
from neuralintents import GenericAssistant
# Módulo com funções de hora e data
from datetime import datetime
# Módulo usada para fechar a tela quando robô se despedir
# Este módulo executa diversas funções integradas ao sistema operacional
import sys
import time
import speech_recognition as sr
import pyttsx3 as tts

# Bibliotecas para adicionar:
# speechRecognition - reconhecimento de voz
# textToSpeech - Ler textos

recognizer = sr.Recognizer()

speaker = tts.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[-2].id)

#Lista de exercicios
exercicios = ['Supino reto, 3 séries de 10', 'Cross over, 4 séries de 8', 'Agachamento, 3 séries de 15']

def mostrar_exercicios():
    print('Lista de exercícios de hoje')
    # Imprimir cada exercicio dentro da lista de exercicios
    # Enumerate gera um número para cada exercicio, começando por zero
    for numero, exercicio in enumerate(exercicios):
        print(f'{numero + 1} - {exercicio}')

    speaker.say('Sua lista de exercícios para hoje')
    for exercicio in exercicios:
        speaker.say(exercicio)
        speaker.runAndWait()

def adicionar_exercicio():

    global recognizer

    speaker.say("Qual exercício você deseja adicionar?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                print("fale o exercicio")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                novoexercicio = recognizer.recognize_google(audio, language='pt')
                novoexercicio = novoexercicio.lower()

                # Função append adiciona um item na lista
                exercicios.append(novoexercicio)
                speaker.say(f"Adicionado {novoexercicio} à lista")
                print(f"Adicionado {novoexercicio} à lista")
                done = True

        except sr.UnknownValueError():
            recognizer = sr.Recognizer()
            speaker.say("Não entendi, pode repetir?")
            speaker.runAndWait()

def remover_exercicio():
    # idx = index (-1 pois o index começa por 0, Por isso se o usuário inserir o número 3, deve estar referenciando o item de número 2)
    idx = int(input('Qual exercicio deseja remover: ')) - 1

    if idx <= len(exercicios):
        # Se o index que o usuário inseriu for menor que o tamanho da lista de exercicios, remover index referente da lista.
        print(f'Removendo exercicio {exercicios[idx]}')
        exercicios.pop(idx)
    else:
        # Senão avisar usuário de que o item não existe.
        print('Não existe um exercício com essa numeração')

def tchau():
    print('Até mais')
    speaker.say("Até mais")
    speaker.runAndWait()
    sys.exit(0)

def cumprimentos():
    speaker.say("Olá, eu sou seu Duck assistente, como posso ajudar?")
    speaker.runAndWait()

def agradecer():
    speaker.say("De nada!")
    speaker.runAndWait()

def motivacional():
    speaker.say("Vamos lá!")
    time.sleep(1)
    speaker.say("Você consegue!")
    time.sleep(1)
    speaker.say("Continue assim!")
    speaker.runAndWait()

# Mapeamento de padrões e funções
# Colocamos a tag do padrão e então a função que ela deve ativar.
mappings = {
        'cumprimentos': cumprimentos,
        'mostrar_exercicios': mostrar_exercicios,
        'adicionar_exercicio': adicionar_exercicio,
        'remover_exercicio': remover_exercicio,
        'despedida': tchau,
        'agradecer': agradecer,
        'motivacional': motivacional
        }

# Instanciando assistente em uma variável, passando como parâmetro o arquivo do modelo e o objeto que referencia o modelo com a função
assistente = GenericAssistant("intents.json", intent_methods=mappings)

# Mandando o assistente treinar com os modelos montados no arquivo intents.json
assistente.train_model()
# Salvando um modelo (Irrelevante por enquanto)
assistente.save_model()

# Ficar solicitando uma mensagem para o usuário
while True:
    try:
        with sr.Microphone() as mic:
            print("Ouvindo...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio, language='pt')
            text = text.lower()

            print(f"Entendi: {text}")

            # Assistente envia uma requisição para o modelo treinado.
            assistente.request(text)

    except sr.UnknownValueError():
        recognizer = sr.Recognizer()
        speaker.say("Eu não entendi, pode repetir?")
        speaker.runAndWait()