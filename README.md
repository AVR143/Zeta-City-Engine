# Attention
You are allowed to use and modify this code in its entirety. When using or modifying code/technology, you must credit me as a co-author of your work. The use of this code for commercial purposes is not permitted except in situations for which I have personally consented.

These rules also apply to *The Indie Stone* studio.

I'm an newbie, so my code is probably not perfect. I ask people who understand programming to avoid unfounded criticism.

# About Zeta: City Engine
Zeta: City Engine is an unfinished prototype of a procedural city generator for the game Project Zomboid. At the moment, the procedural generator can only create the basis for small American-style cities. The generator creates the external roads of the districts. It was planned that in the future it would place roads within areas and attach buildings to them. **This is not implemented at the moment**.

![Example of work](https://github.com/user-attachments/assets/f066f7c7-4588-4689-9c1a-0b27fead7e2c)
The photo shows an example of how the program works. If you manage to implement the functions described below, you will receive a completely ready-made simple city generator.

In addition to City Engine, there is also World Engine, which is currently in closed access, since its technology is outdated due to this program. It was planned that after all the cities were generated, they would be placed in a completely empty world. After this, the World Engine was supposed to generate roads between cities, as well as forests, lakes, small random farms, etc. 

# How to install and run
1. The code is written and runs in Python. **Install Python on your computer**.
2. Download the repository to your computer. For correct operation, the project directory structure must remain the same as in the original repository.
3. In the **project** folder of the repository there is an example project for WorldEd. Use it to test your program.
4. Open the **main.py** file. Replace the path in the **template** variable with the absolute path to the folder with the road files on your computer. They are currently in the **roads** folder, but you can put them anywhere you like.
5. Launch the program. A file with a new map will appear in the **result** folder. Drag this file into the **tmxworld** folder, which is located in the **project** folder.
6. Ready. You can run the project in WorldEd. If you did everything correctly, then you should see something like the following:
   
![example](https://github.com/user-attachments/assets/e8affc4a-91dc-4ab9-8f9d-a78aff2ccb66)


# Features (implemented and not implemented)
| Function | Meaning | Status |
|-------------|-------------|-------------|
| External roads | Generates the outer outline of districts | Completed |
| Writing to a .pzw file | Saves the result to the game world editor file | Completed |
| Internal roads | Generates roads that go deep into areas | Not completed |
| Zoning* | Dividing the city into areas: commercial, residential, industrial | Not completed |
| Placement of buildings | Places buildings next to roads | Not completed |
| Integration** | Integration with Zeta: World Engine  | Not completed |

Zoning* - The plan was that after Zeta created the outer and inner roads, it would randomly divide the city into some types of districts. The main ones are industrial, commercial and residential. And only after this the program should place buildings in these areas that fit the type of this area.

Integration** - It is important to understand that Zeta: City Engine is just a module for creating cities. It was planned that in the future I would integrate it into Zeta: World Engine in order to be able to get a completely finished game world, and not just one city.

