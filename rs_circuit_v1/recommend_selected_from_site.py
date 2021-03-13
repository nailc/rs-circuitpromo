import sys 
import clean_taffy
import make_pool
import preprocess_data
import train_recommend
import train_recommend_selected
import glob

directory = "/var/www/html/users/"+str(sys.argv[1])
province = sys.argv[2]
root_dir = "/var/www/html/"
train_recommend_selected.train_and_recommend_selected(root_dir, directory, province)