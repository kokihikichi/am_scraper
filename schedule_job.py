import schedule
import time
import os


def restart_scrapers():
    for i in range(1, 8):
        instance_name = 'am-scraper-{i}'.format(i=i)
        os.system("gcloud compute ssh -q {instance_name} --zone us-central1-a \
                  --command 'source ~/.bash_profile && \
                             gsutil cp /home/koki_hikichi/am_scraper/df_main.pickle gs://am-scraped/bk/{instance_name}-df_main.pickle &&\
                             gsutil cp /home/koki_hikichi/am_scraper/item_links.pickle gs://am-scraped/bk/{instance_name}-item_links.pickle &&\
                             gsutil cp /home/koki_hikichi/am_scraper/current_url.pickle gs://am-scraped/bk/{instance_name}-current_url.pickle'".format(instance_name=instance_name))
        os.system('gcloud compute instances stop {instance_name} --zone us-central1-a'.format(
            instance_name=instance_name))
        os.system('gcloud compute instances start {instance_name} --zone us-central1-a'.format(
            instance_name=instance_name))
        cmd = """gcloud compute ssh -q {instance_name} --zone us-central1-a \
                   --command "source ~/.bash_profile && \
                   gsutil cp gs://am-scraped/startup_scripts/{instance_name}.sh /home/koki_hikichi/am_scraper/ && \
                   sudo chmod +x /home/koki_hikichi/am_scraper/{instance_name}.sh && \
                   tmux new-session -d -s scrape '/home/koki_hikichi/am_scraper/{instance_name}.sh'"
                   """.format(instance_name=instance_name)
        os.system(cmd)

if __name__ == "__main__":
    schedule.every(30).minites.do(restart_scrapers)
    while True:
        schedule.run_pending()
        time.sleep(1)
