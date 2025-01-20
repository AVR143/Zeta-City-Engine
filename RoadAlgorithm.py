#from PIL import Image, ImageDraw, ImageFont
import time, random, copy

class Point:
    def __init__(self, x, y):
        self.x = x    
        self.y = y  
    def copy_from(self, src):
        self.x = src.x    
        self.y = src.y  
    def to_string(self):
        return "{" + str(self.x) + "; " + str(self.y) + "}"
class Rect:
    def __init__(self, pntLU, pntRD):
        self.pntLU = pntLU   #Left top vertex
        self.pntRD = pntRD   #Bottom right vertex
    def to_string(self):
        return "[" + self.pntLU.to_string() + "; " + self.pntRD.to_string() + "]"
    
    @property
    def width(self):
        return self.pntRD.x - self.pntLU.x + 1;
    @property
    def height(self):
        return self.pntRD.y - self.pntLU.y + 1;
    @property
    def center(self):
        return Point(self.pntLU.x + self.width / 2, self.pntLU.y + self.height / 2);   
    @property
    def square(self):
        return self.width*self.height         


#           Auxiliary functions
# Finds the number of road cells intersecting with the roads of the rectangle
def find_cross_count(field, rect): 
    count = 0
    for dx in range(rect.pntLU.x, rect.pntRD.x + 1):
        if field[dx][rect.pntLU.y] == 1:
                count += 1    
        if field[dx][rect.pntRD.y] == 1:
                count += 1     
    for dy in range(rect.pntLU.y + 1, rect.pntRD.y):
        if field[rect.pntLU.x][dy] == 1:
                count += 1           
        if field[rect.pntRD.x][dy] == 1:
                count += 1           
    return count

# Finds a rectangle that completely describes all roads in the field
def find_main_rect(rect_list, area_rect):
    main_pntLU = Point(0,0)
    main_pntRD = Point(0,0)
    main_pntLU.copy_from(area_rect.pntRD)    
    main_pntRD.copy_from(area_rect.pntLU)    
    rect_found = False
    for rect in rect_list:
        if (rect.pntLU.x >= area_rect.pntLU.x and rect.pntRD.x <= area_rect.pntRD.x and
            rect.pntLU.y >= area_rect.pntLU.y and rect.pntRD.y <= area_rect.pntRD.y):
                rect_found = True
                main_pntLU.x = main_pntLU.x if main_pntLU.x < rect.pntLU.x else rect.pntLU.x
                main_pntLU.y = main_pntLU.y if main_pntLU.y < rect.pntLU.y else rect.pntLU.y
                main_pntRD.x = main_pntRD.x if main_pntRD.x > rect.pntRD.x else rect.pntRD.x
                main_pntRD.y = main_pntRD.y if main_pntRD.y > rect.pntRD.y else rect.pntRD.y
    return Rect(main_pntLU, main_pntRD), rect_found
# Finds all positions in which it is possible and it makes sense to set a rectangle of given parameters,
# returns a list of possible rectangles
def find_avbl_rects(field, field_size, width, height): 
    avaible_rects = []    
    for dx in range(field_size.x - width + 1):     
        for dy in range(field_size.y - height + 1):
            if field[dx][dy] == 2 or field[dx][dy] == 3: # We skip inaccessible areas (can be removed, this is optimization)
                continue
            rect = Rect(Point(dx,dy), Point(dx+width-1, dy+height-1))
            if can_place_rect(field, field_size, rect) and find_cross_count(field, rect) > 0:   
                avaible_rects.append(rect)
    return avaible_rects
          

#                   Rectangle setting functions
# Fills the specified area with roads and inaccessible areas on the field
def fill_rect(field, rect):
    road_pos_x = [rect.pntLU.x, rect.pntRD.x]
    road_pos_y = [rect.pntLU.y, rect.pntRD.y]
    for dx in range(rect.pntLU.x, rect.pntRD.x + 1):     
        for dy in range(rect.pntLU.y, rect.pntRD.y + 1):     
            field[dx][dy] = 1 if road_pos_x.count(dx) > 0 or road_pos_y.count(dy) > 0 else 2
