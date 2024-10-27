import joblib
from sklearn.pipeline import Pipeline


def save_pipelines(all_cls, save_path):
    """Сохранение модели в файл."""

    for i, cls in enumerate(all_cls):
      # сохраняем трансформер
      joblib.dump(cls.named_steps['ohe_scal'], f'{save_path}/ohe_scal_{i}.pkl')
    # сохраняем модель
    joblib.dump(cls.named_steps['cls'], f'{save_path}/cls_{i}.pkl')


def read_piplines(path:str, num_models:int):
    """
    Функция считывания обученного пайплана моделей 
    """
    all_cls = []
    for i in range(num_models):
        loaded_transformer = joblib.load(f'{path}/ohe_scal_{i}.pkl')
        loaded_logreg = joblib.load(f'{path}/cls_{i}.pkl')
        pipe = Pipeline(steps=[
                ('ohe_scal', loaded_transformer),
                ('cls', loaded_logreg)
            ])
        all_cls.append(pipe)
    return all_cls
