#!/usr/bin/env python3
""" Log stats """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db_nginx = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    # Count total logs
    count_logs = db_nginx.count_documents({})
    print(f'{count_logs} logs')

    # Count logs by method
    print('Methods:')
    for method in methods:
        count_method = db_nginx.count_documents({'method': method})
        print(f'\tmethod {method}: {count_method}')

    # Count status check logs
    check = db_nginx.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f'{check} status check')

    # Find the top 10 most present IPs
    top_ips = db_nginx.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print('IPs:')
    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')