# Checks if the rectangle can be placed on the field
def can_place_rect(field, field_size, rect):
    #There are no inaccessible areas on the borders of the rectangle
    bad_zones = [2, 3]    
    for dx in range(rect.pntLU.x, rect.pntRD.x + 1): 
        if bad_zones.count(field[dx][rect.pntLU.y]) > 0 or bad_zones.count(field[dx][rect.pntRD.y]) > 0:
            return False
    for dy in range(rect.pntLU.y + 1, rect.pntRD.y):
        if bad_zones.count(field[rect.pntLU.x][dy]) > 0 or bad_zones.count(field[rect.pntRD.x][dy]) > 0:
            return False
    #The area inside is completely empty
    inner_area_pntLU = Point(rect.pntLU.x + 1, rect.pntLU.y + 1)
    inner_area_pntRD = Point(rect.pntRD.x - 1, rect.pntRD.y - 1)
    for dx in range(rect.pntLU.x + 1, rect.pntRD.x): 
        for dy in range(rect.pntLU.y + 1, rect.pntRD.y):
            if field[dx][dy] != 0:
                return False
    #There are no double roads near the border from the outside
    for dx in range(rect.pntLU.x, rect.pntRD.x): 
        if rect.pntLU.y - 1 >= 0:
            if field[dx][rect.pntLU.y - 1] == 1 and field[dx + 1][rect.pntLU.y - 1] == 1:
                return False
        if rect.pntRD.y + 1 < field_size.y:
            if field[dx][rect.pntRD.y + 1] == 1 and field[dx + 1][rect.pntRD.y + 1] == 1:
                return False
    for dy in range(rect.pntLU.y, rect.pntRD.y):
        if rect.pntLU.x - 1 >= 0:
            if field[rect.pntLU.x - 1][dy] == 1 and field[rect.pntLU.x - 1][dy + 1] == 1:
                return False     
        if rect.pntRD.x + 1 < field_size.x:       
            if field[rect.pntRD.x + 1][dy] == 1 and field[rect.pntRD.x + 1][dy + 1] == 1:
                return False            
    return True
                

#               Criteria extraction functions
# Proportion criteria (the list is passed with a new rectangle)
def rel_field_crit(rect_list, field_size, new_rect_pos, main_road_y, ideal_rel):
    max_rel = max(field_size.x, field_size.y)
    min_rel = 1 / max(field_size.x, field_size.y)
    area_rect = Rect(Point(0, 0), Point(0, 0))
    if new_rect_pos.y < main_road_y:
        area_rect = Rect(Point(0, 0), Point(field_size.x-1, main_road_y))
    else:
        area_rect = Rect(Point(0, main_road_y), Point(field_size.x-1, field_size.y-1))
    cur_main_rect, rect_found = find_main_rect(rect_list, area_rect)
    if not rect_found:
        return 1
    cur_rel = cur_main_rect.width / cur_main_rect.height
    if cur_rel > ideal_rel:
        return 1 - (cur_rel - ideal_rel)/(max_rel - ideal_rel)
    else:
        return (cur_rel - min_rel)/(ideal_rel - min_rel)
# Centrality criterion (the list is transmitted with a new rectangle)
def cntr_field_crit(rect_list, field_size, new_rect_pos, main_road_y):
    max_offset = max(field_size.x, field_size.y) * 0.5
    area_rect = Rect(Point(0, 0), Point(0, 0))
    if new_rect_pos.y < main_road_y:
        area_rect = Rect(Point(0, 0), Point(field_size.x-1, main_road_y))
    else:
        area_rect = Rect(Point(0, main_road_y), Point(field_size.x-1, field_size.y-1))
    cur_center = Point(0, 0)
    rect_count = 0
    for rect in rect_list:
        if (rect.pntLU.x >= area_rect.pntLU.x and rect.pntRD.x <= area_rect.pntRD.x and
            rect.pntLU.y >= area_rect.pntLU.y and rect.pntRD.y <= area_rect.pntRD.y):
                rect_count += 1
                cur_center = Point(cur_center.x + rect.center.x, cur_center.y + rect.center.y)
    if rect_count <= 0:
        return 1
    cur_center = Point(cur_center.x / rect_count, cur_center.y / rect_count)
    cur_offset = (abs(field_size.x/2 - cur_center.x) + abs(main_road_y - cur_center.y))/2
    return 0 if cur_offset > max_offset else 1 - cur_offset / max_offset 
# Area criterion (the list is passed with a new rectangle)
def sqr_field_crit(rect_list, field_size, main_road_y):
    up_square = 0
    down_square = 0
    for rect in rect_list:
            if(rect.pntLU.y < main_road_y):
                up_square += rect.square 
            else:
                down_square += rect.square
    if up_square == down_square:
        return True
    elif up_square == 0 or down_square == 0:
        return False
    else:    
        return up_square/down_square if down_square > up_square else down_square / up_square
# Intersection criterion (the field is transmitted without a new rectangle)
def cross_field_crit(field, rect):
    max_count = (rect.width + rect.height) * 2 - 4 #Number of border cells, NOT perimeter
    count = find_cross_count(field, rect)
    return count / max_count
        

