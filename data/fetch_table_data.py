sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column hr.last_commit_date does not exist
LINE 2: ...n_label, hr.activity_status, hr.status, hr.scope, hr.last_co...
                                                             ^

[SQL: 
            SELECT hr.repo_id, hr.repo_slug, hr.browse_url, hr.app_id, hr.host_name, hr.transaction_cycle, hr.main_language, hr.all_languages, hr.classification_label, hr.activity_status, hr.status, hr.scope, hr.last_commit_date, rc.total_commits, rc.activity_status, rc.repo_age_days, rc.last_commit_date
            FROM harvested_repositories hr
            LEFT JOIN repo_catalog rc ON hr.repo_id = rc.repo_id
        
            ORDER BY hr.last_commit_date DESC NULLS LAST,
                     hr.activity_status ASC
            LIMIT %(limit)s OFFSET %(offset)s
        ]
[parameters: {'limit': 1000, 'offset': 0}]
(Background on this error at: https://sqlalche.me/e/20/f405)