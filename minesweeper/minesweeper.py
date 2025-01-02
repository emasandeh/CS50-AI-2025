import itertools
import random
import copy as cp


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):

        if self.count == len(self.cells) :

            stc=cp.deepcopy(self.cells)
            return stc
        
        else:
            return set()

    def known_safes(self):

        if self.count == 0 :

            stc=cp.deepcopy(self.cells)
            return stc
        
        else:
            return set()

    def mark_mine(self, cell):

        if cell in self.cells:

            self.cells.remove(cell)  
            self.count-=1    
            cell = Sentence(cell,1)
        

    def mark_safe(self, cell):
        
        if cell in self.cells:

            self.cells.remove(cell)     
            cell = Sentence(cell,0)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)

        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)

        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):

        self.moves_made.add(cell)   #1

        self.mark_safe(cell)        #2

        st = set()

        for i in range(cell[0] - 1, cell[0] + 2):           #3
            for j in range(cell[1] - 1, cell[1] + 2):
                 
                 if (i, j) == cell:

                    continue
                 
                 if 0<=i<self.height and 0<=j<self.width and not (i,j) in self.safes and not (i,j) in self.mines :

                    st.add((i,j))
        
        if len(st)>0 : self.knowledge.append(Sentence(st,count))    
            
        for sentence in self.knowledge :     #4

            if len(sentence.known_safes()) > 0 :

                for cls in sentence.known_safes() : #RuntimeError: Set changed size during iteration à régler
                    self.mark_safe(cls)


            if len(sentence.known_mines()) > 0 :

                for cls in sentence.known_mines() :
                    self.mark_mine(cls)


        for i in range(len(self.knowledge)) :  #5
            for j in range(len(self.knowledge)) :

                if self.knowledge[i] == self.knowledge[j] :

                    continue 

                if self.knowledge[i].cells.issubset(self.knowledge[j].cells) :

                    stbis=Sentence(set([elt for elt in self.knowledge[j].cells if not elt in self.knowledge[i].cells]),self.knowledge[j].count-self.knowledge[i].count)
                    
                    if not stbis in self.knowledge :

                        self.knowledge.append(stbis)
                    
        
        #5 parcour knowledge et cherche si y a pas des cells presentes dans deux meme phrases et en déduit une autre


        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """ 
        
        

    def make_safe_move(self):

        for elt in self.safes:
            if not elt in self.moves_made:
                return elt
        return None

        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """


    def make_random_move(self):
        
        for i in range(self.height):
            for j in range(self.width):
                if not (i,j) in self.mines and not (i,j) in self.moves_made:
                    return (i,j)
        return None
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """



