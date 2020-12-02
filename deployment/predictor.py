from gec_model import GecBERTModel


class PythonPredictor:
    def __init__(self, config):
        vocab_path = config['vocab_path']
        model_path = config['model_path']
        self.model = GecBERTModel(vocab_path=vocab_path,
                                  model_paths=[model_path],
                                  max_len=50, min_len=3,
                                  iterations=5,
                                  min_error_probability=0.5,
                                  min_probability=0.5,
                                  lowercase_tokens=0,
                                  model_name='roberta',
                                  special_tokens_fix=1,
                                  log=False,
                                  confidence=0.2,
                                  is_ensemble=0,
                                  weigths=None)

    def predict(self, payload):
        batch_size = 32
        predictions = []
        cnt_corrections = 0
        batch = []
        sent = payload['text']
        batch.append(sent.split())
        if len(batch) == batch_size:
            preds, cnt = self.model.handle_batch(batch)
            predictions.extend(preds)
            cnt_corrections += cnt
            batch = []
        if batch:
            preds, cnt = self.model.handle_batch(batch)
            predictions.extend(preds)
            cnt_corrections += cnt

        return "\n".join([" ".join(x) for x in predictions])
