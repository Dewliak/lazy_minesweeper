import random

def setup():
    size_x_of_map = 30
    size_y_of_map = 16
    number_of_bombs = 99
    size_map = size_x_of_map * size_y_of_map
    m = create_map()
    m,bomb_places = add_number(m)
    flag_map = [[' ' for i in range(30)] for j in range(16)]
    return m, flag_map,bomb_places

def map_data():
    size_x_of_map = 30
    size_y_of_map = 16
    number_of_bombs = 99
    size_map = size_x_of_map * size_y_of_map
    return size_x_of_map, size_y_of_map

def main():
    #creating minesweeper

    # create map
    main_map = create_map()
    for i in main_map:
        print(i)

    print('\n' * 2)

    main_map = add_number(main_map)

    for i in main_map:
        print(i)


# a normal map is 30 x 16 with 99 bombs
def create_map():

    #map config
    size_x_of_map = 30
    size_y_of_map = 16
    number_of_bombs = 99
    size_map = size_x_of_map * size_y_of_map

    #map
    empty_blocks = [' ' for i in range(size_map - number_of_bombs)]
    bomb_block  = ['9' for i in range(number_of_bombs)]
    full_map = empty_blocks + bomb_block
    random.shuffle(full_map)
    main_map = []
    for i in range(size_y_of_map):
        temp = []
        for j in range(size_x_of_map):
            temp.append(full_map[(size_x_of_map * i) + j])
        main_map.append(temp)

    return main_map

#add the numbers
def add_number(whole_map):
    bomb_place = []
    map_x = len(whole_map[0])
    map_y = len(whole_map)
    for i in range(map_y):
        for j in range(map_x):
            if whole_map[i][j] != '9':
                bomb_counter = 0
                if j != (len(whole_map[0]) - 1) and whole_map[i][j + 1] == '9':
                    bomb_counter += 1

                if j != 0 and whole_map[i][j - 1] == '9':
                    bomb_counter += 1

                if i != (len(whole_map) - 1) and whole_map[i + 1][j] == '9':
                    bomb_counter += 1

                if i != 0 and whole_map[i - 1][j] == '9' :
                    bomb_counter += 1

                if i != 0 and j != 0 and whole_map[i - 1][j - 1] == '9':
                    bomb_counter += 1

                if i != 0 and j != (len(whole_map[0]) -1 ) and whole_map[i - 1][j + 1] == '9':
                    bomb_counter += 1

                if i != (len(whole_map) -1) and j != 0 and  whole_map[i + 1][j - 1] == '9':
                        bomb_counter += 1

                if i != (len(whole_map) -1) and j != (len(whole_map[0]) -1) and whole_map[i + 1][j + 1] == '9':
                    bomb_counter += 1

                if bomb_counter != 0:
                    whole_map[i][j] = str(bomb_counter)

                else:
                    pass
            else:
                bomb_place.append(tuple([i,j]))
    return whole_map,bomb_place

if __name__ == '__main__':
    main()