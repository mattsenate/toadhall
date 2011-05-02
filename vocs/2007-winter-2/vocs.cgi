#!/usr/bin/env python

from utils import *
from fastcgi import form
import time, os

members = ['1A Gaby', '1B Adrienne', '1C Nick', '1D Dianna', '1E Eric',
           '1F Andrea', '1F Thea', '1G Willy', '1G Barish',
           '1H Max', '1H Andy',
           '2A Madelyn', '2A Justyna', '2B Navek', '2B Aaron',
           '2C Lisa', '2C Tram', '2D Maya', '2D Claire',
           '2E Caitlyn', '2E Brian', '2E Beaver',
           '2F Daphne', '2G Daisy', '2H Jordan', '2I Kye', '2I Marissa',
           '2J Sarah', '2J David', '2K Elliot', '2K Griffin',
           '2L Phil', '2L Rohit',
           '3A Kate', '3B Rachel', '3B Christina', '3C Yana', '3C Adriana',
           '3D Jonathan', '3D Nate', '3E Athena', '3E Kristina',
           '3F Meaghan', '3F Jenny', '3G Geoff', '3G Zac',
           '3H Ping', '3I Ryan', '3J Tony', '3J Grace',
           'Boarder Sam', 'Boarder Spencer', 'Boarder Shannon',
           'Boarder Dave', 'Boarder Amy', 'Boarder Sarit', 'Boarder Galen',
           'Boarder Mary', 'Boarder Molly']

managers = [('House Manager', '9/16 rent plus 5 hours/week', 'Tony'),
            ('Kitchen Manager', '100% rent plus 5 hours/week', 'Gaby'),
            ('Workshift Manager', '9/16 rent plus 5 hours/week', 'Madelyn'),
            ('Maintenance Manager', '9/16 rent plus 5 hours/week', 'Beaver'),
            ('Board Representative', '5 hours/week', 'Kate'),
            ('President', '5 hours/week', 'Ping'),
            ('Vice President', '3 hours/week', 'Brian'),
            ('Social Manager', '2.5 hours/week', 'Justyna'),
            ('Social Manager', '2.5 hours/week', 'Adriana'),
            ('Waste Reduction Manager', '5 hours/week', 'Lisa'),
            ('Garden Manager', '5 hours/week', 'Grace'),
            ('Network Manager', '3 hours/week', 'Jonathan')]

disabled = {}
for line in readlines('voc-members.txt'):
    disabled[line.strip()] = 1

x = 0
def memberselect(name):
    global x
    x += 1
    dis = disabled.get(name, None)
    return div(input(type='radio', name='member', value=name, disabled=dis,
                     id='radio-%d' % x, onclick='update(%r)' % x),
               label(name, for_='radio-%d' % x),
               id='namediv-%d' % x, c=dis and 'disabled' or None)

y = 0
def managerform((position, comp, name)):
    global y
    nameid = name.strip().lower().replace(' ', '-').replace('.', '')
    buttons = []
    for option in '80% 90% 100% 110% Abstain'.split():
        val = option.replace('%', '').lower()
        y += 1
        buttons.append(div(input(type='radio', name=nameid + '-vote',
                                 value=val, id='vote-%d' % y),
                           label(option, for_='vote-%d' % y),
                           id='votediv-%d' % y))
    fragment = position.split()[0].lower()
    linkposition = link('duties.html#' + fragment, position)
    form = div(linkposition, ' compensation is ', comp, '.', br,
               strong(name), ' deserves this much of the comp:', buttons, br,
               table(tr(td('Comments:', valign='top'),
                        td(textarea(name=nameid + '-text', rows=5, cols=60))),
                     c='textarea'),
               c='manager', id='manager-%d' % y)
    if name == 'Adriana':
        form = [form, div(table(
            tr(td('Comments for both Social Managers together:', valign='top')),
            tr(td(textarea(name='social-managers-text', rows=5, cols=60))),
            c='textarea'))]
    return form

if form.submit:
    if not form.member:
        prologue('Kingman Hall: Votes of Confidence', 'style.css')
        write("You didn't select your name. Please go back and fill it in.")
        raise SystemExit

    results = '\n'
    for (position, comp, name) in managers:
        nameid = name.strip().lower().replace(' ', '-').replace('.', '')
        votefield = nameid + '-vote'
        textfield = nameid + '-text'
        if form.member != 'comment-only':
            if votefield not in form:
                prologue('Kingman Hall: Votes of Confidence', 'style.css')
                write("You didn't choose a compensation amount for %s (%s). "
                      % (name, position))
                write('Please go back and fill it in.')
                raise SystemExit
            results += votefield + ': ' + form[votefield] + '\n'
        if textfield in form and form[textfield]:
            text = form[textfield].replace('\t', ' ').replace('\r\n', '\n'
                 ).replace('\r', '\n').replace('\n', '\t')
            results += textfield + ': ' + text + '\n'
    textfield = 'social-managers-text'
    if textfield in form and form[textfield]:
        text = form[textfield].replace('\t', ' ').replace('\r\n', '\n'
             ).replace('\r', '\n').replace('\n', '\t')
        results += textfield + ': ' + text + '\n'
        
    file = open('voc-members.txt', 'a')
    file.write(form.member + '\n')
    file.close()
    file = open('voc-results.txt', 'a')
    file.write(results)
    file.close()
    prologue('Kingman Hall: Votes of Confidence', 'style.css')
    write(p, 'Thank you.  Your answers have been recorded.')
    write(p, 'You can only vote once for manager compensation, ',
             'but you can resubmit the form to add more comments if you want.')
else:
    cells = []
    names = members[:]
    while names:
        floor = [name for name in names if name[0] == names[0][0]]
        n = min(11, len(floor))
        cells.append([memberselect(name) for name in names[:n]])
        names[:n] = []
    commentonly = [input(type='radio', name='member', value='comment-only',
                         id='comment-only', onclick='update()'),
                   label("I've already cast my votes ",
                         "and I just want to add some comments.",
                         for_='comment-only')]
    n = len(cells)
    membertable = table(tr(td('Choose your name from this list:', colspan=n)),
                        tr([td(cell) for cell in cells]),
                        tr(td(commentonly, colspan=n)), c='members')
    managerfields = [managerform(manager) for manager in managers]

    prologue('Kingman Hall: Votes of Confidence', 'style.css')
    html = readfile('vocs.html')
    write(subst(html, members=membertable, managers=managerfields))
