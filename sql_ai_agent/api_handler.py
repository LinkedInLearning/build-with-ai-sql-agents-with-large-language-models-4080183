from openai import OpenAI
import duckdb as db
from sql_ai_agent import prompt_handler as ph
from sql_ai_agent import parse_query as pq


class SqlAgent:
    def __init__(self, api_key, base_url, model, tbl_name, max_token=5000):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.tbl_name = tbl_name
        self.max_token = max_token

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.system = ph.system_prompt(tbl_name=tbl_name)

    def send_prompt(self, question):
        self.user = ph.user_prompt(question=question)
        self.response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system.system},
                {"role": "user", "content": self.user},
            ],
            max_completion_tokens=self.max_token,
        )

        content = self.response.choices[0].message.content
        if pq.is_markdown_code_chunk(text=content):
            query = pq.extract_code_from_markdown(markdown_text=content)
        else:
            query = content

        self.query = query

    def ask_question(self, question, verbose=True):
        self.send_prompt(question=question)
        self.data = db.sql(self.query)
        if verbose:
            print(self.query)
            print(self.data)
