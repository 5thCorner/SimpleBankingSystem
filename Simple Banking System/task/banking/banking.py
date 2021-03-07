import random
import sqlite3


def create_base():
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute("DROP TABLE IF EXISTS card")
    curr.execute('CREATE TABLE card (id INTEGER DEFAULT 0, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
    conn.commit()
    conn.close()


def add_to_base(card_number, pin_code, balance):
    global id
    id += 1
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (id, card_number, pin_code, balance))
    conn.commit()
    conn.close()


def check_base(card_number, pin_code):
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM card WHERE number = ? AND pin = ?', (card_number, pin_code))
    if curr.fetchone():
        conn.close()
        return True
    else:
        conn.close()
        return False


def check_number_on_base(card_number):
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM card WHERE number = ?', (card_number,))
    if curr.fetchone():
        conn.close()
        return True
    else:
        conn.close()
        return False


def check_balance(card_number):
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute('SELECT balance FROM card WHERE number = ?', (card_number,))
    res = curr.fetchone()
    conn.commit()
    conn.close()
    return res


def change_balance(card_number, balance):
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute('UPDATE card SET balance = ? WHERE number = ?', (balance, card_number))
    conn.commit()
    conn.close()


def delete_card(card_number):
    conn = sqlite3.connect('card.s3db')
    curr = conn.cursor()
    curr.execute('DELETE FROM card WHERE number = ?', (card_number,))
    conn.commit()
    conn.close()


def create_account():
    customer_account_number = create_account_number()
    card_number = str(customer_account_number)
    pin_code = create_pin()
    add_to_base(card_number, pin_code, 0)
    print('\n' + 'Your card has been created')
    print('Your card number:' + '\n' + card_number)
    print('Your card PIN:' + '\n' + str(pin_code) + '\n')
    start()


def create_account_number():
    acc_num = ''
    for i in range(9):
        rand = random.randint(0, 9)
        acc_num = acc_num + str(rand)
    return luhn('400000' + acc_num)


def create_pin():
    pin = ''
    for i in range(4):
        pin = pin + str(random.randint(0, 9))
    return str(pin)


def check_account():
    print()
    number = input('Enter your card number:' + '\n')
    pin = input('Enter your PIN:' + '\n')
    chb = check_base(number, pin)
    if not chb:
        print('\n' + 'Wrong card number or PIN!' + '\n')
        start()
    else:
        print('\n' + 'You have successfully logged in!' + '\n')
        change_function(number)


def change_function(number):
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
    print('0. Exit')
    num = int(input())
    if num == 1:
        balance = check_balance(number)
        print('\n' + 'Balance: ' + str(balance[0]) + '\n')
        change_function(number)
    elif num == 2:
        print()
        inc = int(input('Enter income:' + '\n'))
        balance = inc + int(check_balance(number)[0])
        change_balance(number, balance)
        print('Income was added! ' + '\n')
        change_function(number)
    elif num == 3:
        print('\n' + 'Transfer')
        transfer = input('Enter card number:' + '\n')
        if transfer != luhn(transfer[0:-1]):
            print('Probably you made a mistake in the card number. Please try again!' + '\n')
            change_function(number)
        elif transfer == number:
            print("You can't transfer money to the same account!" + '\n')
            change_function(number)
        elif not check_number_on_base(transfer):
            print('Such a card does not exist.' + '\n')
            change_function(number)
        else:
            mtt = int(input('Enter how much money you want to transfer:' + '\n'))
            bal = int(check_balance(number)[0])
            if mtt > bal:
                print('Not enough money!' + '\n')
                change_function(number)
            else:
                print('Success!' + '\n')
                change_balance(number, bal - mtt)
                change_balance(transfer, mtt)
                change_function(number)
    elif num == 4:
        delete_card(number)
        print('\n' + 'The account has been closed!' + '\n')
        start()
    elif num == 5:
        print('\n' + 'You have successfully logged out!' + '\n')
        start()
    elif num == 0:
        print()
        print('Bye!')
        quit()


def start():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    num = int(input())
    if num == 0:
        print('\n' + 'Bye!')
        quit()
    elif num == 1:
        create_account()
    elif num == 2:
        check_account()


def luhn(line):
    res = []
    for i in range(0, 15, 2):
        if (int(line[i]) * 2) > 9:
            res.append((int(line[i]) * 2) - 9)
            if i != 14:
                res.append(int(line[i + 1]))
            continue
        else:
            res.append(int(line[i]) * 2)
            if i != 14:
                res.append((int(line[i + 1])))
            continue
    check_sum = 0
    for j in range(10):
        if (sum(res) + check_sum) % 10 == 0:
            break
        else:
            check_sum += 1
            continue
    return line + str(check_sum)


id = 0
create_base()
start()
