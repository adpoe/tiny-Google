import os

path = './books'
count = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
count = count - 1
print("number of files : %d"%(count))
