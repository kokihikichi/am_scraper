import schedule
import os


def restart_scrapers():
    for i in range(1, 5):
        instance_name = 'am-scraper-{i}'.format(i=i)
        os.system("gcloud compute ssh -q {instance_name} --zone us-central1-a \
                    --command 'source ~/.bash_profile && \
                                gsutil cp /home/kokihikichi/am_scraper/df_main.csv gs://am-scraped/bk/{instance_name}-df_main.csv &&\
                                gsutil cp /home/kokihikichi/am_scraper/item_links.pickle gs://am-scraped/bk/{instance_name}-item_links.pickle'".format(instance_name=instance_name))
        os.system('gcloud compute instances stop {instance_name} --zone us-central1-a'.format(
            instance_name=instance_name))
        os.system('gcloud compute instances start {instance_name} --zone us-central1-a'.format(
            instance_name=instance_name))
        cmd = """gcloud compute ssh -q {instance_name} --zone us-central1-a \
                    --command "source ~/.bash_profile && \
                    gsutil cp gs://am-scraped/startup_scripts/{instance_name}.sh /home/kokihikichi/am_scraper/ && \
                    sudo chmod +x /home/kokihikichi/am_scraper/{instance_name}.sh && \
                    tmux new-session -d -s scrape '/home/kokihikichi/am_scraper/{instance_name}.sh'"
                    """.format(instance_name=instance_name)
        os.system(cmd)

if __name__ == "__main__":
    schedule.every(30).minutes.do(restart_scrapers)
    while True:
        schedule.run_pending()