#                           Main functions
# Generates and returns a rectangle with the most successful position according to all criteria
def find_best_rect(field, field_size, main_road_y, width, height, entropy, rect_list):
    # Criteria constants (CHANGING IS HIGHLY RECOMMENDED)
    # Imbalance values influence EXCLUSIVELY whether the overall imbalance of the system will be detected or not
    # Multipliers allow you to increase or decrease the priority of a criterion when determining the sort order
    """ Proportion criterion """
    max_rel_disbalance = 0.6
    multip_rel = 0.6
    ideal_area_rel = 5 / 3 
    """ Centrality criterion """
    max_center_disbalance = 0.17
    multip_center = 1.3
    """ Area criterion """
    max_square_disbalance = 0.35
    multip_square = 1
    
    # Current averaged criteria of Proportions and Centralization, criterion of compliance of Areas and general imbalance
    rel_up_std_crit = rel_field_crit(rect_list, field_size, Point(0, 0), main_road_y, ideal_area_rel)
    rel_down_std_crit = rel_field_crit(rect_list, field_size, field_size, main_road_y, ideal_area_rel)
    rel_min_std_crit = min(rel_up_std_crit, rel_down_std_crit)
    cntr_up_std_crit = cntr_field_crit(rect_list, field_size, Point(0, 0), main_road_y)
    cntr_down_std_crit = cntr_field_crit(rect_list, field_size, field_size, main_road_y)
    cntr_min_std_crit = min(cntr_up_std_crit, cntr_down_std_crit)
    sqr_std_crit = sqr_field_crit(rect_list, field_size, main_road_y)
    is_disbalanced = (1 - rel_min_std_crit > max_rel_disbalance or 
                      1 - cntr_min_std_crit > max_center_disbalance or 
                      1 - sqr_std_crit > max_square_disbalance)

    # List of rectangles with criteria values on the field after adding it
    crit_list = []
    rects = find_avbl_rects(field, field_size, width, height)
    new_field = [[0] * field_size.y for i in range(field_size.x)]
    new_list = []    
    for rect in rects:
        for dx in range(field_size.x):     
            for dy in range(field_size.y):
                new_field[dx][dy] = field[dx][dy]
        fill_rect(new_field, rect)
        new_list.clear()
        new_list = rect_list.copy()
        new_list.append(rect)
        crit_list.append((rect,
                          cross_field_crit(field, rect), #1
                          rel_field_crit(new_list, field_size, rect.pntLU, main_road_y, ideal_area_rel), #2
                          cntr_field_crit(new_list, field_size, rect.pntLU, main_road_y), #3
                          sqr_field_crit(new_list, field_size, main_road_y))) #4
        
    # 2 - Proportions, 3 - Centralization, 4 - Areas
    crit_pos = [(rel_min_std_crit / multip_rel, 2), (cntr_min_std_crit / multip_center, 3), (sqr_std_crit / multip_square, 4)] 
    crit_pos.sort()
    # List of rectangles sorted by criteria
    sorted_list = []      
    if is_disbalanced:
        sorted_list = sorted(crit_list, key = lambda x: (x[crit_pos[0][1]], x[crit_pos[1][1]], x[crit_pos[2][1]], x[1]), reverse = True)
    else:
        sorted_list = sorted(crit_list, key = lambda x: (x[1], x[crit_pos[0][1]], x[crit_pos[1][1]], x[crit_pos[2][1]]), reverse =True)
    
    # Return one of the best rectangles and a boolean whether such a rectangle exists
    if len(sorted_list) <= 0:
        return Rect(Point(-1,-1),Point(-1,-1)), False
    max_element = int(entropy * (len(sorted_list)-1))
    if max_element == 0:
        return sorted_list[0][0], True
    else:
        return sorted_list[random.randint(0, max_element)][0], True
# Returns an image of the passed field
def get_field_image(field, field_size, rect_list, block_size):
    scale = Point(50, 50)
    img_size = Point(field_size.x * scale.x, field_size.y * scale.y)

    image = Image.new("RGB", (img_size.x, img_size.y), "white")
    draw = ImageDraw.Draw(image)

    # Draw rectangles
    for dx in range(field_size.x):     
        for dy in range(field_size.y):     
            if field[dx][dy] != 1 and field[dx][dy] != 2:
                continue                            
            left_up_point = (dx * scale.x, dy * scale.y)
            right_down_point = ((dx + 1) * scale.x, (dy + 1) * scale.y)
            draw.rectangle([left_up_point, right_down_point], fill="blue" if field[dx][dy] == 1 else "#FFD09B")
    # Draw numbers of rectangles
    for i in range(len(rect_list)):
        draw.text((rect_list[i].pntLU.x * scale.x, rect_list[i].pntLU.y * scale.y), str(i), fill="black", font_size=min(scale.x, scale.y)/2)
    # Рисуем сетку
    for x in range(field_size.x + 1):
        draw.line([(x * scale.x, 0), (x * scale.x, img_size.y)], fill="lightgray" if x%block_size != 0 else "red", width=1)
    for y in range(field_size.y + 1):
        draw.line([(0, y * scale.y), (img_size.x, y * scale.y)], fill="lightgray" if y%block_size != 0 else "red", width=1)            
    
    return image

