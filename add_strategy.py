def add_step_by_step(*nums, add10s=False):
    return_val = [0]
    for j in nums:
        su = return_val[-1] + j
        return_val.append(su)  
    return return_val

def add_rearrange(*nums):
    return_nums = []
    numsC = list(nums[:])
    while numsC:
        i = numsC.pop(0)
        for j, k in enumerate(numsC):
            for n in range(100, 0, -10):
                if i+k == n:
                    numsC.pop(j)
                    return_nums += [i, k]
                    break            
    for i in nums:
        if i not in return_nums:
            return_nums.append(i)
    return return_nums
                
def add_numlist(start, stop, step):
    numlist = list(range(start, stop+1, step))
    sum_ = start + stop
    if len(numlist) %2 == 0:
        return sum_ * len(numlist)/2
    else:
        return(sum_ * (len(numlist)-1)/2) + numlist[len(numlist) // 2]

print(add_numlist(1, 15, 1))