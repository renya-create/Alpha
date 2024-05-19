import numpy
import tkinter as tk

game = numpy.zeros((8, 8))
game[3][3] =  1
game[4][4] =  1
game[3][4] = -1
game[4][3] = -1

#白：1,黒：-1

def nextgame(game, row, clm, Player):
    if game[row][clm] == 0:
        for d_iter in range(9):
            dc = int(d_iter / 3) - 1
            dr = d_iter % 3 - 1
            length = 0
            while True:
                length += 1
                if row + dr * length < 0 or row + dr * length > 7 \
                or clm + dc * length < 0 or clm + dc * length > 7:
                    break
                buf = game[row + dr * length][clm + dc * length]
                if length == 1 and buf != -1 * Player:
                    break
                if length > 1 and buf == 0:
                    break
                if length > 1 and buf == Player:
                    for iter in range(length):
                        game[row + dr * iter][clm + dc * iter] = Player
def placable(game, Player):
    able = numpy.zeros((8, 8))
    for rowIter in range(8):
        for clmIter in range(8):
            nextstatus = game.copy()
            nextgame(nextstatus, rowIter, clmIter, Player)
            if nextstatus[rowIter][clmIter] != game[rowIter][clmIter]:
                able[rowIter][clmIter] = Player
    return able

class gameUI(tk.Frame):
    def __init__(self, game, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('othello')
        self.c = tk.Canvas(self, width = 640, height = 480, highlightthickness = 0)
        self.c.bind('<Button-1>', self.on_click)
        self.player = 1
        self.c.pack()
        #盤の色を指定
        self.c.create_rectangle(0, 0, 480, 480, width = 0.0, fill = '#006400')
        #升目を表示
        for rowIter in range(8):
            self.c.create_line(0, rowIter * 60, 480, rowIter * 60, width = 1.0, fill = '#FFFFFF')
        for clmIter in range(8):
            self.c.create_line(clmIter * 60, 0, clmIter * 60, 480, width = 1.0, fill = '#FFFFFF')
        #石を配置
        self.game = game
        self.on_draw()

    def on_click(self, event):
        self.x = int(event.x/60)
        self.y = int(event.y/60)
        self.nextstatus = self.game.copy()
        nextgame(self.nextstatus, self.y, self.x, self.player)
        if self.nextstatus[self.y][self.x] != self.game[self.y][self.x]:
            self.game = self.nextstatus
            self.player = -1 * self.player
            able = placable(self.game, self.player)
            if numpy.sum(able) == 0.0: #どこにも置けない場合、手番を変更
                self.player = -1 * self.player
                able = placable(self.game, self.player)
            self.on_draw()
            if numpy.sum(able) == 0.0: #どこにも置けない場合、終局
                self.game_end() 

    def on_draw(self):
        self.c.delete("all")  # キャンバスをクリアする
        self.c.create_rectangle(0, 0, 480, 480, width=0.0, fill='#006400')  # 盤の色を再描画

        for row in range(8):
            for clm in range(8):
                if self.game[row][clm] == 1:
                    self.c.create_oval(clm * 60 + 5, row * 60 + 5, (clm + 1) * 60 - 5, (row + 1) * 60 - 5, width=0.0, fill='#FFFFFF')
                if self.game[row][clm] == -1:
                    self.c.create_oval(clm * 60 + 5, row * 60 + 5, (clm + 1) * 60 - 5, (row + 1) * 60 - 5, width=0.0, fill='#000000')

        for rowIter in range(8):
            self.c.create_line(0, rowIter * 60, 480, rowIter * 60, width=1.0, fill='#FFFFFF')
        for clmIter in range(8):
            self.c.create_line(clmIter * 60, 0, clmIter * 60, 480, width=1.0, fill='#FFFFFF')

        self.c.create_rectangle(500, 20, 620, 60, width=0.0, fill='#ffffaa')
        self.c.create_rectangle(500, 80, 620, 120, width=0.0, fill='#ffffaa')
        lbl_white = tk.Label(text='白：' + str(numpy.count_nonzero(self.game == 1.0)) + '個', bg='#ffffaa', fg='#000000', font=("メイリオ", "16", "bold"))
        lbl_white.place(x=510, y=25)
        lbl_black = tk.Label(text='黒：' + str(numpy.count_nonzero(self.game == -1.0)) + '個', bg='#ffffaa', fg='#000000', font=("メイリオ", "16", "bold"))
        lbl_black.place(x=510, y=85)
        lbl = tk.Label(text='手番', font=("メイリオ", "16", "bold"))
        lbl.place(x=530, y=140)
        self.c.create_rectangle(510, 180, 610, 280, width=0.0, fill='#006400')
        if self.player == 1:
            self.c.create_oval(530, 200, 590, 260, width=0.0, fill='#FFFFFF')
        if self.player == -1:
            self.c.create_oval(530, 200, 590, 260, width=0.0, fill='#000000')
            
    def game_end(self):
        if numpy.count_nonzero(self.game == 1.0) > numpy.count_nonzero(self.game == -1.0):
            lbl_end = tk.Label(text='白の勝ち', font=("メイリオ", "16", "bold")) 
        elif numpy.count_nonzero(self.game == 1.0) < numpy.count_nonzero(self.game == -1.0):
            lbl_end = tk.Label(text='黒の勝ち', font=("メイリオ", "16", "bold")) 
        else:
            lbl_end = tk.Label(text='引き分け', font=("メイリオ", "16", "bold")) 
        lbl_end.place(x=500, y=300) 

f = gameUI(game)
f.pack()
f.mainloop()


        