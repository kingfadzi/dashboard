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