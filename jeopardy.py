#! python3
import json
import requests
from titlecase import titlecase

url = 'http://jservice.io/api/random'

# play = 'y'
money = 0

gametype = input(
    'Enter game type\na - Blitz (5 questions)\nb - Standard (10 questions)\nc - Marathon (20 questions)\n').lower()

if gametype == 'b':
    questions_left = 10
elif gametype == 'c':
    questions_left = 20
else:
    questions_left = 5

while questions_left > 0:
    response = requests.get(url)
    response.raise_for_status()

    question = json.loads(response.text)

    answer = question[0]['answer'].replace('\\', '')
    clue = question[0]['question']
    title = titlecase(question[0]['category']['title'])
    value = question[0]['value']

    if clue == '':
        response = requests.get(url)
        response.raise_for_status()

        question = json.loads(response.text)

        answer = question[0]['answer'].replace('\\', '')
        clue = question[0]['question']
        title = titlecase(question[0]['category']['title'])
        value = question[0]['value']

    print('\n')

    if value == None:
        print('***Daily Double***')
        print(f'Category: {title}')
        if money >= 1000:
            value = int(input(f'Place your wager (Max wager is ${money}): '))
            if value > money:
                value = money
        else:
            value = int(input(f'Place your wager (Max wager is $1000):'))
            if value > 1000:
                value = 1000

        print(f'Clue: {clue}')
    else:
        print(f'Category: {title} - ${value}')
        print(f'Clue: {clue}')

    guess = input("Enter your guess: ")

    if (guess.lower() in answer.lower() and len(guess)/len(answer) >= .4):
        print(f'Answer: {answer} - You are correct')
        if value != None:
            money += value
    else:
        print(f'I\'m sorry, the correct answer is: {answer}')
        if value != None:
            money -= value

    questions_left -= 1

    if questions_left == 0:
        print(f'Game Over. You have finished with ${money}')
    else:
        print(f'You have ${money}')
        print(f'{questions_left} question(s) remaining')
