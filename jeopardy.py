#! python3
import json
import requests
import csv
from titlecase import titlecase

url = 'http://jservice.io/api/random'


data = open('jeopardy_data.csv', 'r')
reader = csv.reader(data, delimiter=',')
for row in reader:
    saved_money = int(row[0])
    saved_correct = int(row[1])
    saved_questions = int(row[2])

data.close()

money = 0
lowest = 0
highest = 0
correct = 0

gametype = input(
    'Enter game type\na - Blitz (5 questions)\nb - Standard (10 questions)\nc - Marathon (20 questions)\n').lower()

if gametype == 'b':
    questions_left = 10
elif gametype == 'c':
    questions_left = 20
else:
    questions_left = 5

total_questions = questions_left

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

    guess = input('Enter your guess: ')

    if (guess.lower() in answer.lower() and len(guess)/len(answer) >= .4):
        print(f'Answer: {answer} - You are correct')
        if value != None:
            money += value
            correct += 1
    else:
        print(f'I\'m sorry, the correct answer is: {answer}')
        if value != None:
            money -= value

    if (money >= highest):
        highest = money

    if (money <= lowest):
        lowest = money

    questions_left -= 1

    if questions_left == 0:
        print('\n')
        print(f'Game Over. You have finished with ${money}')
        print('\n')
        print('Game Stats')
        print('----------')
        print(f'You answered {correct} out of {total_questions} questions correctly.')
        print(f'Highest money amount: ${highest}.')
        print(f'Lowest money amount: ${lowest}.')

        
        saved_money += money
        saved_correct += correct
        saved_questions += total_questions
        percentage = round((saved_correct/saved_questions) * 100, 0)
        
        print('\n')
        print('All-time Stats')
        print('--------------')
        print(f'You have answered {saved_correct} out of {saved_questions} questions correctly. ({percentage}%)')
        print(f'Total money = ${saved_money}.')

        write_data = open('jeopardy_data.csv', 'w')
        writer = csv.writer(write_data, delimiter=',')
        writer.writerow([saved_money, saved_correct, saved_questions])
        write_data.close()

    else:
        print(f'You have ${money}')
        print(f'{questions_left} question(s) remaining')