def main(field_bsize_coord, max_rect_size_coord, min_rect_size_coord, max_rects_count):
    # Generation parameters
    rand_seed = int(time.time()) # int(time.time()) For always different generations
    entropy = 0 # indicator of the randomness of the arrangement of rectangles, from 0.0 to 1.0. It's better to leave 0
    field_border_offset = 1
    block_size = 10 # Block size (Minimum 3)
    field_bsize = Point(*field_bsize_coord) # Field size in 4 by 4 blocks
    max_rect_size = Point(*max_rect_size_coord)
    min_rect_size = Point(*min_rect_size_coord) # THE ALGORITHM CANNOT BE SET LESS THAN 3
    max_rects = max_rects_count
    # Generated parameters
    field_size = Point(field_bsize.x * block_size, field_bsize.y * block_size)


    # We display basic information about the launch
    #print("\tИНФОРМАЦИЯ О ЗАПУСКЕ")
    #print("Сид текущей генерации:", rand_seed)
    #print("Энтропия:", entropy)
    #print("Отступ от границ (в клетках):", field_border_offset)
    #print("Размер блоков:", block_size)
    #print("Размер поля (в блоках):", field_bsize.to_string())
    #print("Максимальный размер прямоугольника (в клетках):", max_rect_size.to_string())
    #print("Минимальный размер прямоугольника (в клетках):", min_rect_size.to_string())
    #print("Максимальное кол-во прямоугольников:", max_rects, "\n")
    
    random.seed(rand_seed)

    # Field generation
    # 0 - empty cell, 1 - road located, 2 - inside a rectangle, 3 - inaccessible area (field boundaries)
    rect_list = []
    field = [[0] * field_size.y for i in range(field_size.x)]

    # Blocking cells with a distance less than or equal to field_border_offset to the field boundaries
    for dx in range(field_size.x):     
        for dy in range(field_size.y):     
            field[dx][dy] = 3 if (dx < field_border_offset or 
                            dy < field_border_offset or 
                            field_size.x - dx <= field_border_offset or 
                            field_size.y - dy <= field_border_offset) else 0
          
    # Main road generation
    main_road_y = random.randint(0, field_bsize.y-1)*block_size + 2
    for dx in range(field_size.x):     
          field[dx][main_road_y] = 1   

    # Generate rectangles
    for i in range(max_rects):
        fails_count = 0
        while fails_count < 20:   
            width = random.randint(min_rect_size.x, max_rect_size.x) 
            height = random.randint(min_rect_size.y, max_rect_size.y)
            rect, rect_found = find_best_rect(field, field_size, main_road_y, width, height, entropy, rect_list)
            if rect_found:
                fill_rect(field, rect)
                rect_list.append(rect)
                #print("Прямоугольник сгенерирован №" + str(i) + ":", rect.to_string())
                break          
            else:  
                fails_count += 1     
                #print("Прямоугольник не удалось разместить:", rect.to_string())
    
    #print("Всего расставленных прямоугольников:", len(rect_list), "из", max_rects, end = "\n\n")

    # Transpose the field, or do not transpose it
    trsp_on = random.randint(0, 1) == 0
    #print("Транспонирование:", "Включено" if trsp_on else "Отключено", end = "\n\n")
    if trsp_on:
        new_field = [[0] * field_size.y for i in range(field_size.x)]
        for dx in range(field_size.x):     
            for dy in range(field_size.y):
                try:
                    new_field[dy][dx] = field[dx][dy]
                except IndexError:
                    main()
        field = new_field
        for rect in rect_list:
            temp = rect.pntLU.x 
            rect.pntLU.x = rect.pntLU.y    
            rect.pntLU.y = temp 
            temp = rect.pntRD.x 
            rect.pntRD.x = rect.pntRD.y    
            rect.pntRD.y = temp 

    # Convert the field to a list of tuples and print
    roads = []
    for dx in range(field_size.x):     
        for dy in range(field_size.y):
            if(field[dx][dy] == 1):
                roads.append((dx, dy)) 
    #print("Все клетки с дорогами в виде списка кортежей:", roads, end = "\n\n")
    return roads
    
if __name__ == "__main__":
    main()
