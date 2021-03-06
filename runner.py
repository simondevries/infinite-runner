"""
INFINITE RUNNER
6.177 Project (IAP 2016)
Completed by:
    Claire Nord   (cnord@mit.edu)
    Shavina Chau  (shavinac@mit.edu)
    Janelle Sands (jcsands@mit.edu)
    Michelle Chen (mxchen@mit.edu)
"""

import pygame, sys
import random
from example_menu import main as menu
from losers_menu import main as losers_menu

### Global Variables
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square
NUM_ROWS = 8 #number of rows
NUM_COLS = 4 #number of columns

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return rowNum * height + 10

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return colNum * width + 10

def update_text(screen, messages): 
    """
    Used to display the text on the right-hand part of the screen.
    Takes in a list of strings called messages and displays each one on the next line.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)

    #use a rectangle to cover up old text
    pygame.draw.rect(screen,black,[310,0,200,620],0)

    #loop through each of the strings in the list to print them on the side panel
    Y_increment=0
    for message in messages:
        textY=textSize+Y_increment
        text=font.render(message, True, white, black)
        textRect = text.get_rect()
        textRect.centerx = (NUM_COLS + 1) * WIDTH + 30
        textRect.centery = textY
        screen.blit(text, textRect)
        Y_increment+=textSize
       
def new_game():
    """
    Sets up all necessary components to start a new game.
    """
    pygame.init() # initialize all imported pygame modules

    window_size = [ NUM_COLS * WIDTH + 200, NUM_ROWS * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Infinite Runner") # caption sets title of Window 

    board = Board()

    moveCount = 0

    clock = pygame.time.Clock()
    #Menu function
    result = menu(screen)
    if result == 0: #THIS MEANS USER SELECTED START GAME
        main_loop(screen, board, moveCount, clock, False, False)
    elif result == 1: #USER SELECTED LOAD GAME
        print "you can't load games -- yet!"
    elif result == 2: #USER SELETED OPTIONS
        print "you have no options -- yet!"

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    board.thePlayer.draw(screen) # draw player Sprite
    board.theItems.draw(screen)
    pygame.display.flip() # update screen

   
    #how to quit the game
    if stop == True:
        again = raw_input("Would you like to play again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()

    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
                sys.exit()
            #how to pause the game, move player right, and move player left
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                        board.player.move_right()
                        board.squares.draw(screen)
                        board.theItems.draw(screen)
                        board.thePlayer.draw(screen)
                        pygame.display.flip()
                elif event.key == pygame.K_LEFT:
                        board.player.move_left()
                        board.squares.draw(screen)
                        board.theItems.draw(screen)
                        board.thePlayer.draw(screen)
                        pygame.display.flip()
                elif event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True
        
        if stop == False and pause == False and board.player.health>0: 
            board.squares.draw(screen) # draw Sprites (Squares)
            board.thePlayer.draw(screen) # draw player Sprite
            board.theItems.draw(screen)
            update_text(screen, ["Meters traveled: ",
                str(int(moveCount/10)), 
                "",
                "Health: " + str(board.player.health),
                "",
                "",
                "INSTRUCTIONS:",
                "You have found free food.",
                "Now you must navigate",
                "through the Infinite",
                "to bring food and glory",
                "back to your dorm wing.",
                "",
                "Move your player",
                "using left/right arrow keys.",
                "Avoid collisions",
                "with MIT tourists.",
                "Such collisions will",
                "decrease your health.",
                "Collect more free food",
                "to increase health.",
                "You will infinitely continue",
                "through the Infinite",
                "unless you lose all health,",
                "and you fall over from",
                "extreme hunger and shame.",
                "Go as far as you can!",
                "(you can pause with 'p')"])
            pygame.display.flip() # update screen
            clock.tick(10)
            moveCount += 1

            #increase the speed of the game as it progresses
            modulo=5
            if moveCount>500: 
                modulo=4
            if moveCount>1000:
                modulo=3
            if moveCount>1500:
                modulo=2

    
            if moveCount % modulo == 0: #actually moving things down
                board.update_board(moveCount) #will progress everything 1 row down
                board.squares.draw(screen) # draw Sprites (Squares)
                board.thePlayer.draw(screen) # draw player Sprite
                board.theItems.draw(screen)
                pygame.display.flip()

        #The menu that pops up when the player loses
        if board.player.health<=0:
            result = losers_menu(screen)
            pygame.display.flip()
            if result == 0: #THIS MEANS USER SELECTED YOU LOSE
                print ":("
            elif result == 1: #USER SELECTED NEW GAME
                board = Board()
                moveCount = 0
                main_loop(screen, board, moveCount, clock, False, False) # call a new game
            elif result == 2: #USER SELETED OPTIONS
                print "you have no options -- yet!"       
    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                          # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = color   

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect

    def get_location(self):
        """
        Returns the location of the Square
        """
        return [self.row, self.col]
   
class Board(object):
    def __init__(self):
        self.rows = NUM_ROWS
        self.cols = NUM_COLS
        self.items = [] #a list of every food and obstacle object
                        #new items created (at the top) will be appended
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        self.checkedLocations=[] # this is used for the path search to store the coordinates that have already been checked
        
        #---Populate boardSquares with Squares---#
        for i in range(self.rows): #rows in 2d array
            col = []
            for j in range(self.cols): #cols #j=col, i=row
                s = Square(i,j,white)
                col.append(s)
                self.squares.add(s)
            self.boardSquares.append(col)
            
        #---Initialize the Player---#
        self.player = Player(self,1) #board, col=1, row=bottom row (default value)

        #---Adds Player to the "thePlayer" Sprite List---#
        self.thePlayer = pygame.sprite.RenderPlain()
        self.thePlayer.add(self.player)
        
        self.theItems = pygame.sprite.RenderPlain()
        #Sprite group for items
    
    def new_food(self, col, nutrients=1):
        """
        Will create a Food object at the location (row=0, col)
        """
        self.boardSquares[0][col] = Food(self,col, nutrients)
        # ITEM WILL BE ADDED TO THE LISTS IN THE UPDATE_BOARD METHOD
        return self.boardSquares[0][col]
        #nutrients = how much it heals
    
    def new_obstacle(self, col, power=1):
        """
        Will create an Obstacle object at the location (row, col)
        """
        self.boardSquares[0][col] = Obstacle(self, col, power)
        # ITEM WILL BE ADDED TO THE LISTS IN THE UPDATE_BOARD METHOD
        return self.boardSquares[0][col]
        #power = how much damage it deals
            
    def update_board(self, moveCount):
        """
        Will call move_down on every square in the grid
        """
        new_items = []
        self.theItems = pygame.sprite.RenderPlain()
        for item in self.items: #items = list of obstacles and food
            if(item.move_down(self.player)):
                #if move_down returns true, it has moved and stays on the board
                new_items.append(item)
                self.theItems.add(item)

        self.items = new_items
        
        #Updating the boardSquares array
        self.boardSquares = []
        
        for i in range(self.rows): #rows in 2d array
            col = []
            for j in range(self.cols): #cols #j=col, i=row
                s = Square(i,j,white)
                col.append(s)
            self.boardSquares.append(col)
        
        #Adding the self.items list into the boardSquares array
        for k in self.items:
            location = k.get_location() #returns a list
            self.boardSquares[location[0]][location[1]] = k
        #Now everything has been moved down, leaving first row empty
        
        #increases difficulty as time passes by changing probabilities 
        probability_list=[.3, .05]
        if moveCount>1000:
            probability_list=[.32,.015]
        if moveCount>2000:
            probability_list=[.34,.013]
        if moveCount>4000:
            probability_list=[.35,.011]
        if moveCount>7000:
            probability_list=[.35,.005]
        if moveCount>10000:
            probability_list=[.38,.0025]

        #Filling in the now-vacant first row
        for fr_item in self.generate_new_row(probability_list):
            if not isinstance(fr_item, Square):
               self.items.append(fr_item)
               self.theItems.add(fr_item)
               #adds to items list and sprite group
        #gen_new_row takes a probability list as an optional argument
        
        #Refilling the squares ----
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = []
        
        for i in range(self.rows): #rows in 2d array
            col = []
            for j in range(self.cols): #cols #j=col, i=row
                s = Square(i,j,white)
                col.append(s)
                self.squares.add(s)
            self.boardSquares.append(col)
        
        #Adding the self.items list into the boardSquares array
        for k in self.items:
            location = k.get_location() #returns a list
            self.boardSquares[location[0]][location[1]] = k  
                    
    def generate_new_row(self, probability_list):
        """
        Takes in a list of probabilities [% obstacle, % food] and generates
        a row with those probabilities
        Returns a list
        """

        self.checkedLocations=[]
        plausible=False
        #probability_list = percent chance of getting an obstacle, food
        
        #did the user get themselves stuck? if creating a blank row allows no possible paths, then yes
        new_row = [Square(0,c,white) for c in range(4)] #row of squares only ("blank")
        for item in new_row: #updating boardSquares
            self.boardSquares[item.get_location()[0]][item.get_location()[1]] = item
        if not self.path_search(self.player.get_location()): #if no possible paths
            #troll the user if they're an idiot w/commented line below:
            #new_row = [self.new_obstacle(d) for d in range(4)]
            
            new_row = []
            for i in range(4):
                rand_num = random.random()
                if rand_num <= probability_list[0]: #probability of obstacle
                    new_row.append(self.new_obstacle(i))
                elif rand_num <= probability_list[0]+probability_list[1]: #prob of food
                    new_row.append(self.new_food(i))
                else: #prob of neither (blank square)
                    new_row.append(Square(0, i, white))
            
            plausible = True
        
        #if the player is not an idiot:
        while plausible==False: # generates a new row as long as there as is not a plausible row
            new_row = []
            for i in range(4):
                rand_num = random.random()
                if rand_num <= probability_list[0]: #probability of obstacle
                    new_row.append(self.new_obstacle(i))
                elif rand_num <= probability_list[0]+probability_list[1]: #prob of food
                    new_row.append(self.new_food(i))
                else: #prob of neither (blank square)
                    new_row.append(Square(0, i, white))
            for item in new_row: #filling the boardSquares array with the newly created row
                self.boardSquares[item.get_location()[0]][item.get_location()[1]] = item
            
            self.checkedLocations = []
            plausible = self.path_search(self.player.get_location()) # changes plausible to true to exit loop only if a path is possible with new row
        return new_row

    def get_neighbors(self, location):
        """
        From the complete boardSquares 2D array and a location (a list), this method will return a list of the coordinates in front of and to the left and right sides of the location if any only if they are not obstacles.
        """

        row = location[0]
        col = location[1]
        neighbors = []
        if row>0: #check if you can actually go up (not in top row)
            front = self.boardSquares[row-1][col]
            if not isinstance(front, Obstacle): #check if front is clear
                neighbors.append(front)
                
        if col>0: #check if you can actually go left (not in leftmost column)
            left = self.boardSquares[row][col-1]
            if not isinstance(left, Obstacle): #check if left is clear
                neighbors.append(left)

        if col<3: #check if you can actually go right (not in rightmost column)
            right = self.boardSquares[row][col+1]
            if not isinstance(right, Obstacle): #check if right is clear
                neighbors.append(right)

        return neighbors


    def path_search(self, location):
        """
        Return true if there is a path that can be made from the player's current location to the top of the board.  Returns false if there is no path.
        Uses recursive depth-first search (DFS).
        There's no default argument taken, so the first time you call if you have to pass in self.player.get_location()
        """
        #adds checked items to a list to avoid double checking same location
        self.checkedLocations.append(location)

        neighbors = self.get_neighbors(location)
        if len(neighbors) == 0: #end case
            return False
        for item in neighbors:
            if item.get_location()[0] == 0: #if it's in the top row
                return True # you made it! end case
            else:
                #neighbors.extend(self.get_neighbors(neighbors[0].get_location()))
                #del neighbors[0]
                if not (item.get_location() in self.checkedLocations):
                    if self.path_search(item.get_location()):
                        return True
        return False

class Player(pygame.sprite.Sprite):
    def __init__(self, board, col, row=NUM_ROWS-1):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        self.health=5
   
    def get_location(self):
        """
        Returns a list (rows,cols) of the player's location
        """

        return [self.row, self.col]
        
    def move_left(self):
        """
        Moves the player one column to the left 
        If the Player is at an edge, the Player will not move off-screen or wrap around.
        """
        if self.col>0: #not in the leftmost column
            self.col -= 1
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

        self.has_collided()

    def move_right(self):
        """
        Moves the player one column to the right
        If the Player is at an edge, the Player will not move off-screen or wrap around.
        """
        if self.col<3: #not in rightmost column
            self.col += 1
    
        #actually changes player's location
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        
        self.has_collided()

    def modify_health(self,potency):
        #Increase/decrease the health of the Player by the amount of potency of the object it collides with
        self.health += potency
        
    def has_collided(self):
        grid = self.board.boardSquares #2D array of items
        if not isinstance(grid[self.row][self.col], Square): #NOT a square i.e. an obstacle or food
            self.modify_health(grid[self.row][self.col].get_potency())
            
            #"remove" the obstacle/food and replace with a square
            self.board.boardSquares[self.row][self.col] = Square(self.row,self.col, white)

class Item(pygame.sprite.Sprite):
    def __init__(self, board, col, row=0):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.board = board
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
        self.potency = 1

    def get_location(self):
    	#note: using this for modify_health method in Player class
        return [self.row, self.col] #returns the coordinates of the item in a list, e.g. [0, 1]

    def get_potency(self): #returns the item potency for the modify_health method in Player class
    	return self.potency 

    def move_down(self, player):
        if self.get_location() == player.get_location():
            player.modify_health(self.potency)
            return False #rather than actually removing the item, it just won't be drawn in the update method
        if self.get_location()[0] >= NUM_ROWS-1: #if in row 7, remove
            return False #rather than actually removing the item, it just won't be drawn in the update method
        else:
            self.row += 1
            self.rect.y = get_row_top_loc(self.row)
            return True
    
class Obstacle(Item):
    def __init__(self, board, col, power):
        self.image = pygame.image.load("img/tourist" + str(random.randint(1,2)) + ".png").convert_alpha()
        super(Obstacle, self).__init__(board, col)
        self.power = power
        self.potency = power * -1

class Food (Item):
    def __init__ (self, board, col, nutrients):
        self.image = pygame.image.load("img/food" + str(random.randint(1,7)) + ".png").convert_alpha()
        super(Food, self).__init__(board, col)
        self.potency = nutrients
        
    def effect(self):
        #will apply the effect of the powerup on the game
        pass

if __name__ == "__main__":
    # Uncomment this line to call new_game when this file is run:
    new_game()
    pass
