import os


DATA_DIR = './data'
OUT_DIR = './msmarco-bio'

# sed 's/	/|n /' collectionandqueries/collection.tsv | sed "s/:/ /g" | sed "s/,/ /g" | sed "s/\./ /g" | tr '[:upper:]' '[:lower:]' | stmr | vw -i model --ngram 2 --skips 1 --predictions preds

def main():
  bioset = set()

  qrels_tsv_path = os.path.join(OUT_DIR, 'qrels.dev.small.tsv')
  queries_tsv_path = os.path.join(OUT_DIR, 'queries.dev.tsv')

  print('loading preds..')
  preds_file = os.path.join(DATA_DIR, 'vw')
  with open(preds_file) as preds:
    for line in preds:
      pred, doc_id = line.strip().split(' ')
      if float(pred) > 0.5:
        bioset.add(doc_id.strip())

  queries = dict()
  print('loading queries..')
  query_file_path = os.path.join(DATA_DIR, 'queries.train.tsv')
  with open(query_file_path) as query_file:
    for line in query_file:
      qid, query = line.strip().split('\t')
      queries[qid] = query

  qrels = set()
  docs_to_queries = dict()
  qrels_file_path = os.path.join(DATA_DIR, 'qrels.train.tsv')
  with open(qrels_file_path) as qrels_file:
    for line in qrels_file:
      qid, _, doc_id, _ = line.strip().split('\t')
      qrels.add((qid, doc_id))
      docs_to_queries[doc_id] = qid

  collection_file = os.path.join(DATA_DIR, 'collection.tsv')
  negative_examples = set()
  example_num = 0
  qrels_dev_file = open(qrels_tsv_path, 'w')
  queries_dev_file = open(queries_tsv_path, 'w')
  with open(collection_file) as collection, open(os.path.join(OUT_DIR, 'collection.tsv'), 'w') as bio, open(os.path.join(OUT_DIR, 'triples.train.small.tsv', 'w')) as train:
    for line in collection:
      doc_id, text = line.strip().split('\t')
      if doc_id in bioset:
        bio.write(line)
        if doc_id in docs_to_queries:
          qid = docs_to_queries[doc_id]
          if len(negative_examples) > 0:
            example_num += 1
            if example_num < 5000:
              qrels_dev_file.write('\t'.join([str(qid), '0', str(doc_id), '1']) + '\n')
              queries_dev_file.write(qid + '\t' + queries[qid] + '\n')
            else:
              sample = queries[qid] + '\t' + text + '\t' + negative_examples.pop()[1] + '\n'
              train.write(sample)
        else:
          negative_examples.add((doc_id, text))


if __name__ == '__main__':
  main()