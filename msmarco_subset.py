import os


DATA_DIR = './data'

# sed 's/	/|n /' collectionandqueries/collection.tsv | sed "s/:/ /g" | sed "s/,/ /g" | sed "s/\./ /g" | tr '[:upper:]' '[:lower:]' | stmr | vw -i model --ngram 2 --skips 1 --predictions preds

def main():
  bioset = set()

  preds_file = os.path.join(DATA_DIR, 'preds')
  with open(preds_file) as preds:
    for line in preds:
      pred, doc_id = line.split('\t')
      if pred > 0.5:
        bioset.add(doc_id.strip())

  queries = dict()
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
  with open(collection_file) as collection, open('bio.tsv') as bio, open('triples.train.small.tsv') as train:
    for line in collection:
      doc_id, text = line.strip().split('\t')
      if doc_id in bioset:
        bio.write(line)
        if doc_id in docs_to_queries:
          qid = docs_to_queries[doc_id]
          if len(negative_examples) > 0:
            train.write(queries[qid] + '\t' + text + '\t' + negative_examples.pop() + '\n')
        else:
          negative_examples.add((doc_id, text))


if __name__ == '__main__':
  main()