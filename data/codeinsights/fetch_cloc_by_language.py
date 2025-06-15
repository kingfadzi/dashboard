import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_cloc_by_language(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                cloc.language AS main_language,
                SUM(cloc.blank) AS blank_lines,
                SUM(cloc.comment) AS comment_lines,
                SUM(cloc.code) AS total_lines_of_code,
                COUNT(*) AS source_code_file_count
            FROM cloc_metrics cloc
            JOIN languages l ON cloc.language = l.name
            WHERE cloc.language IS NOT NULL 
              AND cloc.language != 'SUM'
              AND l.type = 'programming'
        """

        if condition_string:
            base_query += f" AND cloc.repo_id IN (SELECT repo_id FROM harvested_repositories WHERE {condition_string})"

        base_query += """
            GROUP BY cloc.language
            ORDER BY total_lines_of_code DESC
            LIMIT 20
        """

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        numeric_columns = ["blank_lines", "comment_lines", "total_lines_of_code", "source_code_file_count"]
        for column in numeric_columns:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: int(x) if pd.notnull(x) else None)

        return df

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
