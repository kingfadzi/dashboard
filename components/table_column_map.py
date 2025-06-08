# components/table_column_map.py

# Optional repo_catalog (rc) columns used to enrich different table views

RC_COLUMNS_BY_TABLE_ID = {
    # Overview metrics and activity
    "overview": [
        "rc.total_commits",
        "rc.activity_status",
        "rc.repo_age_days",
        "rc.last_commit_date",
    ],

    # Build tools and runtime
    "build-info": [
        "rc.build_tool_version",
        "rc.runtime_version",
        "rc.project_count",
    ],

    # Code insights and static analysis
    "code-insights": [
        "rc.file_count",
        "rc.code_size_bytes",
        "rc.repo_size_bytes",
        "rc.lizard_total_nloc",
        "rc.lizard_total_ccn",
        "rc.source_code_file_count",
        "rc.total_blank",
        "rc.total_comment",
        "rc.total_lines_of_code",
        "rc.main_language",
        "rc.total_semgrep_findings",
        "rc.cat_security",
        "rc.cat_performance",
        "rc.cat_maintainability",
        "rc.cat_compatibility",
        "rc.cat_correctness",
        "rc.cat_best_practice",
        "rc.cat_portability",
    ],

    # Dependency, security, IaC, and EOL insights
    "dependencies": [
        "rc.dependency_count",
        "rc.package_types",
        "rc.top_packages",
        "rc.iac_frameworks",
        "rc.trivy_critical",
        "rc.trivy_high",
        "rc.trivy_medium",
        "rc.trivy_low",
        "rc.total_trivy_vulns",
        "rc.xeol_eol_package_count",
        "rc.xeol_earliest_eol_date",
        "rc.grype_total_vulns",
        "rc.grype_fixable_vulns",
        "rc.grype_critical_fixable",
        "rc.grype_high_fixable",
        "rc.grype_medium_fixable",
        "rc.grype_low_fixable",
        "rc.eol_package_count",
        "rc.earliest_eol_date",
    ],
}


TABLE_COLUMN_DEFS_BY_ID = {
    "overview": [
        {"headerName": "Status", "field": "activity_status"},
        {"headerName": "Size", "field": "classification_label"},
        {"headerName": "Age", "field": "repo_age_days", "type": "numericColumn"},
        {"headerName": "Language", "field": "all_languages"},
        {"headerName": "Scope", "field": "scope"},
        {"headerName": "Commits", "field": "total_commits", "type": "numericColumn"},
        {"headerName": "Contributors", "field": "number_of_contributors", "type": "numericColumn"},
        {
            "headerName": "Last Commit",
            "field": "last_commit_date",
            "valueFormatter": {
                "function": "params.value ? new Date(params.value).toLocaleDateString() : ''"
            },
        },
    ],
    "build-info": [
        {"headerName": "Tool Version", "field": "build_tool_version"},
        {"headerName": "Runtime Version", "field": "runtime_version"},
        {"headerName": "Modules", "field": "project_count", "type": "numericColumn"},
    ],
    "code-insights": [
        {"headerName": "Files", "field": "file_count", "type": "numericColumn"},
        {"headerName": "Size (Bytes)", "field": "code_size_bytes", "type": "numericColumn"},
        {"headerName": "LOC", "field": "total_lines_of_code", "type": "numericColumn"},
        {"headerName": "Blank", "field": "total_blank", "type": "numericColumn"},
        {"headerName": "Comment", "field": "total_comment", "type": "numericColumn"},
        {"headerName": "NLOC", "field": "lizard_total_nloc", "type": "numericColumn"},
        {"headerName": "CCN", "field": "lizard_total_ccn", "type": "numericColumn"},
        {"headerName": "Semgrep", "field": "total_semgrep_findings", "type": "numericColumn"},
        {"headerName": "Correctness", "field": "cat_correctness"},
        {"headerName": "Security", "field": "cat_security"},
    ],
    "dependencies": [
        {"headerName": "Packages", "field": "dependency_count", "type": "numericColumn"},
        {"headerName": "Types", "field": "package_types"},
        {"headerName": "Top Packages", "field": "top_packages"},
        {"headerName": "IaC", "field": "iac_frameworks"},
        {"headerName": "Critical", "field": "trivy_critical"},
        {"headerName": "High", "field": "trivy_high"},
        {"headerName": "Medium", "field": "trivy_medium"},
        {"headerName": "Low", "field": "trivy_low"},
        {"headerName": "EOL Pkgs", "field": "xeol_eol_package_count"},
    ],
}