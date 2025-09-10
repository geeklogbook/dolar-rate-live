#!/usr/bin/env python3
import time
import psycopg2
import boto3

# Configs
PG = {"host": "localhost", "port": 5432, "database": "rates", "user": "postgres", "password": "postgres"}
MINIO = {"endpoint_url": "http://localhost:9000", "aws_access_key_id": "minio", "aws_secret_access_key": "minio123"}
BUCKET = "bitcoin-data"

def test_pg():
    conn = psycopg2.connect(**PG)
    cursor = conn.cursor()
    
    start = time.time()
    cursor.execute("SELECT COUNT(*) FROM bitcoin")
    count = cursor.fetchone()[0]
    count_time = time.time() - start
    
    start = time.time()
    cursor.execute("SELECT * FROM bitcoin ORDER BY created_at DESC LIMIT 100")
    cursor.fetchall()
    read_time = time.time() - start
    
    cursor.close()
    conn.close()
    
    print(f"PostgreSQL: {count} registros, conteo: {count_time:.3f}s, lectura: {read_time:.3f}s")

def test_minio():
    s3 = boto3.client("s3", **MINIO)
    
    start = time.time()
    response = s3.list_objects_v2(Bucket=BUCKET)
    objects = response.get('Contents', [])
    list_time = time.time() - start
    
    start = time.time()
    for obj in objects[:10]:
        s3.get_object(Bucket=BUCKET, Key=obj['Key'])
    read_time = time.time() - start
    
    print(f"MinIO: {len(objects)} objetos, listado: {list_time:.3f}s, lectura: {read_time:.3f}s")

if __name__ == "__main__":
    print("Test Performance:")
    test_pg()
    test_minio()
