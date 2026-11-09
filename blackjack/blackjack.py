import random
import time

# 3 extra 10 cards to represent face cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,]

# saving + loading functions
def load_balance():
    try:
        with open("blackjack_save.txt", "r") as file:
            return int(file.read())
    except (ValueError, FileNotFoundError):
        return 100

def save_balance():
    try:
        with open("blackjack_save.txt", "w") as file:
            file.write(str(balance))
    except FileNotFoundError:
        print("file not found")

    
def hand_total(cards):
    aces = 0
    total = 0
    for value in cards:
        total = total + value
        # since aces can either be 1 or 11 ive written the function to be able to determine when an ace that is 11 should turn into a 1 when the total hand value is >21
        if value == 11:
            aces = aces + 1
    while total > 21 and aces > 0:
        total = total - 10
        aces = aces - 1
    return total
# two inputs: hand_type to specify either the dealer or players deck, and owner to print both "your hand" and "dealer's hand" in one function
def hand_reveal(hand_type, owner):
    print(owner + " hand:\n" + str(hand_type))
    time.sleep(1)
    print("total: " + str(hand_total(hand_type)))

#SETUP
balance = load_balance()
# balance and wagers, game will run until balance is <= 0
while True:
    while balance > 0:
        try:
            bet = int(input(f"balance: {balance}\nhow much money are you betting?: "))
            if bet < 0:
                print("invalid bet amount")
            elif bet > balance:
                print("insufficient balance")
                change_mind = input("bet your whole balance instead?: ")
                if change_mind == "y" or change_mind == "yes":
                    bet = balance
                else:
                    continue

        except ValueError:
            print("not a number")
            time.sleep(1)
            continue


        # round start: starting hand is printed   
        player_hand = [random.choice(deck), random.choice(deck)]
        hand_reveal(player_hand, "your")

        while hand_total(player_hand) < 21:
            #user input
            move = input("hit or stand?: ")
            move = move.lower()
            if move == "hit":
                player_hand.append(random.choice(deck))
                hand_reveal(player_hand, "your")
            else:
                break
        if hand_total(player_hand) > 21:
            print("bust")
            outcome = "lose"
        else:
            # showdown
            dealer_hand = [random.choice(deck), random.choice(deck)]
            hand_reveal(dealer_hand, "dealer's")
            # dealer hits until total is greater or equal to 17
            while hand_total(dealer_hand) < 17:
                dealer_hand.append(random.choice(deck))
                hand_reveal(dealer_hand, "dealer's")

            if hand_total(dealer_hand) <= 21 and hand_total(dealer_hand) > hand_total(player_hand):
                print("lose, dealer had a higher hand")
                outcome = "lose"
            elif hand_total(dealer_hand) == hand_total(player_hand):
                print("draw, same hand")
                continue
            elif hand_total(dealer_hand) >21:
                print("win, dealer bust")
                outcome = "win"
            else:
                print("win, highest hand")
                outcome = "win"
        
        if outcome == "win":
            balance += bet
            save_balance()
        else:
            balance -= bet
            save_balance() 
    time.sleep(1)
    print(f"balance: {balance}")
    time.sleep(1)
    print("your pockets are empty..")
    time.sleep(1)
    print("starting over..")
    time.sleep(1)
    balance = 75
    continue


# restart = input("restart run?: ")