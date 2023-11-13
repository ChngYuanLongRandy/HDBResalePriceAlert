from model.Query import Query
import yaml
config_path = "./src/config/config.yaml"

params = yaml.safe_load(open(config_path))

def run():
    query = Query(params)
    query.run_query_success()
    df = query.write_to_dataframe()

    print(df)

if (__name__ == "__main__") :
    run()