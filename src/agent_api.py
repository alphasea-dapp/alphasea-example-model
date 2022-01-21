from io import StringIO
import requests


def submit_prediction(agent_base_url=None, model_id=None, df=None, prediction_license=None):
    assert (df['execution_start_at'].unique().size == 1)
    assert (prediction_license == 'CC0-1.0')

    execution_start_at = df['execution_start_at'].iloc[0].timestamp()
    tournament_id = 'crypto_daily_{:02}30'.format(df['execution_start_at'].iloc[0].hour)

    df = df.reset_index()
    df = df[['symbol', 'position']]
    df = df.set_index('symbol')

    output = StringIO()
    df.to_csv(output)

    url = agent_base_url + '/submit_prediction'
    data = {
        'model_id': model_id,
        'tournament_id': tournament_id,
        'execution_start_at': execution_start_at,
        'prediction_license': prediction_license,
        'content': output.getvalue(),
    }
    print(data)
    r = requests.post(url, json=data)
    print(r.content)
    return r.json()
