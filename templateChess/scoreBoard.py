from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot

class ScoreBoard(QDockWidget): # base the scoreboard on a QDockWidget

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setFixedWidth(120)
        self.center()
        self.setWindowTitle('ScoreBoard')
        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        #create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time: 1000")
        self.label_playersTurn = QLabel("Player: White")
        self.label_valid_move = QLabel("Valid Move")
        self.mainWidget.setLayout(self.mainLayout)
        # self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_playersTurn)
        self.mainLayout.addWidget(self.label_valid_move)
        self.setWidget(self.mainWidget)
        self.show()

    # you do not need to implement this method
    def center(self):
        '''centers the window on the screen'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

        board.playersTurnSignal.connect(self.setPlayersTurn)

        board.validMove.connect(self.validError)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an arguement of the right type
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        # print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time: " + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        # print('slot '+update)
        # self.redraw()

    @pyqtSlot(int)
    def setPlayersTurn(self, playersTurn):
        '''updates the time remaining label to show the time remaining'''
        update = "Player: "
        if playersTurn == 1:
            update += "White"
        else:
            update += "Black"

        self.label_playersTurn.setText(update)
        print('slot ' + update)
        # self.redraw()

    @pyqtSlot(int)
    def validError(self, value):
        if value == 0:
            self.label_valid_move.setText("Invalid Move")
        else:
            self.label_valid_move.setText("Valid Move")