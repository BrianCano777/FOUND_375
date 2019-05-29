#!/usr/bin/env python  #credit to drewda for original code; modified by @B3CB; code review by @OXAH

import argparse
import boto3
import pandas as pd

if __name__ == '__main__':
  # command-line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--dry-run',
                      default=True,
                      action='store_true',
                      help="don't actually tag S3 buckets; just report which buckets should be tagged")
  args = parser.parse_args()

  # read XLS
  xls_filename = r'S3_what_is_there_v2.xlsx'
  s3_dataframe = pd.read_excel(xls_filename, header=1)
  # TODO: filter down to just buckets marked for datalake tagging
  bucket_names = s3_dataframe['Bucket_name']

  if args.dry_run:
    print("***** the following buckets are marked for datalake tagging *****")
  else: 
    s3 = boto3.resource('s3')
    print("***** starting to tag S3 buckets *****")

  for bucket_name in bucket_names:
    if args.dry_run:
      print(bucket_name)
    else:
      print(bucket_name)
      bucket_tagging = s3.BucketTagging(bucket_name)
      tags = bucket_tagging.tag_set
      tags.append({'datalake': 'true'})
      bucket_tagging.put(Tagging={'TagSet':tags})

  # TODO: in the future, register each S3 bucket to call
  # Lambda function on appropriate events
