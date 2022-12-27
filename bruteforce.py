
import pandas as pd

def knapSack(W, wt, val, n):
    # Base Case
    if n == 0 or W == 0:
        return 0
 
    # If weight of the nth item is
    # more than Knapsack of capacity W,
    # then this item cannot be included
    # in the optimal solution
    if (wt[n-1] > W):
        return knapSack(W, wt, val, n-1)
 
    # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(
            val[n-1] + knapSack(
                W-wt[n-1], wt, val, n-1),
            knapSack(W, wt, val, n-1))
 
# end of function knapSack
 
if __name__ == "__main__":
    # Driver Code
    # val = [500, 150, 60, 40, 30]
    # wt = [2200, 160, 350, 333, 192]
    # W = 3000
    # n = len(val)
    # print(knapSack(W, wt, val, n))

    data = pd.read_csv('bruteInput.csv')
    val = data['Total Fish LB'].tolist()
    wt = data['Distance'].tolist()
    W =  1000
    n = len(val)
    print(knapSack(W, wt, val, n))


    
 
