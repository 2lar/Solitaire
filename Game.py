# Solitaire: Scorpion
#Lawrence Kim
#
#Program is Solitaire: Scorpion game
# but a little more simplifie


import cards, random
random.seed(100) #random number generator will always generate 
                 #the same random number (needed to replicate tests)

MENU = '''     
Input options:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau (column,row) to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def initialize():
    '''That function has no parameters. It creates and initializes the stock, tableau, and foundation, and
then returns them as a tuple, in that order.The deck is shuffled and becomes the initial stock (pile of cards). Forty-nine cards are then
dealt from the stock, left to right, one to each column of a seven-column tableau, and then to
successive rows in the columns'''
    foundation,tableau = [[],[],[],[]],[[],[],[],[],[],[],[]]
    stock = cards.Deck()
    stock.shuffle()
    while len(tableau[6]) != 7:
        for lst in tableau:
            card = stock.deal()
            lst.append(card)
    for lst in tableau[:3]:
        for card in lst[:3]:
            card.flip_card()    
    return stock,tableau,foundation

def display(stock, tableau, foundation):
    '''Display the stock and foundation at the top.
       Display the tableau below.'''
       
    print("\n{:<8s}{:s}".format( "stock", "foundation"))
    if stock.is_empty():
        print("{}{}".format( " ", " "),end='') # fill space where stock would be so foundation gets printed in the right place
    else:
        print("{}{}".format( " X", "X"),end='')  # print as if face-down
    for f in foundation:
        if f:
            print(f[0],end=' ')  # print first card in stack(list) on foundation
        else:
            print("{}{}".format( " ", " "),end='') # fill space where card would be so foundation gets printed in the right place
            
    print()
    print("\ntableau")
    print("   ",end=' ')
    for i in range(1,8):
        print("{:>2d} ".format(i),end=' ')
    print()
    # determine the number of rows in the longest column        
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row+1),end=' ')
        for col in range(7):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row],end=' ')
            else:
                print("   ",end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau
    
def deal_from_stock(stock,tableau):
    '''It will deal a card from the stock to the leftmost three columns of the
tableau. It will always deal three cards. If the stock is empty, do not deal any cards to the
tableau'''
    if stock.is_empty() == False:
        while len(stock) != 0:
            for lst in tableau[:3]:
                card = stock.deal()
                lst.append(card)
        
def validate_move(tableau,src_col,src_row,dst_col):
    '''The function will return True, if the move is valid; and False, otherwise.'''
    try:
        source = tableau[src_col][src_row]
        srank,ssuit = source.rank(),source.suit()
        if len(tableau[dst_col]) == 0:
            if srank == 13:
                return True
            else:
                return False
        acard = tableau[dst_col][-1]
        arank,asuit = acard.rank(),acard.suit()
        if ssuit != asuit or srank+1 != arank:
            return False
        else:
            return True
    except:
        False
    
def move(tableau,src_col,src_row,dst_col):
    '''If the move is valid (determined by calling
validate_move), the function will update the tableau; otherwise, it will do nothing to it
    it will also flip cards if last card in column becomes an unfaced card'''
    if validate_move(tableau, src_col, src_row, dst_col) == True:
        #need the True, if validated, then goes on to move the cards
        sourcepart = tableau[src_col][src_row:]
        dst = tableau[dst_col]
        dst.extend(sourcepart)
        # for i in sourcepart: #I had remove and .pop. .pop was just most recen
        # but they both work the same way
        #     tableau[src_col].remove(i)
        for i in range(len(sourcepart)):
            tableau[src_col].pop()
        if len(tableau[src_col]) != 0:
           if tableau[src_col][-1].is_face_up() == False: 
               tableau[src_col][-1].flip_card()
        return True
    else:
        return False

def check_sequence(column_lst):
    '''The program will use the following function to check if a column in the tableau is a complete
sequence from king down to ace of the same suit:'''
    if len(column_lst) != 13: #no way less than 13 is a full list for foundation
        return False
    suitc,rankc = column_lst[0].suit(),column_lst[0].rank()
    for card in column_lst[1:]: #start from one otherwise the +1 wont work
        suit,rank = card.suit(),card.rank()
        if suit != suitc or rank+1 != rankc: # +1 to check if its 1 apart
            return False
        rankc,suitc = rank,suit
    return True
    
def move_to_foundation(tableau,foundation):
    '''Fill the foundation from left to right; one complete sequence to each foundation slot'''
    for lst in tableau:
        if check_sequence(lst) == True:
            for lst1 in foundation:
                if len(lst1)==0:
                    lst1.extend(lst) #extend, so that it aint a list in a list of a list
                    lst.clear()                  
                    
def check_for_win(foundation):
    '''That function checks to see if the foundation is full. It returns True, if the foundation is full and
False, otherwise.'''
    for lst in foundation:
        if len(lst) != 13:
            return False
    return True

def get_option():
    '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau column,row to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
    '''
    option = input( "Input an option (DMRHQ): " )
    option_list = option.strip().split()
    
    opt_char = option_list[0].upper()
    
    if opt_char in 'DRHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 4 and option_list[1].isdigit() \
        and option_list[2].isdigit() and option_list[3].isdigit():
        return ['M',int(option_list[1]),int(option_list[2]),int(option_list[3])]

    print("Error in option:", option)
    return None   # none of the above
 
def main():
    '''Docstring'''
    
    print("\nWelcome to Scorpion Solitaire.\n")
    stock, tableau, foundation = initialize()
    display(stock, tableau, foundation)
    print(MENU)
    option_lst = get_option()
    while option_lst and option_lst[0] != 'Q':
        if option_lst[0] == "D":
            deal_from_stock(stock, tableau)
            display(stock, tableau, foundation) 
        if option_lst[0] == "M":
            src_col=option_lst[1]-1 #subtract one so that it fits indexing
            src_row=option_lst[2]-1
            dst_col=option_lst[3]-1
            if validate_move(tableau, src_col, src_row, dst_col) == True:
            # this part of validate_move is excessive because move has it in there
            # but I wrote this before getting the move function down completely
            # and I prefer not to fix that part up
                move(tableau, src_col, src_row, dst_col)
                for lstt in tableau:
                    if check_sequence(lstt) == True:
                        move_to_foundation(tableau, foundation)
                if check_for_win(foundation) == True:
                # if else here so that the display doesnt happen twice 
                # when the game is won
                    print("You won!")
                    print("\nNew Game.")
                    stock, tableau, foundation = initialize()
                    display(stock, tableau, foundation)
                    print(MENU)
                else:
                    display(stock, tableau, foundation)
            else:
                # didnt see the else error down below, but this one works for me
                # I know I dont need the .format, but it seems more right to me eyes
                print('Error in move: {} , {} , {} , {}'.format(option_lst[0],option_lst[1],option_lst[2],option_lst[3]))
        if option_lst[0] == "R":
            stock, tableau, foundation = initialize()
            display(stock, tableau, foundation)
            print(MENU)
        if option_lst[0] == "H":
            print(MENU)

        # YOUR CODE HERE # oops
#            else: # move failed
#                print("Error in move:",option,",",option_lst[1],",",option_lst[2],",",option_lst[3])
        option_lst = get_option()
    
    print("Thank you for playing.")
if __name__ == '__main__':
    main()
