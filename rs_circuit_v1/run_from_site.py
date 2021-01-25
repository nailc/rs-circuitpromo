import sys 
import clean_taffy
import make_pool
import preprocess_data
import train_recommend
import glob

directory = "/var/www/html/users/"+str(sys.argv[1])
province = sys.argv[2]
root_dir = "/var/www/html/"


clean_taffy.clean_taffy_liste(root_dir, directory, province)    
make_pool.make_pool_data(root_dir, directory, province)
preprocess_data.preprocess_all_data(root_dir, directory)
train_recommend.train_and_recommend(root_dir, directory, province)
