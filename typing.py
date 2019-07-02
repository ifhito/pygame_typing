import pygame
from pygame.locals import *
import sys

START, PLAY, GAMEOVER = (0, 1, 2)#状態の入力
SCR_RECT = Rect(0, 0, 640, 480)#画面の大きさ


class type:
    def __init__(self):#初期設定
        pygame.init()
        with open("typing.txt") as f:
            text=f.readlines()
        self.list=[]
        for i in text:
            self.list.append(i.rstrip('\n').split(" "))
        self.time_passed = pygame.time.get_ticks()/1000.0
        self.num = 0#打たれた文字数を保持する変数
        self.num_moji = 0
        self.score = 0#スコアを入れる変数
        self.time_start = 0#たった時間を入れる変数
        #coding: shift_jis
        self.answer = self.list[self.num_moji][0]
        self.question = self.list[self.num_moji][1]#Qを入れる変数
        self.game_state = START#最初の状態はSTART
        screen = pygame.display.set_mode(SCR_RECT.size)#displayの設定
        self.clock = pygame.time.Clock()#時間管理のためのオブジェクト
        while(True):#ゲームを更新する
            self.clock.tick(60)#60fps
            self.draw(screen)#drow
            pygame.display.update()#update
            self.key()#キー情報取得のためのオブジェクト
            
    def draw(self, screen):
        screen.fill((0, 0, 0))#背面は黒色
        if self.game_state == START:#スタート状態の場合
            title_font = pygame.font.SysFont(None, 80)#titleのfontの大きさと種類の指定
            title = title_font.render("TYPING", False, (255, 0, 0))#TYPINGをレンダーする
            screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 100))#場所は半分の幅に上から100px
            space_font = pygame.font.SysFont(None, 40)#fontの大きさと種類の指定
            space = space_font.render("TYPE SPACE", False, (0, 255, 0))#TYPE SPACEをレンダー
            screen.blit(space, ((SCR_RECT.width-space.get_width())/2, 380))#真ん中の上から380px

        elif self.game_state == PLAY:#PLAY画面
            mozi_font = pygame.font.Font("ipag.ttf", 40)#fontはipag.ttfに指定、大きさ40px
            answer = mozi_font.render(self.answer,False,(255,255,255))#日本語の方のanswerを表示
            screen.blit(answer,((SCR_RECT.width-answer.get_width())/2, SCR_RECT.height/2-100))#answerを表示する位置を決める
            for q in range(0, len(self.question)):#問題の文字数分回す
                if(q < self.num):#self.numがタイピングで正解した場合の数字が入っている。その数以下なら
                    mozi = mozi_font.render(self.question[q], False, (0, 255, 0))#黄色にする(正解した文字は色を変える)
                else:
                    mozi = mozi_font.render(self.question[q], False, (255, 255, 255))#そうでなければ白文字(ここを黒に帰ると単語テストも可能)
                    #mozi = mozi_font.render(self.question[q], False, (0, 0, 0))
                screen.blit(mozi, ((SCR_RECT.width-len(self.question)*25)/2+25*q, SCR_RECT.height/2))#文字の場所を調整する
            if len(self.question) == self.num:#全ての文字を打ち終わったら
                self.score = self.score + len(self.question)#スコアを入力
                self.num_moji += 1#次の文字へ
                self.answer = self.list[self.num_moji][0]#次の文字のanswer
                self.question = self.list[self.num_moji][1]#次の文字の
                self.num = 0#numは初期化
                
            seconds = (pygame.time.get_ticks() - self.time_start)/1000.0#secondに経過時間を追加
            Time = mozi_font.render(str(60-int(seconds)), False, (255, 255, 255))#残り時間の表示
            screen.blit(Time,(10,10))
            if seconds >= 60:#60秒をすぎるとゲームオーバーへ
                self.game_state = GAMEOVER
            
        
        elif self.game_state == GAMEOVER:#終了画面
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render("Score", False, (255, 0, 0))
            screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 100))

            space_font = pygame.font.SysFont(None, 100)
            space = space_font.render(str(self.score), False, (0, 255, 0))#スコア表示
            screen.blit(space, ((SCR_RECT.width-space.get_width())/2, 380))



    def key(self):#キーボード
        for event in pygame.event.get():
            if event.type == QUIT:#QUITがタイプされたら終了
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:#エスケープの場合も終了
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:#スペースを入力したらPLAY
                if self.game_state == START:
                    self.time_start = pygame.time.get_ticks()
                    self.game_state = PLAY
            elif event.type == KEYDOWN and chr(event.key) == self.question[self.num]:#現在のquestionの単語が入力した文字と同じ場合
                self.num += 1#numにプラス1


type1 = type()
type1.__init__()
