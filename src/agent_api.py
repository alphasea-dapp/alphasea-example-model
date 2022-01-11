import requests


def submit_prediction(agent_base_url=None, model_id=None, df=None, prediction_license=None):
    assert (df['execution_start_at'].unique().size == 1)
    assert (prediction_license == 'CC0-1.0')

    df = df.reset_index()
    df = df[['symbol', 'position']]
    df = df.set_index('symbol')

    output = StringIO()
    df.to_csv(output, index=False)

    url = agent_base_url + '/submit_prediction'
    data = {
        'model_id': model_id,
        'execution_start_at': df['execution_start_at'].iloc[0].timestamp(),
        'prediction_license': prediction_license,
        'content': output.value(),
    }
    r = requests.post(url, data=data)
    return r.content
