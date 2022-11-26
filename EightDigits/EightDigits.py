chart = {0:[1,3], 
         1:[2,4,0], 
         2:[1,5],
         3:[0,4,6], 
         4:[1,3,5,7], 
         5:[2,4,8],
         6:[3,7],  
         7:[4,6,8], 
         8:[5,7]}

def inv_num(s):
    count = 0
    for i in range(1,9):
        inv=0
        for j in range(0,i):
            if(s[j]>s[i] and s[i]!='0'):
                inv+=1
        count+=inv
    return count

def swap(a, i, j):
    if i > j:
        #将i,j变换顺序，便于后面拷贝字符串
        i, j = j, i
    b = a[:i] + a[j] + a[i+1:j] + a[i] + a[j+1:]
    return b


def total_cost(deep,new,dst):
    val = future_cost(new, dst)+deep
    return val

#返回错码和正确码距离之和
def future_cost(src,dst):
    sum = 0
    a = src.index("0")
    for i in range(0,9):
        if i!=a:
            sum=sum+abs(i-dst.index(src[i]))
    return sum

def solve(src, dst, method=2):

    # Open表，以整个字符串为一个表中元素
    # 后续通过查找“0”所在位置来确定可移动方向
    openBox = []
    openBox.append(src)#当前状态存入列表
    
    # Closed表，以字典记录
    # 便于查找是否已扩展，并且记录父节点
    closedBox = {}
    closedBox[src] = -1
    
    deep = {}
    deep[src]= 1
    
    # Open表中各节点的总距离
    openDeep = {}
    openDeep[src] = 1 + future_cost(src, dst)
    
    count=0
    
    while len(openBox) > 0:
        # count+=1
        # print("No.",count)
        if(method==1):
            cur = openBox.pop() # 后进先出，深度优先
        elif(method==2):
            cur = openBox.pop(0) # 先进先出，广度优先
        else:
            #找到当前Open表中总距离最小的节点
            cur = min(openDeep, key=openDeep.get)
            # print("cur:",cur)
            del openDeep[cur]
            openBox.remove(cur) 
        
        
        if cur == dst: #判断当前状态是否为目标状态
            break

        # 寻找0的位置并进行扩展
        init = cur.index("0")
        Available = chart[init]#当前可进行交换的位置集合
        for move in Available:
            new = swap(cur, move, init) #交换后的状态
            if closedBox.get(new) == None:#判断交换后的状态是否已经查询过
                closedBox[new] = cur      #当前扩展节点加入Closed表
                openBox.append(new)       #新节点加入Open表
                if(method==3):
                    val = total_cost(deep[cur] + 1, new, dst)
                    deep[new] = deep[cur] + 1#存入距离
                    openDeep[new] = val#存入val

            
    # 输出
    steps = []
    steps.append(cur)
    # 回溯至根节点src
    while closedBox[cur] != -1: 
        cur = closedBox[cur]
        steps.append(cur)
    steps.reverse()
    return steps



if __name__ == "__main__":
    
    #测试数据输入格式
    src = "541203786"
    dst = "123804765"
    
    method = 2
    assert method in [1,2,3],"方法错误，请重新输入！"
    
    inv1 = inv_num(src)
    inv2 = inv_num(dst)
    assert inv1%2==inv2%2,"不可解！请重新开始！"
    
    steps = solve(src, dst, method)
    for i in range(len(steps)):
        print(f"--Steps:{i+1}--")
        print(steps[i][:3])
        print(steps[i][3:6])
        print(steps[i][6:])