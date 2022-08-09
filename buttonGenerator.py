# Author: Charles Cal
# Date: 8/8/2022
# Description:

with open('buttonCommands.txt', 'w') as f:
    f.write("self.button_list = list()\n")
    for x in range(8):
        f.write("row = list()\n")
        for y in range(8):
            if (x + y) % 2 == 0:
                f.write(f"button{x}{y} = GridButton(position=({x}, {y}), bg = '#EDAA9B', master=self.board, text=f'{{self.show(({x}, {y}))}}', height = 4, width = 6, command=lambda: self.make_a_move(({x},{y})))\n")
            else:
                f.write(f"button{x}{y} = GridButton(position=({x}, {y}), bg = '#AEF0E9', master=self.board, text=f'{{self.show(({x}, {y}))}}', height = 4, width = 6, command=lambda: self.make_a_move(({x},{y})))\n")
            f.write(f"button{x}{y}.grid(row = {x}, column = {y})\n")
            f.write(f"row.append(button{x}{y})\n")
        f.write("self.button_list.append(row)\n")


# bg = '#EDAA9B'
# bg = '#AEF0E9'