import append_dbtrain
import make_weekly
import make_to_recommend

html_dir = "/var/www/html"
root_dir = "/var/www/html"

make_weekly.make_weekly_products(html_dir, root_dir)
append_dbtrain.split_weekly_products(root_dir)
make_to_recommend.process_weekly_products(root_dir)