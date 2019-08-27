from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QImage, QPixmap, QColor
from piece import Piece

class Board(QFrame): # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    playersTurnSignal = pyqtSignal(int)
    validMove = pyqtSignal(int)

    # todo set the board with and height in square
    boardWidth  = 8     # board is 0 square wide - this needs updating
    boardHeight = 8     #
    timerSpeed  = 1000     # the timer updates ever 1 second
    counter     = 120    # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer

        # Todo - create a 2d int/Piece array to story the state of the game
        self.boardArray =[
            [11, 12, 13, 14, 15, 13, 12, 11],
            [19, 19, 19, 19, 19, 19, 19, 19],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [29, 29, 29, 29, 29, 29, 29, 29],
            [21, 22, 23, 24, 25, 23, 22, 21]
        ]

        self.boardArrayHighlight = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False]
        ]

        self.movableHighlight = [
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False]
        ]
        self.printBoardArray()    # Todo - uncomment this method after create the array above

        self.trackPieces = {}

        self.mousePressed = False
        self.firstClick = False
        self.secondClick = False
        self.curPos = []
        self.nextPos = ""
        self.piece = 0
        self.reset = False
        self.turn = 1

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        xPos = event.x()
        yPos = event.y()

        # print("X: ", xPos, "Y: ", yPos)
        # print("Col width: ", self.squareWidth(), "Row height: ", self.squareHeight())
        return str(int(yPos / self.squareHeight())) + ", " + str(int(xPos / self.squareWidth()))

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # boolean which determines if the game has started or not is true
        self.resetGame()                            # reset the game
        self.timer.start(Board.timerSpeed, self)    # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            Board.counter = Board.counter - 1
            # print('timerEvent()', Board.counter)
            self.updateTimerSignal.emit(Board.counter)
        else:
            super(Board, self).timerEvent(event)  # other wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.x())+","+str(event.y())+"]"     # the location where a mouse click was registered
        # print("mousePressEvent() - "+clickLoc)

        pos = self.mousePosToColRow(event)
        turn = [x.strip() for x in pos.split(",")]
        # print("Pos: ", pos)
        # print("Pos: ", self.boardArrayHighlight[int(turn[0])][int(turn[1])])
        print("First click: ")
        print(self.firstClick)
        # print((not self.curPos))

        if not self.firstClick and self.boardArray[int(turn[0])][int(turn[1])] != 0 and not self.curPos \
                and self.turn == int(str(self.boardArray[int(turn[0])][int(turn[1])])[0]):
            self.highlightSelected(pos)
        elif self.curPos:
            print("Hi")
            print(pos)
            self.movePiece(self.curPos, pos)

        self.update()

        # todo you could call some game lodic here
        self.clickLocationSignal.emit(clickLoc)

    def movePiece(self, curpos, pos):
        turn = curpos  # [x.strip() for x in curpos.split(",")]
        next = [int(x.strip()) for x in pos.split(",")]
        piece = self.boardArray[int(turn[0])][int(turn[1])]
        move = self.boardArray[int(next[0])][int(next[1])]

        # print(turn)
        # print(next)
        # print(piece)
        # print(move)
        # print(type(turn[0]))
        # print(type(next[0]))

        '''
            Python: Compare two lists whether they are equal. (a == b)
        '''
        if next != turn:
            valid_move = False

            if piece == 11:
                if move == 0 and (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1])):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move > 20 and (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1])):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 12:
                '''
                    White Knight
                    1. Check for all the possible coordinates
                    (x+2), (y+1) or (y-1)
                    (x-2), (y+1) or (y-1)
                    (x+1) or (x-1), (y+2)
                    (x+1) or (x-1), (y-2)
                '''
                if move == 0 and ((((int(next[0]) == int(turn[0]) + 2) or (int(next[0]) == int(turn[0]) - 2)) and
                                   (int(next[1]) == int(turn[1]) + 1) or int(next[1]) == int(turn[1]) - 1)
                                  or (((int(next[1]) == int(turn[1]) + 2) or (int(next[1]) == int(turn[1]) - 2)) and
                                      (int(next[0]) == int(turn[0]) + 1) or int(next[0]) == int(turn[0]) - 1)):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move > 20 and ((((int(next[0]) == int(turn[0]) + 2) or (int(next[0]) == int(turn[0]) - 2)) and
                                   (int(next[1]) == int(turn[1]) + 1) or int(next[1]) == int(turn[1]) - 1)
                                  or (((int(next[1]) == int(turn[1]) + 2) or (int(next[1]) == int(turn[1]) - 2)) and
                                      (int(next[0]) == int(turn[0]) + 1) or int(next[0]) == int(turn[0]) - 1)):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 13:
                diff1 = int(next[0]) - int(turn[0])
                diff2 = int(next[1]) - int(turn[1])

                if move == 0 and (diff1 == diff2 or diff1 == -diff2):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move > 20 and (diff1 == diff2 or diff1 == -diff2):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 14:
                '''
                    White King
                    1. Check for every possible steps around king
                    2. No more than 1 step at a time. (if 1 in (0, 1, 2))
                '''
                if move == 0 and (int(next[0]) in ((int(turn[0]) - 1), (int(turn[0])), (int(turn[0]) + 1))
                                  and (int(next[1]) in ((int(turn[1]) - 1), (int(turn[1])), (int(turn[1]) + 1)))):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move > 20 and (int(next[0]) in ((int(turn[0]) - 1), (int(turn[0])), (int(turn[0]) + 1))
                                    and int(next[1]) in ((int(turn[1]) - 1), (int(turn[1])), (int(turn[1]) + 1))):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 15:
                diff1 = int(next[0]) - int(turn[0])
                diff2 = int(next[1]) - int(turn[1])
                if move == 0 and ((diff1 == diff2 or diff1 == -diff2)
                                  or (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1]))):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move > 20 and ((diff1 == diff2 or diff1 == -diff2)
                                    or (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1]))):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 19:
                ''' 
                    White Piece not capturing
                    1. Check if the next move is the empty space
                    2. Pawn is only moving 1 step forward. (Add Row)
                    3. Make sure Column doesn't change
                    
                    White Piece capturing
                    1. Check if the next move is not an empty space and has opponent's piece
                    2. Pawn is only moving 1 step forward. (Add Row)
                    3. Make sure Column does change. (Add Column +/- 1)
                    
                '''
                if move == 0 and int(next[0]) == int(turn[0]) + 1 and int(next[1]) == int(turn[1]):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True

                elif move != 0 and move > 20 and (int(next[0]) == int(turn[0]) + 1) \
                        and (int(next[1]) == int(turn[1]) + 1 or int(next[1]) == int(turn[1]) - 1):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 21:
                if move == 0 and (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1])):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1])):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 22:
                if move == 0 and ((((int(next[0]) == int(turn[0]) + 2) or (int(next[0]) == int(turn[0]) - 2)) and
                                   (int(next[1]) == int(turn[1]) + 1) or int(next[1]) == int(turn[1]) - 1)
                                  or (((int(next[1]) == int(turn[1]) + 2) or (int(next[1]) == int(turn[1]) - 2)) and
                                      (int(next[0]) == int(turn[0]) + 1) or int(next[0]) == int(turn[0]) - 1)):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and ((((int(next[0]) == int(turn[0]) + 2) or (int(next[0]) == int(turn[0]) - 2)) and
                                   (int(next[1]) == int(turn[1]) + 1) or int(next[1]) == int(turn[1]) - 1)
                                  or (((int(next[1]) == int(turn[1]) + 2) or (int(next[1]) == int(turn[1]) - 2)) and
                                      (int(next[0]) == int(turn[0]) + 1) or int(next[0]) == int(turn[0]) - 1)):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 23:
                diff1 = int(next[0]) - int(turn[0])
                diff2 = int(next[1]) - int(turn[1])

                '''
                    White Piece not capturing
                    1. Check if the next move is the empty space
                    2. Bishop moves anywhere diagonally on an empty spaces. 
                    3. Make sure the difference of two coordinates matches. (+/-)
                    
                    White Piece capturing
                    1. Check if the next move is not an empty space and has opponent's piece
                '''

                if move == 0 and (diff1 == diff2 or diff1 == -diff2):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and (diff1 == diff2 or diff1 == -diff2):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 24:
                if move == 0 and (int(next[0]) in ((int(turn[0]) - 1), (int(turn[0])), (int(turn[0]) + 1))
                                  and (int(next[1]) in ((int(turn[1]) - 1), (int(turn[1])), (int(turn[1]) + 1)))):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and (int(next[0]) in ((int(turn[0]) - 1), (int(turn[0])), (int(turn[0]) + 1))
                                    and int(next[1]) in ((int(turn[1]) - 1), (int(turn[1])), (int(turn[1]) + 1))):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 25:
                diff1 = int(next[0]) - int(turn[0])
                diff2 = int(next[1]) - int(turn[1])
                if move == 0 and ((diff1 == diff2 or diff1 == -diff2)
                                  or (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1]))):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and ((diff1 == diff2 or diff1 == -diff2)
                                                  or (int(next[0]) == int(turn[0]) or int(next[1]) == int(turn[1]))):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            elif piece == 29:
                if move == 0 and int(next[0]) == int(turn[0]) - 1 and int(next[1]) == int(turn[1]):
                    self.boardArray[int(turn[0])][int(turn[1])] = move
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
                elif move != 0 and move < 20 and (int(next[0]) == int(turn[0]) - 1) and (int(next[1]) == int(turn[1]) + 1
                                                                         or int(next[1]) == int(turn[1]) - 1):
                    self.boardArray[int(turn[0])][int(turn[1])] = 0
                    self.boardArray[int(next[0])][int(next[1])] = piece
                    valid_move = True
            else:
                pass

            if valid_move:
                if self.turn == 1:
                    self.turn = 2
                    self.validMove.emit(1)
                else:
                    self.turn = 1
                    self.validMove.emit(1)
                self.updateTimerSignal.emit(120)
                Board.counter = 120
            else:
                self.validMove.emit(0)

            self.playersTurnSignal.emit(self.turn)

        self.boardArrayHighlight[int(turn[0])][int(turn[1])] = False
        self.curPos = []
        self.firstClick = False


        # self.update()

    def highlightSelected(self, pos):
        turn = [x.strip() for x in pos.split(",")]
        print(pos)

        if self.boardArrayHighlight[int(turn[0])][int(turn[1])]:
            self.boardArrayHighlight[int(turn[0])][int(turn[1])] = False
            self.firstClick = False
        else:
            self.boardArrayHighlight[int(turn[0])][int(turn[1])] = True
            self.curPos = [int(turn[0]), int(turn[1])]
            self.firstClick = True

    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                if (row + col) % 2 == 0 and not self.boardArrayHighlight[row][col]:
                    painter.setBrush(Qt.white)
                elif (row + col) % 2 == 1 and not self.boardArrayHighlight[row][col]:
                    painter.setBrush(QColor("#9A7647"))
                else:
                    painter.setBrush(Qt.blue)

                colTransformation = col * self.squareWidth()  # Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()  # Todo set this value equal the transformation you would like in the column direction
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect(0, 0, self.squareWidth(), self.squareHeight(),
                                 painter.brush())  # Todo provide the required arguements
                painter.restore()


                # colTransformation = self.squareWidth()* col # Todo set this value equal the transformation you would like in the column direction
                # rowTransformation = 0  # Todo set this value equal the transformation you would like in the column direction
                # painter.translate(colTransformation,rowTransformation)
                # painter.fillRect() # Todo provide the required arguements
                # painter.restore()
                # todo change the colour of the brush so that a checkered board is drawn

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                #Todo choose your colour and set the painter brush to the correct colour

                piece = self.boardArray[row][col]
                if piece == 1:
                    painter.setBrush(Qt.lightGray)
                elif piece == 2:
                    painter.setBrush(Qt.red)

                if piece != 0:
                    if piece == 11:
                        pixmap = QPixmap("images/w_haathi.PNG")
                    elif piece == 12:
                        pixmap = QPixmap("images/w_ghoda.PNG")
                    elif piece == 13:
                        pixmap = QPixmap("images/w_unth.PNG")
                    elif piece == 14:
                        pixmap = QPixmap("images/w_raja.PNG")
                    elif piece == 15:
                        pixmap = QPixmap("images/w_wazir.PNG")
                    elif piece == 19:
                        pixmap = QPixmap("images/w_pyada.PNG")
                    elif piece == 21:
                        pixmap = QPixmap("images/b_hathi.PNG")
                    elif piece == 22:
                        pixmap = QPixmap("images/b_ghoda.PNG")
                    elif piece == 23:
                        pixmap = QPixmap("images/b_unth.PNG")
                    elif piece == 24:
                        pixmap = QPixmap("images/b_raja.PNG")
                    elif piece == 25:
                        pixmap = QPixmap("images/b_wazir.PNG")
                    elif piece == 29:
                        pixmap = QPixmap("images/b_pyada.PNG")
                    else:
                        pass

                    pixmap = pixmap.scaled(self.squareWidth(), self.squareHeight())

                    radius = (self.squareWidth() - 2) / 2
                    height = (self.squareHeight() - 2) / 2
                    center = QPoint(radius, height)
                    painter.drawPixmap(0, 0, pixmap)
                    # print(row, ",", col)
                    # self.returnColor(painter)
                    # self.trackPieces[str(row) + ", " + str(col)] = painter.brush().color().name()

                # Todo draw some the pieces as elipses
                # radius = (self.squareWidth() - 2) / 2  # Todo - make a radius in the y direction too
                # center = QPoint(radius, radius)
                # painter.drawEllipse(center, radius, radius)
                painter.restore()
