def float_to_bin(number:float):
    result=[]
    big_int=number*1000000000
    big_bin=bin(int(big_int))
    binary=big_bin.split("b")[1]
    for element in binary:
        result.append(int(element))
    return result

def bin_to_float (bin:list):
    result=[]
    for element in bin:
        result.append(str(element))
    bin_str="".join(result)
    big_int=int(bin_str,2)
    return big_int/1000000000

#list_number=float_to_bin(4.87983245789745)
#print(list_number)
#print(bin_to_float(list_number))