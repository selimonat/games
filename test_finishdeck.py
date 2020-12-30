from skyjo.skyjo import Skyjo

game = Skyjo()
game .start_game()


count = 0
while game .finished is False:
    count += 1
    print(f"TURN {count}")
    game.update_table()

assert game.finished == True