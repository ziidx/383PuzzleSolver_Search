George Chiang
Jack DeGuglielmo

Best Meal:
Jack - Tomahawk Steak
George - New York Strip Steak

Conclusion: After evaluating some sample start states, we conclude that path cost does indeed affect the solutions found.
Using 468530721 as our start state, our A* search produced two different solution paths using noweight and weighted path costs.


$python solver.py astar 468530721 --noweight
0       start   468530721
1       down    460538721
2       right   406538721
3       up      436508721
4       up      436528701
5       left    436528710
6       down    436520718
7       right   436502718
8       right   436052718
9       down    036452718
10      left    306452718
11      left    360452718
12      up      362450718
13      right   362405718
14      down    302465718
15      right   032465718
16      up      432065718
17      left    432605718
18      up      432615708
19      right   432615078
20      down    432015678
21      down    032415678
22      left    302415678
23      up      312405678
24      right   312045678
25      down    012345678
path cost:  25
frontier:  3301
expanded:  2128

$python solver.py astar 468530721
0       start   468530721
1       right   468503721
2       down    408563721
3       right   048563721
4       up      548063721
5       left    548603721
6       left    548630721
7       down    540638721
8       right   504638721
9       up      534608721
10      up      534628701
11      left    534628710
12      down    534620718
13      right   534602718
14      up      534612708
15      right   534612078
16      down    534012678
17      down    034512678
18      left    304512678
19      up      314502678
20      right   314052678
21      down    014352678
22      left    104352678
23      left    140352678
24      up      142350678
25      right   142305678
26      down    102345678
27      right   012345678
path cost:  511
frontier:  1038
expanded:  627