'''this is slightly modified version of k-means, set min_num_points=0 while creating object of KMeans to get effect of original k-means algo'''
import random,os

#loading and formating data
data = []
with open('BCLL.txt','r') as fi:
    for line in fi:
        data.append(line.strip('\n').strip('\t').split('\t'))
data_header = data[1]
data = data[1:]
data_index = [x[:2] for x in data]
data = [x[2:] for x in data]
data = [list(map(float,i)) for i in data]



class KMeans:
    '''
    INPUT : 
    num_centroids : number of clusters to be formed (int)
    min_num_points : number of points each cluster must have otherwise it will be removed (int)
    n_max_itr : maximum number of times we should move centroids for optimization
    
    OUTPUT : 
    cluster_centroids : a 2D list of cluster will be stored in this variable
    cluster_index_dict : this dictionary will contain indexes assigned to clusters
    removed_num_clusters = an integer value specifying number of clusters removed
    '''
    def __init__(self,num_centroids,min_num_points=10,n_max_itr=500):
        self.num_centroids = num_centroids
        self.min_num_points = min_num_points
        self.n_max_itr = n_max_itr
        self.cluster_centroids = []
        self.cluster_index_dict = {}
        self.removed_num_clusters = 0

    def initialize_centroids(self,data):
        '''
        DESCRIPTION :
        takes data as input and generates clusters by randomly selecting data points

        INPUT : 
        data : a 2D list containing training samples
        
        OUTPUT : 
        cluster_centroids : a 2D list of cluster will be stored in this variable
        '''
        n = len(data)
        self.cluster_centroids = []
        for j in range(self.num_centroids):
            self.cluster_centroids.append(data[random.randint(0,n-1)])
     

    def cluster_assignment(self,data):
        '''
        DESCRIPTION :
        takes data as input and assigns each point to a cluster

        INPUT :
        data : a 2D list containing training samples
        
        OUTPUT : 
        cluster_index_dict : this dictionary will contain indexes assigned to clusters
        '''
        self.cluster_index_dict = {}
        for i in range(len(data)):
            min_distance = float('Inf')
            min_index = -1
            for j in range(len(self.cluster_centroids)):
                d = sum([(x-y)**2 for (x,y) in zip(data[i],self.cluster_centroids[j])])**0.5
                if(d < min_distance):
                    min_distance = d
                    min_index = j
            try:
                self.cluster_index_dict[min_index].append(i)
            except:
                self.cluster_index_dict[min_index] = [i]

    #moving cluster centroids and removing unwanted clusters
    def move_centroids(self):
        '''
        DESCRIPTION :
        moves cluster centroids to a new location based on points assigned to it using cluster_index_dict
        
        OUTPUT : 
        removed_num_clusters = an integer value specifying number of clusters removed
        '''
        new_cluster_centroids = []
        for cluster_key in list(self.cluster_index_dict.keys()):
            kn = len(self.cluster_index_dict[cluster_key])
            if(kn < self.min_num_points):
                self.removed_num_clusters += 1
            else:
                kd = [data[x] for x in self.cluster_index_dict[cluster_key]]
                cs = [sum(x)/kn for x in zip(*kd)]
                new_cluster_centroids.append(cs)
        self.cluster_centroids[:] = new_cluster_centroids[:]
    
    def fit(self,data):
        '''
        DESCRIPTION :
        takes a 2D list of data and trains a KMeans model on it

        INPUT:
        data : a 2D list containing training samples
        '''
        self.initialize_centroids(data)
        for j in range(self.n_max_itr):
            old_cluster_centroids = []
            self.cluster_assignment(data)
            old_cluster_centroids[:] = self.cluster_centroids[:]
            self.move_centroids()
            if(sum([sum([(x-y)**2 for (x,y) in zip(old_cluster_centroids[i],self.cluster_centroids[i])]) for i in range(len(self.cluster_centroids))]) == 0): #checking if cluster centroids are converged
                break
        self.cluster_assignment(data)        



#function for writing data into file
def write_data(cluster_index_dict,num_centroids):
    '''
    DESCRIPTION :
    takes a dictionary of indexes assigned to clusters and writes it into a file

    INPUT :
    cluster_index_dict : dictionary containing indexes assigned to clusters
    num_centroids : num of clusters
    
    OUTPU :
    data will be written in appropreate files
    '''
    for cluster_key in list(cluster_index_dict.keys()):
        fn = 'cluster_number_{}/cluster{}.txt'.format(num_centroids,cluster_key)
        if not os.path.exists(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))
        with open(fn,'a') as fo:
            for x in cluster_index_dict[cluster_key]:
                fo.write(str(data_index[x][1])+'\n')

def write_removed_cluster_info(min_num_points,removed_num_clusters,num_centroids):
    '''
    DESCRIPTION : 
    this function is used for writing information about removed number of clusters

    INPUT : 
    min_num_points : min number of points a clusteer must have 
    removed_num_clusters : number of removed clusters for the specific case
    num_centroids : number of clusters 
    
    OUTPUT :
    data will be written in appropreate file
    '''
    fd = 'cluster_number_{}/removed_cluster(s).txt'.format(num_centroids)
    if not os.path.exists(os.path.dirname(fd)):
            os.makedirs(os.path.dirname(fd))
    with open(fd,'a') as fdo:
        fdo.write('Removed {} cluster(s) as there were less than {} elements.'.format(removed_num_clusters,min_num_points))


#runnig kmeans        
n = len(data) #number of data samples
for i in range(10):
    num_centroids = random.randint(2,int(n**0.5)) #choosing a random number in specified range
    print('Running kMeans with {} centroids.'.format(num_centroids));
    k_means = KMeans(num_centroids,min_num_points=25,n_max_itr=100) #creating a KMeans model object
    k_means.fit(data) #fitting data to using the model
    write_data(k_means.cluster_index_dict,num_centroids)
    if(k_means.removed_num_clusters != 0):
        write_removed_cluster_info(k_means.min_num_points,k_means.removed_num_clusters,num_centroids)
