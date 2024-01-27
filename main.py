from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from schema.hello import resolve_hello

from dotenv import load_dotenv


load_dotenv()  # .env ファイルから環境変数を読み込む

query = QueryType()

# リゾルバー関数を登録
query.set_field("hello", resolve_hello)

type_defs = """
    type Fund {
        id: Int
        fundName: String
        currentPrice: Float
        currentPriceGets: Float
        currentRate: Float
    }
    type Query {
        hello(id: Int!): Fund
    }
"""

schema = make_executable_schema(type_defs, query)

app = FastAPI()
app.add_route("/", GraphQL(schema, debug=True))
