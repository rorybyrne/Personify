
from __future__ import division
import itertools
import csv

product_list = []

csv_file = open('ShoppingData.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
next(csv_reader)

for row in csv_reader:
    product_list.append(row[1] + " : " + row[4])

csv_file.close()


def jaccard_set(s1, s2):
    " takes two sets and returns Jaccard coefficient"
    u = s1.union(s2)
    i = s1.intersection(s2)
    return len(i)/len(u)

if __name__ == '__main__':

    # shingle size
    k = 3   
  
    shingles = []
    for product in product_list:
        sh = set()
        size = len(product)
        for i in range(size-k):
            sh.add(product[i:i+k])
        # print("size=%s: %s") %(len(sh), sh)
        shingles.append(sh)

    # print("sets: shingles=%s") %(shingles)

    # print("len(shingles)=%s") %(len(shingles))

    combinations = list(itertools.combinations([x for x in range(len(shingles))], 2) )
    #print("combinations=%s") %(combinations)

	
    group_of_sets=[set() for i in range(len(shingles))]
    setnum=0
    check=0
    num = 0 

    for c in combinations:
        i1 = c[0]
        i2 = c[1]
        jac = jaccard_set(shingles[i1], shingles[i2])

        if jac >= 0.3 :
               
            #print("%s :jaccard=%s") %(c,jac)
    
            for num in range (0, len(group_of_sets)) :
                if not group_of_sets[num] :
                    print 'new set created for'
                    print("%s :jaccard=%s") %(c,jac)
                    print 'set number'
                    print num
                    group_of_sets[num].add(product_list[i1])
                    group_of_sets[num].add(product_list[i2])
                    break
            
                elif product_list[i1] in group_of_sets[num] :
                    group_of_sets[num].add(product_list[i2])
                    print("%s :jaccard=%s") %(c,jac)
                    print 'added to set'
                    print num
                    break
                
# Used to print for testing #
#
#    for s in group_of_sets : 
#        if s :
#            print s
#            print
 

    f = open('ShoppingOutput.csv', 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('ClusterID', 'Product') )
    groupnum = 1
    for s in group_of_sets :
        if s :
            for s1 in s :
                writer.writerow((groupnum, s1))
            groupnum += 1
finally:
    print("Finished")
    f.close()


