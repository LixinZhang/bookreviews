#/usr/bin/python
from clusterBase import importData,pearson_distance

class bicluster:
    def __init__(self, vec, left=None,right=None,distance=0.0,id=None) :
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(blogwords,blognames) :
    biclusters = [ bicluster(vec = blogwords[i], id = i ) for i in range(len(blogwords)) ]
    distances = {}
    flag = None;
    currentclusted = -1
    while(len(biclusters) > 1) :
        min_val = 2;
        biclusters_len = len(biclusters)
        for i in range(biclusters_len-1) :
            for j in range(i + 1, biclusters_len) :
                if distances.get((biclusters[i].id,biclusters[j].id)) == None:
                    distances[(biclusters[i].id,biclusters[j].id)] = pearson_distance(biclusters[i].vec,biclusters[j].vec)
                d = distances[(biclusters[i].id,biclusters[j].id)] 
                if d < min_val :
                    min_val = d
                    flag = (i,j)
        bic1,bic2 = flag
        newvec = [(biclusters[bic1].vec[i] + biclusters[bic2].vec[i])/2 for i in range(len(biclusters[bic1].vec))]
        newbic = bicluster(newvec, left=biclusters[bic1], right=biclusters[bic2], distance=min_val, id = currentclusted)
        currentclusted -= 1
        del biclusters[bic2]
        del biclusters[bic1]
        biclusters.append(newbic)
    return biclusters[0]

'''
Print the tree structure, save as a jpeg image file.
'''

from PIL import Image, ImageDraw

def getheight (clust) :
    if clust.left == None and clust.right == None :return 1
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust) :
    if clust.left == None and clust.right == None :return 0
    return max(getdepth(clust.left),getdepth(clust.right)) + clust.distance

def drawdendrogram(clust,labels,jpeg='clusters.jpg') :
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)
    scaling = float(w-150) / depth
    
    img = Image.new('RGB',(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')

def drawnode(draw, clust, x, y, scaling, labels) :
    if clust.id < 0 :
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1+h2)/2
        bottom = y + (h1+h2)/2
        #line length
        ll = clust.distance * scaling
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))
        drawnode(draw,clust.left, x+ll, top+h1/2,scaling, labels)
        drawnode(draw,clust.right,x+ll, bottom-h2/2,scaling,labels)
    else :
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))

if __name__ == '__main__' :
    #pearson_distance
    blogwords,blognames = importData()
    clust = hcluster(blogwords,blognames)
    print clust
    #drawdendrogram(clust,blognames,jpeg='blogclust.jpg')
