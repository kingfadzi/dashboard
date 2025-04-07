profile_data = {
    'Repo ID': 'CTFd',
    'Status': 'ACTIVE',
    'Security Risk': True,
    'EOL Risk': False,
    'Tech Debt Risk': True,
    'Repo Size (MB)': 25,
    'File Count': 929,
    'Lines of Code': 106417,
    'Total NLOC': 95432,
    'Blank Lines': 12345,
    'Comment Lines': 8540,
    'Avg Cyclomatic Complexity': 3.5,
    'Total Cyclomatic Complexity': 2200,
    'Total Tokens': 560000,
    'Total Functions': 1250,
    'Classification Label': 'Medium',
    'Contributors': 149,
    'Repo Age (Years)': 10,
    'Last Commit Date': '2024-12-27',
    'Activity Status': 'ACTIVE',
    'Active Branch Count': 1,
    'Main Language': 'Python',
    'Other Languages': ['HTML', 'Shell'],
    'Frameworks': ['Flask', 'Jinja2'],
    'Build Tool': 'Poetry',
    'Runtime Version': 'Python 3.9',
    'Language Percentages': {
        'Python': 85,
        'HTML': 10,
        'Shell': 5,
    },
    'Dockerfile': True,
    'CI/CD Present': True,
    'IaC Config Present': True,
    'Deprecated APIs Found': 3,
    'Hardcoded Secrets Found': 2,
    'Other Modernization Findings': 8,
    'Health Scores': {
        'Code Quality': 80,
        'Security': 40,
        'Modernization': 60,
        'IaC Readiness': 50,
    },
    'Cyclomatic Complexity Avg': 3.5,
    'Cyclomatic Complexity Max': 12,
    'Comment Density': 12,
    'Total Dependencies': 8,
    'Outdated Dependencies %': 40,
    'Vulnerable Dependencies %': 20,
    'Critical Vuln Count': 1,
    'EOL Packages Found': 1,
    'Dependency Managers Used': ['PyPI'],
    'Monolith Risk': 'Low',
    'Single Developer Risk': False,
    'DevOps Best Practices': True,
    'Commits Last 12 Months': [5, 10, 8, 15, 9, 12, 6, 14, 11, 7, 13, 10],

    # Updated Dependencies section
    'Dependencies': [
        {
            "name": "Flask",
            "version": "1.0",
            "package_type": "PyPI",
            "category": "Application Development",
            "sub_category": "Web Frameworks",
        },
        {
            "name": "Jinja2",
            "version": "2.11",
            "package_type": "PyPI",
            "category": "Application Development",
            "sub_category": "Template Engines",
        },
        {
            "name": "psycopg2",
            "version": "2.8",
            "package_type": "PyPI",
            "category": "Data Management & Storage",
            "sub_category": "Relational Databases",
        },
        {
            "name": "Redis",
            "version": "4.2",
            "package_type": "PyPI",
            "category": "Data Management & Storage",
            "sub_category": "Caching",
        },
        {
            "name": "requests",
            "version": "2.22.0",
            "package_type": "PyPI",
            "category": "Utilities & Libraries",
            "sub_category": "General-Purpose",
        },
        {
            "name": "gunicorn",
            "version": "20.0.4",
            "package_type": "PyPI",
            "category": "Infrastructure & Deployment",
            "sub_category": "Containerization & Orchestration",
        },
        {
            "name": "bcrypt",
            "version": "3.2.0",
            "package_type": "PyPI",
            "category": "Security & Identity",
            "sub_category": "Authentication",
        },
        {
            "name": "certifi",
            "version": "2020.12.5",
            "package_type": "PyPI",
            "category": "Security & Identity",
            "sub_category": "Transport & Data Security",
        },
    ],

    # Vulnerabilities
    'Vulnerabilities': [
        {
            'package': 'flask',
            'version': '1.0',
            'severity': 'Critical',
            'fix_version': '2.0',
            'source': 'G'
        },
        {
            'package': 'requests',
            'version': '2.8',
            'severity': 'High',
            'fix_version': '2.25.1',
            'source': 'T'
        }
    ],

    # EOL Results
    'EOL Results': [
        {
            'artifact_name': 'Python',
            'artifact_version': '3.6',
            'eol_date': '2021-12-31',
            'latest_release': '3.11'
        },
        {
            'artifact_name': 'Flask',
            'artifact_version': '1.0',
            'eol_date': '2025-01-01',
            'latest_release': '2.3'
        }
    ],
    'Semgrep Findings': [
    {
        'path': 'src/app.py',
        'start_line': 15,
        'end_line': 16,
        'rule_id': 'python.sql.injection',
        'severity': 'Critical',
        'message': 'Possible SQL Injection vulnerability.',
        'category': 'Security',
        'subcategory': 'Injection',
        'technology': 'Python',
        'cwe': 'CWE-89',
        'likelihood': 'High',
        'impact': 'Severe',
        'confidence': 'High'
    },
    {
        'path': 'src/config.py',
        'start_line': 45,
        'end_line': 45,
        'rule_id': 'python.secrets.hardcoded',
        'severity': 'High',
        'message': 'Hardcoded API key.',
        'category': 'Security',
        'subcategory': 'Secrets Management',
        'technology': 'Python',
        'cwe': 'CWE-798',
        'likelihood': 'High',
        'impact': 'Medium',
        'confidence': 'Medium'
    },
    {
        'path': 'src/main.py',
        'start_line': 10,
        'end_line': 12,
        'rule_id': 'python.best_practices.logging',
        'severity': 'Medium',
        'message': 'Logging configuration missing.',
        'category': 'Best Practices',
        'subcategory': 'Logging',
        'technology': 'Python',
        'cwe': None,
        'likelihood': 'Medium',
        'impact': 'Low',
        'confidence': 'High'
    }
]
}