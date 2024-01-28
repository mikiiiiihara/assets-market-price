from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI

from schema.mufg_fund import resolve_mufg_fund
from schema.stock import resolve_stocks

from dotenv import load_dotenv


load_dotenv()  # .env ファイルから環境変数を読み込む

query = QueryType()

# リゾルバー関数を登録
query.set_field("mufgFunds", resolve_mufg_fund)
query.set_field("stocks", resolve_stocks)

type_defs = """
    type Fund {
        id: Int
        fundName: String
        currentPrice: Float
        currentPriceGets: Float
        currentRate: Float
    }
        type Stock {
        ticker: String
        marketPrice: Float
        dividends: [Dividend]
    }

    type Dividend {
        date: String
        value: Float
    }
    type Query {
        mufgFunds(ids: [Int!]!): [Fund!]!
        stocks(tickers: [String!]): [Stock!]!
    }
"""

schema = make_executable_schema(type_defs, query)

app = FastAPI()
app.add_route("/", GraphQL(schema, debug=True))
