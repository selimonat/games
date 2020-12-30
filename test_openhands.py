from skyjo.skyjo import Skyjo

game  = Skyjo()
game.start_game()
for i in range(2,12):
    game.open_card(i)

assert game.finished == True