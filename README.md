# Telecontact-Scraper-Airflow
A tool that uses :
    - Apache airflow 
    - [telecontact-scraper](https://github.com/Tahasadiki/Telecontact-Scraper)
    to schedule and run scraping telecontact.ma

## Single Node Airflow Setup

Run
```bash
docker-compose up -d
```

## Multi-Node (Cluster) Airflow Setup
Change the `cluster.env` file so that the __POSTGRES_HOST__ and __REDIS_HOST__ points to the node where postgres and redis are installed

### Nodes :  

__master__:    
will have the roles : Web Server, Scheduler
```bash
docker-compose -f docer-compose-webserver_scheduler.yml up -d
```

__postgres_redis__:  
will have the role of storing Airflow metadata and queing service and flower service
```bash
docker-compose -f docker-compose-redis_metadata_flower up -d
```

__worker(s)__:  
will have the role : Worker
```bash
docker-compose -f docker-compose-worker.yml up -d
```