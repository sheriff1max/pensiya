from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, recall_score, accuracy_score



def total_model(train_data, agg_transactions):
    """Обучение pipeline на датасете."""

    cat = ['gndr', 'brth_yr', 'prsnt_age', 'pnsn_age', 'prvs_npf', 'okato', 'north_region']
    num = agg_transactions.columns.to_list()[1:11]
    print(num)

    column_transformer = ColumnTransformer([
        ('ohe', OneHotEncoder(handle_unknown="ignore"), cat),
        ('scal', StandardScaler(), num)
    ])


    all_cls = []
    pipes = []
    score_models = []
    for train, val in train_data:
        pipe = Pipeline(steps=[
            ('ohe_scal', column_transformer),
            ('cls', LogisticRegression())
        ])

        cls = pipe.fit(train[cat + num], train['erly_pnsn_flg'])

        all_cls.append(cls)
        pipes.append(pipe)
        score_models.append(
                [round(f1_score(val['erly_pnsn_flg'], cls.predict(val[cat + num])) * 100, 2),\
                round(recall_score(val['erly_pnsn_flg'], cls.predict(val[cat + num])) * 100, 2),\
                round(accuracy_score(val['erly_pnsn_flg'], cls.predict(val[cat + num])) * 100, 2)]
                )

    return all_cls, score_models, pipes
