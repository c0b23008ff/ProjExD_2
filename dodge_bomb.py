import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = { # 移動量辞書（押下キー：移動量タプル）
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct) -> tuple[bool, bool]:
    """
    こうかとんRect,または爆弾Rectの画面内外判定用の関数
    引数:こうかとんRectまたは爆弾Rect
    戻り値：横方向判定結果、縦方向判定結果 (True:画面内, False:画面外)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_img.set_colorkey((0, 0, 0))
    bd_rct = bd_img.get_rect()
    vx, vy = +5, +5
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  #  こうかとんと爆弾がぶつかったら
            game_over() #  ゲームオーバーの関数を呼び出す
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)

def game_over():
    """
    ゲームオーバーになったときに発動する関数
    暗く半透明のバックグラウンド+文字+こうかとん
    """
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    bg_img.set_alpha(100)
    end_kk_rct = pg.image.load("fig/8.png")
    end_kk_rct = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0) 
    screen.blit(bg_img, [0, 0]) #  バックグラウンドを表示
    screen.blit(txt, [WIDTH/2, HEIGHT/2]) #  "Game Over"を表示
    screen.blit(end_kk_rct, [WIDTH/2-100, HEIGHT/2]) #  こうかとんを表示
    screen.blit(end_kk_rct, [WIDTH/2+350, HEIGHT/2]) #  こうかとんを表示
    pg.display.update()
    print("Gmame Over")
    time.sleep(5)
    #clock.tick(1/5)

def kasoku_kyodai():
    """
    爆弾の速度を加速させる関数、また爆弾を拡大する関数
    10段階に分けて速度を加速する、また爆弾を拡大する
    """
    acc = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255,0,0), (10*r, 10*r), 10*r)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
