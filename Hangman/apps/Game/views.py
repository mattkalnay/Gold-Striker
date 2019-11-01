from django.shortcuts import render, redirect
from .forms import GuessForm, LoadingForm
from django.contrib import messages
import requests
import random
from PyDictionary import PyDictionary

dictionary = PyDictionary()

def begin(request):
    # grab difficulty from POST
    adversity = request.POST['difficulty']
    request.session['points'] = 0
    # change level and point total based on difficulty
    if adversity == 'easy':
        level = random.randint(1,3)
        request.session['points'] += 1000
    elif adversity == 'medium':
        level = random.randint(4,6)
        request.session['points'] += 2000
    elif adversity == 'hard':
        level = random.randint(7,8)
        request.session['points'] += 3000
    elif adversity == 'crazy':
        level = random.randint(9,10)
        request.session['points'] += 4000
    print(level)
    # randomize starting word
    start = random.randint(1, 17091)
    print(start)

    # use random start and level to make API call for the word
    url = "http://app.linkedin-reach.io/words?start={0}&count=1&difficulty={1}".format(start, level)
    response = requests.get(url).text

    # create session for wagers, word, mysteryword, guessed, lost, and key
    request.session['wager'] = [request.POST['a'], request.POST['b'], request.POST['c'], request.POST['d'], request.POST['e'], request.POST['f']]
    print(request.session['wager'])
    request.session['word'] = response
    request.session['guessed'] = {}
    request.session['lost'] = []
    request.session['key'] = False
    print(request.session['word'])

    return redirect('/game')


def index(request):
    # reset mysteryword
    mysteryword = []
    # if list of incorrect is 6, redirect to gameover 
    if len(request.session['lost']) == 6:
        request.session['key'] = True
        print('Game Over')
        return redirect('/gameover')
    else: 
        # loop through the word
        for i in request.session['word']:
            # if the letter in the word is a part of the guessed dictionary
            if i in request.session['guessed']:
                mysteryword.append(i)
            # if the letter in the word is NOT a part of the guessed dictionary
            else:
                mysteryword.append('_')

    # if puzzle is solved, then redirect to gameover
    joined = ''.join(mysteryword)
    # save modifications to session
    request.session.modified = True
    if joined == request.session['word']:
        print("game over")
        print(joined)
        request.session['key'] = True
        return redirect('/gameover')
    # send info from view to template
    form = GuessForm()
    context = {'word' : request.session['word'],
    'leng' : len(request.session['word']),
    'guessed' : request.session['guessed'],
    'mysteryword' : mysteryword,
    'guessForm' : form,
    'lost' : request.session['lost'],
    'wagers' : request.session['wager'],
    'score' : request.session['points']}

    return render(request, 'Game/index.html', context)

def guess(request):
    # create lowercase letter
    letter = str(request.POST['letter']).lower()
    # bind for form for validations
    bound_form = GuessForm(request.POST)
    if bound_form.is_valid() == False:
        print(bound_form.errors) 
        messages.error(request, 'Guess Must Be a Letter Between A-Z')
        return redirect('/game')
    else:
        # if the letter has already been guessed
        if letter in request.session['guessed']:
            messages.error(request, 'Guess a New Letter')
            return redirect('/game')
        
        request.session['guessed'][letter] = 1
        request.session.modified = True

        print(request.session['guessed'])

        match = False
        for k in request.session['word']:
            if k == str(request.POST['letter']).lower():
                match = True
                break
        if match == False:
            # pick a random number between 0 and the length of the wager list
            destroy = random.randint(0,len(request.session['wager']) - 1)
            print(len(request.session['wager']) - 1)
            # subtract the amount of points from lost wager
            request.session['points'] = (request.session['points'] - int(request.session['wager'][destroy]))
            # add wager to lost list
            request.session['lost'].append(request.session['wager'][destroy])
            # remove wager from wager list
            request.session['wager'].remove(request.session['wager'][destroy])
            print(request.session['wager'])
        return redirect('/game')



def reset(request):
    return redirect('/')


def gameover(request):
    # make sure the person has finished the puzzle
    if request.session['key'] == False:
        return redirect('/')
    else:
        # find information on the word
        word = request.session['word']
        info = dictionary.meaning("{0}".format(word))
        definition = "Not found"
        # if no information can be found
        if(info != None):
            info = dictionary.meaning("{0}".format(word))
            definition = info.values()[0]
        print(info)
        context = {'word' : request.session['word'],
        'leng' : len(request.session['word']),
        'guessed' : request.session['guessed'],
        'wagers' : request.session['wager'],
        'score' : request.session['points'],
        'information' : info,
        'lost' : request.session['lost'],
        'definition' : definition
        }
        return render(request, 'Game/gameover.html', context)

def loading(request):
    # provide the form for the template
    form = LoadingForm()
    context = {'loadingForm' : form}
    return render(request, 'Game/loading.html', context)
