#include <cstdio>
#include <stack>
#include <iostream>
#include <queue>
using namespace std;
int dis[1<<9];
int pre[1<<9];

inline int set(int status,int p){
    return status|(1<<p);
}
inline int reset(int status,int p){
    int t = 1<<p;
    t = ~t;
    return status&t;
}
inline int get(int status,int p){
    int t = status&(1<<p);
    return t!=0;
}
int bfs(){
    queue<int> q;
    q.push((1<<9)-1);
    dis[(1<<9)-1]=0;
    while(!q.empty()){
        int s = q.front();
        cout<<s<<endl;
        if(s==0){
            break;
        }
        q.pop();
        int cnt=0;
        for(int i=0;i<9;i++){
            int t = get(s,i);
            int ns=-1;
            if(i==0){
                if(t==0){
                    ns = set(s,i);
                }
                else{
                    ns = reset(s,i);
                }
            }
            else{
                if(cnt==1&&get(s,i-1)==1){
                    if(t==0){
                        ns = set(s,i);
                    }
                    else{
                        ns = reset(s,i);
                    }
                }
            }
            if(ns>=0&&dis[ns]<0){
                q.push(ns);
                pre[ns] = s;
                dis[ns] = dis[s]+1;
            }
            if(t!=0){
                cnt++;
                if(cnt==2){
                    break;
                }
            }
        }
    }
}

int main(){
    for(int i=0;i<(1<<9);i++){
        pre[i]=-1;
        dis[i]=-1;
    }
    bfs();
    cout<<"Min step: "<<dis[0]<<endl;
    return 0;
}