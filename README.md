# A* Pathfinding in Snake Game
## How to run the code
- ### To run the code, simply run the Game file, and then the A* with play snake with a loaded UI using PyGame. Then you will be prompted with an input of how long you would like the additional delay to be beyond the normal delay needed to update the UI. After entering this time then the PyGame will pop up with the algorithm playing the game.
## Algorithm Implementation
- ### To run this project, the A* algorithm receives an array of the snake board and then determines the path to get to the food and then moves in the first direction of the list. Then after moving it will redo the path and then again move in the first direction again. If the snake cannot find an immediate path to the food, then the direction will not change.
## Heuristic Choices
- ### This algorithm is heuristic because it is not fully deterministic and based on the distance from the current node to the final node.
- ### The algorith calculates this distance through Euclidean distance(pythagorean theorem), but it would also work by just adding the difference of the row and column.
## Future improvements
- ### In the future, I am thinking about possibly making a way that the snake would stall, because the algorithm does not know where the tail is leaving, and then while waiting for there to be an opening it crashes into the wall. As such, I might try to find a way to have the snake stall to allow it to get higher scores by letting it find a way out despite not having a direct path at the start.
## Sources/Credits
### I looked at a lot of different oython implementations of A star before actually writing my own, and my own used a lot of their commonalities because of the little variance in creating an A* algorithm.
- ### https://www.studocu.com/in/document/srm-institute-of-science-and-technology/artificial-intelligence/aprogram/88108309
- ### https://en.wikipedia.org/wiki/A*_search_algorithm
- ### http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
- ### https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1
- ### https://towardsdatascience.com/understanding-a-path-algorithms-and-implementation-with-python-4d8458d6ccc7
- ### https://www.redblobgames.com/pathfinding/a-star/implementation.html
### Additionally, I used another person's snake game and only modified it to make it work better with my program, but the general structure was still there. 
- ### https://github.com/patrickloeber/snake-ai-pytorch/blob/main/game.py
## 
