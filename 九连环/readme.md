# 九连环

九连环可以看做初始状态是九个状态为1的bit，目标是状态全部变成0。  
转换条件是：当bit[x]=1且bit[x+1,8]=0时，b[x-1]可以转换状态。

解出最短路，并打印。

一遍BFS就好